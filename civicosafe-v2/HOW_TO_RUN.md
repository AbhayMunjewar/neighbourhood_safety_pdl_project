# 🚀 How to Run the Civicosafe Application

## Quick Start Guide

### Prerequisites

- Python 3.7 or higher installed
- Terminal/Command Prompt access

---

## Step-by-Step Instructions

### ✅ Step 1: Install Python Dependencies (First Time Only)

1. Open Terminal/Command Prompt
2. Navigate to the project folder
3. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
4. Wait for installation to complete

---

### ✅ Step 2: Start Flask Backend Server (Terminal 1)

1. In the `backend` folder, run:

   ```bash
   cd backend
   python app.py
   ```

   OR use the run script:

   ```bash
   python run.py
   ```

2. **Wait** until you see:

   ```
   🚀 Server running on http://localhost:3000
   📡 API endpoint: http://localhost:3000/api
   ```

3. **Leave this terminal running** - Don't close it!

---

### ✅ Step 3: Start Frontend Server (Terminal 2)

1. **Open a NEW terminal/command prompt window**

2. Navigate to the frontend folder:

   ```bash
   cd civicosafe/civicosafe
   ```

3. Start the HTTP server:

   ```bash
   python -m http.server 5500
   ```

   On Mac/Linux, if that doesn't work, try:

   ```bash
   python3 -m http.server 5500
   ```

4. **Wait** until you see:

   ```
   Serving HTTP on 0.0.0.0 port 5500
   ```

5. **Leave this terminal running** - Don't close it!

---

### ✅ Step 4: Open Website in Browser

Open your web browser and navigate to:

```
http://localhost:5500/login.html
```

Or start from the index:

```
http://localhost:5500/index.html
```

---

## 📋 Quick Checklist

Before using the app, verify:

- [ ] **Terminal 1**: Flask backend running (`http://localhost:3000`)
- [ ] **Terminal 2**: Frontend server running (`http://localhost:5500`)
- [ ] **Browser**: Open to `http://localhost:5500/login.html`

---

## 🎯 Available Pages

Once everything is running, you can access:

### Main Pages:

- **Login/Signup**: `http://localhost:5500/login.html` ⭐ Start here!
- **Dashboard**: `http://localhost:5500/dashboard.html`
- **Report Incident**: `http://localhost:5500/incidents.html`
- **Community Alerts**: `http://localhost:5500/alerts.html`
- **Members Directory**: `http://localhost:5500/members.html`
- **Emergency Contacts**: `http://localhost:5500/emergency.html`
- **Admin Panel**: `http://localhost:5500/admin.html`
- **About Us**: `http://localhost:5500/about.html`

### Backend API Endpoints:

- **API Health Check**: `http://localhost:3000/api/health`
- **API Info**: `http://localhost:3000/`

---

## 🧪 Testing the Application

### Test Registration and Login:

1. **Go to**: `http://localhost:5500/login.html`

2. **Test Resident Registration**:

   - Click "Sign Up" tab
   - Fill in:
     - Name: Test User
     - Email: test@example.com
     - Password: test123456
     - Confirm Password: test123456
   - Check "I agree to Terms"
   - Click "Create Account"

3. **Test Login**:

   - Click "Login" tab
   - Select "Resident" from "Login As" dropdown
   - Enter email: test@example.com
   - Enter password: test123456
   - Click "Sign In"
   - Should redirect to Dashboard

4. **Test Admin Login** (if you have admin account):
   - Select "Admin" from "Login As" dropdown
   - Enter admin credentials
   - Should redirect to Admin Panel

---

## ⚠️ Troubleshooting

### "Connection refused" or "Failed to fetch" Error

**Problem**: Frontend can't connect to backend

**Solutions**:

1. ✅ Make sure Flask backend is running (Terminal 1)
2. ✅ Check Terminal 1 shows: "Running on http://127.0.0.1:3000"
3. ✅ Verify CORS is configured (should be fixed in our updates)
4. ✅ Check both servers are on correct ports (3000 for backend, 5500 for frontend)

### CORS Error (Fixed!)

**Problem**: "Access to fetch blocked by CORS policy"

**Solution**: This should now be fixed! If you still see it:

1. Make sure you're using the updated `app.py` and `auth.py` files
2. Restart the Flask backend server
3. Clear browser cache and reload

### "api.js not found" (404 Error)

**Problem**: Frontend can't find the JavaScript file

**Solutions**:

1. ✅ Make sure frontend server is running from `civicosafe/civicosafe` folder
2. ✅ Check Terminal 2 shows: "Serving HTTP on port 5500"
3. ✅ Verify you're accessing `http://localhost:5500/login.html` (not just `/`)

### Port Already in Use

**Problem**: Port 3000 or 5500 is already taken

**Solutions**:

1. Close other programs using these ports
2. Change ports:
   - Backend: Edit `backend/app.py` and change port 3000 to another port
   - Frontend: Use `python -m http.server 5501` (or another port)

### Python Command Not Found

**Problem**: `python` command doesn't work

**Solutions**:

- **Windows**: Use `py` instead of `python`
- **Mac/Linux**: Use `python3` instead of `python`
- **Mac**: You might need to install Python from python.org

### Module Not Found (Backend)

**Problem**: Missing Python packages

**Solutions**:

```bash
cd backend
pip install -r requirements.txt
```

If pip doesn't work, try:

```bash
pip3 install -r requirements.txt
```

---

## 💡 Pro Tips

### Make It Easier Next Time

#### Option 1: Use the Start Scripts

**Windows** - Double-click `start_all.bat`

**Mac/Linux** - Run `./start_all.sh`

#### Option 2: Create VS Code Tasks

1. Create `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Start Backend",
      "type": "shell",
      "command": "cd backend && python app.py",
      "isBackground": true
    },
    {
      "label": "Start Frontend",
      "type": "shell",
      "command": "cd civicosafe/civicosafe && python -m http.server 5500",
      "isBackground": true
    },
    {
      "label": "Start Both",
      "dependsOn": ["Start Backend", "Start Frontend"]
    }
  ]
}
```

2. Press `Ctrl+Shift+P` → "Run Task" → "Start Both"

---

## 🎉 Success Indicators

When everything works correctly, you should see:

- ✅ Login page loads without errors
- ✅ Can register new accounts (Residents)
- ✅ Can login as Resident or Admin
- ✅ Dashboard shows real data from backend
- ✅ Can report incidents without CORS errors
- ✅ All buttons are functional
- ✅ About page displays beautifully
- ✅ No console errors in browser

---

## 📝 Important Notes

### New Features Added:

1. **Separate Login Options**:

   - Select "Resident" or "Admin" when logging in
   - Different redirects based on role

2. **Functional Buttons**:

   - Admin panel: All approval, export, and settings buttons work
   - Alerts page: Create new alert button works
   - Incidents page: Save as draft functionality added

3. **Redesigned About Page**:

   - Modern UI with sections for features, mission, team, and contact

4. **CORS Fix**:
   - Preflight requests now handled correctly
   - No more redirect errors

---

## 🆘 Still Having Issues?

1. **Check both terminals** - Make sure both servers are running
2. **Check browser console** - Press F12, look for error messages
3. **Verify file paths** - Make sure you're in the right directories
4. **Restart everything** - Close terminals, restart servers

---

**Happy coding! 🚀**
