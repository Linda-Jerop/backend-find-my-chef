# Find My Chef Backend - Deployment Guide

## Quick Deploy to Render

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Add API routes and Render deployment config"
   git push origin main
   ```

2. **Deploy on Render:**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repo: `Linda-Jerop/backend-find-my-chef`
   - Render will auto-detect `render.yaml` and create:
     - PostgreSQL database
     - Web service with auto-generated SECRET_KEY
   - Click "Apply"

3. **Update Frontend:**
   Add your Render backend URL to frontend:
   ```javascript
   const API_URL = "https://find-my-chef-api.onrender.com"
   ```

## Environment Variables (Auto-configured in render.yaml)

- `DATABASE_URL` - Auto-provided by Render PostgreSQL
- `SECRET_KEY` - Auto-generated on first deploy
- `CORS_ORIGINS` - Includes your frontend URL

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user (chef or client)
- `POST /api/auth/login` - Login with email/password
- `POST /api/auth/google` - Google login (TODO)

### Chefs
- `GET /api/chefs` - List all chefs (with filters: cuisine, location, max_price, search)
- `GET /api/chefs/{id}` - Get specific chef
- `PUT /api/chefs/{id}` - Update chef profile (auth required)

### Clients
- `GET /api/clients/{id}` - Get client profile
- `PUT /api/clients/{id}` - Update client profile (auth required)

### Bookings
- `POST /api/bookings` - Create new booking (client only)
- `GET /api/bookings` - List user's bookings (filter by status)
- `PATCH /api/bookings/{id}` - Update booking status (chef only)

### Health Check
- `GET /api/health` - Check API status

## Local Development

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Run server
python run.py
```

API available at: http://localhost:8000
Docs at: http://localhost:8000/api/docs

## Database

Development uses SQLite. Production (Render) automatically uses PostgreSQL.

To initialize database: `python init_db.py`
