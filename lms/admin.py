from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import CustomUser, Course, Enrollment, Notification, Quiz, Question, Thread, Reply

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role')
    list_filter = ('role',)

    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),  # Include the role field in the admin form
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),  # Include the role field when adding a new user
    )

    def role(self, instance):
        return instance.role
    role.short_description = 'Role'

# Unregister the default User admin if it exists
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass  # Ignore if User is not registered

# Register the custom User admin
admin.site.register(CustomUser, UserAdmin)

# Register other models
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    search_fields = ('title',)

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at')
    list_filter = ('course',)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read',)

admin.site.register(Course, CourseAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Thread)
admin.site.register(Reply)
