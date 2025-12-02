# MediSafe+ Project Transfer & Migration Guide
## How to Safely Transfer This Project to Another Device

**Version:** 1.0  
**Last Updated:** December 1, 2025

---

## Table of Contents
1. [Overview](#overview)
2. [Pre-Transfer Checklist](#pre-transfer-checklist)
3. [System Requirements](#system-requirements)
4. [Transfer Methods](#transfer-methods)
5. [Step-by-Step Migration Process](#step-by-step-migration-process)
6. [Database Migration](#database-migration)
7. [Environment Configuration](#environment-configuration)
8. [Post-Transfer Verification](#post-transfer-verification)
9. [Troubleshooting](#troubleshooting)

---

## 1. Overview

This guide provides comprehensive instructions for transferring the MediSafe+ healthcare management system from one device to another while preserving all data, configurations, and functionality.

### What Gets Transferred
✅ Complete codebase (Django project)  
✅ Database connection settings (not the database itself - it's cloud-based)  
✅ Environment variables  
✅ Static files and media configurations  
✅ Python dependencies  
✅ Project documentation  

### What Stays in Cloud
☁️ Database (PostgreSQL on Supabase)  
☁️ Uploaded photos (Supabase Storage)  
☁️ User sessions (database-based)  

### Important Notes
⚠️ The database is hosted on Supabase cloud - you only need database credentials  
⚠️ Keep `.env` file secure - it contains sensitive credentials  
⚠️ Python 3.9+ required on new device  
⚠️ Internet connection required for database access  

---

## 2. Pre-Transfer Checklist

### On Current Device (Source)

#### ✅ Step 1: Verify Project is Working
```bash
# Navigate to project directory
cd "path\to\PBL"

# Check for errors
python manage.py check

# Test database connection
python manage.py migrate --check
```

#### ✅ Step 2: Document Current Setup
- [ ] Python version: `python --version`
- [ ] Django version: `python -m django --version`
- [ ] Current working directory path
- [ ] Database connection working
- [ ] Supabase credentials accessible

#### ✅ Step 3: Backup Important Files
Create a backup of these critical files:
- [ ] `.env` file (contains all secrets)
- [ ] `requirements.txt` (dependencies)
- [ ] `db.sqlite3` (if exists, though PostgreSQL is primary)
- [ ] Any custom configuration files

#### ✅ Step 4: Export Requirements
```bash
# Ensure requirements.txt is up to date
pip freeze > requirements.txt
```

#### ✅ Step 5: List Environment Variables
```bash
# On Windows PowerShell
Get-Content .env

# Or manually note down:
- DJANGO_SECRET_KEY
- DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
- SUPABASE_URL, SUPABASE_SERVICE_KEY, SUPABASE_ANON_KEY
```

---

## 3. System Requirements

### New Device Requirements

#### Operating System
- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu 20.04+, Debian, CentOS)

#### Software Requirements
- **Python**: 3.9 or higher (3.11 recommended)
- **pip**: Latest version
- **virtualenv** or **venv**: For isolated environment
- **Git** (optional, for version control)
- **PostgreSQL Client Tools** (optional, for database management)

#### Hardware Requirements
- **Processor**: 2+ cores
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space for project + dependencies
- **Network**: Internet connection for database access

#### Development Tools (Recommended)
- **Code Editor**: VS Code, PyCharm, or Sublime Text
- **Database Client**: pgAdmin, DBeaver (for PostgreSQL management)
- **API Testing**: Postman or Insomnia

---

## 4. Transfer Methods

### Method 1: Direct File Transfer (Recommended)

**Best For**: Same network, USB drive, cloud storage

**Steps**:
1. Copy entire project folder
2. Transfer via:
   - External drive (USB, HDD)
   - Network share
   - Cloud storage (Google Drive, Dropbox, OneDrive)
   - Direct cable connection

**Advantages**:
- Simple and straightforward
- No data loss
- Fast for local transfers

### Method 2: Git Repository

**Best For**: Version control, multiple developers, remote transfer

**Steps**:
1. Initialize Git repository (if not already)
2. Push to GitHub/GitLab/Bitbucket
3. Clone on new device
4. Manually transfer `.env` file separately (don't commit to Git)

**Advantages**:
- Version control
- Easy updates
- Collaboration support

**Setup**:
```bash
# On current device
git init
git add .
git commit -m "Initial commit"
git remote add origin <repository-url>
git push -u origin main

# On new device
git clone <repository-url>
cd MediSafe
# Copy .env file separately
```

### Method 3: Compressed Archive

**Best For**: Email, file hosting, archival

**Steps**:
1. Compress project folder (ZIP, 7z, tar.gz)
2. Transfer via email, file hosting, or cloud
3. Extract on new device

**Windows PowerShell**:
```powershell
# Compress
Compress-Archive -Path "D:\DOWNLOADS\PBL - LATEST\PBL - POLISHING OF ALL\PBL" -DestinationPath "MediSafe_Backup.zip"

# Extract
Expand-Archive -Path "MediSafe_Backup.zip" -DestinationPath "C:\Projects\"
```

---

## 5. Step-by-Step Migration Process

### Phase 1: Prepare Source Device

#### Step 1: Clean Unnecessary Files
Already done! These files were removed:
- ✅ `test_notification_file.py`
- ✅ `test_download_188.jpg`
- ✅ `db.sqlite3` (local SQLite, not needed)
- ✅ `user_views_fixed.py` (duplicate file)

#### Step 2: Verify Project Structure
```
PBL/
├── .env                          ← Important!
├── manage.py
├── requirements.txt              ← Important!
├── MEDISAFE_PBL/
│   └── settings.py               ← Important!
├── myapp/
│   ├── models.py
│   ├── urls.py
│   └── features/
├── media/                        ← Can be empty (Supabase Storage used)
├── static/
└── Documentation files (*.md)
```

#### Step 3: Create Transfer Package

**Option A: Simple Copy**
```powershell
# Copy entire folder to external drive
Copy-Item -Path "D:\DOWNLOADS\PBL - LATEST\PBL - POLISHING OF ALL\PBL" -Destination "E:\Transfer\" -Recurse
```

**Option B: Archive**
```powershell
# Create zip file
Compress-Archive -Path "D:\DOWNLOADS\PBL - LATEST\PBL - POLISHING OF ALL\PBL" -DestinationPath "E:\MediSafe_Project.zip"
```

### Phase 2: Setup New Device

#### Step 1: Install Python

**Windows**:
1. Download Python 3.11 from [python.org](https://www.python.org/downloads/)
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Complete installation
5. Verify: `python --version`

**macOS**:
```bash
# Using Homebrew
brew install python@3.11

# Verify
python3 --version
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
python3.11 --version
```

#### Step 2: Create Project Directory
```powershell
# Windows PowerShell
New-Item -Path "C:\Projects\MediSafe" -ItemType Directory
cd "C:\Projects\MediSafe"
```

```bash
# macOS/Linux
mkdir -p ~/Projects/MediSafe
cd ~/Projects/MediSafe
```

#### Step 3: Transfer Project Files

**If Using External Drive**:
```powershell
# Windows
Copy-Item -Path "E:\Transfer\PBL\*" -Destination "C:\Projects\MediSafe\" -Recurse
```

**If Using Compressed Archive**:
```powershell
# Windows
Expand-Archive -Path "E:\MediSafe_Project.zip" -DestinationPath "C:\Projects\MediSafe\"
```

**If Using Git**:
```bash
git clone <repository-url> .
# Then copy .env file separately from secure location
```

### Phase 3: Environment Setup

#### Step 1: Create Virtual Environment

**Windows**:
```powershell
# Navigate to project
cd "C:\Projects\MediSafe"

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**macOS/Linux**:
```bash
cd ~/Projects/MediSafe

# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate
```

**Verification**: Your prompt should show `(venv)` prefix

#### Step 2: Upgrade pip
```bash
python -m pip install --upgrade pip
```

#### Step 3: Install Dependencies
```bash
# Install from requirements.txt
pip install -r requirements.txt

# This installs:
# - Django 5.2.6
# - PostgreSQL driver (psycopg2)
# - Supabase SDK
# - All other dependencies
```

**Common Installation Issues**:

**Issue: psycopg2 fails to install**
```bash
# Try psycopg2-binary instead
pip install psycopg2-binary
```

**Issue: Pillow fails on Windows**
```bash
# Install Visual C++ Redistributable from Microsoft
# Then retry: pip install pillow
```

### Phase 4: Environment Configuration

#### Step 1: Verify .env File Exists
```bash
# Check if .env exists
# Windows PowerShell
Test-Path .env

# macOS/Linux
ls -la .env
```

#### Step 2: Review .env Contents
```bash
# Windows PowerShell
Get-Content .env

# macOS/Linux
cat .env
```

**Required Variables**:
```env
# Django Configuration
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database Configuration (Supabase PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres.wqoluwmdzljpvzimjiyr
DB_PASSWORD=your-database-password
DB_HOST=aws-1-ap-southeast-1.pooler.supabase.com
DB_PORT=5432
DB_SSLMODE=require

# Supabase Storage
SUPABASE_URL=https://wqoluwmdzljpvzimjiyr.supabase.co
SUPABASE_SERVICE_KEY=your-service-key
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_STORAGE_BUCKET=profile-photos
SUPABASE_STORAGE_BUCKET_PRESCRIPTIONS=prescriptions
SUPABASE_STORAGE_BUCKET_NOTIFICATIONS=notifications
```

#### Step 3: Update Settings (If Needed)

**If changing host IP**:
Edit `MEDISAFE_PBL/settings.py`:
```python
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "192.168.x.x",  # Your new IP if needed
]
```

### Phase 5: Database Migration

#### Step 1: Test Database Connection
```bash
python manage.py check
```

**Expected Output**:
```
System check identified no issues (0 silenced).
```

**If Errors**:
- Check `.env` database credentials
- Verify internet connection
- Test Supabase database is accessible

#### Step 2: Apply Migrations
```bash
python manage.py migrate
```

**Expected Output**:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, myapp, sessions
Running migrations:
  No migrations to apply.
```

**Note**: Since database is cloud-based, migrations are already applied. This just verifies connection.

#### Step 3: Create Superuser (If Needed)
```bash
# Only if starting fresh or need new admin
python manage.py createsuperuser

# Follow prompts:
# Username: admin
# Email: admin@medisafe.com
# Password: (secure password)
```

---

## 6. Database Migration

### Understanding the Database Setup

**Current Setup**: Cloud-based PostgreSQL on Supabase
- Database is NOT on your local machine
- Database remains in the cloud
- Only connection credentials needed
- All data is already there

### No Database File to Transfer!

✅ **Good News**: You don't need to transfer any database file  
✅ Database is accessible from any device with credentials  
✅ All patient data, appointments, users are in the cloud  

### If You Need to Backup Database

**Option 1: Supabase Dashboard**
1. Login to [Supabase Dashboard](https://app.supabase.com/)
2. Select your project
3. Go to Database → Backups
4. Create manual backup
5. Download backup file

**Option 2: pg_dump (Command Line)**
```bash
# Requires PostgreSQL client tools installed
pg_dump -h aws-1-ap-southeast-1.pooler.supabase.com \
        -p 5432 \
        -U postgres.wqoluwmdzljpvzimjiyr \
        -d postgres \
        -F c -b -v -f medisafe_backup.dump

# Enter password when prompted
```

### If Switching Databases

**To Use New Database**:
1. Create new Supabase project or PostgreSQL instance
2. Update `.env` with new credentials
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Create superuser
5. Import data (if needed)

---

## 7. Environment Configuration

### Configuring for Different Environments

#### Development Environment
**.env**:
```env
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,192.168.x.x
```

#### Production Environment
**.env**:
```env
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Network Configuration

#### For LAN Access
1. Find your IP address:
   ```bash
   # Windows
   ipconfig
   
   # macOS/Linux
   ifconfig
   ```

2. Add IP to `ALLOWED_HOSTS` in settings.py:
   ```python
   ALLOWED_HOSTS = [
       "localhost",
       "127.0.0.1",
       "192.168.1.100",  # Your IP
   ]
   ```

3. Run server on all interfaces:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

4. Access from other devices:
   ```
   http://192.168.1.100:8000
   ```

---

## 8. Post-Transfer Verification

### Verification Checklist

#### ✅ Step 1: System Check
```bash
python manage.py check
```
**Expected**: `System check identified no issues`

#### ✅ Step 2: Database Connection
```bash
python manage.py migrate --check
```
**Expected**: No pending migrations

#### ✅ Step 3: Static Files
```bash
python manage.py collectstatic --noinput
```
**Expected**: Static files collected successfully

#### ✅ Step 4: Run Development Server
```bash
python manage.py runserver
```
**Expected**:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
December 01, 2025 - 10:00:00
Django version 5.2.6, using settings 'MEDISAFE_PBL.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

#### ✅ Step 5: Access Homepage
1. Open browser
2. Navigate to: `http://127.0.0.1:8000/`
3. Verify homepage loads

#### ✅ Step 6: Test Login
1. Go to login page
2. Try logging in with existing credentials
3. Verify dashboard loads

#### ✅ Step 7: Test Admin Panel
1. Navigate to: `http://127.0.0.1:8000/moddashboard/`
2. Login with admin credentials
3. Verify dashboard displays correctly

#### ✅ Step 8: Test Database Read
- View users list
- View appointments
- Check statistics display

#### ✅ Step 9: Test Database Write
- Try creating a test appointment
- Verify data saves
- Delete test data

#### ✅ Step 10: Test File Upload
- Try updating profile photo
- Verify Supabase connection
- Check photo displays

### Verification Results
- [ ] All checks pass
- [ ] Server runs without errors
- [ ] Homepage accessible
- [ ] Login works
- [ ] Admin panel accessible
- [ ] Database reads work
- [ ] Database writes work
- [ ] File uploads work
- [ ] No console errors
- [ ] All features functional

---

## 9. Troubleshooting

### Common Issues and Solutions

#### Issue 1: Module Not Found Error
```
ModuleNotFoundError: No module named 'django'
```

**Solution**:
```bash
# Verify virtual environment is activated
# Windows
.\venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### Issue 2: Database Connection Failed
```
django.db.utils.OperationalError: could not connect to server
```

**Solutions**:
1. Check internet connection
2. Verify `.env` database credentials
3. Test Supabase project is active
4. Check firewall settings
5. Verify database host URL

```bash
# Test connection
python manage.py dbshell
```

#### Issue 3: Permission Denied on Virtual Environment
```
Activate.ps1 cannot be loaded because running scripts is disabled
```

**Solution** (Windows):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Issue 4: Port Already in Use
```
Error: That port is already in use.
```

**Solution**:
```bash
# Use different port
python manage.py runserver 8080

# Or find and kill process using port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# macOS/Linux
lsof -i :8000
kill -9 <process_id>
```

#### Issue 5: Static Files Not Loading
```
404 errors for CSS/JS files
```

**Solution**:
```bash
# Collect static files
python manage.py collectstatic

# Verify STATIC_URL in settings.py
# Check STATICFILES_DIRS configuration
```

#### Issue 6: Supabase File Upload Fails
```
Error uploading to Supabase Storage
```

**Solutions**:
1. Check SUPABASE_SERVICE_KEY in `.env`
2. Verify bucket names are correct
3. Check bucket permissions in Supabase dashboard
4. Test internet connection

#### Issue 7: Migration Errors
```
django.db.migrations.exceptions.InconsistentMigrationHistory
```

**Solution**:
```bash
# This shouldn't happen with cloud database
# If it does:
python manage.py migrate --fake-initial
```

#### Issue 8: ImportError After Transfer
```
ImportError: cannot import name 'X' from 'Y'
```

**Solution**:
```bash
# Clear Python cache
# Windows
Remove-Item -Recurse -Force __pycache__
Remove-Item -Recurse -Force *.pyc

# macOS/Linux
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name *.pyc -delete

# Restart server
python manage.py runserver
```

---

## 10. Best Practices

### Security Best Practices

1. **Never Commit .env to Git**
   ```bash
   # Add to .gitignore
   echo ".env" >> .gitignore
   ```

2. **Use Strong SECRET_KEY**
   ```python
   # Generate new secret key
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

3. **Secure Database Credentials**
   - Don't share `.env` file via public channels
   - Use secure file transfer methods
   - Change passwords if exposed

4. **Production Settings**
   - Set `DEBUG=False`
   - Use HTTPS
   - Configure proper ALLOWED_HOSTS
   - Enable security middleware

### Performance Best Practices

1. **Use Virtual Environment**
   - Isolates dependencies
   - Prevents conflicts
   - Easy to recreate

2. **Keep Dependencies Updated**
   ```bash
   pip list --outdated
   pip install --upgrade package-name
   ```

3. **Monitor Database Connection**
   - Use connection pooling
   - Set appropriate CONN_MAX_AGE
   - Monitor query performance

4. **Static Files Optimization**
   ```bash
   python manage.py collectstatic
   ```

### Maintenance Best Practices

1. **Regular Backups**
   - Weekly database backups
   - Version control for code
   - Document changes

2. **Testing After Transfer**
   - Test all features
   - Verify all API endpoints
   - Check file uploads
   - Test user workflows

3. **Documentation**
   - Keep transfer log
   - Document any changes
   - Update README

---

## 11. Quick Reference

### Essential Commands

```bash
# Activate virtual environment
# Windows
.\venv\Scripts\Activate.ps1
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run development server
python manage.py runserver

# Run on network
python manage.py runserver 0.0.0.0:8000

# Check for issues
python manage.py check

# Database shell
python manage.py dbshell

# Python shell
python manage.py shell
```

### File Locations

```
Critical Files:
├── .env                          (Database credentials, secrets)
├── requirements.txt              (Python dependencies)
├── manage.py                     (Django management)
├── MEDISAFE_PBL/settings.py     (Project configuration)
├── MEDISAFE_PBL/urls.py         (URL routing)
└── myapp/models.py              (Database models)

Documentation:
├── PROJECT_DOCUMENTATION.md      (Complete project overview)
├── PATIENT_PORTAL_GUIDE.md       (Patient features)
├── DOCTOR_PORTAL_GUIDE.md        (Doctor features)
├── ADMIN_PORTAL_GUIDE.md         (Admin features)
└── MIGRATION_GUIDE.md           (This file)
```

### Support Contacts

- **Technical Issues**: IT Department
- **Database Issues**: Database Administrator
- **Transfer Help**: System Administrator
- **Documentation**: Refer to guide files

---

## 12. Checklist: Complete Transfer Process

### Pre-Transfer
- [ ] Project working on current device
- [ ] `.env` file backed up securely
- [ ] Requirements.txt updated
- [ ] Unnecessary files cleaned
- [ ] Documentation reviewed

### During Transfer
- [ ] Python 3.9+ installed on new device
- [ ] Project files transferred
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] `.env` file configured

### Post-Transfer
- [ ] System check passes
- [ ] Database connection works
- [ ] Development server runs
- [ ] Homepage loads
- [ ] Login functional
- [ ] Admin panel accessible
- [ ] File uploads work
- [ ] All features tested

### Final Steps
- [ ] Documentation updated
- [ ] Transfer notes created
- [ ] Old device backup maintained
- [ ] Team notified (if applicable)

---

## Success!

If all verification steps pass, your MediSafe+ project has been successfully transferred to the new device! 🎉

### Next Steps
1. **Test thoroughly**: Use the system for a day to ensure everything works
2. **Monitor logs**: Check for any errors in console
3. **Update documentation**: Note any custom changes
4. **Keep backup**: Maintain backup of old device until confident

### Need Help?
Refer to:
- PROJECT_DOCUMENTATION.md for system overview
- Specific portal guides for feature details
- Django documentation for framework help
- Supabase documentation for database/storage

---

**Migration Guide Version:** 1.0  
**Last Updated:** December 1, 2025  
**For Support**: Contact your system administrator or IT department
