"""
Republic of Kandhla - Content Admin Configuration
Posts aur Concerns ka admin panel management.
"""

from django.contrib import admin
from content.models import Post, Concern


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Post admin — content moderation, pinned announcements, ad tracking.
    """

    list_display = ('user', 'mohalla', 'post_type', 'is_anonymous', 'created_at')
    list_filter = ('post_type', 'is_anonymous', 'mohalla__city', 'mohalla')
    search_fields = ('user__name', 'content_text', 'mohalla__name')
    readonly_fields = ('id', 'created_at')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Post Details', {
            'fields': ('id', 'user', 'mohalla', 'post_type'),
        }),
        ('Content', {
            'fields': ('content_text', 'image_url', 'is_anonymous'),
        }),
        ('Timestamps', {
            'fields': ('created_at',),
        }),
    )


@admin.register(Concern)
class ConcernAdmin(admin.ModelAdmin):
    """
    Concern (Samasya) admin — issue tracking, support counts, status management.
    Admin can escalate pending issues to city_priority or mark resolved.
    """

    list_display = (
        'user',
        'mohalla',
        'status',
        'support_count',
        'do_not_support_count',
        'net_support',
        'created_at',
    )
    list_filter = ('status', 'mohalla__city', 'mohalla')
    search_fields = ('user__name', 'description', 'mohalla__name')
    readonly_fields = ('id', 'support_count', 'do_not_support_count', 'created_at')
    list_editable = ('status',)
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Concern Details', {
            'fields': ('id', 'user', 'mohalla'),
        }),
        ('Issue Content', {
            'fields': ('description', 'image_url'),
        }),
        ('Status & Votes', {
            'fields': ('status', 'support_count', 'do_not_support_count'),
            'description': 'Support/Do Not Support counts API se update hoti hain. Admin sirf status change kar sakta hai.',
        }),
        ('Timestamps', {
            'fields': ('created_at',),
        }),
    )

    def net_support(self, obj):
        """Net support score display in admin list."""
        return obj.net_support
    net_support.short_description = 'Net Support'
