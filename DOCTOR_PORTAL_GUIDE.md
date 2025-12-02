# MediSafe+ Doctor Portal
## User Guide and Technical Documentation

**Version:** 1.0  
**Last Updated:** December 1, 2025

---

## Table of Contents
1. [Doctor Portal Overview](#doctor-portal-overview)
2. [Getting Started](#getting-started)
3. [Features & Functionality](#features--functionality)
4. [Live Consultation System](#live-consultation-system)
5. [Prescription Management](#prescription-management)
6. [Patient Management](#patient-management)
7. [Technical Reference](#technical-reference)

---

## 1. Doctor Portal Overview

The MediSafe+ Doctor Portal is a comprehensive clinical platform that enables healthcare providers to manage patient consultations, conduct live examinations, create digital prescriptions, access medical records, and provide quality patient care.

### Key Capabilities
- **Live Consultations**: Real-time patient examination interface
- **Digital Prescriptions**: E-prescription creation with digital signatures
- **Patient Records**: Access to medical history and lab results
- **Appointment Management**: View and manage consultations
- **Medical Documentation**: Record symptoms, diagnoses, and treatment plans
- **Patient Search**: Quick access to patient information
- **Prescription History**: Track all issued prescriptions
- **Vital Signs Recording**: Document clinical measurements

---

## 2. Getting Started

### Account Setup
Doctor accounts are created by administrators with the following information:
- Username
- Email
- Password
- Doctor-specific information:
  - Specialization (Cardiology, Pediatrics, etc.)
  - License number
  - Years of experience
  - Contact information
  - Availability schedule

### First Login
1. Navigate to login page
2. Enter username and password
3. System validates credentials
4. Automatic redirect to Doctor Panel (`/doctor/panel/`)
5. Complete profile setup if needed

### Profile Management
**URL**: `/doctor/panel/`  
**Endpoint**: `POST /doctor/api/update-profile/`

**Editable Information**:
- Specialization
- Years of experience
- Contact information
- Availability schedule (JSON format)
- Profile photo (via user profile)

---

## 3. Features & Functionality

### 3.1 Doctor Dashboard
**URL**: `/doctor/panel/`

#### Dashboard Sections

**1. Today's Appointments**
- List of scheduled consultations for current day
- Appointment details:
  - Appointment number
  - Patient name
  - Time slot
  - Consultation type (F2F/Tele)
  - Status (Pending/Approved/Scheduled)
- Quick actions:
  - View patient details
  - Start consultation
  - Cancel appointment

**2. Pending Approvals**
- New appointment requests awaiting approval
- Patient information
- Requested time slots
- Reason for visit
- Actions:
  - Approve appointment
  - Reject with reason
  - Request reschedule

**3. Recent Patients**
- List of recently seen patients
- Quick access to patient records
- Last consultation date
- Medical record number

**4. Statistics**
- Total patients seen
- Consultations this month
- Pending appointments
- Prescriptions issued

**5. Notifications**
- Appointment confirmations
- Patient messages
- System updates
- Lab result alerts

### 3.2 Appointment Management

#### Viewing Appointments
- **All Appointments**: Chronological list with filters
- **By Status**: Pending, Approved, Scheduled, Completed
- **By Type**: F2F or Tele-consultation
- **By Date**: Custom date range

#### Appointment Details
- Patient demographics
- Contact information
- Medical history
- Previous consultations
- Lab results
- Allergies and conditions
- Emergency contact

#### Approving Appointments
1. Review appointment request
2. Check availability
3. Review patient information
4. Click "Approve"
5. System sends confirmation to patient
6. Generates meeting link (for tele-consultations)

#### Managing Meeting Links
- For tele-consultations
- Automatically generated unique links
- Accessible to patient 15 minutes before appointment
- Valid for appointment duration + buffer

### 3.3 Patient Search
**URL**: `/doctors/search-patients/`  
**Method**: GET with query parameters

#### Search Functionality
```javascript
Parameters:
- search: Patient name or medical record number
- Returns: List of matching patients with:
  - Patient ID
  - Full name
  - MRN (Medical Record Number)
  - Contact information
  - Last visit date
```

#### Usage
1. Enter patient name or MRN in search box
2. System searches database
3. Results displayed with patient cards
4. Click patient to view full details

### 3.4 Patient Medical Records

#### Accessing Records
**URL**: `/doctors/patient-lab-results/<patient_id>/`

**Available Information**:
1. **Personal Information**
   - Name, age, sex
   - Blood type
   - Allergies
   - Chronic conditions
   - Emergency contact

2. **Consultation History**
   - Date and time
   - Type of consultation
   - Diagnosis
   - Treatment provided
   - Follow-up notes

3. **Lab Results**
   - Lab type
   - Date performed
   - Result file
   - Interpretation notes
   - Normal ranges

4. **Prescriptions**
   - Prescription number
   - Date issued
   - Medications
   - Dosage instructions
   - Duration

5. **Vital Signs History**
   - Blood pressure trends
   - Heart rate patterns
   - Temperature records
   - Weight changes

#### Downloading Lab Results
**Endpoint**: `GET /doctors/download-lab-result/<result_id>/`
1. Navigate to patient lab results
2. Click "Download" on specific result
3. File downloaded to device
4. Supports PDF, images, and other formats

---

## 4. Live Consultation System

The Live Consultation System is the core feature of the doctor portal, providing a comprehensive interface for conducting patient examinations and documenting medical information in real-time.

### 4.1 Consultation Interface
**URL**: `/doctors/live-appointment/`

#### Starting a Consultation
**Endpoint**: `POST /doctors/start-consultation/<appointment_id>/`

1. Navigate to today's appointments
2. Click "Start Consultation" on scheduled appointment
3. System creates LiveAppointment record
4. Status changes to "In Progress"
5. Live consultation interface opens
6. Timer starts recording session duration

#### Interface Layout

**Left Panel: Patient Information**
- Patient photo
- Name and demographics
- Medical record number
- Contact information
- Known allergies (highlighted)
- Chronic conditions
- Previous consultation summary

**Center Panel: Clinical Documentation**
1. **Vital Signs Section**
   ```
   - Blood Pressure (systolic/diastolic)
   - Heart Rate (BPM)
   - Temperature (°F or °C)
   - Respiratory Rate
   - Oxygen Saturation (SpO2)
   - Weight
   - Height
   ```

2. **Live Patient Vitals (Smartwatch Integration)** ⭐ NEW
   - **Real-time monitoring** of patient vital signs from connected smartwatch
   - **Auto-refresh** every 10 seconds
   - **Manual refresh** button available
   - **Live indicator** shows connection status
   - **Color-coded values**:
     - 🟢 Green: Normal range
     - 🟡 Yellow: Warning range
     - 🔴 Red: Critical range
   
   **Displayed Vitals**:
   - Blood Pressure (systolic/diastolic mmHg)
   - Heart Rate (BPM)
   - Oxygen Saturation (SpO2 %)
   - Last updated timestamp
   
   **How It Works**:
   - Vitals fetch automatically when appointment loads
   - Data pulled from `watch_vitals` table using patient's `user_id`
   - Updates continuously during consultation
   - Click refresh button for immediate update
   - "LIVE" badge indicates active monitoring

3. **Symptoms Section**
   - Chief complaint
   - Duration
   - Severity (1-10 scale)
   - Associated symptoms
   - Previous episodes

4. **Physical Examination**
   - General appearance
   - System-by-system examination
   - Findings and observations

5. **Diagnosis Section**
   - Primary diagnosis
   - Differential diagnoses
   - ICD-10 codes (optional)
   - Diagnosis certainty

6. **Treatment Plan**
   - Recommended medications
   - Lifestyle modifications
   - Follow-up schedule
   - Referrals if needed

7. **Clinical Notes**
   - Detailed examination notes
   - Assessment
   - Plan
   - Patient education provided

**Right Panel: Actions**
- Save progress (auto-save every 30 seconds)
- Create prescription
- Complete consultation
- Cancel consultation
- Access patient history
- View lab results

### 4.2 Recording Clinical Data
**Endpoint**: `POST /doctors/update-consultation/<live_session_id>/`

#### Vital Signs Entry
```javascript
Data Structure:
{
  "vital_signs": {
    "blood_pressure": "120/80",
    "heart_rate": "72",
    "temperature": "98.6",
    "respiratory_rate": "16",
    "oxygen_saturation": "98",
    "weight": "70",
    "height": "170"
  }
}
```

**Process**:
1. Click "Vital Signs" section
2. Enter measurements
3. System validates input ranges
4. Flags abnormal values
5. Saves to LiveAppointment.vital_signs (JSON)
6. Displays historical comparison

#### Symptoms Documentation
1. Click "Symptoms" section
2. Enter chief complaint
3. Document duration and severity
4. Note associated symptoms
5. Save to LiveAppointment.symptoms
6. System suggests common diagnoses (future feature)

#### Diagnosis Entry
1. Navigate to "Diagnosis" section
2. Enter primary diagnosis
3. Add differential diagnoses if applicable
4. Save to LiveAppointment.diagnosis
5. Diagnosis saved permanently with consultation

#### Treatment Plan Creation
1. Open "Treatment Plan" section
2. Document recommended treatment:
   - Medications (detailed in prescription)
   - Lifestyle changes
   - Home care instructions
   - Activity restrictions
   - Diet modifications
3. Set follow-up date
4. Save to LiveAppointment.treatment_plan

### 4.3 Auto-Save Feature
- Automatically saves every 30 seconds
- Prevents data loss
- Shows "Saved" indicator
- Manual save button available
- Saves to database immediately

### 4.4 Restarting Consultations
**Endpoint**: `POST /doctors/restart-consultation/<appointment_id>/`

**When to Use**:
- Consultation accidentally closed
- Need to add more information
- Technical interruption
- Forgot to create prescription

**Process**:
1. Find completed consultation
2. Click "Restart Consultation"
3. System reopens LiveAppointment
4. Status changes to "In Progress"
5. All previous data preserved
6. Continue documentation

### 4.5 Completing Consultations
**Endpoint**: `POST /doctors/complete-consultation/<live_session_id>/`

**Pre-Completion Checklist**:
- [ ] Vital signs recorded
- [ ] Symptoms documented
- [ ] Diagnosis entered
- [ ] Treatment plan created
- [ ] Prescription created (if needed)
- [ ] Follow-up date set
- [ ] Patient education provided

**Process**:
1. Review all sections
2. Ensure all required fields filled
3. Click "Complete Consultation"
4. System prompts: "Create prescription now?"
5. Choose:
   - Yes: Proceed to prescription creation
   - No: Complete without prescription
   - Cancel: Return to consultation
6. Status changes to "Completed"
7. Session duration calculated
8. Appointment status updated
9. Patient receives notification

### 4.6 Consultation History
- All consultations archived permanently
- Accessible from patient records
- Shows:
  - Date and time
  - Duration
  - Vital signs
  - Diagnosis
  - Treatment plan
  - Prescriptions issued
  - Follow-up notes

---

## 5. Prescription Management

### 5.1 Creating Prescriptions
**URL**: `/doctors/create-prescription/<live_session_id>/`  
**Method**: POST

#### Prescription Creation Process

**Step 1: Prescription Wizard Opens**
- Linked to current LiveAppointment
- Auto-generates prescription number (RX-XXXXXXXX)
- Pre-fills patient and doctor information

**Step 2: Add Medications**
```javascript
Medicine Object:
{
  "name": "Medication name",
  "dosage": "500mg",
  "frequency": "Twice daily",
  "duration": "7 days",
  "instructions": "Take with food",
  "quantity": "14 tablets"
}
```

**Adding Medicines**:
1. Click "Add Medication"
2. Enter medicine details:
   - Generic/brand name
   - Dosage (mg, ml, etc.)
   - Frequency (Once/Twice/Three times/Four times daily)
   - Duration (days)
   - Special instructions
   - Quantity to dispense
3. Click "Add to Prescription"
4. Repeat for all medications
5. Medicines stored in JSON array

**Step 3: General Instructions**
- Overall prescription instructions
- Diet recommendations
- Activity restrictions
- When to return

**Step 4: Follow-up**
- Set follow-up date
- Follow-up instructions
- When to call if symptoms worsen

**Step 5: Save Draft**
- Prescription saved as "Draft"
- Can edit before signing
- Review all information

### 5.2 Signing Prescriptions
**Endpoint**: `POST /doctors/sign-prescription/<prescription_id>/`

#### Digital Signature Process

**Requirements**:
- All medication details complete
- Instructions provided
- Follow-up date set
- Doctor logged in

**Signing Method 1: Signature Pad**
1. Click "Sign Prescription"
2. Signature pad modal opens
3. Draw signature with mouse/stylus/finger
4. Click "Apply Signature"
5. Signature converted to Base64 image
6. Saved to Prescription.doctor_signature
7. Signature date recorded
8. Status changes to "Signed"

**Signing Method 2: Upload Signature**
1. Upload pre-made signature image
2. System converts to Base64
3. Applies to prescription
4. Status updates

**Post-Signing**:
- Prescription locked (no edits)
- Patient receives notification
- Prescription available in patient portal
- Can generate PDF

### 5.3 Prescription PDF Generation
**Endpoint**: `GET /doctors/prescription-pdf/<prescription_id>/`

#### PDF Contents
```
Header:
- Clinic logo
- Clinic name and address
- Doctor name and specialization
- License number
- Contact information

Patient Information:
- Name
- Age, Sex
- MRN
- Date

Rx Symbol

Medications Table:
| Medicine | Dosage | Frequency | Duration |
|----------|---------|-----------|----------|

Instructions:
- General instructions
- Diet recommendations
- Follow-up information

Signature:
- Doctor's digital signature
- Date signed
- Stamp (optional)

Footer:
- Prescription number
- "This is a digital prescription"
```

**Generation Process**:
1. Click "Generate PDF"
2. System renders HTML template
3. Converts to PDF
4. Downloads to device
5. Patient can also download from portal

### 5.4 Uploading Prescription Files
**Endpoint**: `POST /doctors/upload-prescription-file/<prescription_id>/`

**Use Cases**:
- Upload scanned handwritten prescription
- Upload pre-filled prescription form
- Attach additional documentation

**Process**:
1. Click "Upload Prescription File"
2. Select PDF or image file
3. File converted to Base64
4. Saved to Prescription.prescription_file
5. Available for patient download

### 5.5 Viewing All Prescriptions
**URL**: `/api/get-all-prescriptions/`  
**Method**: GET

#### Prescription List Features
- All prescriptions issued by doctor
- Sortable by date
- Filterable by:
  - Patient name
  - Date range
  - Status (Draft/Signed/Printed)
  - Prescription number
- Search functionality

#### Prescription Details View
**URL**: `/doctors/prescription-details/<prescription_id>/`

**Available Information**:
- Full prescription details
- Patient information
- Medications list
- Instructions
- Signature status
- Creation and signing dates
- Associated consultation
- Download options

### 5.6 Downloading Prescriptions
**Endpoint**: `GET /doctors/download-prescription/<prescription_id>/`

1. Navigate to prescription list
2. Click "Download" on specific prescription
3. System retrieves prescription file
4. If PDF uploaded: Downloads uploaded file
5. If no upload: Generates PDF on-the-fly
6. File downloaded to device

---

## 6. Patient Management

### 6.1 Patient Overview
Doctors have read-only access to comprehensive patient information for informed clinical decision-making.

#### Patient Profile Access
- Basic demographics
- Medical record number
- Blood type
- Known allergies (prominently displayed)
- Chronic conditions
- Emergency contact information
- Insurance information (if applicable)

### 6.2 Medical History Review

**Consultation History**:
- Previous diagnoses
- Treatment outcomes
- Prescribed medications
- Adverse reactions
- Hospitalization records

**Lab Results History**:
- Blood work
- Imaging studies
- Pathology reports
- Diagnostic test results
- Trends over time

**Prescription History**:
- All previously issued prescriptions
- Current medications
- Medication adherence
- Drug interactions

### 6.3 Patient Communication

**In-Portal Communication**:
- Notifications to patients
- Follow-up reminders
- Test result availability alerts
- Appointment reminders

**External Communication**:
- Contact via registered phone/email
- Emergency contact when needed

---

## 7. Technical Reference

### 7.1 API Endpoints Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/doctor/panel/` | GET | Doctor dashboard |
| `/doctor/api/update-profile/` | POST | Update doctor profile |
| `/doctors/search-patients/` | GET | Search patients |
| `/doctors/patient-lab-results/<id>/` | GET | View patient lab results |
| `/doctors/download-lab-result/<id>/` | GET | Download lab result file |
| `/doctors/live-appointment/` | GET | Live consultation interface |
| `/doctors/start-consultation/<id>/` | POST | Start live consultation |
| `/doctors/restart-consultation/<id>/` | POST | Restart consultation |
| `/doctors/update-consultation/<id>/` | POST | Save consultation data |
| `/doctors/complete-consultation/<id>/` | POST | Complete consultation |
| `/doctors/create-prescription/<id>/` | POST | Create prescription |
| `/doctors/sign-prescription/<id>/` | POST | Sign prescription |
| `/doctors/prescription-pdf/<id>/` | GET | Generate prescription PDF |
| `/doctors/upload-prescription-file/<id>/` | POST | Upload prescription file |
| `/api/get-all-prescriptions/` | GET | Get all doctor's prescriptions |
| `/doctors/prescription-details/<id>/` | GET | View prescription details |
| `/doctors/download-prescription/<id>/` | GET | Download prescription |
| `/doctors/api/mark-notification-read/` | POST | Mark notification read |

### 7.2 Data Models

#### LiveAppointment Model
```python
Fields:
- live_appointment_id (PK)
- appointment (FK to Appointment)
- status (waiting/in_progress/completed/cancelled)
- started_at, completed_at
- session_duration (calculated)
- vital_signs (JSONField)
- symptoms (TextField)
- diagnosis (TextField)
- clinical_notes (TextField)
- treatment_plan (TextField)
- follow_up_notes (TextField)
- doctor_notes (TextField)
- recommendations (TextField)
```

#### Prescription Model
```python
Fields:
- prescription_id (PK)
- live_appointment (FK to LiveAppointment)
- prescription_number (Unique)
- doctor (FK to Doctor)
- medicines (JSONField)
- instructions (TextField)
- follow_up_date (DateField)
- follow_up_instructions (TextField)
- doctor_signature (TextField - Base64)
- signature_date (DateTimeField)
- prescription_file (TextField - Base64)
- status (draft/signed/printed/cancelled)
```

### 7.3 Security & Permissions

#### Access Control
- Only logged-in doctors can access doctor portal
- Session validation on every request
- Role verification: `session['role'] == 'doctor'`
- Cannot access other doctors' private data

#### Data Protection
- Patient medical records encrypted
- Prescriptions digitally signed
- Audit trail for all access
- HIPAA-compliant practices

#### Authentication Flow
```
1. Doctor logs in
2. Session created with role='doctor'
3. Each request validates session
4. Doctor ID retrieved from User model
5. Access granted to authorized resources
```

### 7.4 Front-End Technologies

**Interface Components**:
- HTML5 forms for data entry
- Tailwind CSS for responsive design
- JavaScript for real-time updates
- Fetch API for AJAX calls
- Canvas for signature capture

**Real-Time Features**:
- Auto-save functionality
- Live session timer
- Notification updates
- Search autocomplete

### 7.5 Error Handling

**Common Errors**:
- Session expired: Redirect to login
- Invalid appointment ID: Show error message
- Missing required fields: Highlight fields
- Network errors: Retry with user prompt
- File upload errors: Size/type validation

**User Notifications**:
- Success messages (green)
- Warning messages (yellow)
- Error messages (red)
- Info messages (blue)

---

## Best Practices for Doctors

### Clinical Documentation
1. **Complete All Fields**: Ensure thorough documentation
2. **Use Standard Terminology**: Medical abbreviations and terms
3. **Be Specific**: Detailed symptoms and findings
4. **Record Vital Signs**: Always document measurements
5. **Document Reasoning**: Explain diagnosis rationale

### Prescription Writing
1. **Generic Names**: Use generic medication names
2. **Clear Dosing**: Specify dose, frequency, duration
3. **Special Instructions**: Note timing, food interactions
4. **Drug Interactions**: Check patient's current medications
5. **Follow-up**: Always set follow-up date

### Patient Safety
1. **Allergy Check**: Review allergies before prescribing
2. **Contraindications**: Check medical conditions
3. **Drug Interactions**: Verify compatibility
4. **Patient Education**: Explain treatment clearly
5. **Emergency Instructions**: When to seek immediate care

### Workflow Efficiency
1. **Review Before Consultation**: Check patient history
2. **Use Templates**: Standard documentation templates
3. **Auto-Save**: Rely on auto-save but save manually
4. **Batch Processing**: Handle similar tasks together
5. **End-of-Day Review**: Complete pending documentation

---

## Troubleshooting

### Cannot Start Consultation
- Verify appointment is approved
- Check appointment time is current
- Ensure stable internet connection
- Try refreshing browser

### Auto-Save Not Working
- Check internet connection
- Look for "Saved" indicator
- Save manually if uncertain
- Contact support if persistent

### Signature Not Capturing
- Ensure mouse/touch input working
- Try different browser
- Clear browser cache
- Use signature upload instead

### Patient Records Not Loading
- Verify patient ID correct
- Check permissions
- Refresh page
- Report to admin if persistent

### PDF Not Generating
- Ensure all required fields filled
- Check prescription is signed
- Try different browser
- Contact support for assistance

---

## Mobile Usage

### Mobile Doctor Portal
- Responsive design for tablets and phones
- Touch-optimized interface
- Simplified navigation
- Essential features accessible

### Limitations on Mobile
- Signature capture may be challenging on small screens
- File uploads may require desktop
- Complex documentation easier on larger screens
- Recommend tablet or desktop for consultations

---

## Support & Resources

### Getting Help
- **Technical Issues**: Contact IT support
- **Clinical Questions**: Consult medical director
- **Account Problems**: Contact admin
- **Feature Requests**: Submit via feedback form

### Training Resources
- User guide (this document)
- Video tutorials
- In-person training sessions
- Quick reference cards

---

## Appendix

### Keyboard Shortcuts
- `Ctrl+S`: Save consultation data
- `Ctrl+P`: Print prescription
- `Ctrl+N`: New prescription
- `Esc`: Close modals

### Glossary
- **F2F**: Face-to-Face consultation
- **Tele**: Tele-consultation
- **MRN**: Medical Record Number
- **Rx**: Prescription
- **BP**: Blood Pressure
- **HR**: Heart Rate
- **SpO2**: Oxygen Saturation
- **ICD**: International Classification of Diseases

---

**Doctor Portal Version:** 1.0  
**Last Updated:** December 1, 2025  
**For Support**: Contact MediSafe+ IT Department
