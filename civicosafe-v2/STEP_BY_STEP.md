# 📖 Step-by-Step Guide to Run the Full Website

## Prerequisites Check

Before starting, make sure you have:
- ✅ Python installed (check: `python --version` should show Python 3.8+)
- ✅ VS Code open with your project folder
- ✅ Dependencies installed (if not, see Step 0)

---

## Step 0: First-Time Setup (Do This Once)

### 0.1 Install Python Dependencies

1. Open terminal in VS Code (`` Ctrl+` ``)
2. Type:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. Wait for installation to complete
4. You should see: "Successfully installed..." messages

### 0.2 Initialize Database

1. Still in the `backend` folder, type:
   ```bash
   python scripts/init_database.py
   ```
2. You should see: "✅ Database initialized successfully!"

---

## Step 1: Start Flask Backend Server

### 1.1 Open Terminal 1

1. In VS Code, click **Terminal** menu → **New Terminal**
   - OR press `` Ctrl+` `` (backtick key)
   - This opens Terminal 1

### 1.2 Navigate to Backend Folder

In Terminal 1, type:
```bash
cd backend
```

You should now see your prompt shows: `...\backend>`

### 1.3 Start Flask Server

In Terminal 1, type:
```bash
python app.py
```

### 1.4 Wait for Flask to Start

You should see output like:
```
🚀 Server running on http://localhost:3000
📡 API endpoint: http://localhost:3000/api
 * Running on http://0.0.0.0:3000
 * Debug mode: on
```

✅ **Keep this terminal open!** Flask must keep running.

---

## Step 2: Start Frontend Web Server

### 2.1 Open Terminal 2

1. In VS Code, **click the + button** in the terminal panel
   - OR press `` Ctrl+Shift+` `` (creates new terminal)
   - This opens Terminal 2

### 2.2 Navigate to Frontend Folder

In Terminal 2, type:
```bash
cd civicosafe\civicosafe
```

You should now see your prompt shows: `...\civicosafe\civicosafe>`

### 2.3 Start Web Server

In Terminal 2, type:
```bash
python -m http.server 5500
```

### 2.4 Wait for Server to Start

You should see output like:
```
Serving HTTP on 0.0.0.0 port 5500 (http://0.0.0.0:5500/)
```

✅ **Keep this terminal open!** Frontend server must keep running.

---

## Step 3: Open Website in Browser

### 3.1 Open Your Web Browser

Open any browser (Chrome, Firefox, Edge, etc.)

### 3.2 Go to Login Page

In the browser address bar, type:
```
http://localhost:5500/login.html
```

Press Enter.

### 3.3 What You Should See

✅ You should see:
- A login/signup page
- "Civicosafe" logo at the top
- Two tabs: "Login" and "Sign Up"
- A form with email and password fields

---

## Step 4: Test the Website

### 4.1 Create a Test Account

1. Click the **"Sign Up"** tab at the top
2. Fill in the form:
   - **Full Name**: Test User
   - **Email**: test@example.com
   - **Password**: test123456
   - **Confirm Password**: test123456
   - ✅ Check "I agree to the Terms of Service"
3. Click **"Create Account"** button

### 4.2 What Should Happen

✅ You should:
- See a success message: "Account created successfully!"
- Be automatically redirected to the dashboard
- See dashboard with statistics and recent activity

### 4.3 Explore the Website

You can now:
- ✅ View dashboard with real data
- ✅ Report incidents
- ✅ View alerts
- ✅ Browse members
- ✅ Navigate between pages using the header menu

---

## Step 5: Verify Everything is Working

### 5.1 Check Both Servers are Running

**Terminal 1** should show:
```
* Running on http://0.0.0.0:3000
```

**Terminal 2** should show:
```
Serving HTTP on 0.0.0.0 port 5500
```

### 5.2 Check Browser Console (Optional)

1. In browser, press **F12** (opens Developer Tools)
2. Click **Console** tab
3. You should see NO red errors
   - ✅ Favicon 404 is OK to ignore
   - ❌ Other errors mean something is wrong

### 5.3 Test API Connection

1. In browser, go to: `http://localhost:3000/api/health`
2. You should see: `{"status":"ok","message":"Civicosafe API is running"}`

---

## 📋 Quick Reference - What Should Be Running

| Terminal | Command | What It Shows | Status |
|----------|---------|---------------|--------|
| Terminal 1 | `python app.py` | "Running on http://0.0.0.0:3000" | ✅ Running |
| Terminal 2 | `python -m http.server 5500` | "Serving HTTP on port 5500" | ✅ Running |
| Browser | `http://localhost:5500/login.html` | Login page loads | ✅ Working |

---

## 🎯 All Available Pages

Once running, you can access these pages:

- **Login/Signup**: `http://localhost:5500/login.html`
- **Dashboard**: `http://localhost:5500/dashboard.html`
- **Report Incident**: `http://localhost:5500/incidents.html`
- **Alerts**: `http://localhost:5500/alerts.html`
- **Members**: `http://localhost:5500/members.html`
- **Emergency**: `http://localhost:5500/emergency.html`
- **Admin**: `http://localhost:5500/admin.html`
- **About**: `http://localhost:5500/about.html`

---

## ⚠️ Troubleshooting

### Problem: "Module not found" error
**Solution**: Run `pip install -r requirements.txt` in the backend folder

### Problem: "Port already in use"
**Solution**: 
- Close other programs using ports 3000 or 5500
- Or restart your computer

### Problem: Website shows "Failed to fetch"
**Solution**: 
- Make sure Terminal 1 (Flask) is still running
- Check it shows "Running on http://0.0.0.0:3000"

### Problem: "api.js not found" error
**Solution**: 
- Make sure Terminal 2 is running from `civicosafe\civicosafe` folder
- Check Terminal 2 shows "Serving HTTP on port 5500"

### Problem: Can't see login page
**Solution**: 
- Make sure you're opening: `http://localhost:5500/login.html`
- Not just: `http://localhost:5500/`

---

## ✅ Success Checklist

When everything is working correctly:

- [ ] Terminal 1 shows Flask is running
- [ ] Terminal 2 shows frontend server is running
- [ ] Browser opens login page successfully
- [ ] Can create a new account
- [ ] Can login with created account
- [ ] Dashboard loads with data
- [ ] Can navigate between pages
- [ ] Forms submit successfully
- [ ] No errors in browser console (except favicon)

---

## 🎉 You're Done!

Your full-stack website is now running! You can:
- Register new users
- Login
- Report incidents
- View dashboard statistics
- Browse all pages
- Everything is connected and working!

---

## 💡 Pro Tips

1. **Keep both terminals open** - Don't close them while using the website
2. **To stop servers**: Press `Ctrl+C` in each terminal
3. **To restart**: Just run the commands again in each terminal
4. **For faster startup**: Use the `start_all.bat` file I created (double-click it)

---

## Need Help?

If something doesn't work:
1. Check both terminals are running
2. Check browser console (F12) for errors
3. Make sure you followed every step exactly
4. Try restarting both servers

Happy coding! 🚀

