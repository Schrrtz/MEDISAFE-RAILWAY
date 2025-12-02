# MediSafe+ - Railway Deployment Guide

## 🚀 Quick Deployment to Railway

This guide will help you deploy MediSafe+ to Railway in minutes.

### Prerequisites
- Railway account (https://railway.app)
- GitHub account
- Your Supabase credentials

### Step 1: Push to GitHub

```bash
cd PBL
git init
git add .
git commit -m "Initial commit - MediSafe+ for Railway"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Step 2: Deploy on Railway

1. Go to https://railway.app
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your MediSafe repository
5. Railway will automatically detect Django and start building

### Step 3: Add Database (Optional)

If you want to use Railway's PostgreSQL instead of Supabase:
1. In your project, click **"New"** → **"Database"** → **"PostgreSQL"**
2. Railway will automatically set `DATABASE_URL`
3. Your app will use this instead of Supabase database

### Step 4: Configure Environment Variables

In Railway project settings → **Variables**, add:

```env
DJANGO_SECRET_KEY=<generate-new-secret-key>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-app.railway.app
CSRF_TRUSTED_ORIGINS=https://your-app.railway.app

# Supabase (for storage only if using Railway DB)
SUPABASE_URL=https://wqoluwmdzljpvzimjiyr.supabase.co
SUPABASE_SERVICE_KEY=<your-service-key>
SUPABASE_ANON_KEY=<your-anon-key>
```

### Step 5: Deploy!

Railway will automatically:
- Install dependencies from `requirements.txt`
- Run migrations with `python manage.py migrate`
- Collect static files
- Start the server with Gunicorn

Your app will be live at: `https://your-app.railway.app`

### Important Notes

✅ **Database**: Use either Supabase OR Railway PostgreSQL  
✅ **Static Files**: Handled by WhiteNoise (already configured)  
✅ **Media Files**: Stored in Supabase Storage (already configured)  
✅ **Migrations**: Run automatically on each deployment  

### Troubleshooting

**Build fails?**
- Check Railway logs for errors
- Verify all required env variables are set

**Database connection errors?**
- If using Railway DB: Check `DATABASE_URL` is set
- If using Supabase: Verify DB credentials in env variables

**Static files not loading?**
- Run `python manage.py collectstatic` in Railway console
- Check `STATIC_ROOT` and `STATICFILES_DIRS` in settings.py

### What's Included

✅ `Procfile` - Railway deployment configuration  
✅ `railway.json` - Build and deploy settings  
✅ `requirements.txt` - All Python dependencies including gunicorn  
✅ `.gitignore` - Excludes sensitive files  
✅ `settings.py` - Production-ready with Railway support  
✅ WhiteNoise - Static file serving  
✅ Database URL parsing - Automatic Railway/Supabase detection  

### Next Steps

After deployment:
1. Visit your app URL
2. Create admin account: Railway console → `python manage.py createsuperuser`
3. Test all features
4. Update `ALLOWED_HOSTS` with your custom domain if needed

Need help? Check the full documentation in PROJECT_DOCUMENTATION.md
