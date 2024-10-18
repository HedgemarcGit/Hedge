# admin.py
from django.contrib import admin
from .models import *

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

admin.site.site_header = "Hedge+"
admin.site.site_title = "Hedge+"
admin.site.index_title = "Hedge+"


class ModelLogAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'action', 'user', 'timestamp')  # Fields to display in the list view
    list_filter = ('action', 'model_name', 'user', 'timestamp')  # Filters for the sidebar
    search_fields = ('model_name', 'action', 'user__username')  # Fields to search

# Register the ModelLog model with the ModelLogAdmin class
admin.site.register(ModelLog, ModelLogAdmin)


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('plan_name', 'billings', 'unlimited_strategy_data', 'unlimited_orders', 'api_keys', 'ai_assistant', 'unlimited_devices', 'supports_long', 'supports_short', 'all_markets', 'all_brokers', 'custom_strategy', 'dedicated_support_manager')
    list_filter = ('plan_name', 'billings', 'unlimited_strategy_data', 'unlimited_orders', 'ai_assistant', 'supports_long', 'supports_short', 'all_markets', 'all_brokers')
    search_fields = ('plan_name',)


# Register the UserActivePlan model
@admin.register(UserActivePlan)
class UserActivePlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'status', 'start_date', 'end_date', 'created_at')  # Columns to display in the admin list view
    search_fields = ('user__username', 'plan__name')  # Fields that can be searched in the admin
    list_filter = ('status', 'start_date', 'end_date')  # Filters for the admin list view
    ordering = ('-created_at',)  # Default ordering of the list view


# Register the UserActivePlan model
@admin.register(UserTransections)
class UserTransectionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'status', 'start_date', 'end_date', 'created_at')  # Columns to display in the admin list view
    search_fields = ('user__username', 'plan__name')  # Fields that can be searched in the admin
    list_filter = ('status', 'start_date', 'end_date')  # Filters for the admin list view
    ordering = ('-created_at',)  # Default ordering of the list view


class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'plan', 'status', 'created_at')  # Columns to display in the admin list view
    search_fields = ('code', 'plan__name')  # Fields that can be searched
    list_filter = ('status', 'plan')  # Filters for the admin list view

admin.site.register(Coupon, CouponAdmin)


@admin.register(SubscriptionButtonClicked)
class SubscriptionButtonClickedAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'count')  # Customize fields shown in list view
    search_fields = ('user__username', 'plan__name')  # Enable search functionality
    list_filter = ('plan',)  # Add filter for the plans


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile_no', 'created_at')  # Columns to display in the admin list view
    search_fields = ( 'mobile_no',)  # Fields that can be searched
    list_filter = ( 'mobile_no',)  # Filters for the admin list view
