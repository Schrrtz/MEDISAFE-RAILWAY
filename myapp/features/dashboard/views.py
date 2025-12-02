from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from ...models import User, Appointment, BookedService, LabResult, Prescription, Doctor

def dashboard(request):
    """Client-facing homepage for regular users"""
    user_id = request.session.get("user_id") or request.session.get("user")
    is_logged_in = user_id is not None
    
    # Initialize statistics for non-logged-in users
    user_appointments = 0
    user_booked_services = 0
    user_lab_results = 0
    user_prescriptions = 0
    
    if is_logged_in:
        try:
            user = User.objects.get(user_id=user_id)
            # Get user-specific statistics
            user_appointments = Appointment.objects.filter(patient=user).count()
            user_booked_services = BookedService.objects.filter(user=user).count()
            user_lab_results = LabResult.objects.filter(user=user).count()
            
            # Get prescriptions through live appointments
            user_prescriptions = Prescription.objects.filter(
                live_appointment__appointment__patient=user
            ).count()
            
        except User.DoesNotExist:
            is_logged_in = False
    
    # Get doctors with their appointment counts for the doctors tab
    doctors_with_appointments = Doctor.objects.select_related(
        'user',
        'user__userprofile'
    ).annotate(
        appointment_count=Count('doctor_consultations')
    ).filter(
        appointment_count__gt=0
    ).order_by('-appointment_count')
    
    # Pass user object for template authentication checks
    context = {
        "is_logged_in": is_logged_in,
        "user_id": user_id if is_logged_in else None,
        "user": request.user if hasattr(request, 'user') else None,
        "user_appointments": user_appointments,
        "user_booked_services": user_booked_services,
        "user_lab_results": user_lab_results,
        "user_prescriptions": user_prescriptions,
        "doctors_with_appointments": doctors_with_appointments,
    }
    
    return render(request, "Homepage.html", context)