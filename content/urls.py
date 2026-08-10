"""
Republic of Kandhla - Content URL Configuration
Feed, Post/Concern creation, Interactions endpoints.
"""

from django.urls import path
from content.views import (
    MohallaFeedView,
    CreatePostView,
    CreateConcernView,
    ConcernListView,
    InteractionVoteView,
)

app_name = 'content'

urlpatterns = [
    # GET /api/feed/{mohalla_id}/ -> Paginated mohalla feed (pinned at top)
    path('feed/<uuid:mohalla_id>/', MohallaFeedView.as_view(), name='mohalla-feed'),

    # POST /api/posts/create/ -> New post create (profanity filter + RBAC check)
    path('posts/create/', CreatePostView.as_view(), name='create-post'),

    # POST /api/concerns/create/ -> New concern (samasya) raise karo
    path('concerns/create/', CreateConcernView.as_view(), name='create-concern'),

    # GET /api/concerns/{mohalla_id}/ -> Mohalla concerns list
    path('concerns/<uuid:mohalla_id>/', ConcernListView.as_view(), name='concern-list'),

    # POST /api/interactions/vote/ -> Like/Dislike/Support updates
    path('interactions/vote/', InteractionVoteView.as_view(), name='interaction-vote'),
]
