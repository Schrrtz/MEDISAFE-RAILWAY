from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse, FileResponse, HttpResponse
from django.db import IntegrityError, models
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from ...models import User, UserProfile, Notification
import json
import os
import base64


def _get_session_admin_user(request):
    """Return the logged-in user object if available."""
    session_user_id = request.session.get("user_id") or request.session.get("user")
    if not session_user_id:
        return None
    try:
        return User.objects.get(user_id=session_user_id)
    except User.DoesNotExist:
        return None

def mod_users(request):
    """User management view"""
    # Check for admin session first
    if request.session.get("is_admin"):
        if request.method == 'POST':
            action = request.POST.get('action')
            
            if action == 'add':
                # Get form data
                username = request.POST.get('username')
                email = request.POST.get('email')
                role = request.POST.get('role')
                password = request.POST.get('password')
                sex = request.POST.get('sex', '')
                birthday = request.POST.get('birthday', '')
                first_name = request.POST.get('first_name', '')
                last_name = request.POST.get('last_name', '')
                middle_name = request.POST.get('middle_name', '')
                address = request.POST.get('address', '')
                contact_number = request.POST.get('contact_number', '')
                civil_status = request.POST.get('civil_status', '')

                if not all([username, email, role, password]):
                    messages.error(request, "All fields are required")
                    return redirect('mod_users')

                try:
                    new_user = User.objects.create(
                        username=username,
                        email=email,
                        role=role,
                        is_active=True,
                        first_name=first_name,
                        last_name=last_name
                    )
                    new_user.set_password(password)
                    new_user.save()

                    UserProfile.objects.create(
                        user=new_user,
                        sex=sex,
                        birthday=birthday if birthday else None,
                        middle_name=middle_name,
                        address=address,
                        contact_number=contact_number,
                        civil_status=civil_status
                    )
                    
                    messages.success(request, f"{role.capitalize()} added successfully!")
                except IntegrityError:
                    messages.error(request, "Username or email already exists")
                except Exception as e:
                    if 'new_user' in locals():
                        new_user.delete()
                    messages.error(request, f"Error adding user: {str(e)}")

            elif action == 'edit':
                user_id = request.POST.get('user_id')
                if not user_id:
                    messages.error(request, "No user specified for editing")
                    return redirect('mod_users')

                try:
                    user_to_edit = User.objects.get(user_id=user_id)
                    user_to_edit.username = request.POST.get('username', user_to_edit.username)
                    user_to_edit.email = request.POST.get('email', user_to_edit.email)
                    user_to_edit.role = request.POST.get('role', user_to_edit.role)
                    
                    new_password = request.POST.get('password')
                    if new_password and new_password.strip():
                        user_to_edit.set_password(new_password)
                    
                    status_value = request.POST.get('status')
                    if status_value:
                        is_active_flag = True if status_value == 'active' else False
                        user_to_edit.is_active = is_active_flag
                        if hasattr(user_to_edit, 'status'):
                            user_to_edit.status = is_active_flag
                    
                    user_to_edit.save()

                    profile, created = UserProfile.objects.get_or_create(user=user_to_edit)
                    
                    profile.first_name = request.POST.get('first_name', profile.first_name)
                    profile.middle_name = request.POST.get('middle_name', profile.middle_name)
                    profile.last_name = request.POST.get('last_name', profile.last_name)
                    profile.sex = request.POST.get('sex', profile.sex)
                    profile.contact_number = request.POST.get('contact_number', profile.contact_number)
                    contact_person = request.POST.get('contact_person')
                    if contact_person is None:
                        contact_person = request.POST.get('emergency_contact')
                    if contact_person is not None:
                        profile.contact_person = contact_person
                    profile.address = request.POST.get('address', profile.address)
                    profile.civil_status = request.POST.get('civil_status', profile.civil_status)
                    
                    birthday = request.POST.get('birthday')
                    if birthday:
                        try:
                            from datetime import datetime
                            profile.birthday = datetime.strptime(birthday, '%Y-%m-%d').date()
                        except (ValueError, TypeError):
                            pass
                    
                    profile.save()

                    messages.success(request, f"User '{user_to_edit.username}' updated successfully!")
                except User.DoesNotExist:
                    messages.error(request, "User not found")
                except IntegrityError:
                    messages.error(request, "Username or email already exists")
                except Exception as e:
                    messages.error(request, f"Error updating user: {str(e)}")
                
            elif action == 'delete':
                user_id_to_delete = request.POST.get('user_id')
                if not user_id_to_delete:
                    messages.error(request, "No user specified for deletion")
                    return redirect('mod_users')

                try:
                    user_to_delete = User.objects.get(user_id=user_id_to_delete)
                    username = user_to_delete.username
                    user_to_delete.delete()
                    messages.success(request, f"User '{username}' deleted successfully!")
                except User.DoesNotExist:
                    messages.error(request, "User not found")
                except Exception as e:
                    messages.error(request, f"Error deleting user: {str(e)}")

            elif action == 'toggle_status':
                user_id_to_toggle = request.POST.get('user_id')
                if not user_id_to_toggle:
                    messages.error(request, "No user specified for status toggle")
                    return redirect('mod_users')

                try:
                    user_to_toggle = User.objects.get(user_id=user_id_to_toggle)
                    user_to_toggle.is_active = not user_to_toggle.is_active
                    user_to_toggle.save()
                    status = "activated" if user_to_toggle.is_active else "deactivated"
                    messages.success(request, f"User '{user_to_toggle.username}' {status} successfully!")
                except User.DoesNotExist:
                    messages.error(request, "User not found")
                except Exception as e:
                    messages.error(request, f"Error toggling user status: {str(e)}")

        # Get all users
        # Super admin checks and deleted accounts data
        is_super_admin = request.session.get("is_super_admin", False)
        deleted_accounts = []
        deleted_accounts_count = 0
        
        if is_super_admin:
            # Super admin sees all users and accounts including deleted ones
            users = User.objects.all().select_related('userprofile').order_by('username')
            all_accounts = User.objects.order_by('-date_joined')
            # Get deleted accounts (username starts with deleted_)
            deleted_accounts = User.objects.filter(
                username__startswith="deleted_"
            ).order_by('-date_joined')
            deleted_accounts_count = deleted_accounts.count()
        else:
            # Regular admin only sees non-deleted users and accounts
            users = User.objects.exclude(
                username__startswith="deleted_"
            ).select_related('userprofile').order_by('username')
            all_accounts = User.objects.exclude(
                username__startswith="deleted_"
            ).order_by('-date_joined')
        
        total_users_count = User.objects.count()
        active_users_count = User.objects.filter(is_active=True).count()
        inactive_users_count = User.objects.filter(is_active=False).count()
        total_accounts = User.objects.count()
        if hasattr(User, 'status'):
            active_accounts = User.objects.filter(status=True).count()
            inactive_accounts = User.objects.filter(status=False).count()
        else:
            active_accounts = User.objects.filter(is_active=True).count()
            inactive_accounts = User.objects.filter(is_active=False).count()

        context = {
            'users': users,
            'user_roles': ['admin', 'staff', 'patient'],
            'total_users_count': total_users_count,
            'active_users_count': active_users_count,
            'inactive_users_count': inactive_users_count,
            'total_accounts': total_accounts,
            'active_accounts': active_accounts,
            'inactive_accounts': inactive_accounts,
            'accounts': all_accounts,
            'all_accounts': all_accounts,
            'is_super_admin': is_super_admin,
            'deleted_accounts': deleted_accounts,
            'deleted_accounts_count': deleted_accounts_count,
        }
        return render(request, "user_management.html", context)
    
    # Check for regular admin user
    user_id = request.session.get("user_id") or request.session.get("user")
    if not user_id:
        messages.error(request, "Please login first")
        return redirect("homepage2")
    
    try:
        admin = User.objects.get(user_id=user_id)
        if admin.role != 'admin':
            messages.error(request, "Access denied. Admin privileges required.")
            return redirect("homepage2")

        # Super admin checks and deleted accounts data
        is_super_admin = request.session.get("is_super_admin", False)
        deleted_accounts = []
        deleted_accounts_count = 0
        
        if is_super_admin:
            # Super admin sees all users and accounts including deleted ones
            users = User.objects.exclude(user_id=user_id).select_related('userprofile').order_by('username')
            all_accounts = User.objects.order_by('-date_joined')
            # Get deleted accounts (username starts with deleted_)
            deleted_accounts = User.objects.filter(
                username__startswith="deleted_"
            ).order_by('-date_joined')
            deleted_accounts_count = deleted_accounts.count()
        else:
            # Regular admin only sees non-deleted users and accounts
            users = User.objects.exclude(user_id=user_id).exclude(
                username__startswith="deleted_"
            ).select_related('userprofile').order_by('username')
            all_accounts = User.objects.exclude(
                username__startswith="deleted_"
            ).order_by('-date_joined')
        
        total_users_count = User.objects.count()
        active_users_count = User.objects.filter(is_active=True).count()
        inactive_users_count = User.objects.filter(is_active=False).count()
        total_accounts = User.objects.count()
        if hasattr(User, 'status'):
            active_accounts = User.objects.filter(status=True).count()
            inactive_accounts = User.objects.filter(status=False).count()
        else:
            active_accounts = User.objects.filter(is_active=True).count()
            inactive_accounts = User.objects.filter(is_active=False).count()

        context = {
            'users': users,
            'current_admin_id': user_id,
            'user_roles': ['admin', 'staff', 'patient'],
            'total_users_count': total_users_count,
            'active_users_count': active_users_count,
            'inactive_users_count': inactive_users_count,
            'total_accounts': total_accounts,
            'active_accounts': active_accounts,
            'inactive_accounts': inactive_accounts,
            'accounts': all_accounts,
            'all_accounts': all_accounts,
            'is_super_admin': is_super_admin,
            'deleted_accounts': deleted_accounts,
            'deleted_accounts_count': deleted_accounts_count,
        }
        return render(request, "user_management.html", context)

    except User.DoesNotExist:
        messages.error(request, "User not found")
        return redirect("homepage2")


