"""
Republic of Kandhla - Ecosystem Admin Configuration
City, Mohalla, MohallaChangeRequest, Cabinet ka admin panel management.
"""

from django.contrib import admin
from ecosystem.models import City, Mohalla, MohallaChangeRequest, Cabinet


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """City model ka admin — Samvidhan management, Achaar Sanhita toggle."""

    list_display = ('name', 'state', 'is_code_of_conduct_active')
    list_filter = ('state', 'is_code_of_conduct_active')
    search_fields = ('name', 'state')
    readonly_fields = ('id',)

    fieldsets = (
        ('City Info', {
            'fields': ('id', 'name', 'state'),
        }),
        ('Samvidhan (Constitution)', {
            'fields': ('samvidhan_content',),
            'description': 'City ki Samvidhan ka HTML content yahan manage karo.',
        }),
        ('Election Controls', {
            'fields': ('is_code_of_conduct_active',),
            'description': 'Achaar Sanhita active karne se poori city mein posting disabled ho jati hai.',
        }),
    )


class MohallaInline(admin.TabularInline):
    """City admin mein Mohallas inline dikhao."""
    model = Mohalla
    extra = 1
    readonly_fields = ('id', 'population_count')


@admin.register(Mohalla)
class MohallaAdmin(admin.ModelAdmin):
    """Mohalla model ka admin — population tracking, city filtering."""

    list_display = ('name', 'city', 'population_count')
    list_filter = ('city',)
    search_fields = ('name', 'city__name')
    readonly_fields = ('id', 'population_count')

    fieldsets = (
        ('Mohalla Info', {
            'fields': ('id', 'city', 'name', 'population_count'),
        }),
    )


@admin.register(MohallaChangeRequest)
class MohallaChangeRequestAdmin(admin.ModelAdmin):
    """
    Mohalla Change Request admin — pending requests ko approve/reject karo.
    REQUIREMENTS.md: "All requests freeze automatically when an election date is announced."
    """

    list_display = ('user', 'target_mohalla', 'status', 'created_at')
    list_filter = ('status', 'target_mohalla__city')
    search_fields = ('user__name', 'user__email', 'target_mohalla__name')
    readonly_fields = ('id', 'user', 'target_mohalla', 'reason', 'created_at')
    list_editable = ('status',)

    fieldsets = (
        ('Request Details', {
            'fields': ('id', 'user', 'target_mohalla', 'reason'),
        }),
        ('Admin Action', {
            'fields': ('status',),
            'description': 'Pending request ko approve ya reject karo. Election announce hone par freeze ho jati hain.',
        }),
        ('Timestamps', {
            'fields': ('created_at',),
        }),
    )


@admin.register(Cabinet)
class CabinetAdmin(admin.ModelAdmin):
    """
    Cabinet member admin — City (max 11) aur Mohalla (max 5) level cabinet management.
    """

    list_display = ('user', 'department_name', 'city', 'mohalla', 'ruby_color', 'is_active')
    list_filter = ('is_active', 'city', 'mohalla', 'ruby_color')
    search_fields = ('user__name', 'department_name')
    readonly_fields = ('id',)

    fieldsets = (
        ('Member Info', {
            'fields': ('id', 'user', 'department_name', 'ruby_color'),
        }),
        ('Assignment Level', {
            'fields': ('city', 'mohalla'),
            'description': 'City level (Supreme Minister team, max 11) ya Mohalla level (Mohalla Minister team, max 5)',
        }),
        ('Status', {
            'fields': ('is_active',),
        }),
    )
