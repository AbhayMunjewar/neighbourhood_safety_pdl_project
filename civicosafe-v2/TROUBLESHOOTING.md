# Troubleshooting Guide - 404 Errors

## Common Issue: 404 (NOT FOUND) Error

If you're seeing a 404 error, follow these steps:

### Step 1: Check if Flask Backend is Running

**In VS Code Terminal:**
1. Open terminal (`` Ctrl+` ``)
2. Navigate to backend:
   ```bash
   cd backend
   ```
3. Start Flask:
   ```bash
   python app.py
   ```

**You should see:**
```
🚀 Server running on http://localhost:3000
📡 API endpoint: http://localhost:3000/api
 * Running on http://0.0.0.0:3000
 * Debug mode: on
```

**If you see errors**, check:
- Did you run `pip install -r requirements.txt`?
- Is Python installed? Try `python --version`
- Is port 3000 already in use? Try changing the port in `app.py`

### Step 2: Test Backend is Working

Open your browser and go to:
- `http://localhost:3000/` - Should show API info
- `http://localhost:3000/api/health` - Should return `{"status":"ok",...}`

**If these don't work:**
- Backend is NOT running → Go back to Step 1
- Check firewall isn't blocking port 3000
- Try `http://127.0.0.1:3000` instead of `localhost`

### Step 3: Check Frontend is Loading Correctly

**In VS Code Terminal (new terminal):**
1. Navigate to frontend:
   ```bash
   cd civicosafe/civicosafe
   ```
2. Start a web server:
   ```bash
   python -m http.server 5500
   ```

3. Open browser to: `http://localhost:5500/login.html`

### Step 4: Check Browser Console

**Press F12 in your browser** and check:
- **Console tab**: Look for JavaScript errors
- **Network tab**: Look for failed requests (red entries)

**Common issues:**

#### Issue: `api.js` file not found
**Error:** `Failed to load resource: api.js (404)`

**Solution:**
- Make sure you're opening from `civicosafe/civicosafe/` folder
- Check that `api.js` file exists in `civicosafe/civicosafe/api.js`
- Use the correct path: `http://localhost:5500/login.html` (not `http://localhost:5500/index.html`)

#### Issue: API calls failing
**Error:** `Failed to fetch` or `CORS error`

**Solutions:**
1. **Backend not running:**
   - Make sure Flask is running on port 3000
   - Check terminal shows Flask server is active

2. **CORS issues:**
   - Check `backend/.env` has: `FRONTEND_URL=http://localhost:5500`
   - Or update in `app.py` line 13 if no `.env` file

3. **Wrong API URL:**
   - Check `civicosafe/civicosafe/api.js` line 2:
   - Should be: `const API_BASE_URL = 'http://localhost:3000/api';`

### Step 5: Verify Both Servers Running

You need **TWO terminals running**:

**Terminal 1 (Backend - Flask):**
```bash
cd backend
python app.py
# Should show: Server running on http://localhost:3000
```

**Terminal 2 (Frontend - HTTP Server):**
```bash
cd civicosafe/civicosafe
python -m http.server 5500
# Should show: Serving HTTP on 0.0.0.0 port 5500
```

### Quick Test Checklist

- [ ] Backend Flask running? → Check `http://localhost:3000/api/health`
- [ ] Frontend server running? → Check `http://localhost:5500/login.html`
- [ ] `api.js` file exists? → Check `civicosafe/civicosafe/api.js`
- [ ] Browser console shows no errors?
- [ ] Network tab shows successful API calls?

### Still Not Working?

1. **Clear browser cache:**
   - Press `Ctrl+Shift+Delete`
   - Clear cached images and files
   - Reload page with `Ctrl+F5`

2. **Check Python dependencies:**
   ```bash
   cd backend
   pip list
   # Should show: Flask, flask-cors, bcrypt, PyJWT, python-dotenv
   ```

3. **Reinitialize database:**
   ```bash
   cd backend
   python scripts/init_database.py
   ```

4. **Check file paths:**
   - All files should be in correct folders
   - No spaces in folder names
   - Backend folder contains: `app.py`, `routes/`, `database/`

### Need More Help?

Check the console output from both terminals:
- **Backend terminal** - Shows Flask requests and errors
- **Frontend terminal** - Shows HTTP requests
- **Browser console (F12)** - Shows JavaScript errors

Share these outputs for more specific help!

