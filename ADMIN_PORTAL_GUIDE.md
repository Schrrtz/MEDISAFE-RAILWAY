# MediSafe+ Admin Portal
## Administrative User Guide and Technical Documentation

**Version:** 1.0  
**Last Updated:** December 1, 2025

---

## Table of Contents
1. [Admin Portal Overview](#admin-portal-overview)
2. [Getting Started](#getting-started)
3. [Dashboard Management](#dashboard-management)
4. [User Management](#user-management)
5. [Account Management](#account-management)
6. [Patient Records Management](#patient-records-management)
7. [Doctor Management](#doctor-management)
8. [Consultation Management](#consultation-management)
9. [Analytics & Reporting](#analytics--reporting)
10. [System Administration](#system-administration)

---

## 1. Admin Portal Overview

The MediSafe+ Admin Portal is a comprehensive management system that provides administrators with complete control over users, accounts, medical records, appointments, analytics, and system configuration.

### Administrative Roles
- **Admin**: Standard administrative access
- **Super Admin**: Elevated privileges for critical operations

### Key Capabilities
- **User Management**: Create, edit, delete users and manage roles
- **Account Control**: Activate, deactivate, soft-delete, restore, permanent delete
- **Patient Records**: View, manage lab results, prescriptions, services
- **Doctor Management**: Manage doctor profiles, specializations, patients
- **Consultation Oversight**: Approve, monitor, manage appointments
- **Analytics**: Comprehensive statistics and insights
- **Notification System**: Password reset approvals, system alerts
- **Permission Management**: Control role-based access
- **Audit Trail**: Activity monitoring and logs

---

## 2. Getting Started

### Admin Account Creation
Admin accounts are created by existing super admins or through initial system setup.

**Required Information**:
- Username
- Email
- Password
- Role: Admin
- Personal information (name, contact)

### First Login
1. Navigate to login page
2. Enter admin credentials
3. System validates and creates session
4. Redirected to Admin Dashboard (`/moddashboard/`)

### Super Admin Mode
**URL**: `/super-admin-login/`

**Purpose**: Elevated access for sensitive operations like permanent account deletion.

**Activation**:
1. Login as regular admin
2. Navigate to super admin login
3. Enter admin password again
4. Session flag `is_super_admin` set to True
5. Access to restricted features enabled

**Exit Super Admin**:
**Endpoint**: `POST /exit-super-admin/`
1. Click "Exit Super Admin Mode"
2. Elevated privileges revoked
3. Returns to standard admin access

---

## 3. Dashboard Management

### 3.1 Admin Dashboard
**URL**: `/moddashboard/`

#### Dashboard Layout

**Top Statistics Cards**:
1. **Total Users**: Count of all registered users
2. **Active Patients**: Patients with active accounts
3. **Active Doctors**: Doctors currently in system
4. **Total Appointments**: All consultations (past and future)
5. **Pending Approvals**: Appointments awaiting review
6. **Lab Results Uploaded**: Total lab reports
7. **Prescriptions Issued**: Total prescriptions

**Charts & Graphs**:
- User registration trends
- Appointment statistics by type (F2F vs Tele)
- Consultation status distribution
- Revenue tracking (if applicable)
- Monthly activity comparison

**Recent Activity Feed**:
- User registrations
- Appointments booked
- Lab results uploaded
- Prescriptions created
- Account status changes
- System events

**Password Reset Notifications**:
**Endpoint**: `GET /api/admin/password-reset-notifications/`
- Bell icon with unread count
- Click to view all password reset requests
- Shows:
  - User requesting reset
  - Date of request
  - ID photo attached
  - Priority level
  - Read/Unread status

#### Managing Password Reset Requests

**Viewing Requests**:
1. Click password reset notification bell
2. Modal opens with list of requests
3. Each request shows:
   - Username and email
   - Date requested
   - Priority
   - ID photo badge if attached

**Viewing ID Photo**:
**Endpoint**: `GET /api/download-password-reset-file/<notification_id>/`
1. Click "View Photo" button next to "ID Photo Attached"
2. ID verification photo downloads
3. Review for identity verification

**Processing Request**:
**Endpoint**: `POST /api/admin/mark-password-reset-read/<notification_id>/`
1. Review user information and ID
2. Verify identity
3. Manually reset user password in database or contact user
4. Click "Mark as Read"
5. Notification archived

#### Clearing Activity Log
**Endpoint**: `POST /moddashboard/clear-activity/`
- Admin can clear recent activity feed
- Removes display items only (permanent records preserved)
- Requires confirmation

### 3.2 Notification Management

**Batch Delete Notifications**:
**Endpoint**: `POST /api/admin/batch-delete-notifications/`
- Select multiple notifications
- Bulk delete operation
- Confirmation required
- Permanent deletion

**Getting Notification Files**:
**Endpoint**: `GET /get_notification_file/<notification_id>/`
- Download attached files from notifications
- Supports base64 encoded files
- Returns file with proper mime type

---

## 4. User Management

**URL**: `/manage/users/`

### 4.1 User Management Interface

#### User List Display
- Comprehensive table of all users
- Columns:
  - User ID
  - Username
  - Email
  - Role (Admin/Doctor/Nurse/Lab Tech/Patient)
  - Status (Active/Inactive)
  - Date Joined
  - Actions

#### Search & Filter
- Search by username, email, name
- Filter by role
- Filter by status (Active/Inactive)
- Filter by date range
- Sort by any column

### 4.2 Creating Users

**Add User Form**:
1. Click "Add User" button
2. Fill required fields:
   - Username (unique)
   - Email (unique)
   - Password
   - Role selection
   - First name, Last name
   - Middle name (optional)
   - Sex
   - Birthday
   - Civil status
   - Address
   - Contact number
3. Submit form
4. System validates data
5. User account created
6. UserProfile created automatically
7. Confirmation message shown

**Role-Specific Setup**:
- **Doctor**: Additional doctor record created with specialization, license number
- **Patient**: Patient record created with MRN
- **Admin**: Granted administrative access
- **Nurse/Lab Tech**: Standard user access with role permissions

### 4.3 Viewing User Details

**User Profile View**:
1. Click on username or "View" button
2. Modal opens with:
   - Personal information
   - Profile photo
   - Account status
   - Role information
   - Contact details
   - Date joined
   - Last login
   - Related records count (appointments, prescriptions, lab results)

### 4.4 Editing Users

**Edit User Form**:
1. Click "Edit" button on user row
2. Modal opens with pre-filled data
3. Editable fields:
   - Email
   - Role (changing role updates permissions)
   - Personal information
   - Contact details
   - Account status
4. Save changes
5. Database updated
6. User notified if role changed

### 4.5 Password Reset Requests
**Endpoint**: `GET /api/password-reset-requests/<user_id>/`

**Viewing User's Password Reset Requests**:
1. Click "View Password Reset Requests" (3rd action button)
2. Modal shows all reset requests for that user
3. Each request displays:
   - Request title and message
   - Date submitted
   - Priority level
   - ID photo status
4. Download ID photo for verification
5. Manually reset password in system
6. Mark request as read

**Downloading ID Photos**:
**Endpoint**: `GET /api/download-password-reset-file/<notification_id>/`
- Click "View Photo" button
- ID verification photo downloads
- Use for identity confirmation before password reset

**Marking as Read**:
**Endpoint**: `POST /api/password-reset-mark-read/<notification_id>/`
- After processing request
- Click "Read" button
- Request marked as handled

### 4.6 Deleting Users

**Soft Delete** (Managed in Account Management):
- Username prefixed with "deleted_"
- Account deactivated
- Records preserved
- Reversible

**Permanent Delete** (Super Admin Only):
**Endpoint**: `POST /manage/accounts/permanent-delete/`
- Requires super admin privileges
- Only for soft-deleted accounts
- Deletes ALL associated records:
  - User profile
  - Doctor/Patient records
  - Appointments
  - Lab results
  - Prescriptions
  - Notifications
- Irreversible operation
- Confirmation required
- Audit log created

---

## 5. Account Management

**URL**: `/manage/accounts/`

### 5.1 Account Management Interface

**Account List**:
- All user accounts
- Status indicators (Active/Inactive/Deleted)
- Account information
- Quick actions

### 5.2 Account Actions

#### Activate Account
**Endpoint**: `POST /manage/accounts/activate/<user_id>/`

**Purpose**: Enable disabled account

**Process**:
1. Find inactive account
2. Click "Activate"
3. System sets status = True, is_active = True
4. User can log in
5. Confirmation message

#### Deactivate Account
**Endpoint**: `POST /manage/accounts/deactivate/<user_id>/`

**Purpose**: Temporarily disable account

**Process**:
1. Find active account
2. Click "Deactivate"
3. System sets status = False, is_active = False
4. User cannot log in
5. All data preserved
6. Reversible by reactivation

#### Soft Delete Account
**Endpoint**: `POST /manage/accounts/delete/<user_id>/`

**Purpose**: Mark account as deleted without removing data

**Process**:
1. Select account
2. Click "Delete"
3. Confirmation prompt
4. System performs soft delete:
   - Username changed to "deleted_{timestamp}_{original_username}"
   - Email changed to "deleted_{timestamp}_{original_email}"
   - Account deactivated
   - All medical records preserved
   - User cannot log in
5. Moved to "Deleted Accounts" section
6. Reversible with restore

#### Restore Deleted Account
**Endpoint**: `POST /manage/accounts/restore/<user_id>/`

**Purpose**: Undo soft delete

**Process**:
1. Navigate to "Deleted Accounts" section
2. Find account with "deleted_" prefix
3. Click "Restore"
4. System extracts original username and email
5. Restores original credentials
6. Reactivates account
7. User can log in again

#### Permanent Delete Account
**Endpoint**: `POST /manage/accounts/permanent-delete/`

**Requirements**:
- Super admin privileges required
- Account must be soft-deleted first

**Process**:
1. Activate super admin mode
2. Navigate to deleted accounts
3. Click "Permanent Delete"
4. **WARNING**: Irreversible operation
5. Confirmation dialog with details
6. System deletes:
   - User account
   - User profile
   - Doctor/Patient records
   - All appointments (as patient and doctor)
   - All lab results
   - All prescriptions
   - All notifications
   - All associated data
7. Deletion log created
8. Success message with deleted record counts

---

## 6. Patient Records Management

**URL**: `/manage/patients/`

### 6.1 Patient Records Interface

**Patient List**:
- All registered patients
- Medical record numbers (MRN)
- Personal information
- Contact details
- Recent activity

### 6.2 Lab Results Management

**Viewing Lab Results**:
1. Click on patient
2. Navigate to "Lab Results" tab
3. See all lab reports:
   - Lab type
   - Date performed
   - Uploaded by (staff name)
   - File information

**Uploading Lab Results** (Admin/Lab Tech):
1. Select patient
2. Click "Upload Lab Result"
3. Fill form:
   - Lab type
   - Result file (PDF/image)
   - File name
   - Notes
4. File converted to Base64
5. Saved to database
6. Patient receives notification

**Downloading Lab Results**:
**Endpoint**: `GET /api/download-lab-result/<result_id>/`
1. Click "Download" on result
2. File retrieved from database
3. Base64 decoded
4. Downloaded to device

### 6.3 Prescription Management

**Viewing Prescriptions**:
**Endpoint**: `GET /api/admin-prescription-details/<prescription_id>/`
1. Click on patient
2. Navigate to "Prescriptions" tab
3. See all prescriptions:
   - Prescription number
   - Doctor
   - Date issued
   - Medications
   - Status

**Downloading Prescriptions**:
**Endpoint**: `GET /api/admin-prescription-download/<prescription_id>/`
1. Click "Download" on prescription
2. PDF or image file retrieved
3. Downloaded to device

**Deleting Prescriptions** (Admin Override):
**Endpoint**: `POST /api/delete-prescription/<prescription_id>/`
1. Select prescription
2. Click "Delete"
3. Confirmation required
4. Prescription removed from system
5. Audit log created

### 6.4 Booked Services Management

**Viewing Booked Services**:
- All lab service bookings
- Service name, date, time
- Status (Pending/Confirmed/Completed/Cancelled)
- Patient information

**Updating Service Status**:
**Endpoint**: `POST /api/update-booked-service/`
1. Click on booked service
2. Change status
3. Add notes if needed
4. Save changes
5. Patient notified

**Deleting Bookings**:
**Endpoint**: `POST /api/delete-booked-service/`
1. Select booking
2. Click "Delete"
3. Confirmation required
4. Booking removed

### 6.5 Patient Statistics
**Endpoint**: `GET /api/patient-stats/<patient_id>/`

**Available Statistics**:
- Total appointments
- Completed consultations
- Pending appointments
- Lab results count
- Prescriptions received
- Last visit date
- Upcoming appointments

### 6.6 Sending Notifications to Patients
**Endpoint**: `POST /api/send-notification/`

**Creating Patient Notifications**:
1. Select patient
2. Click "Send Notification"
3. Fill notification form:
   - Title
   - Message
   - Type (Account/Urgent/Appointment/Lab Result/System)
   - Priority (Low/Medium/High/Urgent)
   - Attach file (optional)
4. Submit
5. Notification created
6. Patient sees in their portal
7. Optional: Email/SMS sent (if configured)

---

## 7. Doctor Management

**URL**: `/manage/doctors/`

### 7.1 Doctor Management Interface

**Doctor List**:
- All registered doctors
- Specializations
- License numbers
- Contact information
- Patient count
- Active status

### 7.2 Adding Doctors

**Add Doctor**:
1. Click "Add Doctor"
2. Creates user with role='doctor'
3. Additional doctor form:
   - Specialization
   - License number (unique)
   - Years of experience
   - Availability schedule (JSON)
   - Contact information
4. Doctor record created
5. Doctor can log in with credentials

### 7.3 Viewing Doctor Details
**Endpoint**: `GET /mod_doctors/get/<doctor_id>/`

**Doctor Profile**:
- Personal information
- Specialization
- License number
- Years of experience
- Contact info
- Availability schedule
- Statistics:
  - Total patients
  - Consultations conducted
  - Prescriptions issued
  - Average rating (if applicable)

### 7.4 Editing Doctor Information
**Endpoint**: `POST /mod_doctors/edit/<doctor_id>/`

**Editable Fields**:
- Specialization
- License number
- Years of experience
- Availability schedule
- Contact information

**Process**:
1. Click "Edit" on doctor
2. Modal opens with current data
3. Update fields
4. Save changes
5. Doctor record updated

### 7.5 Doctor's Patients
**Endpoint**: `GET /mod_doctors/patients/<doctor_id>/`

**View Doctor's Patient List**:
1. Click "View Patients" on doctor
2. Shows all patients who had consultations
3. Patient information displayed
4. Quick access to patient records

### 7.6 Converting Doctor to Patient
**Endpoint**: `POST /mod_doctors/convert/<doctor_id>/`

**Use Case**: Doctor becomes patient (e.g., retired doctor)

**Process**:
1. Select doctor
2. Click "Convert to Patient"
3. Confirmation required
4. System changes role to 'patient'
5. Doctor record preserved (historical data)
6. Patient record created
7. MRN assigned

### 7.7 Adding MediSafe Members
**Endpoint**: `POST /mod_doctors/add-medisafe-member/`

**Purpose**: Add non-patient users to system

**Process**:
1. Click "Add Member"
2. Fill member form
3. Role: Patient (but without medical records initially)
4. Member can book appointments
5. Records created as needed

### 7.8 Converting Member to Patient
**Endpoint**: `POST /mod_doctors/convert-member-to-patient/<user_id>/`

**Process**:
1. Find member
2. Click "Convert to Patient"
3. Patient record created
4. MRN assigned
5. Full patient portal access

---

## 8. Consultation Management

**URL**: `/manage/consultations/`

### 8.1 Consultation Management Interface

**Consultation List**:
- All appointments (past, present, future)
- Filterable by:
  - Status
  - Date range
  - Doctor
  - Patient
  - Type (F2F/Tele)

**Consultation Details**:
- Appointment number
- Patient and doctor information
- Date and time
- Type (F2F/Tele-consultation)
- Approval status
- Consultation status
- Meeting link (if tele)
- Reason for visit
- Notes

### 8.2 Viewing Consultation Details
**Endpoint**: `GET /api/get-consultation/`

**Parameters**: `consultation_id`

**Retrieved Information**:
- Complete appointment details
- Patient medical history
- Doctor information
- Booking information
- Status history
- Associated live session (if started)
- Prescription (if issued)

### 8.3 Updating Consultation Status
**Endpoint**: `POST /api/update-consultation-status/`

**Status Options**:
- **Approval Status**:
  - Pending → Approved
  - Pending → Rejected
- **Consultation Status**:
  - Scheduled → Completed
  - Scheduled → Cancelled

**Process**:
1. Select consultation
2. Click "Update Status"
3. Choose new status
4. Add notes/reason (for rejection/cancellation)
5. Save changes
6. Patient and doctor notified
7. Calendar updated

### 8.4 Approving Appointments

**Approval Workflow**:
1. Review pending appointments
2. Check:
   - Doctor availability
   - Patient information
   - Requested time slot
   - Reason for visit
3. Click "Approve"
4. System:
   - Changes approval_status to 'Approved'
   - Sets status to 'Scheduled'
   - Generates meeting link (for tele-consultations)
   - Records approval timestamp
   - Notifies patient and doctor
   - Schedules reminder

### 8.5 Rejecting Appointments

**Rejection Process**:
1. Select pending appointment
2. Click "Reject"
3. Enter rejection reason
4. Confirm
5. System:
   - Changes approval_status to 'Rejected'
   - Notifies patient with reason
   - Doctor notified
   - Time slot released

### 8.6 Deleting Consultations
**Endpoint**: `POST /api/delete-consultation/`

**Admin Override**:
1. Select consultation
2. Click "Delete"
3. Confirmation required (irreversible)
4. System deletes:
   - Appointment record
   - Associated live session (if exists)
   - Meeting link
5. Patient and doctor notified

### 8.7 Saving Consultation Changes
**Endpoint**: `POST /api/save-consultation/`

**Editable Fields**:
- Date and time (reschedule)
- Meeting link
- Notes
- Duration

**Process**:
1. Click "Edit" on consultation
2. Modify fields
3. Save changes
4. All parties notified of changes

---

## 9. Analytics & Reporting

**URL**: `/analytics/`

### 9.1 Analytics Dashboard

**Overview Statistics**:
- Total users by role
- Active vs inactive accounts
- New registrations (daily, weekly, monthly)
- Appointment trends
- Revenue (if applicable)
- System usage metrics

### 9.2 Analytics API
**Endpoint**: `GET /api/analytics/`

**Available Metrics**:
```javascript
{
  "users": {
    "total": 1500,
    "patients": 1200,
    "doctors": 50,
    "nurses": 30,
    "lab_techs": 20,
    "admins": 10,
    "active": 1450,
    "inactive": 50
  },
  "appointments": {
    "total": 5000,
    "pending": 50,
    "approved": 200,
    "completed": 4500,
    "cancelled": 250,
    "f2f": 3000,
    "tele": 2000
  },
  "medical_records": {
    "lab_results": 8000,
    "prescriptions": 4500
  },
  "trends": {
    "daily_registrations": [...],
    "monthly_appointments": [...],
    "consultation_types": [...]
  }
}
```

### 9.3 Dynamic Statistics
**Endpoint**: `GET /api/analytics/dynamic-stats/`

**Real-Time Data**:
- Current active sessions
- Today's appointments
- Pending approvals
- Recent activity
- System performance metrics

### 9.4 Report Generation

**Available Reports**:
1. **User Reports**
   - User activity
   - Registration trends
   - Role distribution

2. **Appointment Reports**
   - Appointment statistics
   - Doctor performance
   - Patient visit frequency
   - Cancellation rates

3. **Medical Reports**
   - Lab results summary
   - Prescription trends
   - Common diagnoses
   - Treatment outcomes

4. **Financial Reports** (if applicable)
   - Revenue by service
   - Doctor earnings
   - Payment collection

### 9.5 Exporting Data

**Export Options**:
- CSV export for spreadsheet analysis
- PDF reports for documentation
- JSON export for data integration
- Custom date ranges
- Filterable datasets

---

## 10. System Administration

### 10.1 Permission Management
**Endpoint**: `GET/POST /api/admin/permissions/`

**Role Permissions**:
- Control which roles can access features
- Enable/disable roles system-wide
- Granular permission control

**Available Roles for Permission Control**:
- Doctor
- Nurse
- Lab Technician
- Patient

**Managing Permissions**:
1. Navigate to permissions management
2. See list of roles with enable/disable toggle
3. Click toggle to enable/disable role
4. Changes take effect immediately
5. Users of disabled roles cannot log in

### 10.2 System Configuration

**Configurable Settings**:
- Appointment duration defaults
- Session timeout duration
- Notification preferences
- Email/SMS settings
- File upload limits
- Security settings

### 10.3 Audit Trail

**Activity Logging**:
- User logins
- Account changes
- Data modifications
- Permission changes
- File uploads/downloads
- Critical operations

**Audit Log Information**:
- Timestamp
- User performing action
- Action type
- Affected entity
- IP address
- Result (success/failure)

### 10.4 Backup & Maintenance

**Database Backups**:
- Regular automated backups
- Manual backup trigger
- Backup verification
- Restore procedures

**System Maintenance**:
- Check system health
- Monitor database size
- Review error logs
- Update dependencies
- Security patches

### 10.5 Security Management

**Security Features**:
1. **Session Management**
   - Monitor active sessions
   - Force logout capabilities
   - Session timeout configuration

2. **Password Policies**
   - Minimum length requirements
   - Complexity requirements
   - Expiration policies

3. **Access Control**
   - IP whitelisting (optional)
   - Failed login monitoring
   - Account lockout policies

4. **Data Protection**
   - Encryption settings
   - Data retention policies
   - Privacy compliance

---

## Best Practices for Administrators

### Daily Tasks
1. **Review Dashboard**: Check system statistics and alerts
2. **Approve Appointments**: Process pending consultation requests
3. **Handle Password Resets**: Verify identities and reset passwords
4. **Monitor Notifications**: Address urgent system alerts
5. **Check Activity Log**: Review unusual activity

### Weekly Tasks
1. **User Management**: Review new registrations
2. **Account Cleanup**: Handle inactive accounts
3. **Data Quality**: Verify data integrity
4. **Report Review**: Analyze weekly reports
5. **Backup Verification**: Ensure backups successful

### Monthly Tasks
1. **Analytics Review**: Analyze trends and patterns
2. **Performance Review**: Check system performance
3. **Security Audit**: Review security logs
4. **User Feedback**: Address user issues
5. **System Updates**: Apply patches and updates

### Best Practices
1. **Document Actions**: Keep logs of major changes
2. **Verify Before Deletion**: Double-check permanent deletions
3. **Communicate Changes**: Inform users of system changes
4. **Regular Backups**: Maintain backup schedule
5. **Security First**: Prioritize data protection
6. **User Support**: Respond promptly to user issues
7. **Data Privacy**: Respect patient confidentiality
8. **Training**: Keep staff trained on system updates
9. **Testing**: Test changes in staging environment
10. **Monitoring**: Continuously monitor system health

---

## Troubleshooting

### Common Admin Issues

**Cannot Access Super Admin Features**
- Ensure super admin mode activated
- Re-login to super admin
- Check session validity
- Contact technical support

**Password Reset Requests Not Showing**
- Refresh page
- Check notification bell
- Verify user submitted request
- Check notification filters

**Unable to Delete User**
- For permanent delete: Activate super admin mode
- Ensure account is soft-deleted first
- Check for dependencies
- Verify permissions

**Analytics Not Loading**
- Check database connection
- Verify date range parameters
- Clear browser cache
- Contact technical support

**Reports Generating Slowly**
- Reduce date range
- Limit filters
- Schedule report for off-peak hours
- Increase server resources

---

## Security Considerations

### Admin Account Security
- Use strong, unique passwords
- Enable two-factor authentication (if available)
- Don't share admin credentials
- Log out when finished
- Use super admin mode only when necessary

### Data Protection
- Access only necessary patient data
- Log all sensitive operations
- Report security incidents immediately
- Follow HIPAA compliance guidelines
- Regular security training

### Audit Compliance
- Maintain activity logs
- Document major changes
- Preserve records per retention policy
- Regular compliance audits
- Incident response procedures

---

## Support & Resources

### Getting Help
- **Technical Support**: IT department
- **System Issues**: Submit support ticket
- **Training**: Request admin training sessions
- **Documentation**: Refer to user guides

### Contact Information
- **IT Support**: support@medisafeplus.com
- **Emergency**: Emergency hotline
- **Training**: training@medisafeplus.com

---

## Appendix

### Keyboard Shortcuts
- `Ctrl+F`: Search users/records
- `Ctrl+N`: New user/record
- `F5`: Refresh dashboard
- `Esc`: Close modals

### Admin Action Quick Reference

| Action | URL/Endpoint | Access Level |
|--------|-------------|--------------|
| Dashboard | `/moddashboard/` | Admin |
| Analytics | `/analytics/` | Admin |
| User Management | `/manage/users/` | Admin |
| Account Management | `/manage/accounts/` | Admin |
| Patient Records | `/manage/patients/` | Admin |
| Doctor Management | `/manage/doctors/` | Admin |
| Consultations | `/manage/consultations/` | Admin |
| Permanent Delete | `/manage/accounts/permanent-delete/` | Super Admin Only |
| Super Admin Login | `/super-admin-login/` | Admin |
| Exit Super Admin | `/exit-super-admin/` | Super Admin |

---

**Admin Portal Version:** 1.0  
**Last Updated:** December 1, 2025  
**For Support**: Contact MediSafe+ IT Department
