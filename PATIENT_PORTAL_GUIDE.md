# MediSafe+ Patient Portal
## User Guide and Technical Documentation

**Version:** 1.0  
**Last Updated:** December 1, 2025

---

## Table of Contents
1. [Patient Portal Overview](#patient-portal-overview)
2. [Getting Started](#getting-started)
3. [Features & Functionality](#features--functionality)
4. [User Interface Guide](#user-interface-guide)
5. [Technical Architecture](#technical-architecture)
6. [Patient Workflows](#patient-workflows)

---

## 1. Patient Portal Overview

The MediSafe+ Patient Portal is a comprehensive healthcare platform that enables patients to manage their medical care, book consultations, view lab results, access prescriptions, and communicate with healthcare providers.

### Key Capabilities
- **Appointment Booking**: Schedule face-to-face or tele-consultations
- **Lab Results**: View and download lab reports
- **Prescriptions**: Access digital prescriptions from doctors
- **Medical Records**: View personal health information
- **Profile Management**: Update personal information and photos
- **Health Tools**: Access BMI calculators and health assessments
- **Notifications**: Receive alerts for appointments and results

---

## 2. Getting Started

### Account Creation
1. Navigate to the MediSafe+ homepage
2. Click "Sign Up" button
3. Fill in registration form:
   - Username (unique identifier)
   - Email address (for notifications)
   - Password (minimum 8 characters)
   - First name, Last name
   - Sex, Birthday
   - Civil status
   - Address
   - Contact number
   - Profile photo (optional)
   - Data privacy consent (required)
4. Submit form
5. Account created automatically with "Patient" role
6. Redirected to dashboard

### Login Process
1. Go to login page
2. Enter username and password
3. Click "Login"
4. System validates credentials
5. Redirected to patient dashboard

### Password Recovery
1. Click "Forgot Password" on login page
2. Enter username
3. Upload ID photo for verification
4. Admin receives notification with ID photo
5. Admin verifies identity and resets password
6. Patient receives notification of password change
7. Login with new password provided by admin

---

## 3. Features & Functionality

### 3.1 Dashboard
**URL**: `/dashboard/`  
**Description**: Central hub for patient activities

#### Dashboard Sections
1. **Upcoming Appointments**
   - View scheduled consultations
   - See appointment details (date, time, doctor, type)
   - Access meeting links for tele-consultations
   - Cancel appointments if needed

2. **Recent Lab Results**
   - View latest lab reports
   - Download result files
   - See lab type and upload date
   - Access full lab results archive

3. **Active Prescriptions**
   - View current prescriptions
   - Download prescription files
   - See medication details
   - Check doctor information

4. **Quick Actions**
   - Book new consultation
   - View all lab results
   - Access health tools
   - Update profile

5. **Notifications**
   - Appointment reminders
   - Lab result availability
   - Prescription updates
   - System announcements

### 3.2 Consultations
**URL**: `/consultations/`

#### Booking a Consultation
**Endpoint**: `POST /api/book-consultation/`

1. Navigate to consultations page
2. Click "Book Consultation"
3. Fill in booking form:
   - **Doctor Selection**: Choose from available doctors
   - **Consultation Type**:
     - Face-to-Face (F2F): In-person visit
     - Tele-Consultation: Video call
   - **Date**: Select consultation date
   - **Time**: Choose available time slot
   - **Reason for Visit**: Describe symptoms/purpose
4. Submit booking
5. Receive confirmation with appointment number (format: APT-XXXXXX)
6. Wait for admin/doctor approval

#### Appointment Status
- **Pending**: Awaiting approval from doctor/admin
- **Approved**: Confirmed by healthcare provider
- **Scheduled**: Ready for consultation
- **Completed**: Consultation finished
- **Cancelled**: Appointment cancelled
- **Rejected**: Request denied

#### Managing Appointments
- **View Details**: Click appointment to see full information
- **Cancel Appointment**: `POST /api/cancel-consultation/`
  - Only available for pending/approved appointments
  - Requires confirmation
- **Join Tele-Consultation**: Click meeting link when appointment time arrives
- **Reschedule**: Cancel and create new appointment

#### Guest Booking
**Endpoint**: `POST /api/book-consultation-guest/`
- Allows booking without account
- Requires contact information
- Limited features compared to registered users

### 3.3 Lab Results
**URL**: `/labresults/`

#### Viewing Lab Results
1. Navigate to lab results page
2. See list of all lab reports:
   - Lab type (Blood Test, Urinalysis, X-Ray, etc.)
   - Upload date
   - Uploaded by (staff name)
   - File type (PDF, image)
   - Notes from lab technician

#### Accessing Results
- **View Result**: `GET /labresults/view/<result_id>/`
  - Opens result file in browser
  - For PDFs and images
- **Download Result**: `GET /labresults/download/<result_id>/`
  - Downloads file to device
  - Original filename preserved

#### Lab Services Booking
**Endpoint**: `POST /labservices/book/`

1. Click "Book Lab Service"
2. Fill in service details:
   - Service name (Blood Test, X-Ray, etc.)
   - Preferred date
   - Preferred time
   - Additional notes
3. Submit booking
4. Receive confirmation
5. Track booking status:
   - Pending: Awaiting confirmation
   - Confirmed: Appointment scheduled
   - Completed: Service done, results pending
   - Cancelled: Booking cancelled

### 3.4 Profile Management
**URL**: `/userprofile/`

#### Viewing Profile
- Personal information display
- Profile photo
- Cover photo
- Contact details
- Emergency contact

#### Updating Profile
**Endpoint**: `POST /api/update-profile/`

**Editable Fields**:
- First name, Middle name, Last name
- Birthday
- Sex (Male/Female/Other)
- Civil status (Single/Married/Divorced/Widowed/Separated)
- Address
- Contact number
- Phone type (Mobile/Home/Work/Other)
- Contact person (emergency contact)
- Relationship to patient
- Email

**Process**:
1. Click "Edit Profile"
2. Update desired fields
3. Click "Save Changes"
4. Profile updated immediately

#### Photo Management

**Profile Photo**:  
**Endpoint**: `POST /api/update-profile-photo/`
1. Click profile photo or "Change Photo"
2. Select image file (JPEG, PNG)
3. Image uploaded to Supabase Storage
4. Photo URL saved in database
5. New photo displayed immediately

**Cover Photo**:  
**Endpoint**: `POST /api/update-cover-photo/`
1. Click "Change Cover Photo"
2. Select image file
3. Uploaded to Supabase Storage
4. Cover updated on profile

**Technical Details**:
- Storage: Supabase Storage (cloud)
- Bucket: `profile-photos`
- Public access via CDN
- Automatic resizing recommended
- Supports: JPEG, PNG, GIF

### 3.5 Prescriptions

Prescriptions are automatically available after doctor consultations.

#### Viewing Prescriptions
1. Access from dashboard or prescriptions page
2. See prescription details:
   - Prescription number (RX-XXXXXXXX)
   - Doctor name and specialization
   - Date issued
   - Medications list
   - Dosage and instructions
   - Follow-up date

#### Prescription Information
- **Medicines**: Name, dosage, frequency, duration
- **Instructions**: How to take medications
- **Follow-up**: Next appointment date
- **Doctor Signature**: Digital signature
- **Status**: Draft/Signed/Printed

#### Downloading Prescriptions
- Click "Download" button
- Receives PDF or image file
- Printable for pharmacy use

### 3.6 Health Tools
**URL**: `/health-tools/`

#### Available Tools
1. **BMI Calculator**
   - Calculate Body Mass Index
   - Weight and height input
   - Result interpretation
   - Health recommendations

2. **Health Assessment**
   - General health questionnaire
   - Risk assessment
   - Personalized recommendations

3. **Medical Information**
   - Disease information
   - Symptom checker
   - Health education

### 3.7 Messaging Admin
**Endpoint**: `POST /api/send-message-to-admin/`

1. Go to profile or help section
2. Click "Contact Admin"
3. Fill in message form:
   - Subject
   - Message content
   - Priority (optional)
4. Submit message
5. Admin receives notification
6. Admin responds via notification system

### 3.8 Notifications

Patients receive notifications for:
- Appointment confirmations
- Appointment reminders (24 hours before)
- Lab results available
- Prescription ready
- Password reset confirmations
- System announcements
- Admin messages

**Notification Types**:
- **Account**: Account-related updates
- **Appointment**: Consultation alerts
- **Lab Result**: New lab results
- **System**: Platform updates
- **Urgent**: Critical alerts

**Managing Notifications**:
- View unread count in header
- Click notification to view details
- Mark as read automatically
- Filter by type
- Clear old notifications

---

## 4. User Interface Guide

### Navigation
- **Header**: Logo, navigation menu, notifications, profile
- **Sidebar** (Desktop): Quick access to main sections
- **Bottom Nav** (Mobile): Touch-friendly navigation
- **Dashboard**: Central hub with overview cards

### Design Elements
- **Color Scheme**:
  - Primary: Healthcare Blue (#003366)
  - Accent: Healthcare Red (#FF0000)
  - Success: Green
  - Warning: Yellow
  - Error: Red
- **Icons**: Font Awesome 6.0
- **Layout**: Responsive design (mobile, tablet, desktop)
- **Typography**: Clean, readable fonts

### Accessibility Features
- Large touch targets for mobile
- Clear labels and instructions
- High contrast text
- Keyboard navigation support
- Screen reader compatible

---

## 5. Technical Architecture

### Frontend Technologies
- **HTML5**: Semantic markup
- **Tailwind CSS**: Utility-first styling
- **JavaScript**: Vanilla JS with Fetch API
- **AJAX**: Dynamic content loading without page refresh

### Backend Integration
- **RESTful APIs**: JSON responses
- **Session-based Authentication**: Secure session cookies
- **CSRF Protection**: Token-based protection for forms
- **Error Handling**: User-friendly error messages

### Data Flow
1. User interacts with UI (button click, form submit)
2. JavaScript captures event
3. AJAX request sent to backend API
4. Django view processes request
5. Database query/update
6. JSON response returned
7. UI updated dynamically
8. Success/error notification shown

### Security Measures
- Password hashing (PBKDF2-SHA256)
- Session management (24-hour timeout)
- CSRF tokens on all forms
- HttpOnly cookies
- SQL injection prevention (Django ORM)
- XSS protection (template escaping)

### File Handling
- **Profile Photos**: Supabase Storage (cloud CDN)
- **Lab Results**: Base64 encoded in database
- **Prescriptions**: Base64 encoded PDF/images
- **Notifications**: Base64 encoded attachments

---

## 6. Patient Workflows

### Workflow 1: Complete Consultation Journey

1. **Book Appointment**
   - Login to patient portal
   - Navigate to consultations
   - Fill booking form (doctor, date, time, reason)
   - Submit and receive appointment number
   - Wait for approval

2. **Receive Confirmation**
   - Check notification for approval
   - View appointment details on dashboard
   - Add to personal calendar
   - Receive reminder 24 hours before

3. **Attend Consultation**
   - **For F2F**: Visit clinic at scheduled time
   - **For Tele**: Click meeting link in dashboard
   - Doctor conducts examination
   - Vital signs recorded
   - Symptoms and diagnosis documented

4. **Receive Prescription**
   - Doctor creates digital prescription
   - Signs prescription with digital signature
   - Prescription available in patient portal
   - Download prescription PDF
   - Print for pharmacy

5. **Follow-up**
   - Check follow-up date on prescription
   - Book new appointment if needed
   - View consultation history

### Workflow 2: Lab Results Access

1. **Lab Test Ordered**
   - Doctor orders lab test during consultation
   - Patient books lab service
   - Visits lab for sample collection

2. **Results Upload**
   - Lab technician processes sample
   - Uploads result to patient account
   - System sends notification to patient

3. **Patient Access**
   - Receives notification "New lab result available"
   - Logs in to patient portal
   - Navigates to lab results
   - Views/downloads result file
   - Discusses with doctor if needed

### Workflow 3: Profile Update

1. **Access Profile**
   - Login and go to profile page
   - Click "Edit Profile"

2. **Update Information**
   - Modify personal details
   - Change profile photo
   - Update contact information
   - Add emergency contact

3. **Save Changes**
   - Click "Save"
   - System validates data
   - Updates database
   - Confirmation message shown

### Workflow 4: Password Recovery

1. **Initiate Reset**
   - Click "Forgot Password"
   - Enter username

2. **Identity Verification**
   - Upload clear ID photo
   - Submit request
   - Admin receives notification with ID

3. **Admin Review**
   - Admin verifies identity from ID photo
   - Admin resets password manually
   - Generates temporary password

4. **Regain Access**
   - Patient receives notification
   - Contacts admin for new password
   - Logs in with temporary password
   - Changes password immediately

---

## Common Patient Actions

### Quick Reference

| Action | URL/Endpoint | Method |
|--------|-------------|--------|
| View Dashboard | `/dashboard/` | GET |
| Book Appointment | `/api/book-consultation/` | POST |
| Cancel Appointment | `/api/cancel-consultation/` | POST |
| View Lab Results | `/labresults/` | GET |
| Download Lab Result | `/labresults/download/<id>/` | GET |
| Book Lab Service | `/labservices/book/` | POST |
| Update Profile | `/api/update-profile/` | POST |
| Change Profile Photo | `/api/update-profile-photo/` | POST |
| View Prescriptions | Dashboard widget | GET |
| Contact Admin | `/api/send-message-to-admin/` | POST |
| View Health Tools | `/health-tools/` | GET |

---

## Mobile Experience

### Responsive Design
- Optimized for phones and tablets
- Touch-friendly buttons (minimum 44x44px)
- Simplified navigation
- Collapsible menus
- Optimized images

### Mobile Features
- One-tap calling
- Location services (for F2F appointments)
- Camera access (for ID uploads)
- Push notifications (recommended)
- Offline capabilities (future enhancement)

---

## Troubleshooting

### Common Issues

**Cannot Login**
- Verify username and password
- Check caps lock
- Try password reset
- Contact admin if account inactive

**Appointment Not Showing**
- Refresh page
- Check approval status
- Verify not cancelled
- Check notifications for updates

**Lab Results Not Visible**
- Ensure results uploaded by staff
- Check notification for availability alert
- Contact clinic if missing

**Photo Upload Failed**
- Check file size (max 5MB recommended)
- Use JPEG or PNG format
- Ensure stable internet connection
- Try different browser

**Meeting Link Not Working**
- Check appointment time
- Link active 15 minutes before
- Test internet connection
- Use recommended browser (Chrome, Firefox)

---

## Best Practices for Patients

1. **Keep Profile Updated**: Ensure contact information is current
2. **Check Notifications**: Review regularly for important updates
3. **Book Early**: Schedule appointments in advance
4. **Prepare for Consultations**: Write down symptoms and questions
5. **Download Important Documents**: Save prescriptions and lab results
6. **Report Issues**: Contact admin for technical problems
7. **Protect Password**: Don't share login credentials
8. **Verify Information**: Double-check appointment details
9. **Follow Up**: Adhere to follow-up instructions from doctor
10. **Use Health Tools**: Monitor your health regularly

---

## Support & Assistance

### Getting Help
1. **In-Portal Messaging**: Contact admin via messaging feature
2. **Email Support**: Use registered email for inquiries
3. **Phone Support**: Call clinic during business hours
4. **FAQ Section**: Check common questions
5. **User Guide**: Refer to this documentation

### Reporting Issues
- Technical problems: Contact admin with screenshot
- Medical concerns: Contact your doctor or clinic
- Billing questions: Reach out to administrative staff
- Feedback: Submit via admin messaging

---

## Privacy & Data Protection

### Patient Rights
- Access to own medical records
- Control over personal information
- Right to correct inaccurate data
- Right to delete account (soft delete)

### Data Security
- All data encrypted in transit (HTTPS)
- Secure database storage
- Regular backups
- Access logs maintained
- HIPAA-compliant practices

### Data Sharing
- Medical records shared only with treating doctors
- No third-party sharing without consent
- Admin access for system management only
- Audit trail for all access

---

## Glossary

- **F2F**: Face-to-Face consultation
- **Tele-Consultation**: Video consultation
- **MRN**: Medical Record Number
- **Rx**: Prescription
- **APT**: Appointment number prefix
- **Vital Signs**: BP (Blood Pressure), HR (Heart Rate), Temp (Temperature)
- **Base64**: Data encoding format for file storage

---

**Patient Portal Version:** 1.0  
**Last Updated:** December 1, 2025  
**For Support**: Contact MediSafe+ Administrative Team
