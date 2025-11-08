# Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Install Backend Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Initialize Database & Start Backend
```bash
# Initialize database
python scripts/init_database.py

# Start backend server (runs on port 3000)
python app.py
```

### Step 3: Start Frontend
Open the frontend folder (`civicosafe/civicosafe/`) in VS Code and use Live Server extension, OR:

```bash
cd civicosafe/civicosafe
python -m http.server 5500
```

Then open: `http://localhost:5500/login.html`

## ✅ Verify It's Working

1. Backend should show: `🚀 Server running on http://localhost:3000`
2. Frontend should open in browser at `http://localhost:5500`
3. Try registering a new account on the login page
4. After login, you'll be redirected to the dashboard with real data

## 🔧 Troubleshooting

**Backend won't start?**
- Make sure you're in the `backend` folder
- Run `pip install -r requirements.txt` first
- Make sure Python 3.8+ is installed
- Check if port 3000 is already in use

**Frontend can't connect to backend?**
- Make sure backend is running on port 3000
- Check browser console for CORS errors
- Verify `API_BASE_URL` in `civicosafe/civicosafe/api.js` is `http://localhost:3000/api`

**Database errors?**
- Run `python scripts/init_database.py` again to recreate database
- Check that `backend/database/civicosafe.db` file exists

## 📝 Default Test Credentials

After running `python scripts/init_database.py`, you can register any new user. The first user you create will be the first member!

For testing, register with:
- Email: test@example.com
- Password: test123456
- Name: Test User

## 🎯 Next Steps

1. ✅ Backend running
2. ✅ Frontend running
3. ✅ Register/Login works
4. ✅ Try reporting an incident
5. ✅ Check dashboard for statistics

Enjoy! 🎉

