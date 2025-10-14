from django.http import HttpResponseForbidden
from .models import Doctor

class DoctorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        # If a Doctor profile exists attach it. If not, but the user is a
        # registered and approved doctor, create a lightweight Doctor record
        # on-the-fly so they can access doctor-only pages. This avoids
        # denying access when admin approved the user but the Doctor profile
        # hasn't been filled out yet.
        try:
            request.doctor = Doctor.objects.get(user=request.user)
        except Doctor.DoesNotExist:
            user = getattr(request, 'user', None)
            if user and getattr(user, 'is_authenticated', False) and getattr(user, 'user_role', None) == 'doctor' and getattr(user, 'is_approved', False):
                # create a minimal Doctor instance; other fields can be filled later
                from django.conf import settings as dj_settings
                defaults = {
                    'first_name': user.first_name or '',
                    'last_name': user.last_name or '',
                    'registration_id': f"AUTO-{user.id}",
                    'specialty': 'General',
                    'max_patients': int(getattr(dj_settings, 'MAX_PATIENTS_PER_DOCTOR', 100)) or 100,
                }
                request.doctor, _ = Doctor.objects.get_or_create(user=user, defaults=defaults)
            else:
                return HttpResponseForbidden("Access Denied. You must be a doctor to access this page.")
        return super().dispatch(request, *args, **kwargs)