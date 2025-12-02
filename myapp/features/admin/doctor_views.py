from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import json
from ...models import User, UserProfile, Doctor, Appointment, Prescription, Patient

def mod_doctors(request):
    """Doctor management view"""
    if not (request.session.get("is_admin") or 
            User.objects.filter(user_id=request.session.get("user"), role="admin").exists()):
        return JsonResponse({"error": "Unauthorized"}, status=403)

    if request.method == "DELETE":
        try:
            doctor_id = request.GET.get('doctor_id')
            if not doctor_id:
                return JsonResponse({"error": "Doctor ID is required"}, status=400)

            with transaction.atomic():
                # Get the doctor
                doctor = Doctor.objects.select_related('user').get(doctor_id=doctor_id)
                user = doctor.user
                
                # Delete all consultations with this doctor
                doctor.doctor_consultations.all().delete()
                
                # Delete the doctor record
                doctor.delete()
                
                # Update the user's role and delete them
                user.delete()  # This will cascade delete the UserProfile as well

            return JsonResponse({
                "success": True,
                "message": "Doctor deleted successfully"
            })

        except Doctor.DoesNotExist:
            return JsonResponse({"error": "Doctor not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    elif request.method == "POST":
        try:
            user_id = request.POST.get('user_id')
            specialization = request.POST.get('specialization')
            license_number = request.POST.get('license_number')
            years_of_experience = request.POST.get('years_of_experience')
            availability = {
                'days': request.POST.getlist('availability_days[]'),
                'start': request.POST.get('availability_start'),
                'end': request.POST.get('availability_end')
            }
            contact_info = request.POST.get('contact_info')

            # Get the user and update their role to doctor
            user = User.objects.get(user_id=user_id)
            if Doctor.objects.filter(user=user).exists():
                return JsonResponse({"error": "User is already a doctor"}, status=400)

            user.role = 'doctor'
            user.save()

            # Create new doctor
            doctor = Doctor.objects.create(
                user=user,
                specialization=specialization,
                license_number=license_number,
                years_of_experience=int(years_of_experience),
                availability=availability,
                contact_info=contact_info
            )

            return JsonResponse({
                "success": True,
                "message": "Doctor added successfully",
                "doctor": {
                    "id": doctor.doctor_id,
                    "user_id": user.user_id,
                    "name": user.get_full_name(),
                    "specialization": doctor.specialization,
                    "license_number": doctor.license_number,
                    "years_of_experience": doctor.years_of_experience
                }
            })
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # GET request handling
    # Get Medisafe Team members (admin, nurse, lab_tech) - excluding doctors
    team_members = User.objects.filter(
        role__in=['admin', 'nurse', 'lab_tech']
    ).exclude(
        user_id__in=Doctor.objects.values_list('user__user_id', flat=True)
    ).select_related('userprofile').order_by('role', 'username')
    
    if request.session.get("is_admin"):
        # For secret admin login
        doctors = Doctor.objects.select_related('user').all()
        # Get all users who are not already doctors or team members
        available_users = User.objects.exclude(
            Q(user_id__in=Doctor.objects.values_list('user__user_id', flat=True)) |
            Q(role__in=['admin', 'nurse', 'lab_tech'])
        ).select_related('userprofile')

        context = {
            "doctors": doctors,
            "team_members": team_members,
            "available_users": available_users,
            "admin": {"username": "Administrator"}
        }
        return render(request, "mod_doctors.html", context)
    
    # For regular admin login
    user_id = request.session.get("user_id") or request.session.get("user")
    if not user_id:
        messages.error(request, "Please login to access admin dashboard")
        return redirect("homepage2")
    
    try:
        admin_user = User.objects.get(user_id=user_id, role="admin")
        doctors = Doctor.objects.select_related('user').all()
        # Get all users who are not already doctors or team members
        available_users = User.objects.exclude(
            Q(user_id__in=Doctor.objects.values_list('user__user_id', flat=True)) |
            Q(role__in=['admin', 'nurse', 'lab_tech'])
        ).select_related('userprofile')

        context = {
            "doctors": doctors,
            "team_members": team_members,
            "available_users": available_users,
            "admin": admin_user
        }
        return render(request, "mod_doctors.html", context)
    except User.DoesNotExist:
        messages.error(request, "Unauthorized access")
        return redirect("homepage2")


@require_http_methods(["GET"])
def get_doctor_details(request, doctor_id):
    """Return JSON details for a doctor used by the edit modal."""
    if not (request.session.get("is_admin") or 
            User.objects.filter(user_id=request.session.get("user"), role="admin").exists()):
        return JsonResponse({"error": "Unauthorized"}, status=403)

    try:
        doctor = Doctor.objects.select_related('user').get(doctor_id=doctor_id)
        try:
            profile = UserProfile.objects.get(user=doctor.user)
            # photo_url is now a TextField with base64 data URL
            photo_url = profile.photo_url if profile.photo_url else None
            first_name = profile.first_name
            last_name = profile.last_name
        except UserProfile.DoesNotExist:
            photo_url = None
            first_name = ''
            last_name = ''

        return JsonResponse({
            "doctor_id": doctor.doctor_id,
            "user_id": doctor.user.user_id,
            "first_name": first_name,
            "last_name": last_name,
            "name": doctor.user.get_full_name(),
            "specialization": doctor.specialization,
            "license_number": doctor.license_number,
            "years_of_experience": doctor.years_of_experience,
            "contact_info": doctor.contact_info,
            "photo_url": photo_url,
        })
    except Doctor.DoesNotExist:
        return JsonResponse({"error": "Doctor not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@require_http_methods(["POST"])
def edit_doctor(request, doctor_id):
    """Update doctor fields (admin) and return JSON."""
    if not (request.session.get("is_admin") or 
            User.objects.filter(user_id=request.session.get("user"), role="admin").exists()):
        return JsonResponse({"error": "Unauthorized"}, status=403)

    try:
        doctor = Doctor.objects.select_related('user').get(doctor_id=doctor_id)
        # Basic fields
        if 'specialization' in request.POST:
            doctor.specialization = request.POST.get('specialization')
        if 'license_number' in request.POST:
            doctor.license_number = request.POST.get('license_number')
        if 'years_of_experience' in request.POST:
            try:
                doctor.years_of_experience = int(request.POST.get('years_of_experience') or 0)
            except ValueError:
                pass
        if 'contact_info' in request.POST:
            doctor.contact_info = request.POST.get('contact_info')
        doctor.save()

        # Handle profile photo upload if provided
        try:
            profile, created = UserProfile.objects.get_or_create(user=doctor.user)
            if 'photo' in request.FILES:
                uploaded = request.FILES['photo']
                profile.photo_url = uploaded
                profile.save()
        except Exception:
            # Non-fatal: allow doctor update to continue even if profile save fails
            pass

        return JsonResponse({
            "success": True,
            "doctor": {
                "doctor_id": doctor.doctor_id,
                "user_id": doctor.user.user_id,
                "specialization": doctor.specialization,
                "license_number": doctor.license_number,
                "years_of_experience": doctor.years_of_experience,
                "contact_info": doctor.contact_info,
            }
        })
    except Doctor.DoesNotExist:
        return JsonResponse({"error": "Doctor not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@require_http_methods(["GET"])
def get_doctor_patients(request, doctor_id):
    """Return unique patients for a specific doctor (admin view, JSON)."""
    if not (request.session.get("is_admin") or 
            User.objects.filter(user_id=request.session.get("user"), role="admin").exists()):
        return JsonResponse({"error": "Unauthorized"}, status=403)

    try:
        doctor = Doctor.objects.get(doctor_id=doctor_id)
        # Gather unique patient users from the doctor's appointments
        appts = (
            Appointment.objects
            .select_related('patient', 'patient__userprofile')
            .filter(doctor=doctor)
        )
        seen = set()
        patients = []
        for appt in appts:
            uid = getattr(appt.patient, 'user_id', None)
            if uid and uid not in seen:
                seen.add(uid)
                profile = getattr(appt.patient, 'userprofile', None)
                # photo_url is now a TextField with base64 data URL
                photo_url = profile.photo_url if (profile and profile.photo_url) else None
                patients.append({
                    'user_id': uid,
                    'name': appt.patient.get_full_name(),
                    'email': appt.patient.email,
                    'photo_url': photo_url,
                })

        # Appointments of this doctor
        appointments = []
        try:
            appt_qs = Appointment.objects.select_related('patient').filter(doctor=doctor).order_by('-consultation_date', '-consultation_time')
            for a in appt_qs:
                appointments.append({
                    'appointment_id': getattr(a, 'consultation_id', None),
                    'patient_name': a.patient.get_full_name() if getattr(a, 'patient', None) else '',
                    'patient_id': getattr(a.patient, 'user_id', None) if getattr(a, 'patient', None) else None,
                    'consultation_type': getattr(a, 'consultation_type', ''),
                    'consultation_date': getattr(a, 'consultation_date', None).isoformat() if getattr(a, 'consultation_date', None) else None,
                    'consultation_time': getattr(a, 'consultation_time', None).isoformat() if getattr(a, 'consultation_time', None) else None,
                    'status': getattr(a, 'status', ''),
                    'created_at': getattr(a, 'created_at', None).isoformat() if getattr(a, 'created_at', None) else None,
                })
        except Exception:
            appointments = []

        # Prescriptions made by this doctor (via live appointment -> appointment)
        prescriptions = []
        try:
            # Include prescriptions either directly linked to the doctor or via the appointment
            pres_qs = Prescription.objects.select_related('live_appointment__appointment__patient').filter(
                Q(live_appointment__appointment__doctor=doctor) | Q(doctor=doctor)
            ).order_by('-created_at')
            for p in pres_qs:
                patient = None
                try:
                    patient = p.live_appointment.appointment.patient
                except Exception:
                    patient = None
                prescriptions.append({
                    'prescription_id': getattr(p, 'prescription_id', None),
                    'prescription_number': p.prescription_number,
                    'patient_name': patient.get_full_name() if patient else '',
                    'patient_id': getattr(patient, 'user_id', None) if patient else None,
                    'status': p.status,
                    'created_at': getattr(p, 'created_at', None).isoformat() if getattr(p, 'created_at', None) else None,
                    'has_file': bool(getattr(p, 'prescription_file', None)),
                })
        except Exception:
            prescriptions = []

        return JsonResponse({
            'doctor_id': doctor_id,
            'patients': patients,
            'appointments': appointments,
            'prescriptions': prescriptions,
            'count': len(patients),
        })
    except Doctor.DoesNotExist:
        return JsonResponse({"error": "Doctor not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@require_http_methods(["POST"])
@csrf_exempt
def add_medisafe_member(request):
    """Convert a user to admin, nurse, or lab_tech (Radiologic Technologist)"""
    if not (request.session.get("is_admin") or 
            User.objects.filter(user_id=request.session.get("user"), role="admin").exists()):
        return JsonResponse({"error": "Unauthorized"}, status=403)
    
    try:
        data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
        user_id = data.get('user_id')
        role = data.get('role')  # 'admin', 'nurse', or 'lab_tech'
        
        if not user_id or not role:
            return JsonResponse({"error": "User ID and role are required"}, status=400)
        
        if role not in ['admin', 'nurse', 'lab_tech']:
            return JsonResponse({"error": "Invalid role. Must be admin, nurse, or lab_tech"}, status=400)
        
        with transaction.atomic():
            user = User.objects.get(user_id=user_id)
            
            # Check if user is already a doctor
            if Doctor.objects.filter(user=user).exists():
                return JsonResponse({"error": "User is already a doctor. Cannot convert to team member."}, status=400)
            
            # Check if user already has this role
            if user.role == role:
                return JsonResponse({"error": f"User is already a {role}"}, status=400)
            
            # If user was a patient, remove patient record
            if user.role == 'patient':
                try:
                    Patient.objects.filter(user=user).delete()
                except Exception:
                    pass  # Non-fatal
            
            # Update user role
            user.role = role
            user.save()
            
            # Get user profile for display
            try:
                profile = UserProfile.objects.get(user=user)
                name = f"{profile.first_name or ''} {profile.last_name or ''}".strip() or user.username
            except UserProfile.DoesNotExist:
                name = user.username
            
            role_display = {
                'admin': 'Admin',
                'nurse': 'Nurse',
                'lab_tech': 'Radiologic Technologist'
            }.get(role, role)
            
            return JsonResponse({
                "success": True,
                "message": f"User successfully converted to {role_display}",
                "member": {
                    "user_id": user.user_id,
                    "name": name,
                    "email": user.email,
                    "role": role,
                    "role_display": role_display
                }
            })
            
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)


@require_http_methods(["POST"])
@csrf_exempt
def convert_member_to_patient(request, user_id):
    """Convert a team member (admin/nurse/lab_tech/doctor) to patient"""
    if not (request.session.get("is_admin") or 
            User.objects.filter(user_id=request.session.get("user"), role="admin").exists()):
        return JsonResponse({"error": "Unauthorized"}, status=403)
    
    try:
        with transaction.atomic():
            user = User.objects.get(user_id=user_id)
            
            # Check if user is a team member (including doctor)
            if user.role not in ['admin', 'nurse', 'lab_tech', 'doctor']:
                return JsonResponse({"error": "User is not a team member"}, status=400)
            
            # Store original role for logging
            original_role = user.role
            
            # If user is a doctor, we need to handle the Doctor record
            if user.role == 'doctor':
                try:
                    doctor_record = Doctor.objects.get(user=user)
                    # We keep the doctor record but mark user as patient
                    # This preserves historical data while changing access level
                except Doctor.DoesNotExist:
                    pass
            
            # Update user role to patient
            user.role = 'patient'
            user.save()
            
            # Create patient record if it doesn't exist
            patient, created = Patient.objects.get_or_create(user=user)
            
            return JsonResponse({
                "success": True,
                "message": f"Team member successfully converted from {original_role} to patient",
                "original_role": original_role,
                "new_role": "patient",
                "patient_created": created
            })
            
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)

@require_http_methods(["POST"])
@csrf_exempt
def convert_doctor_to_patient(request, doctor_id):
    """Convert a doctor to patient and delete their doctor record"""
    if not (request.session.get("is_admin") or 
            User.objects.filter(user_id=request.session.get("user"), role="admin").exists()):
        return JsonResponse({"error": "Unauthorized"}, status=403)
    
    try:
        with transaction.atomic():
            # Get the doctor record
            doctor = Doctor.objects.get(doctor_id=doctor_id)
            user = doctor.user
            
            # Store original info for logging
            doctor_name = user.get_full_name()
            
            # Create patient record if it doesn't exist
            patient, created = Patient.objects.get_or_create(user=user)
            
            # Update user role to patient
            user.role = 'patient'
            user.save()
            
            # Delete the doctor record (this removes them from doctor table)
            doctor.delete()
            
            return JsonResponse({
                "success": True,
                "message": f"Doctor {doctor_name} has been successfully converted to patient and removed from doctor list.",
                "patient_created": created
            })
            
    except Doctor.DoesNotExist:
        return JsonResponse({"error": "Doctor not found"}, status=404)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)
