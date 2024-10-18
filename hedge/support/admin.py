from django.contrib import admin
from .models import Support_query, Support_query_message

# Register Support_query model in admin
@admin.register(Support_query)
class SupportQueryAdmin(admin.ModelAdmin):
    list_display = ('support_id', 'user', 'title', 'mobile', 'status', 'date_time')  # Fields to display in the list view
    list_filter = ('status', 'date_time', 'Issue_type')  # Add filters for easier management
    search_fields = ('support_id', 'user__username', 'title')  # Enable search by support ID, user, and title

# Register Support_query_message model in admin
@admin.register(Support_query_message)
class SupportQueryMessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'user', 'support', 'date_time')  # Fields to display in the list view
    search_fields = ('message_id', 'user__username', 'message', 'support__support_id')  # Search by message ID, user, and related query
