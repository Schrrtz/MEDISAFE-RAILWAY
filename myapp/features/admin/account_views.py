from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from ...models import User, UserProfile

def mod_accounts(request):
    """Account management view"""
    # Check for admin session first
    if request.session.get("is_admin"):
        # Get account statistics
        total_accounts = User.objects.count()
        active_accounts = User.objects.filter(status=True, is_active=True).count()
        inactive_accounts = User.objects.filter(status=False, is_active=True).count()
        
        # Only super admins can see deleted accounts
        is_super_admin = request.session.get("is_super_admin", False)
        deleted_accounts = 0
        deleted_accounts_list = []
        
        if is_super_admin:
            deleted_accounts = User.objects.filter(is_active=False, username__startswith='deleted_').count()
            # Get deleted accounts for admin review
            deleted_accounts_list = User.objects.filter(
                username__startswith='deleted_'
            ).order_by('-date_joined')[:10]  # Show last 10 deleted accounts

        # Get recent activity (last 5 user creations/modifications)
        recent_accounts = User.objects.exclude(username__startswith='deleted_').order_by('-date_joined')[:5]

        context = {
            'total_accounts': total_accounts,
            'active_accounts': active_accounts,
            'inactive_accounts': inactive_accounts,
            'deleted_accounts': deleted_accounts,
            'accounts': recent_accounts,  # Changed from recent_accounts to accounts
            'deleted_accounts_list': deleted_accounts_list,
            'is_super_admin': is_super_admin,
        }
        return render(request, "mod_accounts.html", context)
    
    # Check for regular admin user
    user_id = request.session.get("user_id") or request.session.get("user")
    if not user_id:
        messages.error(request, "Please login first")
        return redirect("homepage2")
    
    try:
        user = User.objects.get(user_id=user_id)
        if user.role != 'admin':
            messages.error(request, "Access denied. Admin privileges required.")
            return redirect("homepage2")

        # Get account statistics
        total_accounts = User.objects.count()
        active_accounts = User.objects.filter(status=True, is_active=True).count()
        inactive_accounts = User.objects.filter(status=False, is_active=True).count()
        
        # Check if user is super admin for deleted accounts visibility
        is_super_admin = user.role == 'admin' and getattr(user, 'is_superuser', False)
        deleted_accounts = 0
        deleted_accounts_list = []
        
        if is_super_admin:
            deleted_accounts = User.objects.filter(is_active=False, username__startswith='deleted_').count()
            # Get deleted accounts for admin review
            deleted_accounts_list = User.objects.filter(
                username__startswith='deleted_'
            ).order_by('-date_joined')[:10]  # Show last 10 deleted accounts

        # Get recent activity (last 5 user creations/modifications)
        recent_accounts = User.objects.exclude(username__startswith='deleted_').order_by('-date_joined')[:5]

        context = {
            'total_accounts': total_accounts,
            'active_accounts': active_accounts,
            'inactive_accounts': inactive_accounts,
            'deleted_accounts': deleted_accounts,
            'accounts': recent_accounts,  # Changed from recent_accounts to accounts
            'deleted_accounts_list': deleted_accounts_list,
            'is_super_admin': is_super_admin,
        }

    except User.DoesNotExist:
        messages.error(request, "User not found")
        return redirect("homepage2")
        
    return render(request, "mod_accounts.html", context)

@require_POST
def activate_account(request, user_id):
    """Activate a user account"""
    if not request.session.get("is_admin"):
        return JsonResponse({"error": "Unauthorized"}, status=403)
    
    try:
        user = get_object_or_404(User, user_id=user_id)
        user.status = True
        user.is_active = True
        user.save()
        
        return JsonResponse({
            "success": True,
            "message": f"Account {user.username} has been activated successfully."
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": f"Error activating account: {str(e)}"
        }, status=400)

@require_POST
def deactivate_account(request, user_id):
    """Deactivate a user account"""
    if not request.session.get("is_admin"):
        return JsonResponse({"error": "Unauthorized"}, status=403)
    
    try:
        user = get_object_or_404(User, user_id=user_id)
        user.status = False
        user.is_active = False
        user.save()
        
        return JsonResponse({
            "success": True,
            "message": f"Account {user.username} has been deactivated successfully."
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": f"Error deactivating account: {str(e)}"
        }, status=400)

