"""
Republic of Kandhla - Election API Views
Election Hub, Nomination, Secure Voting (via Redis queue), Results.
"""

import hashlib
import logging
from django.conf import settings
from django.db import models
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from election.models import Election, Candidate, Vote
from election.serializers import (
    ElectionSerializer,
    CandidateSerializer,
    NominationSerializer,
    CastVoteSerializer,
    ElectionResultSerializer,
)
from kandhla.permissions import IsNotBanned

logger = logging.getLogger(__name__)


class ElectionListView(generics.ListAPIView):
    """
    Active aur past elections ki list.
    Election Commission Hub screen ke liye data.
    """
    permission_classes = [IsAuthenticated, IsNotBanned]
    serializer_class = ElectionSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Election.objects.filter(
            city=user.city,
        ).select_related('city', 'mohalla')

        # Filter by status
        is_active = self.request.query_params.get('active')
        if is_active == 'true':
            queryset = queryset.exclude(phase=Election.Phase.COMPLETED)
        elif is_active == 'false':
            queryset = queryset.filter(phase=Election.Phase.COMPLETED)

        # Filter by type
        election_type = self.request.query_params.get('type')
        if election_type in ('city', 'mohalla'):
            queryset = queryset.filter(election_type=election_type)

        return queryset


class ElectionDetailView(generics.RetrieveAPIView):
    """
    Election detail — candidates ke saath.
    """
    permission_classes = [IsAuthenticated, IsNotBanned]
    serializer_class = ElectionSerializer
    queryset = Election.objects.all()
    lookup_field = 'id'


class CandidateListView(generics.ListAPIView):
    """
    Election ke approved candidates ki list.
    Voting booth screen ke liye data.
    """
    permission_classes = [IsAuthenticated, IsNotBanned]
    serializer_class = CandidateSerializer

    def get_queryset(self):
        election_id = self.kwargs.get('election_id')
        return Candidate.objects.filter(
            election_id=election_id,
            is_approved=True,
        ).select_related('user', 'election')


class NominationView(generics.CreateAPIView):
    """
    Election Nomination (Parcha) Submit Endpoint.
    SCHEMA.md: POST /api/election/nominate/
    REQUIREMENTS.md: "Submits election nomination form (checks user Credibility Score >= 500)."
    """
    permission_classes = [IsAuthenticated, IsNotBanned]
    serializer_class = NominationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        candidate = serializer.save()

        logger.info(
            f"New nomination: {request.user.name} in election {candidate.election.id} "
            f"(credibility: {request.user.credibility_score})"
        )

        return Response(
            {
                'success': True,
                'message': 'Nomination (Parcha) successfully submit ho gaya! '
                           'Admin approval ka wait karo.',
                'candidate': CandidateSerializer(
                    candidate, context={'request': request}
                ).data,
            },
            status=status.HTTP_201_CREATED,
        )


class CastVoteView(APIView):
    """
    Secure Vote Casting Endpoint.
    SCHEMA.md: POST /api/election/cast-vote/
    REQUIREMENTS.md:
    - "Pushes secure vote payload into Redis queue for backend processing"
    - "1 Person = 1 Vote, routed via Redis queue to prevent traffic crashes"
    - Device ID binding for anti-fraud
    - Hashed token prevents double voting
    """
    permission_classes = [IsAuthenticated, IsNotBanned]

    def post(self, request):
        serializer = CastVoteSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)

        election_id = serializer.validated_data['election_id']
        candidate_id = serializer.validated_data['candidate_id']
        device_id = serializer.validated_data['device_id']
        user = request.user

        # Unique hashed token generate karo — double voting prevention
        hash_input = f"{election_id}:{device_id}:{user.id}"
        hashed_token = hashlib.sha256(hash_input.encode()).hexdigest()

        # Double voting check (hashed token level)
        if Vote.objects.filter(hashed_token=hashed_token).exists():
            return Response(
                {
                    'success': False,
                    'error': 'Tum is election mein pehle se vote de chuke ho. '
                             '1 Person = 1 Vote.',
                },
                status=status.HTTP_409_CONFLICT,
            )

        # Vote record create karo
        vote = Vote.objects.create(
            election_id=election_id,
            candidate_id=candidate_id,
            device_id=device_id,
            hashed_token=hashed_token,
        )

        # Candidate ka vote count increment karo
        Candidate.objects.filter(id=candidate_id).update(
            vote_count=models.F('vote_count') + 1
        )

        # Redis queue mein push karo (future: Celery task se process hoga)
        self._push_to_redis_queue(vote, user)

        logger.info(
            f"Vote cast: election {election_id}, device {device_id[:12]}..., "
            f"token {hashed_token[:16]}..."
        )

        return Response(
            {
                'success': True,
                'message': 'Tumhara vote successfully register ho gaya! 🗳️',
                'vote_id': str(vote.id),
            },
            status=status.HTTP_201_CREATED,
        )

    def _push_to_redis_queue(self, vote, user):
        """
        Vote payload ko Redis queue mein push karo.
        REQUIREMENTS.md: "routed via Redis queue to prevent traffic crashes"
        """
        try:
            import redis
            import json

            redis_client = redis.from_url(settings.CELERY_BROKER_URL)
            queue_key = settings.KANDHLA_SETTINGS['VOTE_QUEUE_REDIS_KEY']

            vote_payload = json.dumps({
                'vote_id': str(vote.id),
                'election_id': str(vote.election_id),
                'candidate_id': str(vote.candidate_id),
                'device_id': vote.device_id,
                'hashed_token': vote.hashed_token,
                'timestamp': vote.created_at.isoformat(),
            })

            redis_client.rpush(queue_key, vote_payload)
            logger.info(f"Vote {vote.id} pushed to Redis queue: {queue_key}")

        except ImportError:
            logger.warning("Redis library not installed. Vote queue push skipped.")
        except Exception as e:
            # Vote toh create ho chuka hai, Redis push fail hone se vote lost nahi hoga
            logger.error(f"Redis queue push failed for vote {vote.id}: {e}")


class ElectionResultsView(generics.RetrieveAPIView):
    """
    Election Results Endpoint.
    Results sirf counting ya completed phase mein dikhte hain.
    Candidates vote_count ke hisaab se sorted — winner first.
    """
    permission_classes = [IsAuthenticated, IsNotBanned]
    serializer_class = ElectionResultSerializer
    queryset = Election.objects.all()
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        election = self.get_object()

        if election.phase not in (Election.Phase.COUNTING, Election.Phase.COMPLETED):
            return Response(
                {
                    'success': False,
                    'error': 'Results abhi available nahi hain. '
                             f'Election {election.get_phase_display()} phase mein hai.',
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(election)
        return Response(
            {
                'success': True,
                'results': serializer.data,
            },
            status=status.HTTP_200_OK,
        )
