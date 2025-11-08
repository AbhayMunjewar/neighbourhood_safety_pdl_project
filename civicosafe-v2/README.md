# Civicosafe - Neighborhood Watch Application

A full-stack neighborhood watch and safety management application with integrated frontend and backend.

## Project Structure

```
.
├── backend/                 # Flask backend API
│   ├── database/           # Database configuration and initialization
│   ├── middleware/         # Authentication middleware
│   ├── routes/            # API route handlers (Blueprints)
│   ├── scripts/           # Database initialization scripts
│   ├── app.py             # Main Flask application
│   └── requirements.txt   # Python dependencies
│
└── civicosafe/
    └── civicosafe/        # Frontend HTML/CSS/JS files
        ├── *.html         # Frontend pages
        ├── api.js         # API communication utility
        └── styles.css     # Global styles
```

## Features

- ✅ User authentication (login/register)
- ✅ Incident reporting and management
- ✅ Community alerts system
- ✅ Member directory
- ✅ Dashboard with statistics
- ✅ Admin panel
- ✅ Dark mode support
- ✅ Responsive design

## Prerequisites

- Python 3.8 or higher
- pip (Python Package Manager)

## Setup Instructions

### 1. Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```bash
   python scripts/init_database.py
   ```
   This creates the SQLite database with all necessary tables.

5. Start the backend server:
   ```bash
   python app.py
   ```

   The backend API will run on `http://localhost:3000`

### 2. Frontend Setup

The frontend is static HTML/CSS/JS, so you can:

**Option A: Using a simple HTTP server (VS Code Live Server)**
- Install VS Code Live Server extension
- Right-click on any HTML file and select "Open with Live Server"
- The frontend will be served on `http://localhost:5500` (or similar)

**Option B: Using Python HTTP server**
```bash
cd civicosafe/civicosafe
python -m http.server 5500
```

**Option C: Using Node.js http-server (if you have Node.js)**
```bash
npm install -g http-server
cd civicosafe/civicosafe
http-server -p 5500
```

### 3. Configuration

The API endpoint is configured in `civicosafe/civicosafe/api.js`:
```javascript
const API_BASE_URL = 'http://localhost:3000/api';
```

If your backend runs on a different port, update this URL accordingly.

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Incidents
- `GET /api/incidents` - Get all incidents
- `GET /api/incidents/:id` - Get incident by ID
- `POST /api/incidents` - Create new incident
- `PATCH /api/incidents/:id/status` - Update incident status

### Alerts
- `GET /api/alerts` - Get all alerts (with optional filters)
- `POST /api/alerts` - Create new alert

### Members
- `GET /api/members` - Get all members (with optional search)
- `GET /api/members/:id` - Get member by ID
- `PATCH /api/members/:id` - Update member profile

### Dashboard
- `GET /api/dashboard/stats` - Get dashboard statistics
- `GET /api/dashboard/activity` - Get recent activity

## Database Schema

The application uses SQLite with the following tables:
- `users` - User accounts
- `incidents` - Reported incidents
- `alerts` - Community alerts
- `members` - Member profiles
- `emergency_contacts` - Emergency contact information

## Testing the Integration

1. Start the backend server (port 3000)
2. Start the frontend server (port 5500)
3. Open `http://localhost:5500/login.html` in your browser
4. Register a new account or login
5. Navigate through the application:
   - Dashboard - View statistics and recent activity
   - Incidents - Report new incidents
   - Alerts - View and create alerts
   - Members - Browse member directory

## Troubleshooting

### CORS Errors
If you see CORS errors, ensure:
- Backend CORS is configured correctly in `server.js`
- Frontend URL in backend `.env` matches your frontend URL
- Backend is running on the correct port

### Authentication Issues
- Check that JWT_SECRET is set in backend `.env`
- Verify token is being stored in localStorage
- Check browser console for API errors

### Database Issues
- Run `python scripts/init_database.py` to recreate database
- Check that `backend/database/civicosafe.db` file exists
- Verify Python SQLite3 module is working (usually built-in)

## Development

### Backend Development
- Flask runs in debug mode by default (auto-reload enabled)
- Logs are printed to console
- Database file: `backend/database/civicosafe.db`

### Frontend Development
- All API calls are handled in `api.js`
- Update API base URL in `api.js` if needed
- Check browser console for debugging

## Production Deployment

For production:
1. Update `JWT_SECRET` in backend `.env` to a secure random string
2. Set `FLASK_ENV=production` in backend `.env` or disable debug mode in `app.py`
3. Use a production WSGI server (gunicorn, uWSGI) instead of Flask's built-in server
4. Use a production database (PostgreSQL/MySQL) instead of SQLite
5. Update CORS settings to allow only your production domain
6. Serve frontend through a proper web server (nginx, Apache, etc.)

## License

© 2025 Civicosafe. All rights reserved.