@require_POST
def delete_account(request, user_id):
    """Delete a user account while preserving all medical records and historical data"""
    if not request.session.get("is_admin"):
        return JsonResponse({"error": "Unauthorized"}, status=403)
    
    try:
        from django.db import transaction
        from django.utils import timezone
        from ...models import User, Notification
        
        user = get_object_or_404(User, user_id=user_id)
        username = user.username
        original_email = user.email
        
        # Check if user is trying to delete their own account
        admin_user_id = request.session.get("user_id") or request.session.get("user")
        if str(user.user_id) == str(admin_user_id):
            return JsonResponse({
                "success": False,
                "error": "You cannot delete your own admin account."
            }, status=400)
        
        with transaction.atomic():
            try:
                # Instead of deleting the account, we "soft delete" it by:
                # 1. Deactivating the account completely
                user.is_active = False
                user.status = False
                
                # 2. Marking email as deleted to prevent conflicts if they try to recreate
                deleted_timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
                user.email = f"deleted_{deleted_timestamp}_{original_email}"
                user.username = f"deleted_{deleted_timestamp}_{username}"
                
                # 3. Clear sensitive authentication data
                user.set_unusable_password()  # This makes login impossible
                user.last_login = None
                
                # 4. Save the changes
                user.save()
                
                # 5. Create a system notification about the account deletion
                Notification.objects.create(
                    user=user,
                    title="Account Deactivated",
                    message=f"This account has been permanently deactivated by an administrator on {timezone.now().strftime('%B %d, %Y at %I:%M %p')}. All medical records and historical data have been preserved.",
                    notification_type='system',
                    priority='high',
                    is_read=False
                )
                
                return JsonResponse({
                    "success": True,
                    "message": f"Account '{username}' has been permanently deactivated. All medical records and historical data have been preserved. The account cannot be used for login but data remains accessible for medical continuity."
                })
                
            except Exception as deletion_error:
                import traceback
                error_details = traceback.format_exc()
                print(f"Account deactivation error for user {user_id}: {error_details}")
                return JsonResponse({
                    "success": False,
                    "error": f"Error deactivating account: {str(deletion_error)}"
                }, status=500)
                
    except User.DoesNotExist:
        return JsonResponse({
            "success": False,
            "error": "Account not found"
        }, status=404)
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"General error for user {user_id}: {error_details}")
        return JsonResponse({
            "success": False,
            "error": f"Unexpected error occurred: {str(e)}"
        }, status=500)

@require_POST
def restore_deleted_account(request, user_id):
    """Restore a previously deleted account"""
    if not request.session.get("is_admin"):
        return JsonResponse({"error": "Unauthorized"}, status=403)
    
    try:
        from django.db import transaction
        from django.utils import timezone
        from ...models import User, Notification
        
        user = get_object_or_404(User, user_id=user_id)
        
        # Check if this is actually a deleted account
        if not user.username.startswith('deleted_'):
            return JsonResponse({
                "success": False,
                "error": "This account was not marked as deleted."
            }, status=400)
        
        with transaction.atomic():
            try:
                # Extract original username and email from the deleted format
                # Format: deleted_YYYYMMDD_HHMMSS_originalusername
                parts = user.username.split('_', 3)
                if len(parts) >= 4:
                    original_username = parts[3]
                else:
                    original_username = f"restored_user_{user.user_id}"
                
                parts_email = user.email.split('_', 3)
                if len(parts_email) >= 4:
                    original_email = parts_email[3]
                else:
                    original_email = f"restored_{user.user_id}@restored.local"
                
                # Check if original username/email already exists
                if User.objects.filter(username=original_username).exclude(user_id=user.user_id).exists():
                    original_username = f"{original_username}_restored_{timezone.now().strftime('%Y%m%d')}"
                
                if User.objects.filter(email=original_email).exclude(user_id=user.user_id).exists():
                    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
                    original_email = f"restored_{timestamp}_{original_email}"
                
                # Restore the account
                user.username = original_username
                user.email = original_email
                user.is_active = True
                user.status = True
                
                # Note: Password remains unusable - admin needs to reset it
                user.save()
                
                # Create restoration notification
                Notification.objects.create(
                    user=user,
                    title="Account Restored",
                    message=f"Your account has been restored by an administrator on {timezone.now().strftime('%B %d, %Y at %I:%M %p')}. Please contact an administrator to reset your password.",
                    notification_type='system',
                    priority='high',
                    is_read=False
                )
                
                return JsonResponse({
                    "success": True,
                    "message": f"Account restored successfully as '{original_username}'. The user will need a password reset to log in."
                })
                
            except Exception as restore_error:
                import traceback
                error_details = traceback.format_exc()
                print(f"Account restoration error for user {user_id}: {error_details}")
                return JsonResponse({
                    "success": False,
                    "error": f"Error restoring account: {str(restore_error)}"
                }, status=500)
                
    except User.DoesNotExist:
        return JsonResponse({
            "success": False,
            "error": "Account not found"
        }, status=404)
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"General error for user {user_id}: {error_details}")
        return JsonResponse({
            "success": False,
            "error": f"Unexpected error occurred: {str(e)}"
        }, status=500)
