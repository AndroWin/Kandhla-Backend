"""
Republic of Kandhla - Content API Views
Mohalla Feed, Post/Concern creation, Interactions (Like/Dislike/Support).
"""

import logging
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from content.models import Post, Concern
from content.serializers import (
    PostSerializer,
    PostCreateSerializer,
    ConcernSerializer,
    ConcernCreateSerializer,
    InteractionSerializer,
)
from kandhla.permissions import IsNotBanned, IsCitizen
from django.conf import settings

logger = logging.getLogger(__name__)


class MohallaFeedView(generics.ListAPIView):
    """
    Mohalla Feed Endpoint.
    SCHEMA.md: GET /api/feed/{mohalla_id}/
    REQUIREMENTS.md:
    - Fetches paginated posts for a specific mohalla
    - Pins admin announcements/ads at top
    - Cross-Mohalla: users can view other mohallas' feeds
    """
    permission_classes = [IsAuthenticated, IsNotBanned]
    serializer_class = PostSerializer

    def get_queryset(self):
        mohalla_id = self.kwargs.get('mohalla_id')

        # Pinned posts (announcements, ads) pehle, phir normal posts chronologically
        queryset = Post.objects.filter(
            mohalla_id=mohalla_id,
        ).select_related(
            'user', 'mohalla', 'mohalla__city'
        ).order_by(
            # Announcements aur ads ko top pe pin karo
            '-post_type',  # announcement/ad/official_order > normal
            '-created_at',
        )

        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        # Pinned posts ko alag se mark karo
        results = response.data.get('results', response.data)
        if isinstance(results, list):
            for post_data in results:
                post_data['is_pinned'] = post_data.get('post_type') in (
                    Post.PostType.ANNOUNCEMENT,
                    Post.PostType.AD,
                )

        return response


class CreatePostView(generics.CreateAPIView):
    """
    Post Create Endpoint.
    SCHEMA.md: POST /api/posts/create/
    REQUIREMENTS.md:
    - Validates against profanity filter
    - Checks minister permissions for official orders
    - Achaar Sanhita active hone par posting disabled
    """
    permission_classes = [IsAuthenticated, IsNotBanned]
    serializer_class = PostCreateSerializer

    def create(self, request, *args, **kwargs):
        # Fetch the user's city (assuming user belongs to a mohalla which belongs to a city)
        city = request.user.city
        if not city and request.user.mohalla:
            city = request.user.mohalla.city
            
        if city:
            if city.is_emergency_rule_active:
                return Response(
                    {'success': False, 'error': 'City is under EMERGENCY RULE. All posting is locked.'},
                    status=status.HTTP_403_FORBIDDEN
                )
            if city.is_code_of_conduct_active:
                return Response(
                    {'success': False, 'error': 'Achaar Sanhita is active. Posting is currently disabled.'},
                    status=status.HTTP_403_FORBIDDEN
                )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = serializer.save(user=request.user)

        logger.info(
            f"New post created: {post.id} by {request.user.name} "
            f"in {post.mohalla.name} (type: {post.post_type})"
        )

        return Response(
            {
                'success': True,
                'message': 'Post successfully create ho gayi!',
                'post': PostSerializer(post, context={'request': request}).data,
            },
            status=status.HTTP_201_CREATED,
        )


class CreateConcernView(generics.CreateAPIView):
    """
    Concern (Samasya) Create Endpoint.
    REQUIREMENTS.md: "Users can raise issues with images and details."
    """
    permission_classes = [IsAuthenticated, IsNotBanned]
    serializer_class = ConcernCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        concern = serializer.save()

        logger.info(
            f"New concern raised: {concern.id} by {request.user.name} "
            f"in {concern.mohalla.name}"
        )

        return Response(
            {
                'success': True,
                'message': 'Concern (Samasya) successfully raise ho gayi!',
                'concern': ConcernSerializer(concern, context={'request': request}).data,
            },
            status=status.HTTP_201_CREATED,
        )


class ConcernListView(generics.ListAPIView):
    """
    Mohalla ke concerns (samasya) ki list.
    Support count ke hisaab se sorted — high support = city priority.
    """
    permission_classes = [IsAuthenticated, IsNotBanned]
    serializer_class = ConcernSerializer

    def get_queryset(self):
        mohalla_id = self.kwargs.get('mohalla_id')
        queryset = Concern.objects.filter(
            mohalla_id=mohalla_id,
        ).select_related('user', 'mohalla')

        # Status filter
        concern_status = self.request.query_params.get('status')
        if concern_status:
            queryset = queryset.filter(status=concern_status)

        return queryset


class InteractionVoteView(APIView):
    """
    Like/Dislike/Support Interaction Endpoint.
    SCHEMA.md: POST /api/interactions/vote/
    REQUIREMENTS.md:
    - Cross-Mohalla users can Like/Dislike/Support
    - "Commenting is strictly blocked"
    - "Likes from other mohallas show aggregate counts per mohalla, hiding individual user identities"
    - Support/Do Not Support on Concerns affects Credibility Score
    """
    permission_classes = [IsAuthenticated, IsNotBanned]

    def post(self, request):
        serializer = InteractionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        target_type = serializer.validated_data['target_type']
        target_id = serializer.validated_data['target_id']
        action = serializer.validated_data['action']

        if target_type == 'concern':
            return self._handle_concern_interaction(target_id, action, request.user)

        # Post interactions — future mein Firebase Realtime DB se sync hogi
        # Filhaal acknowledgment return karo
        return Response(
            {
                'success': True,
                'message': f'{action.title()} registered! Firebase sync pending.',
                'target_type': target_type,
                'target_id': str(target_id),
                'action': action,
            },
            status=status.HTTP_200_OK,
        )

    def _handle_concern_interaction(self, concern_id, action, user):
        """
        Concern pe Support/Do Not Support handle karo.
        REQUIREMENTS.md: "High support increases the author's Credibility Score."
        """
        try:
            concern = Concern.objects.select_related('user').get(id=concern_id)
        except Concern.DoesNotExist:
            return Response(
                {'success': False, 'error': 'Concern not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if action == 'support':
            concern.support_count += 1
            concern.save(update_fields=['support_count'])

            # Credibility Score boost for concern author
            boost = settings.KANDHLA_SETTINGS['CREDIBILITY_BOOST_PER_SUPPORT']
            concern.user.credibility_score += boost
            concern.user.save(update_fields=['credibility_score'])

            # High support = city_priority
            if concern.support_count >= 50 and concern.status == Concern.Status.PENDING:
                concern.status = Concern.Status.CITY_PRIORITY
                concern.save(update_fields=['status'])

        elif action == 'do_not_support':
            concern.do_not_support_count += 1
            concern.save(update_fields=['do_not_support_count'])

        logger.info(
            f"Concern {concern_id}: {action} by {user.name} "
            f"(support: {concern.support_count}, dns: {concern.do_not_support_count})"
        )

        return Response(
            {
                'success': True,
                'message': f'{action.replace("_", " ").title()} registered!',
                'support_count': concern.support_count,
                'do_not_support_count': concern.do_not_support_count,
            },
            status=status.HTTP_200_OK,
        )
