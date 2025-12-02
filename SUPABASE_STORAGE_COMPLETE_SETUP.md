# Complete Supabase Storage Setup Guide

## Overview
Your MediSafe application now uses Supabase Storage for all file uploads instead of local storage. This provides cloud-based storage with persistent URLs accessible from anywhere.

## Files Stored in Supabase Storage

1. **Profile Photos** - User and doctor profile pictures
2. **Prescriptions** - Prescription PDFs and images uploaded by doctors
3. **Notifications** - ID photos and attachments for password reset requests
4. **Lab Results** - Already configured (no changes needed)

---

## Step 1: Create Storage Buckets

You need to create **THREE** buckets in your Supabase dashboard:

### 1. Profile Photos Bucket
- **Bucket Name:** `profile-photos`
- **Public:** ✅ Yes (make public)
- **File size limit:** 10 MB
- **Allowed MIME types:** image/jpeg, image/png, image/gif

### 2. Prescriptions Bucket
- **Bucket Name:** `prescriptions`
- **Public:** ✅ Yes (make public)
- **File size limit:** 10 MB
- **Allowed MIME types:** application/pdf, image/jpeg, image/png, image/gif

### 3. Notifications Bucket
- **Bucket Name:** `notifications`
- **Public:** ✅ Yes (make public)
- **File size limit:** 10 MB
- **Allowed MIME types:** image/jpeg, image/png, image/gif

---

## Step 2: Create Buckets in Supabase Dashboard

1. **Go to Supabase Dashboard:**
   - Visit: https://supabase.com/dashboard
   - Select your project: `wqoluwmdzljpvzimjiyr`

2. **Navigate to Storage:**
   - Click "Storage" in the left sidebar
   - Click "New bucket" button

3. **Create Each Bucket:**
   
   **For profile-photos:**
   ```
   Name: profile-photos
   Public bucket: ✅ CHECKED
   File size limit: 10485760 (10 MB in bytes)
   Allowed MIME types: image/jpeg,image/png,image/gif,image/jpg
   ```
   
   **For prescriptions:**
   ```
   Name: prescriptions
   Public bucket: ✅ CHECKED
   File size limit: 10485760 (10 MB in bytes)
   Allowed MIME types: application/pdf,image/jpeg,image/png,image/gif,image/jpg
   ```
   
   **For notifications:**
   ```
   Name: notifications
   Public bucket: ✅ CHECKED
   File size limit: 10485760 (10 MB in bytes)
   Allowed MIME types: image/jpeg,image/png,image/gif,image/jpg
   ```

---

## Step 3: Configure Storage Policies

For each bucket, you need to set up RLS (Row Level Security) policies:

### Policy Configuration for All Buckets:

1. **Click on the bucket name**
2. **Go to "Policies" tab**
3. **Click "New Policy"**
4. **Create these policies:**

#### Policy 1: Allow Public Read Access
```sql
Policy name: Public read access
Allowed operation: SELECT
Policy definition: true
```

#### Policy 2: Allow Authenticated Uploads
```sql
Policy name: Allow authenticated uploads
Allowed operation: INSERT
Policy definition: true
```

#### Policy 3: Allow Authenticated Updates
```sql
Policy name: Allow authenticated updates
Allowed operation: UPDATE
Policy definition: true
```

**Note:** Since we're using the `service_role` key from the backend, these policies will allow the Django backend to upload, update, and manage files on behalf of users.

---

## Step 4: Verify Settings Configuration

Your `settings.py` has been updated with these configurations:

```python
# Supabase Storage Configuration
SUPABASE_URL = 'https://wqoluwmdzljpvzimjiyr.supabase.co'

# Service role key for backend operations (full access)
SUPABASE_SERVICE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'

# Anon key for frontend/client operations (limited access)
SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'

# Storage buckets
SUPABASE_STORAGE_BUCKET = 'profile-photos'
SUPABASE_STORAGE_BUCKET_PRESCRIPTIONS = 'prescriptions'
SUPABASE_STORAGE_BUCKET_NOTIFICATIONS = 'notifications'
```

---

## Step 5: Test the Setup

### Test Profile Photo Upload:
1. **Sign up with a new user** or **update existing profile photo**
2. **Check Supabase Dashboard** → Storage → `profile-photos` bucket
3. You should see a file with name like: `user_id_uuid.jpg`

### Test Prescription Upload:
1. **As a doctor, upload a prescription file** in the doctor panel
2. **Check Supabase Dashboard** → Storage → `prescriptions` bucket
3. You should see a file with name like: `prescription_123_uuid.pdf`

### Test Notification File Upload:
1. **Submit a password reset request** with ID photo
2. **Check Supabase Dashboard** → Storage → `notifications` bucket
3. You should see a file with name like: `id_photo_userid_uuid.jpg`

