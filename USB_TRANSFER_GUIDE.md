# Quick USB Transfer Guide
## Running MediSafe+ on Another Device

---

## What You Need to Install

### 1. Python 3.9 or Higher
- Download from: https://python.org/downloads/
- ✅ **Important**: Check "Add Python to PATH" during installation
- Verify installation: `python --version`

### 2. That's It for Software!
All other dependencies will be installed automatically from `requirements.txt`

---

## Step-by-Step Instructions

### Step 1: Copy to USB
1. Copy the entire `PBL` folder to your USB drive
2. Make sure `.env` file is included (it contains database credentials)

### Step 2: On New Device

#### A. Copy from USB
```powershell
# Copy to your preferred location
Copy-Item -Path "E:\PBL" -Destination "C:\Projects\MediSafe" -Recurse
cd "C:\Projects\MediSafe"
```

#### B. Create Virtual Environment
```powershell
python -m venv venv
```

#### C. Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

**If you get an error**, run this first:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then try activating again.

#### D. Install All Dependencies
```powershell
pip install -r requirements.txt
```
This installs Django, PostgreSQL driver, Supabase SDK, and everything else needed.

#### E. Verify Setup
```powershell
python manage.py check
```
Should show: `System check identified no issues`

#### F. Run the Server
```powershell
python manage.py runserver
```

#### G. Access the Application
Open browser and go to: `http://127.0.0.1:8000/`

---

## That's It! 🎉

Your application should now be running on the new device.

### Important Notes:
- ✅ Database is in the cloud (Supabase) - no database file to transfer
- ✅ All patient data is already accessible from any device
- ✅ Just need Python + dependencies from requirements.txt
- ✅ Make sure `.env` file is present (has database credentials)

### To Run Again Later:
```powershell
cd "C:\Projects\MediSafe"
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

---

## Troubleshooting

**Problem**: Module not found error  
**Solution**: Make sure virtual environment is activated (you should see `(venv)` in your terminal)

**Problem**: Can't connect to database  
**Solution**: Check that `.env` file exists and has correct credentials

**Problem**: Port already in use  
**Solution**: Use different port: `python manage.py runserver 8080`

---

**For detailed instructions, see:** `MIGRATION_GUIDE.md`