@csrf_exempt
@require_http_methods(["POST"])
def mark_password_reset_as_read(request, notification_id):
    """Mark a password reset notification as read"""
    session_admin = _get_session_admin_user(request)
    if not (request.session.get("is_admin") or (session_admin and session_admin.role == 'admin')):
        return JsonResponse({"error": "Unauthorized", "success": False}, status=403)
    
    try:
        notification = Notification.objects.get(notification_id=notification_id)
        notification.is_read = True
        notification.save()
        return JsonResponse({"success": True, "message": "Notification marked as read"})
    except Notification.DoesNotExist:
        return JsonResponse({"error": "Notification not found", "success": False}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e), "success": False}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def download_password_reset_file(request, notification_id):
    """
    Download the ID photo file from a password reset request
    """
    session_admin = _get_session_admin_user(request)
    if not (request.session.get("is_admin") or (session_admin and session_admin.role == 'admin')):
        return JsonResponse({"error": "Unauthorized"}, status=403)
    
    try:
        notification = Notification.objects.get(notification_id=notification_id)
        
        if not notification.file:
            return JsonResponse({"error": "No file attached to this notification"}, status=404)
        
        # Notification.file contains base64 data URL (data:image/jpeg;base64,...)
        # Extract the base64 part and decode it
        try:
            if notification.file.startswith('data:'):
                # Parse data URL: data:mime/type;base64,base64data
                header, base64_data = notification.file.split(',', 1)
                mime_type = header.split(':')[1].split(';')[0]
                
                # Decode base64
                file_content = base64.b64decode(base64_data)
                
                # Determine file extension from mime type
                extension_map = {
                    'image/jpeg': '.jpg',
                    'image/png': '.png',
                    'image/gif': '.gif'
                }
                file_ext = extension_map.get(mime_type, '.jpg')
                
                # Create response
                response = HttpResponse(file_content, content_type=mime_type)
                response['Content-Disposition'] = f'attachment; filename="id_photo_{notification_id}{file_ext}"'
                return response
            else:
                return JsonResponse({"error": "Invalid file format"}, status=400)
        except Exception as decode_error:
            return JsonResponse({"error": f"Error decoding file: {str(decode_error)}"}, status=500)
        
    except Notification.DoesNotExist:
        return JsonResponse({"error": "Notification not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_password_reset_requests(request, user_id):
    """
    API endpoint to get all password reset requests for a specific user
    Returns JSON list of password reset notifications with file info
    """
    session_admin = _get_session_admin_user(request)
    if not (request.session.get("is_admin") or (session_admin and session_admin.role == 'admin')):
        return JsonResponse({"error": "Unauthorized"}, status=403)
    
    try:
        user = User.objects.get(user_id=user_id)
        
        notifications = Notification.objects.filter(
            notification_type='password_reset',
            related_id=user_id
        ).exclude(user=user).select_related('user').order_by('-created_at')
        
        data = {
            "success": True,
            "user_id": user_id,
            "username": user.username,
            "email": user.email,
            "total_requests": notifications.count(),
            "requests": []
        }
        
        for notification in notifications:
            request_data = {
                "notification_id": notification.notification_id,
                "title": notification.title,
                "message": notification.message,
                "created_at": notification.created_at.isoformat(),
                "is_read": notification.is_read,
                "priority": notification.priority,
                "has_file": bool(notification.file),
                "file_name": f"id_photo_{notification.notification_id}" if notification.file else None,
                "file_url": notification.file if notification.file else None  # Direct base64 data URL
            }
            data["requests"].append(request_data)
        
        return JsonResponse(data)
        
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found", "success": False}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e), "success": False}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def permanent_delete_account(request):
    """
    Permanently delete a user account and ALL associated records (Super Admin only)
    This is irreversible and removes all medical data
    """
    # Check for admin/super admin permission with multiple fallbacks
    is_admin = (
        request.session.get("is_admin", False) or
        request.session.get("is_super_admin", False) or
        User.objects.filter(user_id=request.session.get("user"), role="admin").exists()
    )
    
    if not is_admin:
        return JsonResponse({
            "success": False,
            "message": "Access denied. Admin privileges required to permanently delete accounts."
        }, status=403)
    
    try:
        user_id = request.POST.get('user_id')
        if not user_id:
            return JsonResponse({
                "success": False,
                "message": "User ID is required"
            }, status=400)
        
        user = User.objects.get(user_id=user_id)
        
        # Verify this is a deleted account (starts with deleted_)
        if not user.username.startswith('deleted_'):
            return JsonResponse({
                "success": False,
                "message": "Only soft-deleted accounts can be permanently deleted"
            }, status=400)
        
        # Store username for logging
        username = user.username
        
        # Import all related models
        from ...models import (
            UserProfile, Doctor, Patient, Appointment, 
            LabResult, Prescription, Notification, LiveAppointment
        )
        from django.db.models import Q
        
        # Count records before deletion for logging
        deleted_counts = {}
        
        # Delete all related records (Django CASCADE will handle most, but being explicit)
        try:
            # User Profile
            profiles = UserProfile.objects.filter(user=user)
            deleted_counts['profiles'] = profiles.count()
            profiles.delete()
            
            # Doctor records
            doctors = Doctor.objects.filter(user=user)
            deleted_counts['doctors'] = doctors.count()
            doctors.delete()
            
            # Patient records
            patients = Patient.objects.filter(user=user)
            deleted_counts['patients'] = patients.count()
            patients.delete()
            
            # Appointments (as patient or doctor)
            appointments_as_patient = Appointment.objects.filter(patient=user)
            appointments_as_doctor = Appointment.objects.filter(doctor__user=user)
            deleted_counts['appointments'] = appointments_as_patient.count() + appointments_as_doctor.count()
            appointments_as_patient.delete()
            appointments_as_doctor.delete()
            
            # Live Appointments - using Q for complex queries
            live_appointments = LiveAppointment.objects.filter(
                Q(appointment__patient=user) | Q(appointment__doctor__user=user)
            )
            deleted_counts['live_appointments'] = live_appointments.count()
            live_appointments.delete()
            
            # Lab Results
            lab_results = LabResult.objects.filter(user=user)
            deleted_counts['lab_results'] = lab_results.count()
            lab_results.delete()
            
            # Prescriptions - using correct fields based on model
            prescriptions = Prescription.objects.filter(
                Q(live_appointment__appointment__patient=user) | Q(doctor__user=user)
            )
            deleted_counts['prescriptions'] = prescriptions.count()
            prescriptions.delete()
            
            # Notifications
            notifications = Notification.objects.filter(user=user)
            deleted_counts['notifications'] = notifications.count()
            notifications.delete()
            
            # Finally delete the user account
            user.delete()
            
            # Log the permanent deletion
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"PERMANENT DELETION: User {username} (ID: {user_id}) and all records permanently deleted by super admin. "
                       f"Deleted: {deleted_counts}")
            
            return JsonResponse({
                "success": True,
                "message": f"Account {username} and all associated records permanently deleted",
                "deleted_counts": deleted_counts
            })
            
        except Exception as deletion_error:
            return JsonResponse({
                "success": False,
                "message": f"Error during deletion: {str(deletion_error)}"
            }, status=500)
        
    except User.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "User not found"
        }, status=404)
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": f"An error occurred: {str(e)}"
        }, status=500)

