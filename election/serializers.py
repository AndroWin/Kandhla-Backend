"""
Republic of Kandhla - Election Serializers
Election, Candidate, Vote ke DRF serializers.
Nomination, voting, aur results display ke liye.
"""

from rest_framework import serializers
from django.conf import settings
from election.models import Election, Candidate, Vote
from accounts.serializers import UserMinimalSerializer


class ElectionSerializer(serializers.ModelSerializer):
    """
    Election read serializer — election hub display ke liye.
    """
    city_name = serializers.CharField(source='city.name', read_only=True)
    mohalla_name = serializers.CharField(source='mohalla.name', read_only=True, default=None)
    election_type_display = serializers.CharField(source='get_election_type_display', read_only=True)
    phase_display = serializers.CharField(source='get_phase_display', read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_voting_open = serializers.BooleanField(read_only=True)
    candidate_count = serializers.SerializerMethodField()
    total_votes = serializers.SerializerMethodField()

    class Meta:
        model = Election
        fields = [
            'id',
            'city',
            'city_name',
            'mohalla',
            'mohalla_name',
            'election_type',
            'election_type_display',
            'phase',
            'phase_display',
            'start_date',
            'end_date',
            'is_active',
            'is_voting_open',
            'candidate_count',
            'total_votes',
            'created_at',
        ]
        read_only_fields = fields

    def get_candidate_count(self, obj):
        """Approved candidates ki count."""
        return obj.candidates.filter(is_approved=True).count()

    def get_total_votes(self, obj):
        """Total votes cast — sirf counting/completed phase mein dikhao."""
        if obj.phase in (Election.Phase.COUNTING, Election.Phase.COMPLETED):
            return obj.votes.count()
        return None  # Voting phase mein vote count hidden


class CandidateSerializer(serializers.ModelSerializer):
    """
    Candidate read serializer — manifesto aur symbol ke saath.
    Vote count sirf results phase mein dikhega.
    """
    user_details = UserMinimalSerializer(source='user', read_only=True)
    election_type = serializers.CharField(source='election.election_type', read_only=True)

    class Meta:
        model = Candidate
        fields = [
            'id',
            'election',
            'election_type',
            'user',
            'user_details',
            'manifesto',
            'symbol',
            'vote_count',
            'is_approved',
            'created_at',
        ]
        read_only_fields = fields

    def to_representation(self, instance):
        """Vote count sirf counting/completed phase mein dikhao."""
        data = super().to_representation(instance)
        election = instance.election
        if election.phase not in (Election.Phase.COUNTING, Election.Phase.COMPLETED):
            data['vote_count'] = None  # Hide vote count during voting
        return data


class NominationSerializer(serializers.ModelSerializer):
    """
    Nomination (Parcha) submit serializer.
    SCHEMA.md: POST /api/election/nominate/
    REQUIREMENTS.md: "Requires minimum Credibility Score" (>= 500).
    """

    class Meta:
        model = Candidate
        fields = ['election', 'manifesto']

    def validate_election(self, value):
        """Election nomination phase mein honi chahiye."""
        if value.phase != Election.Phase.NOMINATION:
            raise serializers.ValidationError(
                'Nomination sirf Nomination phase mein ho sakti hai. '
                f'Abhi election {value.get_phase_display()} phase mein hai.'
            )
        return value

    def validate(self, data):
        """
        User eligibility checks:
        1. Credibility Score >= 500
        2. User banned nahi hona chahiye
        3. Duplicate nomination check
        """
        user = self.context['request'].user
        election = data['election']

        # Credibility Score check
        min_score = settings.KANDHLA_SETTINGS['MIN_CREDIBILITY_FOR_NOMINATION']
        if user.credibility_score < min_score:
            raise serializers.ValidationError(
                f'Nomination ke liye minimum Credibility Score {min_score} chahiye. '
                f'Tumhara score: {user.credibility_score}.'
            )

        # Ban check
        if user.is_banned:
            raise serializers.ValidationError(
                'Banned users nomination nahi kar sakte.'
            )

        # Duplicate nomination check
        if Candidate.objects.filter(election=election, user=user).exists():
            raise serializers.ValidationError(
                'Tum is election mein pehle se nominate ho.'
            )

        # City check — user usi city ka hona chahiye
        if user.city != election.city:
            raise serializers.ValidationError(
                'Tum sirf apni city ki election mein nominate ho sakte ho.'
            )

        # Mohalla election mein mohalla match honi chahiye
        if election.election_type == Election.ElectionType.MOHALLA:
            if not election.mohalla or user.mohalla != election.mohalla:
                raise serializers.ValidationError(
                    'Mohalla election mein sirf usi mohalla ke log nominate ho sakte hain.'
                )

        return data

    def create(self, validated_data):
        """Nomination create karte waqt user auto-set hoga."""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CastVoteSerializer(serializers.Serializer):
    """
    Secure Vote casting serializer.
    SCHEMA.md: POST /api/election/cast-vote/
    REQUIREMENTS.md:
    - "Voting happens exclusively via an internal secure digital poll system"
    - "1 Person = 1 Vote, routed via Redis queue to prevent traffic crashes"
    - Device ID binding for anti-fraud
    """
    election_id = serializers.UUIDField(
        help_text='Jis election mein vote de rahe ho',
    )
    candidate_id = serializers.UUIDField(
        help_text='Jis candidate ko vote de rahe ho',
    )
    device_id = serializers.CharField(
        max_length=255,
        help_text='Physical device identifier',
    )

    def validate_election_id(self, value):
        """Election exist aur voting phase mein honi chahiye."""
        try:
            election = Election.objects.get(id=value)
        except Election.DoesNotExist:
            raise serializers.ValidationError('Election not found.')

        if election.phase != Election.Phase.VOTING:
            raise serializers.ValidationError(
                f'Voting abhi band hai. Election {election.get_phase_display()} phase mein hai.'
            )

        return value

    def validate_candidate_id(self, value):
        """Candidate exist aur approved hona chahiye."""
        try:
            candidate = Candidate.objects.get(id=value)
        except Candidate.DoesNotExist:
            raise serializers.ValidationError('Candidate not found.')

        if not candidate.is_approved:
            raise serializers.ValidationError('Ye candidate approved nahi hai.')

        return value

    def validate(self, data):
        """
        Strict security validations:
        1. Candidate election match
        2. 1 device = 1 vote
        3. User apni city/mohalla ki election mein hi vote kare
        """
        election_id = data['election_id']
        candidate_id = data['candidate_id']
        device_id = data['device_id']
        user = self.context['request'].user

        # Candidate election match
        try:
            candidate = Candidate.objects.get(id=candidate_id)
            election = Election.objects.get(id=election_id)
        except (Candidate.DoesNotExist, Election.DoesNotExist):
            raise serializers.ValidationError('Invalid election or candidate.')

        if candidate.election_id != election.id:
            raise serializers.ValidationError(
                'Ye candidate is election ka nahi hai.'
            )

        # Device ID match with user's registered device
        if user.device_id and user.device_id != device_id:
            raise serializers.ValidationError(
                'Vote sirf registered device se de sakte ho. Device mismatch detected.'
            )

        # 1 device = 1 vote check
        if Vote.objects.filter(election=election, device_id=device_id).exists():
            raise serializers.ValidationError(
                'Is device se is election mein pehle se vote ho chuka hai. 1 Device = 1 Vote.'
            )

        # City match
        if user.city != election.city:
            raise serializers.ValidationError(
                'Tum sirf apni city ki election mein vote de sakte ho.'
            )

        # Mohalla election mein mohalla match
        if election.election_type == Election.ElectionType.MOHALLA:
            if user.mohalla != election.mohalla:
                raise serializers.ValidationError(
                    'Mohalla election mein sirf usi mohalla ke log vote de sakte hain.'
                )

        # Ban check
        if user.is_banned:
            raise serializers.ValidationError('Banned users vote nahi de sakte.')

        return data


class ElectionResultSerializer(serializers.ModelSerializer):
    """
    Election results serializer — completed elections ke results.
    Candidates vote_count ke hisaab se sorted.
    """
    candidates = serializers.SerializerMethodField()
    city_name = serializers.CharField(source='city.name', read_only=True)
    total_votes = serializers.SerializerMethodField()

    class Meta:
        model = Election
        fields = [
            'id',
            'city_name',
            'election_type',
            'phase',
            'start_date',
            'end_date',
            'candidates',
            'total_votes',
        ]
        read_only_fields = fields

    def get_candidates(self, obj):
        """Candidates sorted by vote count (winner first)."""
        candidates = obj.candidates.filter(is_approved=True).order_by('-vote_count')
        return CandidateSerializer(candidates, many=True, context=self.context).data

    def get_total_votes(self, obj):
        return obj.votes.count()