---

## What Changed in the Code

### 1. Authentication Fix (403 Error)
**Problem:** Using `anon` key which has restricted permissions
**Solution:** Now using `service_role` key for backend operations

**Before:**
```python
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
```

**After:**
```python
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
```

### 2. Model Changes
**Changed from FileField to URLField:**
- `UserProfile.photo_url` - Now stores full Supabase URL
- `Notification.file` - Now stores full Supabase URL
- `Prescription.prescription_file` - Now stores full Supabase URL

### 3. Upload Functions Updated
All file uploads now follow this pattern:
```python
# Upload to Supabase Storage
unique_filename = f"prefix_{id}_{uuid.uuid4()}.{ext}"
file_content = uploaded_file.read()

response = supabase.storage.from_(bucket_name).upload(
    path=unique_filename,
    file=file_content,
    file_options={"content-type": content_type}
)

# Get public URL
file_url = supabase.storage.from_(bucket_name).get_public_url(unique_filename)
```

### 4. Download Functions Updated
**Before:** Served files from local filesystem
**After:** Redirect to Supabase Storage URL

```python
# Old way
response = FileResponse(open(file_path, 'rb'))

# New way
return redirect(file_url)  # Direct redirect to Supabase URL
```

---

## Files Modified

### Settings:
- ✅ `MEDISAFE_PBL/settings.py` - Added service_role key and bucket names

### Models:
- ✅ `myapp/models.py` - Changed FileField to URLField for:
  - `UserProfile.photo_url`
  - `Notification.file`
  - `Prescription.prescription_file`

### Views (Upload Functions):
- ✅ `myapp/features/auth/views.py` - Signup & password reset
- ✅ `myapp/features/profiles/views.py` - Profile photo update
- ✅ `myapp/features/doctors/views.py` - Doctor profile & prescription upload

### Views (Download Functions):
- ✅ `myapp/features/medical/views.py` - Prescription download
- ✅ `myapp/features/admin/user_views.py` - Notification file download
- ✅ `myapp/features/admin/user_views_fixed.py` - Notification file download

### Migrations:
- ✅ `0016_alter_userprofile_photo_url.py` - Profile photo URL field
- ✅ `0017_alter_notification_file_and_more.py` - Notification and prescription URL fields

---

## Troubleshooting

### Issue: 403 Forbidden Error
**Cause:** Buckets not created or not public
**Solution:** 
1. Create all three buckets in Supabase dashboard
2. Set all buckets to PUBLIC
3. Configure storage policies (see Step 3)

### Issue: Files Upload but URLs Don't Work
**Cause:** Bucket is not public
**Solution:** Go to bucket settings and check "Public bucket"

### Issue: File Upload Takes Too Long
**Cause:** Large file size or slow connection
**Solution:** Check file size limit (max 10 MB)

### Issue: Old Profile Photos Still Show Local Paths
**Cause:** Existing data has local paths like `/media/profile_photos/...`
**Solution:** Users need to re-upload their photos to migrate to Supabase Storage

---

## Migration Notes

### Existing Data:
- Old profile photos stored locally will NOT be automatically migrated
- Users need to re-upload their profile photos
- Old prescription/notification files remain in local storage but new ones go to Supabase

### Backward Compatibility:
- The system will work for new uploads immediately
- Old data with local paths may not display correctly
- Consider running a migration script to move existing files to Supabase Storage

---

## Security Best Practices

1. **Never expose service_role key in frontend JavaScript**
   - Only use in backend (Django views)
   - Service role key has full access to everything

2. **Use anon key for frontend operations** (if needed)
   - Limited permissions
   - Safe to expose in client-side code

3. **Keep buckets public for this use case**
   - Profile photos need to be publicly accessible
   - Prescriptions need to be accessible by patients
   - Notifications need to be accessible by admins

4. **Implement file validation**
   - Already done: File type validation
   - Already done: File size validation (10 MB max)
   - Consider: Virus scanning for production

---

## Next Steps

1. ✅ **Create all three buckets** in Supabase dashboard
2. ✅ **Test profile photo upload** (signup or profile update)
3. ✅ **Test prescription upload** (doctor panel)
4. ✅ **Test password reset** with ID photo
5. ⏳ *Optional:* Migrate existing local files to Supabase Storage
6. ⏳ *Optional:* Clean up old local media files

---

## Support

If you encounter issues:
1. Check Supabase dashboard for bucket creation
2. Verify buckets are set to PUBLIC
3. Check Django server logs for error messages
4. Ensure `service_role` key is correct in settings.py
5. Test with a fresh signup to verify profile photo upload

---

**Last Updated:** November 30, 2025
**Migration Applied:** 0017_alter_notification_file_and_more.py
**Status:** ✅ Ready for Testing
