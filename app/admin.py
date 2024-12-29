from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, Activity

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    ordering = ('created_at',)
    list_filter = ('created_at',)

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_active', 'timestamp', 'end_time')
    search_fields = ('user__name',)
    ordering = ('-timestamp',)  # Order by the most recent activity
    list_filter = ('is_active', 'timestamp', 'end_time')
