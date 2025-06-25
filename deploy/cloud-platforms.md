# Cloud Platform Deployment Options

## Option A: Railway (Recommended for beginners)

**Pros**: Very easy, automatic deployments, built-in database
**Cost**: ~$5-15/month

### Steps:
1. Push code to GitHub
2. Connect Railway to your GitHub repo
3. Set environment variables in Railway dashboard
4. Deploy with one click

### Railway Setup:
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

## Option B: Render

**Pros**: Free tier available, easy setup
**Cost**: Free tier, then $7+/month

### Steps:
1. Create web services for frontend and backend
2. Create PostgreSQL database
3. Set environment variables
4. Auto-deploys from GitHub

## Option C: Vercel + PlanetScale

**Frontend**: Vercel (free)
**Backend**: Railway/Render
**Database**: PlanetScale (free tier)

### Frontend on Vercel:
```bash
npm install -g vercel
cd frontend
vercel
```

### Backend on Railway/Render
- Deploy backend separately
- Connect to PlanetScale database

## Option D: DigitalOcean App Platform

**Pros**: Managed platform, easy scaling
**Cost**: ~$12+/month

1. Create App Platform app
2. Connect GitHub repo
3. Configure services (frontend, backend, database)
4. Deploy