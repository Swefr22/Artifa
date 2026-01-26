from django.contrib import admin
from .models import Event, Registration, Schedule, ContactMessage, ErrorLog, Coordinator, Team, TeamMember, ChatbotTraining

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'event_type', 'duration', 'venue', 'start_time', 'end_time', 'event_date', 'registration_count']
    list_filter = ['event_type', 'is_team_event', 'event_date']
    search_fields = ['name', 'description', 'venue']
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Event Information', {
            'fields': ('name', 'slug', 'description', 'event_type', 'icon_class')
        }),
        ('Event Details', {
            'fields': ('duration', 'venue'),
            'description': 'Set duration and venue for this event'
        }),
        ('Event Schedule', {
            'fields': ('start_time', 'end_time', 'event_date'),
            'description': 'Set the time and date for this event'
        }),
        ('Team Settings', {
            'fields': ('is_team_event', 'min_team_size', 'max_team_size')
        }),
        ('Meta Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']
    
    def registration_count(self, obj):
        count = obj.registration_set.count()
        return f"{count} registrations"
    registration_count.short_description = "Registrations"

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'register_number', 'year', 'department', 'event_name', 'team_name', 'registered_at']
    list_filter = ['event__event_type', 'registered_at', 'year', 'department', 'team_name', 'is_verified']
    search_fields = ['full_name', 'register_number', 'event__name', 'team_name', 'email']
    readonly_fields = ['registered_at']
    ordering = ['team_name', 'full_name', 'event__name']
    
    fieldsets = (
        ('Registration Details', {
            'fields': ('register_number', 'full_name', 'email', 'event', 'registered_at')
        }),
        ('Personal Information', {
            'fields': ('year', 'department', 'phone_number')
        }),
        ('Team Information', {
            'fields': ('team', 'team_name', 'team_members', 'team_password', 'is_team_lead')
        }),
        ('Account Status', {
            'fields': ('is_verified',)
        }),
    )
    
    def event_name(self, obj):
        return obj.event.name
    event_name.short_description = "Event"

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'start_time', 'end_time', 'is_break', 'event']
    list_filter = ['date', 'is_break', 'event']
    ordering = ['date', 'start_time']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_at']

@admin.register(Coordinator)
class CoordinatorAdmin(admin.ModelAdmin):
    list_display = ['name', 'event', 'register_number', 'year', 'event_type', 'created_at']
    list_filter = ['event_type', 'year', 'event', 'created_at']
    search_fields = ['name', 'register_number', 'event__name']
    fieldsets = (
        ('Coordinator Information', {
            'fields': ('name', 'register_number', 'year', 'event_type')
        }),
        ('Event', {
            'fields': ('event',)
        }),
        ('Meta', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at']

class TeamMemberInline(admin.TabularInline):
    """Inline admin for team members"""
    model = TeamMember
    extra = 1
    fields = ['registration', 'status', 'joined_at', 'added_at']
    readonly_fields = ['joined_at', 'added_at']
    raw_id_fields = ['registration']

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'event', 'created_by', 'member_count', 'pending_count', 'created_at']
    list_filter = ['event', 'created_at', 'updated_at']
    search_fields = ['name', 'description', 'created_by__full_name', 'event__name']
    readonly_fields = ['created_at', 'updated_at', 'member_count', 'pending_count', 'total_count']
    inlines = [TeamMemberInline]
    
    fieldsets = (
        ('Team Information', {
            'fields': ('name', 'event', 'created_by', 'description')
        }),
        ('Team Statistics', {
            'fields': ('member_count', 'pending_count', 'total_count'),
            'classes': ('collapse',)
        }),
        ('Meta', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def member_count(self, obj):
        return obj.member_count
    member_count.short_description = "Joined Members"
    
    def pending_count(self, obj):
        return obj.pending_count
    pending_count.short_description = "Pending Members"
    
    def total_count(self, obj):
        return obj.total_count
    total_count.short_description = "Total Members"

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['registration_name', 'team', 'status', 'joined_at', 'added_at']
    list_filter = ['status', 'team__event', 'added_at']
    search_fields = ['registration__full_name', 'team__name', 'registration__register_number']
    readonly_fields = ['added_at', 'joined_at']
    raw_id_fields = ['registration', 'team']
    
    fieldsets = (
        ('Member Information', {
            'fields': ('registration', 'team')
        }),
        ('Status', {
            'fields': ('status', 'joined_at')
        }),
        ('Meta', {
            'fields': ('added_at',),
            'classes': ('collapse',)
        }),
    )
    
    def registration_name(self, obj):
        return f"{obj.registration.full_name} ({obj.registration.register_number})"
    registration_name.short_description = "Member"
    
    def has_delete_permission(self, request, obj=None):
        """Only superuser can delete team members"""
        if not request.user.is_superuser:
            return False
        return True
    
    def has_change_permission(self, request, obj=None):
        """Only superuser can edit team members"""
        if not request.user.is_superuser:
            return False
        return True
    
    def has_add_permission(self, request):
        """Only superuser can add team members"""
        if not request.user.is_superuser:
            return False
        return True

@admin.register(ErrorLog)
class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ['status_code', 'error_type', 'method', 'path', 'client_ip', 'timestamp', 'resolved']
    list_filter = ['status_code', 'error_type', 'timestamp', 'resolved']
    search_fields = ['path', 'client_ip', 'error_message']
    readonly_fields = ['status_code', 'error_type', 'method', 'path', 'query_string', 'client_ip', 'user_agent', 'error_message', 'timestamp']
    ordering = ['-timestamp']
    
    fieldsets = (
        ('Error Information', {
            'fields': ('status_code', 'error_type', 'error_message', 'timestamp')
        }),
        ('Request Details', {
            'fields': ('method', 'path', 'query_string', 'client_ip', 'user_agent')
        }),
        ('Resolution', {
            'fields': ('resolved', 'resolution_notes'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(ChatbotTraining)
class ChatbotTrainingAdmin(admin.ModelAdmin):
    list_display = ['question_preview', 'intent', 'is_active', 'created_at', 'created_by']
    list_filter = ['intent', 'is_active', 'created_at']
    search_fields = ['question', 'answer', 'keywords', 'intent']
    readonly_fields = ['created_at', 'updated_at', 'created_by']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Training Data', {
            'fields': ('question', 'answer', 'keywords')
        }),
        ('Classification', {
            'fields': ('intent',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )
    
    def question_preview(self, obj):
        return f"{obj.question[:50]}..." if len(obj.question) > 50 else obj.question
    question_preview.short_description = "Question"
    
    def save_model(self, request, obj, form, change):
        """Set created_by when saving"""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
