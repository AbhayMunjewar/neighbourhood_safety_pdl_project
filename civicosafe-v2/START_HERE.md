# 🔥 QUICK FIX: 404 Error on api.js

## The Problem
You're getting `Failed to load resource: api.js (404)` because the web server isn't running from the correct folder.

## ✅ Solution - Follow These Steps EXACTLY:

### Step 1: Start Flask Backend (Terminal 1)

1. Open VS Code
2. Press `` Ctrl+` `` (backtick) to open terminal
3. Type these commands:
   ```bash
   cd backend
   python app.py
   ```
4. **WAIT** until you see:
   ```
   🚀 Server running on http://localhost:3000
   * Running on http://0.0.0.0:3000
   ```

### Step 2: Start Frontend Server (Terminal 2)

1. **Click the + button** in the terminal panel (or press `Ctrl+Shift+` ` to create new terminal)
2. Type these commands:
   ```bash
   cd civicosafe\civicosafe
   python -m http.server 5500
   ```
3. **IMPORTANT:** Make sure you're in `civicosafe\civicosafe` folder (two levels deep!)
4. You should see:
   ```
   Serving HTTP on 0.0.0.0 port 5500
   ```

### Step 3: Open Browser

Open: `http://localhost:5500/login.html`

**NOT** `http://localhost:5500/` (that's just the index)
**NOT** `http://localhost:5500/civicosafe/civicosafe/login.html`

### Step 4: Verify api.js is Loading

1. Press `F12` in browser (opens Developer Tools)
2. Click **Network** tab
3. Refresh page (`F5`)
4. Look for `api.js` - should show status `200` (not `404`)

---

## ⚠️ Common Mistakes:

### ❌ Wrong: Running server from wrong folder
```bash
cd civicosafe
python -m http.server 5500
# WRONG - api.js won't be found!
```

### ✅ Correct: Running from the folder WITH api.js
```bash
cd civicosafe\civicosafe
python -m http.server 5500
# CORRECT - api.js is in this folder!
```

### ❌ Wrong: Opening wrong URL
- `http://localhost:5500/` ❌
- `http://localhost:5500/index.html` ❌

### ✅ Correct: Opening the login page
- `http://localhost:5500/login.html` ✅

---

## 🔍 How to Check if You're in the Right Folder:

When you run `cd civicosafe\civicosafe`, then `python -m http.server 5500`:
- The server should list files it's serving
- You should see `api.js` in that list

If you don't see `api.js` listed → you're in the wrong folder!

---

## 📋 Quick Checklist:

- [ ] Flask backend running on port 3000
- [ ] Frontend server running on port 5500
- [ ] Frontend server is running from `civicosafe\civicosafe` folder
- [ ] Opening `http://localhost:5500/login.html` (not just localhost:5500)
- [ ] Browser console (F12) shows `api.js` loaded with status 200

---

## 🆘 Still Getting 404?

1. **Double-check the folder:**
   ```bash
   cd civicosafe\civicosafe
   dir api.js
   # Should show: api.js file exists
   ```

2. **Verify Flask is running:**
   - Open: `http://localhost:3000/api/health`
   - Should see: `{"status":"ok",...}`

3. **Check browser console (F12):**
   - Look at the exact URL it's trying to load
   - Should be: `http://localhost:5500/api.js`
   - If it shows a different path, the HTML is referencing it wrong

4. **Hard refresh:**
   - Press `Ctrl+Shift+R` or `Ctrl+F5` to clear cache

---

## ✅ When It Works:

You should see:
- Login page loads without errors
- Browser console (F12) shows no red errors
- Network tab shows `api.js` with status `200`
- Can type email/password in the form

Then try registering a new account!

