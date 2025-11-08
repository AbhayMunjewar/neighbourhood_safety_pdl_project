# 🚀 QUICK START - Fix 404 Error

## The Issue
You're seeing: `Failed to load resource: api.js (404)`

This means the web server can't find the `api.js` file.

---

## ✅ Fix in 30 Seconds:

### 1. Open TWO Terminals in VS Code

**Terminal 1 - Backend (Flask):**
```bash
cd backend
python app.py
```
✅ Wait for: "Server running on http://localhost:3000"

**Terminal 2 - Frontend (Web Server):**
```bash
cd civicosafe\civicosafe
python -m http.server 5500
```
✅ Wait for: "Serving HTTP on 0.0.0.0 port 5500"

### 2. Open Browser
Go to: **`http://localhost:5500/login.html`**

---

## ⚠️ CRITICAL: Folder Location

The frontend server **MUST** run from `civicosafe\civicosafe` folder!

❌ **WRONG:**
```bash
cd civicosafe
python -m http.server 5500
```

✅ **CORRECT:**
```bash
cd civicosafe\civicosafe
python -m http.server 5500
```

---

## 🧪 Test if it's working:

1. Go to: `http://localhost:5500/test.html`
2. Open browser console (F12)
3. Should see: "✅ api.js loaded successfully!"

---

## Still Not Working?

**Option 1: Use VS Code Live Server**
1. Install "Live Server" extension in VS Code
2. Right-click `login.html` → "Open with Live Server"

**Option 2: Check file exists**
```bash
cd civicosafe\civicosafe
dir api.js
```
Should show the file exists.

**Option 3: Use full path**
Try opening: `file:///C:/Users/abhay/OneDrive/Desktop/civicosafe-v(2)/civicosafe/civicosafe/login.html`
(Replace with your actual path)

