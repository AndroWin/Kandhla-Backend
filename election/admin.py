"""
Republic of Kandhla - Election Admin Configuration
Election Commission dashboard — Election lifecycle, Candidate approval, Vote audit.
"""

from django.contrib import admin
from election.models import Election, Candidate, Vote


class CandidateInline(admin.TabularInline):
    """Election admin mein candidates inline dikhao."""
    model = Candidate
    extra = 0
    readonly_fields = ('id', 'user', 'manifesto', 'vote_count', 'created_at')
    fields = ('user', 'manifesto', 'symbol', 'is_approved', 'vote_count', 'created_at')


@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    """
    Election admin — Phase management, candidate approval, results oversight.
    REQUIREMENTS.md ke mutabiq 7-phase election cycle manage hota hai yahan se.
    """

    list_display = (
        'election_type',
        'city',
        'mohalla',
        'phase',
        'start_date',
        'end_date',
        'is_active',
        'candidate_count',
        'total_votes',
    )
    list_filter = ('election_type', 'phase', 'city')
    search_fields = ('city__name', 'mohalla__name')
    readonly_fields = ('id', 'created_at')
    date_hierarchy = 'start_date'
    inlines = [CandidateInline]

    fieldsets = (
        ('Election Info', {
            'fields': ('id', 'city', 'mohalla', 'election_type'),
        }),
        ('Phase Control', {
            'fields': ('phase',),
            'description': 'Phase change karo: nomination → allocation → campaign → code_of_conduct → voting → counting → completed',
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date'),
        }),
        ('Timestamps', {
            'fields': ('created_at',),
        }),
    )

    def candidate_count(self, obj):
        """Approved candidates ki count."""
        return obj.candidates.filter(is_approved=True).count()
    candidate_count.short_description = 'Approved Candidates'

    def total_votes(self, obj):
        """Total votes cast in this election."""
        return obj.votes.count()
    total_votes.short_description = 'Total Votes'

    def is_active(self, obj):
        """Election active hai ya complete."""
        return obj.is_active
    is_active.boolean = True
    is_active.short_description = 'Active?'


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    """
    Candidate admin — Nomination review, symbol allocation, vote tracking.
    Admin top 30 candidates select karke symbols allocate karta hai.
    """

    list_display = (
        'user',
        'election',
        'symbol',
        'is_approved',
        'vote_count',
        'created_at',
    )
    list_filter = ('is_approved', 'election__election_type', 'election__city')
    search_fields = ('user__name', 'user__email', 'manifesto')
    readonly_fields = ('id', 'vote_count', 'created_at')
    list_editable = ('is_approved', 'symbol')

    fieldsets = (
        ('Candidate Info', {
            'fields': ('id', 'election', 'user'),
        }),
        ('Manifesto & Symbol', {
            'fields': ('manifesto', 'symbol'),
            'description': 'Symbol allocation: Admin emoji symbol assign karta hai (e.g., 🚲, 🌺)',
        }),
        ('Approval & Votes', {
            'fields': ('is_approved', 'vote_count'),
        }),
        ('Timestamps', {
            'fields': ('created_at',),
        }),
    )


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    """
    Vote admin — Audit trail for election integrity.
    Read-only access — votes should never be manually edited.
    Security: 1 device = 1 vote, hashed token prevents double voting.
    """

    list_display = ('election', 'device_id_short', 'hashed_token_short', 'created_at')
    list_filter = ('election__election_type', 'election__city')
    search_fields = ('device_id', 'hashed_token')
    readonly_fields = ('id', 'election', 'candidate', 'device_id', 'hashed_token', 'created_at')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Vote Record (Read-Only)', {
            'fields': ('id', 'election', 'candidate', 'device_id', 'hashed_token', 'created_at'),
            'description': 'Votes sirf audit ke liye hain — manually edit nahi karne chahiye.',
        }),
    )

    def device_id_short(self, obj):
        """Device ID ka truncated display for privacy."""
        return f"{obj.device_id[:12]}..." if len(obj.device_id) > 12 else obj.device_id
    device_id_short.short_description = 'Device ID'

    def hashed_token_short(self, obj):
        """Hashed token ka truncated display."""
        return f"{obj.hashed_token[:16]}..." if len(obj.hashed_token) > 16 else obj.hashed_token
    hashed_token_short.short_description = 'Vote Token'

    def has_add_permission(self, request):
        """Admin se manually vote add nahi kar sakte — security measure."""
        return False

    def has_change_permission(self, request, obj=None):
        """Admin se votes edit nahi kar sakte — integrity measure."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Admin se votes delete nahi kar sakte — audit trail maintain."""
        return False
