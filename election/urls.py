"""
Republic of Kandhla - Election URL Configuration
Election Hub, Nomination, Secure Voting, Results endpoints.
"""

from django.urls import path
from election.views import (
    ElectionListView,
    ElectionDetailView,
    CandidateListView,
    NominationView,
    CastVoteView,
    ElectionResultsView,
)

app_name = 'election'

urlpatterns = [
    # GET /api/elections/ -> Active/past elections list
    path('elections/', ElectionListView.as_view(), name='election-list'),

    # GET /api/elections/{id}/ -> Election detail
    path('elections/<uuid:id>/', ElectionDetailView.as_view(), name='election-detail'),

    # GET /api/elections/{election_id}/candidates/ -> Approved candidates list
    path('elections/<uuid:election_id>/candidates/', CandidateListView.as_view(), name='candidate-list'),

    # POST /api/election/nominate/ -> Nomination submit (Credibility >= 500)
    path('election/nominate/', NominationView.as_view(), name='nominate'),

    # POST /api/election/cast-vote/ -> Secure vote via Redis queue
    path('election/cast-vote/', CastVoteView.as_view(), name='cast-vote'),

    # GET /api/elections/{id}/results/ -> Election results (counting/completed phase only)
    path('elections/<uuid:id>/results/', ElectionResultsView.as_view(), name='election-results'),
]
