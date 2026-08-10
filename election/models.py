"""
Republic of Kandhla - Election Models
SCHEMA.md ke mutabiq: Election, Candidate, Vote tables.
REQUIREMENTS.md ke mutabiq:
- City Election (Supreme Minister) - Har 3 mahine
- Mohalla Election (Mohalla Minister) - Har 1 mahina
- Strict 7-phase election cycle
- 1 Device = 1 Vote security (hashed token + device ID)
- NO digital voter slips (App Store compliance)
"""

import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone


class Election(models.Model):
    """
    Election Model — City ya Mohalla level election.
    SCHEMA.md: election_election table
    REQUIREMENTS.md - Election Phases:
    City: Nomination(5d) → Allocation(1d) → Campaign(4d) → Achaar Sanhita(1d) → Voting(2d) → Counting(1d) → Completed
    Mohalla: Nomination(2d) → Allocation(1d) → Campaign(4d) → Achaar Sanhita(1d) → Voting/Counting(1d) → Completed
    """

    class ElectionType(models.TextChoices):
        CITY = 'city', 'City Election (Supreme Minister)'
        MOHALLA = 'mohalla', 'Mohalla Election (Mohalla Minister)'

    class Phase(models.TextChoices):
        NOMINATION = 'nomination', 'Nomination (Parcha)'
        ALLOCATION = 'allocation', 'Symbol Allocation'
        CAMPAIGN = 'campaign', 'Campaign (Prachar)'
        CODE_OF_CONDUCT = 'code_of_conduct', 'Achaar Sanhita (Code of Conduct)'
        VOTING = 'voting', 'Voting'
        COUNTING = 'counting', 'Counting'
        COMPLETED = 'completed', 'Completed (Results Declared)'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='Election ID',
    )
    city = models.ForeignKey(
        'ecosystem.City',
        on_delete=models.CASCADE,
        related_name='elections',
        verbose_name='City',
    )
    mohalla = models.ForeignKey(
        'ecosystem.Mohalla',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='elections',
        verbose_name='Mohalla',
        help_text='Mohalla election ke liye set karo. City election mein null hoga.',
    )
    election_type = models.CharField(
        max_length=10,
        choices=ElectionType.choices,
        verbose_name='Election Type',
    )
    phase = models.CharField(
        max_length=20,
        choices=Phase.choices,
        default=Phase.NOMINATION,
        verbose_name='Current Phase',
    )
    start_date = models.DateTimeField(
        verbose_name='Start Date',
    )
    end_date = models.DateTimeField(
        verbose_name='End Date',
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Created At',
    )

    class Meta:
        db_table = 'election_election'
        verbose_name = 'Election'
        verbose_name_plural = 'Elections'
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['city', 'election_type'], name='idx_election_city_type'),
            models.Index(fields=['phase'], name='idx_election_phase'),
            models.Index(fields=['-start_date'], name='idx_election_start'),
        ]

    def __str__(self):
        target = self.mohalla.name if self.mohalla else self.city.name
        return f"{self.get_election_type_display()} - {target} ({self.get_phase_display()})"

    @property
    def is_active(self):
        """Check karo ki election abhi chal rahi hai ya nahi."""
        return self.phase != self.Phase.COMPLETED

    @property
    def is_voting_open(self):
        """Check karo ki voting phase active hai ya nahi."""
        return self.phase == self.Phase.VOTING


class Candidate(models.Model):
    """
    Candidate Model — Election mein khada hone wala candidate.
    SCHEMA.md: election_candidate table
    REQUIREMENTS.md:
    - Minimum Credibility Score >= 500 chahiye nomination ke liye
    - Admin top 30 candidates select karke symbol allocate karta hai (City election)
    - Manifesto text aur emoji symbol hota hai (e.g., '🚲')
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='Candidate ID',
    )
    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE,
        related_name='candidates',
        verbose_name='Election',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='candidacies',
        verbose_name='Candidate User',
    )
    manifesto = models.TextField(
        verbose_name='Manifesto',
        help_text='Candidate ka election manifesto / vaade',
    )
    symbol = models.CharField(
        max_length=10,
        blank=True,
        default='',
        verbose_name='Election Symbol',
        help_text='Emoji symbol — e.g., 🚲, 🌺, 🏠 (Admin allocate karta hai)',
    )
    vote_count = models.IntegerField(
        default=0,
        verbose_name='Vote Count',
        help_text='Total votes received (Redis queue se count hoti hai)',
    )
    is_approved = models.BooleanField(
        default=False,
        verbose_name='Approved by Admin',
        help_text='Admin ne approve kiya hai ya nahi (symbol allocation phase mein)',
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Nominated At',
    )

    class Meta:
        db_table = 'election_candidate'
        verbose_name = 'Candidate'
        verbose_name_plural = 'Candidates'
        ordering = ['-vote_count']
        unique_together = [['election', 'user']]
        indexes = [
            models.Index(fields=['election', 'is_approved'], name='idx_candidate_election_appr'),
            models.Index(fields=['-vote_count'], name='idx_candidate_votes'),
        ]

    def __str__(self):
        symbol_display = f" {self.symbol}" if self.symbol else ""
        return f"{self.user.name}{symbol_display} - {self.election}"


class Vote(models.Model):
    """
    Vote Model — Strict Security: 1 Device = 1 Vote.
    SCHEMA.md: election_vote table
    REQUIREMENTS.md:
    - "Voting happens exclusively via an internal secure digital poll system"
    - "NO Digital Voter Slips or fake IDs will ever be generated"
    - Device ID ensures one physical device can only vote once per election
    - Hashed token prevents double voting
    - Vote payload goes through Redis queue to prevent traffic crashes
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='Vote ID',
    )
    election = models.ForeignKey(
        Election,
        on_delete=models.CASCADE,
        related_name='votes',
        verbose_name='Election',
    )
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name='received_votes',
        verbose_name='Voted For',
        null=True,
        blank=True,
        help_text='Kis candidate ko vote diya (tracking ke liye)',
    )
    device_id = models.CharField(
        max_length=255,
        verbose_name='Device ID',
        help_text='Physical device identifier — ensures 1 device = 1 vote',
    )
    hashed_token = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Hashed Vote Token',
        help_text='Unique hash to prevent double voting (election_id + device_id + user_id hash)',
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Voted At',
    )

    class Meta:
        db_table = 'election_vote'
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'
        ordering = ['-created_at']
        # Ek device se ek election mein sirf 1 vote
        unique_together = [['election', 'device_id']]
        indexes = [
            models.Index(fields=['election', 'device_id'], name='idx_vote_election_device'),
            models.Index(fields=['hashed_token'], name='idx_vote_hashed_token'),
        ]

    def __str__(self):
        return f"Vote in {self.election} by device {self.device_id[:12]}..."
