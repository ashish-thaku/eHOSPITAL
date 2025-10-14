from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Doctor, Patient


@admin.action(description='Approve selected users')
def approve_users(modeladmin, request, queryset):
	updated = queryset.update(is_approved=True)
	modeladmin.message_user(request, f"{updated} user(s) marked as approved.")


class CustomUserAdmin(BaseUserAdmin):
	model = User
	list_display = ('username', 'email', 'user_role', 'is_staff', 'is_superuser', 'is_approved')
	list_filter = ('user_role', 'is_approved', 'is_staff', 'is_superuser')
	search_fields = ('username', 'email')
	ordering = ('username',)
	actions = [approve_users]

	fieldsets = BaseUserAdmin.fieldsets + (
		('Additional', {'fields': ('user_role', 'user_id', 'is_approved', 'gender')}),
	)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'registration_id', 'specialty', 'user')
	search_fields = ('first_name', 'last_name', 'registration_id', 'specialty', 'user__username')


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'user', 'phone_number')
	search_fields = ('first_name', 'last_name', 'user__username', 'phone_number')


admin.site.register(User, CustomUserAdmin)
