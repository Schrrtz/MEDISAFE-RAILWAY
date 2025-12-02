# Signup Profile Photo Fix Summary

## Issues Fixed

### 1. Profile Photo Not Saving to Database
**Problem**: During signup, the profile photo was not being saved to `user_profiles.photo_url` column.

**Root Cause**: The signup form was sending data as JSON, which cannot include file uploads. Files must be sent as `multipart/form-data` (FormData).

**Solution**:
- Modified `auth/views.py` signup function to handle both FormData and JSON requests
- Added `photo_url = request.FILES.get("photo_url")` to retrieve uploaded files
- Updated `UserProfile.objects.create()` to include `photo_url=photo_url` parameter
- Changed frontend to send FormData instead of JSON

### 2. Camera Access Not Working Properly
**Problem**: Camera functionality existed but wasn't fully integrated with the form submission.

**Solution**:
- Fixed camera initialization with proper error handling for different error types:
  - `NotAllowedError`: User denied camera permission
  - `NotFoundError`: No camera device available
  - `NotReadableError`: Camera already in use
- Improved video stream handling with `await video.play()`
- Enhanced photo capture with higher quality (0.9 JPEG quality, 1280x720 resolution)
- Added DataTransfer to properly set file input with captured photo
- Added visual feedback when photo is captured or file is selected
- Added automatic cleanup of camera stream

## Technical Changes

### Backend (auth/views.py)

```python
# Now handles both FormData and JSON
is_multipart = request.content_type and 'multipart/form-data' in request.content_type

if is_multipart:
    # Handle FormData with file upload
    photo_url = request.FILES.get("photo_url")
else:
    # Handle JSON (backward compatibility)
    photo_url = None

# Save photo to UserProfile
UserProfile.objects.create(
    user=user,
    # ... other fields ...
    photo_url=photo_url if photo_url else None,
)
```

### Frontend (auth_modals.html)

**Form Submission**: Changed from JSON to FormData
```javascript
// Old: JSON.stringify(userData)
// New: FormData with file support
const formData = new FormData();
formData.append('first_name', ...);
formData.append('photo_url', photoInput.files[0]);

const response = await fetch('/signup/', {
    method: 'POST',
    headers: { 'X-CSRFToken': csrfToken },
    body: formData  // Not JSON
});
```

**Camera Functionality**: Enhanced error handling and feedback
```javascript
// Improved camera access with specific error messages
stream = await navigator.mediaDevices.getUserMedia({ 
    video: { 
        facingMode: 'user',
        width: { ideal: 1280 },
        height: { ideal: 720 }
    } 
});

// Proper photo capture with file creation
canvas.toBlob((blob) => {
    const file = new File([blob], `profile_photo_${timestamp}.jpg`, { 
        type: 'image/jpeg' 
    });
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    patientPhotoInput.files = dataTransfer.files;
}, 'image/jpeg', 0.9);
```

## Database Schema

The profile photo is stored in:
- **Table**: `user_profiles`
- **Column**: `photo_url` (ImageField)
- **Upload Path**: `media/profile_photos/`
- **File Format**: JPEG (from camera) or any image format (from file upload)

## How to Test

1. **Server is running** at http://127.0.0.1:8000/

2. **Test File Upload**:
   - Click "Click to Register" on homepage
   - Fill out signup form
   - Click "Choose File" under "Patient Photo"
   - Select an image file
   - Submit form
   - Check database: `SELECT photo_url FROM user_profiles WHERE user_id = [new_user_id]`

3. **Test Camera Capture**:
   - Click "Click to Register"
   - Fill out signup form
   - Click "Take Photo with Camera" button
   - Allow camera access when prompted by browser
   - Wait for camera preview to appear
   - Click "Capture" button
   - Photo will be automatically added to form
   - Submit form
   - Verify photo saved in database

4. **Expected Result**:
   - Photo file saved to: `media/profile_photos/[filename]`
   - Database record: `user_profiles.photo_url = 'profile_photos/[filename]'`
   - Photo visible in user profile after login

## Browser Permissions

For camera access to work, users must:
1. Use HTTPS in production (HTTP localhost works for development)
2. Grant camera permission when browser prompts
3. Have a working camera device
4. Ensure camera is not in use by another application

## Error Handling

The system now provides specific error messages:
- ✅ "Camera access denied. Please allow camera access in your browser settings and try again."
- ✅ "No camera found on your device."
- ✅ "Camera is already in use by another application."
- ✅ "Photo captured successfully! (X.X KB)"
- ✅ "Photo selected: filename.jpg (X.X KB)"

## Files Modified

1. `PBL/myapp/features/auth/views.py` - Backend signup handler
2. `PBL/myapp/templates/components/auth_modals.html` - Frontend form and camera logic

## Testing Status

- ✅ Server running successfully
- ✅ No syntax errors
- ✅ Backward compatibility maintained (JSON still works)
- ⏳ Ready for user testing

## Next Steps

1. Test signup with file upload
2. Test signup with camera capture
3. Verify photos appear in user profiles
4. Check media folder for saved files
5. Verify database records

---
**Date**: November 30, 2025
**Status**: ✅ Complete - Ready for Testing
