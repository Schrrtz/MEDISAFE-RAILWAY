# MediSafe+ Healthcare Management System
## Comprehensive Project Documentation

**Version:** 1.0  
**Framework:** Django 5.2.6  
**Database:** PostgreSQL (Supabase)  
**Last Updated:** December 1, 2025

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [System Architecture](#system-architecture)
4. [Database Schema](#database-schema)
5. [API Endpoints](#api-endpoints)
6. [Security Features](#security-features)
7. [Module Breakdown](#module-breakdown)
8. [Authentication System](#authentication-system)

---

## 1. Project Overview

**MediSafe+** is a comprehensive healthcare management system that facilitates seamless interactions between patients, doctors, and administrative staff. The platform supports appointment scheduling, live consultations, prescription management, lab results, and comprehensive patient records.

### Key Features
- **Multi-Role System**: Patients, Doctors, Nurses, Lab Technicians, and Admins
- **Live Consultations**: Real-time video consultations with medical record keeping
- **Digital Prescriptions**: E-prescription generation with digital signatures
- **Lab Results Management**: Secure upload and access to lab reports
- **Appointment System**: Booking, approval, and management of consultations
- **Notification System**: Real-time alerts for appointments, results, and system updates
- **Password Recovery**: Secure password reset with admin verification and ID photo upload
- **Profile Management**: User profiles with photo uploads (Supabase Storage)
- **Analytics Dashboard**: Comprehensive statistics and insights for administrators

---

## 2. Technology Stack

### Backend
- **Framework**: Django 5.2.6 (Python)
- **Database**: PostgreSQL (Supabase Cloud)
- **Authentication**: Django Session-based + Custom User Model
- **File Storage**: Supabase Storage (for photos) + Base64 encoding (for documents)
- **API**: RESTful JSON APIs

### Frontend
- **CSS Framework**: Tailwind CSS 3.x
- **JavaScript**: Vanilla JS with Fetch API
- **Icons**: Font Awesome 6.0
- **UI Components**: Custom modals, notifications, and interactive elements

### Cloud Services
- **Supabase**: PostgreSQL database + Storage buckets
- **Deployment Ready**: Environment-based configuration

### Key Dependencies
```
Django==5.2.6
psycopg2-binary==2.9.10
pillow==11.3.0
python-dotenv==1.1.1
supabase==2.21.1
cryptography==46.0.2
PyJWT==2.10.1
requests==2.32.3
```

---

## 3. System Architecture

### Application Structure
```
PBL/
├── MEDISAFE_PBL/          # Django project settings
│   ├── settings.py        # Configuration (DB, middleware, apps)
│   ├── urls.py            # Main URL routing
│   └── wsgi.py            # WSGI application
├── myapp/                 # Main application
│   ├── models.py          # Database models
│   ├── urls.py            # Feature routing
│   └── features/          # Modular features
│       ├── admin/         # Admin panel & management
│       ├── auth/          # Authentication
│       ├── consultations/ # Appointment booking
│       ├── dashboard/     # User dashboards
│       ├── doctors/       # Doctor panel & live consultations
│       ├── home/          # Landing page
│       ├── medical/       # Lab results & services
│       ├── profiles/      # User profile management
│       ├── healthtools/   # Health calculators
│       └── conditions/    # Medical conditions info
├── media/                 # Local media files (deprecated)
├── static/                # Static assets (CSS, JS, images)
└── requirements.txt       # Python dependencies
```

### Design Pattern
- **Modular Feature-Based Architecture**: Each feature (auth, doctors, admin) is self-contained
- **MVC Pattern**: Models, Views (controllers), Templates
- **RESTful APIs**: JSON responses for AJAX operations
- **Session-based Authentication**: Secure server-side sessions

---

## 4. Database Schema

### Core Models

#### User (Custom Auth Model)
```python
Fields:
- user_id (PK, AutoField)
- username (Unique, CharField)
- email (Unique, EmailField)
- password (Hashed, TextField)
- role (CharField): admin, doctor, nurse, lab_tech, patient
- status (Boolean): Active/Inactive
- date_joined (DateTime)
- is_active, is_staff, is_superuser (Boolean)
```

#### UserProfile
```python
Fields:
- profile_id (PK)
- user (FK to User, OneToOne)
- first_name, middle_name, last_name
- birthday (DateField)
- sex, civil_status
- address, contact_number
- photo_url (TextField - Base64 data URL)
- contact_person, relationship_to_patient
- data_privacy_consent (Boolean)
```

#### Doctor
```python
Fields:
- doctor_id (PK)
- user (FK to User, OneToOne)
- specialization
- license_number (Unique)
- years_of_experience
- availability (JSONField)
- contact_info
```

#### Patient
```python
Fields:
- user (FK to User, OneToOne)
- medical_record_number (Unique)
- date_of_birth, gender, blood_type
- allergies, conditions
- emergency_contact_name, emergency_contact_phone
```

#### Appointment
```python
Fields:
- consultation_id (PK)
- appointment_number (Unique)
- patient (FK to User)
- doctor (FK to Doctor)
- consultation_type (F2F/Tele)
- consultation_date, consultation_time
- approval_status (Pending/Approved/Rejected)
- status (Scheduled/Completed/Cancelled)
- meeting_link, reason_for_visit
- duration_minutes, reminder_sent
```

#### LiveAppointment
```python
Fields:
- live_appointment_id (PK)
- appointment (FK to Appointment, OneToOne)
- live_appointment_number (from appointment)
- status (waiting/in_progress/completed/cancelled)
- started_at, completed_at
- vital_signs (JSONField): BP, HR, Temp, etc.
- symptoms, diagnosis, clinical_notes
- treatment_plan, follow_up_notes
- doctor_notes, recommendations
```

#### Prescription
```python
Fields:
- prescription_id (PK)
- live_appointment (FK to LiveAppointment)
- prescription_number (Unique, RX-XXXXXXXX)
- doctor (FK to Doctor)
- medicines (JSONField): list of medicine objects
- instructions, follow_up_date
- doctor_signature (Base64 image)
- prescription_file (Base64 PDF/image)
- status (draft/signed/printed/cancelled)
```

#### LabResult
```python
Fields:
- lab_result_id (PK)
- user (FK to User)
- lab_type
- result_file (Base64 data URL)
- file_type, file_name
- uploaded_by (FK to User)
- upload_date, notes
```

#### Notification
```python
Fields:
- notification_id (PK)
- user (FK to User)
- title, message
- notification_type (account/urgent/appointment/lab_result/system/password_reset)
- is_read (Boolean)
- priority (low/medium/high/urgent)
- related_id (Integer - links to related entity)
- file (TextField - Base64 data URL for attachments)
- created_at, updated_at
```

#### BookedService
```python
Fields:
- booking_id (PK)
- user (FK to User)
- service_name
- booking_date, booking_time
- status (Pending/Confirmed/Completed/Cancelled)
- notes
```

#### RolePermission
```python
Fields:
- permission_id (PK)
- role (Unique: doctor/nurse/lab_tech/patient)
- is_enabled (Boolean)
```

#### WatchVitals ⭐ NEW
```python
Fields:
- id (PK, AutoField)
- user (FK to User via user_id, CASCADE)
- device_id (CharField)
- heart_rate (Integer, BPM)
- systolic (Integer, mmHg)
- diastolic (Integer, mmHg)
- spo2 (Integer, Oxygen Saturation %)
- steps, calories, distance_m (Integer)
- captured_at (DateTime - when watch captured data)
- created_at (DateTime - when record created in DB)
- measured_by (CharField)
- user_email (CharField)
- raw_payload (JSONField - original smartwatch data)

Table: watch_vitals (Supabase)
Purpose: Store real-time vital signs from connected smartwatches
Related API: GET /api/watch-vitals/patient/<user_id>/
```

### Database Relationships
- **User → UserProfile**: One-to-One
- **User → Doctor/Patient**: One-to-One (role-specific)
- **User → Appointments**: One-to-Many (as patient)
- **Doctor → Appointments**: One-to-Many
- **Appointment → LiveAppointment**: One-to-One
- **LiveAppointment → Prescriptions**: One-to-Many
- **User → Notifications**: One-to-Many
- **User → LabResults**: One-to-Many
- **User → WatchVitals**: One-to-Many ⭐ NEW

---

## 5. API Endpoints

### Authentication APIs
```
POST /login/                          - User login
POST /signup/                         - User registration
POST /logout/                         - User logout
POST /forgot-password/                - Request password reset
POST /verify-account/                 - Verify email/account
POST /super-admin-login/              - Super admin login
GET  /check-super-admin-status/       - Check super admin session
POST /exit-super-admin/               - Exit super admin mode
```

### Dashboard APIs
```
GET  /dashboard/                      - User dashboard (role-based redirect)
```

### Profile APIs
```
GET  /userprofile/                    - View user profile
POST /api/update-profile/             - Update profile information
POST /api/update-profile-photo/       - Update profile photo (Supabase)
POST /api/update-cover-photo/         - Update cover photo (Supabase)
POST /api/send-message-to-admin/      - Send message to admin
```

### Consultation APIs (Patient)
```
GET  /consultations/                  - View consultations
POST /api/book-consultation/          - Book consultation (logged in)
POST /api/book-consultation-guest/    - Book consultation (guest)
POST /api/create-appointment/         - Create appointment
POST /api/cancel-consultation/        - Cancel consultation
GET  /api/get-consultation-details/<id>/ - Get consultation details
```

### Lab Results APIs (Patient)
```
GET  /labresults/                     - View lab results
GET  /labresults/view/<id>/           - View specific result
GET  /labresults/download/<id>/       - Download lab result file
POST /labservices/book/               - Book lab service
```

### Doctor APIs
```
GET  /doctor/panel/                   - Doctor dashboard
POST /doctor/api/update-profile/      - Update doctor profile
GET  /doctors/search-patients/        - Search patients
GET  /doctors/patient-lab-results/<id>/ - View patient lab results
GET  /doctors/download-lab-result/<id>/ - Download lab result
GET  /doctors/live-appointment/       - Live appointment interface
POST /doctors/start-consultation/<id>/ - Start live consultation
POST /doctors/restart-consultation/<id>/ - Restart consultation
POST /doctors/update-consultation/<id>/ - Update consultation data
POST /doctors/complete-consultation/<id>/ - Complete consultation
POST /doctors/create-prescription/<id>/ - Create prescription
POST /doctors/sign-prescription/<id>/ - Sign prescription
GET  /doctors/prescription-pdf/<id>/  - Generate prescription PDF
POST /doctors/upload-prescription-file/<id>/ - Upload prescription file
GET  /api/get-all-prescriptions/      - Get all prescriptions (doctor)
GET  /doctors/prescription-details/<id>/ - View prescription details
GET  /doctors/download-prescription/<id>/ - Download prescription
POST /doctors/api/mark-notification-read/ - Mark notification read
GET  /api/watch-vitals/patient/<id>/  - Get patient smartwatch vitals (NEW)
```

### Admin Dashboard APIs
```
GET  /moddashboard/                   - Admin dashboard
POST /moddashboard/clear-activity/    - Clear activity log
GET  /get_notification_file/<id>/     - Get notification file
GET  /api/admin/password-reset-notifications/ - Get password reset requests
POST /api/admin/mark-password-reset-read/<id>/ - Mark password reset as read
POST /api/admin/batch-delete-notifications/ - Batch delete notifications
```

### Admin Analytics APIs
```
GET  /analytics/                      - Analytics dashboard
GET  /api/analytics/                  - Get analytics data
GET  /api/analytics/dynamic-stats/    - Get dynamic statistics
```

### Admin User Management APIs
```
GET  /manage/users/                   - User management interface
GET  /api/password-reset-requests/<user_id>/ - Get user's password reset requests
POST /api/password-reset-mark-read/<id>/ - Mark reset request as read
GET  /api/download-password-reset-file/<id>/ - Download ID photo from reset request
```

### Admin Account Management APIs
```
GET  /manage/accounts/                - Account management interface
POST /manage/accounts/activate/<id>/  - Activate account
POST /manage/accounts/deactivate/<id>/ - Deactivate account
POST /manage/accounts/delete/<id>/    - Soft delete account
POST /manage/accounts/restore/<id>/   - Restore deleted account
POST /manage/accounts/permanent-delete/ - Permanently delete account
```

### Admin Patient Management APIs
```
GET  /manage/patients/                - Patient records management
POST /api/update-booked-service/      - Update booked service
POST /api/delete-booked-service/      - Delete booked service
GET  /api/patient-stats/<id>/         - Get patient statistics
GET  /api/admin-prescription-download/<id>/ - Download prescription (admin)
GET  /api/admin-prescription-details/<id>/ - Get prescription details (admin)
POST /api/delete-prescription/<id>/   - Delete prescription
GET  /api/download-lab-result/<id>/   - Download lab result (admin)
POST /api/send-notification/          - Send notification to user
```

### Admin Doctor Management APIs
```
GET  /manage/doctors/                 - Doctor management interface
GET  /mod_doctors/get/<id>/           - Get doctor details
POST /mod_doctors/edit/<id>/          - Edit doctor information
GET  /mod_doctors/patients/<id>/      - Get doctor's patients
POST /mod_doctors/add-medisafe-member/ - Add MediSafe member
POST /mod_doctors/convert-member-to-patient/<id>/ - Convert member to patient
POST /mod_doctors/convert/<id>/       - Convert doctor to patient
```

### Admin Consultation Management APIs
```
GET  /manage/consultations/           - Consultation management interface
POST /api/update-consultation-status/ - Update consultation status
POST /api/delete-consultation/        - Delete consultation
GET  /api/get-consultation/           - Get consultation details
POST /api/save-consultation/          - Save consultation changes
```

### Permission Management APIs
```
GET/POST /api/admin/permissions/      - Manage role permissions
```

### Health Tools APIs
```
GET  /health-tools/                   - Health calculators and tools
```

---

## 6. Security Features

### Authentication & Authorization
1. **Custom User Model**: Extends Django AbstractBaseUser with role-based access
2. **Password Hashing**: PBKDF2-SHA256 algorithm (Django default)
3. **Session Management**: 
   - 24-hour session timeout
   - HttpOnly cookies
   - Session stored in database
4. **Role-Based Access Control (RBAC)**: 
   - Admin, Doctor, Nurse, Lab Tech, Patient roles
   - View decorators check session and role
5. **Super Admin Mode**: Special elevated access for administrative tasks

### Data Security
1. **CSRF Protection**: Django CSRF middleware enabled
2. **SQL Injection Prevention**: Django ORM parameterized queries
3. **XSS Protection**: Template auto-escaping enabled
4. **Secure Headers**: 
   - X-Frame-Options
   - Content-Type-Options
5. **File Upload Security**:
   - Base64 encoding for secure storage
   - File type validation
   - Size limits enforced
6. **Password Reset Security**:
   - Admin verification required
   - ID photo upload for identity verification
   - Notification system for audit trail

### Database Security
1. **PostgreSQL with SSL**: Required connection encryption
2. **Supabase Security**:
   - Row-level security policies
   - Service role key for backend
   - Anonymous key for limited frontend access
3. **Environment Variables**: Sensitive credentials stored in .env file
4. **Connection Pooling**: Managed connections to prevent exhaustion

### API Security
1. **CSRF Tokens**: Required for POST/PUT/DELETE requests
2. **Session Verification**: All endpoints verify user authentication
3. **Role Verification**: Endpoints check user role permissions
4. **Rate Limiting**: (Recommended for production - not implemented)

### Privacy & Compliance
1. **Data Privacy Consent**: Explicit user consent tracking
2. **Soft Delete**: User accounts soft-deleted (username prefixed with "deleted_")
3. **Audit Trail**: Activity logging in notifications table
4. **Medical Data Protection**: Encrypted connections, secure storage

### Recommended Production Enhancements
- Enable HTTPS (set SESSION_COOKIE_SECURE=True)
- Implement rate limiting (django-ratelimit)
- Add two-factor authentication (django-otp)
- Enable security headers (django-csp)
- Regular security audits and updates
- Implement API rate limiting
- Add request logging and monitoring

---

## 7. Module Breakdown

### 7.1 Home Module (`features/home/`)
**Purpose**: Landing page and public information  
**Views**: `homepage2`  
**Features**:
- Public landing page
- Information about services
- Links to login/signup

### 7.2 Authentication Module (`features/auth/`)
**Purpose**: User authentication and account management  
**Key Views**:
- `login()` - User login with role-based redirect
- `signup()` - New user registration
- `logout()` - Session termination
- `forgot_password()` - Password reset with admin notification & ID upload
- `verify_account()` - Email verification
- `super_admin_login()` - Elevated admin access
- `exit_super_admin()` - Exit super admin mode

**Features**:
- Multi-role login (patients, doctors, admin)
- Password hashing (PBKDF2)
- Profile photo upload during signup (Supabase)
- Admin-verified password reset with ID photo
- Session management

### 7.3 Dashboard Module (`features/dashboard/`)
**Purpose**: Role-based user dashboards  
**Key Views**: `dashboard()`  
**Features**:
- Automatic redirect based on user role
- Patient: Appointments, lab results, prescriptions
- Doctor: Appointments, patient search, live consultations
- Admin: System statistics, user management, analytics

### 7.4 Profile Module (`features/profiles/`)
**Purpose**: User profile management  
**Key Views**:
- `userprofile()` - View/edit profile
- `update_profile()` - Update personal information
- `update_profile_photo()` - Upload profile photo (Supabase)
- `update_cover_photo()` - Upload cover photo (Supabase)
- `send_message_to_admin()` - Contact admin

**Features**:
- Personal information management
- Photo uploads (Supabase Storage)
- Cover photo customization
- Admin messaging

### 7.5 Consultations Module (`features/consultations/`)
**Purpose**: Appointment booking and management  
**Key Views**:
- `consultations()` - View appointments
- `book_consultation()` - Book new appointment
- `book_consultation_guest()` - Guest booking
- `cancel_consultation()` - Cancel appointment
- `get_consultation_details()` - View details

**Features**:
- Face-to-face and tele-consultation booking
- Guest booking (no login required)
- Appointment approval workflow
- Calendar integration
- Meeting link generation (for tele-consultations)
- Appointment reminders

### 7.6 Medical Module (`features/medical/`)
**Purpose**: Lab results and medical services  
**Key Views**:
- `lab_results()` - View lab results
- `view_lab_result()` - View specific result
- `download_lab_result()` - Download result file
- `book_service()` - Book lab services

**Features**:
- Lab result upload (by admin/lab tech)
- Secure file storage (Base64)
- Patient access to own results
- Service booking

### 7.7 Doctors Module (`features/doctors/`)
**Purpose**: Doctor panel and live consultations  
**Key Views**:
- `doctor_panel()` - Doctor dashboard
- `live_appointment()` - Live consultation interface
- `start_live_consultation()` - Start session
- `update_consultation_data()` - Save medical data
- `complete_consultation()` - Finish session
- `create_prescription()` - Create prescription
- `sign_prescription()` - Digital signature
- `upload_prescription_file()` - Upload prescription PDF
- `search_patients()` - Search patient records
- `patient_lab_results()` - View patient lab results

**Features**:
- Real-time consultation interface
- Vital signs recording (BP, HR, Temp, etc.)
- Symptoms and diagnosis documentation
- Treatment plan creation
- Digital prescription generation
- Prescription signing with signature capture
- PDF generation for prescriptions
- Patient search functionality
- Lab result access
- Appointment management

### 7.8 Admin Module (`features/admin/`)
**Purpose**: Administrative management and oversight  

#### 7.8.1 Dashboard (`dashboard_views.py`)
- System statistics and overview
- Recent activity monitoring
- Notification management
- Password reset request handling

#### 7.8.2 Analytics (`analytics_views.py`)
- User statistics (patients, doctors, appointments)
- Consultation analytics
- Revenue tracking
- Dynamic statistics API

#### 7.8.3 User Management (`user_views.py`)
- Create, edit, delete users
- View password reset requests
- Download ID verification photos
- Permanent account deletion

#### 7.8.4 Account Management (`account_views.py`)
- Activate/deactivate accounts
- Soft delete accounts
- Restore deleted accounts
- Account status management

#### 7.8.5 Patient Management (`patient_views.py`)
- View all patient records
- Manage lab results
- Manage prescriptions
- Send notifications to patients
- Booked services management

#### 7.8.6 Doctor Management (`doctor_views.py`)
- Add/edit doctor profiles
- Manage doctor specializations
- View doctor statistics
- Convert doctors to patients

#### 7.8.7 Consultation Management (`consultation_views.py`)
- View all appointments
- Approve/reject consultations
- Update appointment status
- Delete appointments
- Manage meeting links

**Admin Features Summary**:
- Comprehensive user management
- Role-based permission control
- Analytics and reporting
- System configuration
- Notification system
- Activity monitoring
- Audit trails

### 7.9 Health Tools Module (`features/healthtools/`)
**Purpose**: Health calculators and utilities  
**Key Views**: `health_tools()`  
**Features**:
- BMI calculator
- Health assessment tools
- Medical calculators

### 7.10 Conditions Module (`features/conditions/`)
**Purpose**: Medical condition information  
**Features**:
- Disease information
- Symptom checker
- Health education content

---

## 8. Authentication System

### Login Flow
1. User submits username/password
2. System validates credentials
3. Password checked with `check_password()`
4. Session created with user data:
   - `user_id`
   - `role`
   - `is_admin` (if admin role)
   - `username`
   - `first_name`, `last_name`
5. Role-based redirect:
   - Admin → `/moddashboard/`
   - Doctor → `/doctor/panel/`
   - Patient → `/dashboard/`

### Signup Flow
1. User fills registration form
2. Profile photo uploaded to Supabase
3. User account created with hashed password
4. UserProfile created with photo URL
5. Auto-login and redirect to dashboard

### Password Reset Flow
1. User requests password reset
2. System sends notification to admin
3. User uploads ID photo for verification
4. Admin reviews request and ID photo
5. Admin manually resets password or contacts user
6. User notified of password change

### Session Management
- **Duration**: 24 hours (configurable)
- **Storage**: Database (django_session table)
- **Security**: HttpOnly cookies, CSRF protection
- **Refresh**: Session saved on every request

### Role-Based Access
```python
Roles:
- admin: Full system access
- doctor: Patient records, consultations, prescriptions
- nurse: Limited patient records, appointment management
- lab_tech: Lab results upload/management
- patient: Own records, appointments, results

Access Control:
- View decorators check session['is_admin']
- Role checked via session['role']
- Permission model for fine-grained control
```

---

## Project Statistics
- **Total Models**: 11 (User, UserProfile, Doctor, Patient, Appointment, LiveAppointment, Prescription, LabResult, Notification, BookedService, RolePermission)
- **Total Features**: 11 modules
- **API Endpoints**: 80+ RESTful endpoints
- **User Roles**: 5 (Admin, Doctor, Nurse, Lab Tech, Patient)
- **Database Tables**: 11 core tables + Django system tables
- **Authentication**: Session-based with CSRF protection
- **File Storage**: Supabase Storage + Base64 encoding

---

## Environment Configuration

### Required Environment Variables (.env)
```env
# Django
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Supabase PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres.wqoluwmdzljpvzimjiyr
DB_PASSWORD=your-password
DB_HOST=aws-1-ap-southeast-1.pooler.supabase.com
DB_PORT=5432
DB_SSLMODE=require

# Supabase Storage
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-key
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_STORAGE_BUCKET=profile-photos
SUPABASE_STORAGE_BUCKET_PRESCRIPTIONS=prescriptions
SUPABASE_STORAGE_BUCKET_NOTIFICATIONS=notifications
```

---

## Development Commands

```bash
# Run development server
python manage.py runserver

# Run on network (LAN access)
python manage.py runserver 0.0.0.0:8000

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Check for issues
python manage.py check

# Shell access
python manage.py shell
```

---

## Notes
- This is a production-ready healthcare management system
- All sensitive data is encrypted in transit and at rest
- Regular backups of PostgreSQL database recommended
- Monitor Supabase usage and quotas
- Keep Django and dependencies updated for security
- Review and test all endpoints before production deployment

---

**Documentation Version:** 1.0  
**Last Updated:** December 1, 2025  
**Maintained By:** MediSafe+ Development Team
