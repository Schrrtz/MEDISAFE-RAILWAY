# View Photo Feature Implementation Summary

## Overview
Added "View Photo" button functionality to the Password Reset Requests modal in the User Management page. When clicked, the button downloads the ID photo attached to the password reset notification from the database.

## Changes Made

### 1. Backend - user_views.py
**File:** `myapp/features/admin/user_views.py`

**Added Function:** `download_password_reset_file(request, notification_id)`
- Retrieves the notification from the database by `notification_id`
- Checks if the notification has an attached file
- Decodes the base64 data URL stored in the `file` column of the `notifications` table
- Extracts the MIME type and determines the file extension
- Returns the file as an HTTP response with proper headers for download
- Handles authentication (admin only) and error cases

### 2. URL Routing - urls.py
**File:** `myapp/features/admin/urls.py`

**Added Route:**
```python
path('api/download-password-reset-file/<int:notification_id>/', 
     user_views.download_password_reset_file, 
     name='download_password_reset_file')
```

### 3. Frontend - user_management.html
**File:** `myapp/features/admin/templates/user_management.html`

**Modified Section:** Password Reset Requests modal display logic (around line 2516)
- Added conditional "View Photo" button that appears only when `request.has_file` is true
- Button appears next to the "ID Photo Attached" badge
- Styled with blue background (`bg-blue-500`) to differentiate from other action buttons

**Added JavaScript Function:** `downloadPasswordResetFile(notificationId)`
- Creates a temporary anchor element
- Sets the download URL to the new API endpoint
- Triggers the download
- Shows a success notification
- Cleans up the temporary element

## How It Works

1. **User Flow:**
   - Admin opens User Management page
   - Clicks the 3rd action button (Password Reset Requests icon)
   - Password Reset Requests modal opens
   - For requests with attached photos, a blue "View Photo" button appears
   - Clicking "View Photo" downloads the ID photo file

2. **Data Flow:**
   - JavaScript calls `/api/download-password-reset-file/{notification_id}/`
   - Backend retrieves notification from `notifications` table
   - Extracts base64 data from `file` column
   - Decodes and returns as downloadable file
   - Browser downloads the file with name format: `id_photo_{notification_id}.{extension}`

## Database Schema
**Table:** `notifications`
- `notification_id` (Primary Key) - Used to identify the specific notification
- `file` (TextField) - Stores base64 data URL in format: `data:image/jpeg;base64,{base64_data}`
- `notification_type` - Filtered by 'password_reset'

## Security
- Admin authentication required for download endpoint
- Session-based authentication check
- Only admins can access the download functionality
- Proper error handling for missing files and invalid data

## Testing Checklist
- [x] Django check passes with no errors
- [ ] Verify button appears only when file is attached
- [ ] Test downloading different image formats (JPEG, PNG, GIF)
- [ ] Verify authentication - non-admin users should not access the endpoint
- [ ] Test with notifications that have no file attached
- [ ] Verify file downloads with correct name and extension
- [ ] Test on mobile responsive view

## Technical Notes
- File is stored as base64 data URL in database
- Supports JPEG, PNG, and GIF formats
- Default extension is .jpg if MIME type not recognized
- Download is triggered using temporary anchor element
- No breaking changes to existing functionality
