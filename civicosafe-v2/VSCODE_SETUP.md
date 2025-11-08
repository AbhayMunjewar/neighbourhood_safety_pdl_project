# Running Flask Backend in VS Code

## Quick Setup Guide

### Step 1: Install Python Extension in VS Code

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X or Cmd+Shift+X)
3. Search for "Python" by Microsoft
4. Click Install

### Step 2: Set Up Python Interpreter

1. Open the `backend` folder in VS Code
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
3. Type "Python: Select Interpreter"
4. Choose your Python 3.8+ interpreter
5. If you don't see one, install Python from [python.org](https://www.python.org/downloads/)

### Step 3: Install Dependencies

1. Open the integrated terminal in VS Code:
   - Press `` Ctrl+` `` (backtick) or go to `Terminal > New Terminal`
2. Navigate to backend folder:
   ```bash
   cd backend
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Step 4: Initialize Database

In the same terminal:
```bash
python scripts/init_database.py
```

### Step 5: Run the Flask App

You have **3 ways** to run the Flask backend:

## Method 1: Using VS Code Debugger (Recommended)

1. Open `backend/app.py` in VS Code
2. Press `F5` or click the "Run and Debug" icon in the sidebar
3. Select "Python: Flask" from the dropdown
4. The Flask server will start and you'll see output in the Debug Console

**Benefits:**
- Can set breakpoints to debug
- Auto-reloads on file changes
- Easy to stop/restart

## Method 2: Using Integrated Terminal

1. Open terminal in VS Code (`` Ctrl+` ``)
2. Navigate to backend:
   ```bash
   cd backend
   ```
3. Run:
   ```bash
   python app.py
   ```

## Method 3: Using Flask CLI

1. Open terminal in VS Code
2. Navigate to backend:
   ```bash
   cd backend
   ```
3. Set environment variables:
   ```bash
   # Windows PowerShell:
   $env:FLASK_APP="app.py"
   $env:FLASK_ENV="development"
   
   # Windows CMD:
   set FLASK_APP=app.py
   set FLASK_ENV=development
   
   # macOS/Linux:
   export FLASK_APP=app.py
   export FLASK_ENV=development
   ```
4. Run Flask:
   ```bash
   flask run --host=0.0.0.0 --port=3000
   ```

## Verifying It's Running

Once started, you should see:
```
🚀 Server running on http://localhost:3000
📡 API endpoint: http://localhost:3000/api
 * Running on http://0.0.0.0:3000
 * Debug mode: on
```

## Setting Breakpoints for Debugging

1. Click in the left margin of `app.py` or any route file to set a breakpoint (red dot)
2. Press `F5` to start debugging
3. When the code hits the breakpoint, execution will pause
4. You can:
   - Inspect variables in the Variables panel
   - Step through code (F10 for step over, F11 for step into)
   - Continue execution (F5)

## Troubleshooting

### "Python extension not found"
- Install the Python extension from VS Code marketplace
- Restart VS Code after installation

### "Module not found" errors
- Make sure you're in the `backend` directory
- Run `pip install -r requirements.txt`
- Check that your Python interpreter is selected correctly

### Port 3000 already in use
- Stop any other Flask/Node.js processes using port 3000
- Or change the port in `app.py`: `port = int(os.getenv('PORT', 3001))`

### Database errors
- Make sure you ran `python scripts/init_database.py`
- Check that `backend/database/civicosafe.db` exists

## Recommended VS Code Extensions

1. **Python** - by Microsoft (Required)
2. **Python Docstring Generator** - for better documentation
3. **Python Indent** - for proper indentation
4. **Auto Rename Tag** - helpful for HTML editing

## Running Both Frontend and Backend

To run both simultaneously in VS Code:

1. **Backend Terminal:**
   - Open terminal 1: `cd backend && python app.py`

2. **Frontend Terminal:**
   - Open terminal 2: Right-click terminal panel → "New Terminal"
   - `cd civicosafe/civicosafe`
   - Use Live Server extension or `python -m http.server 5500`

Or use VS Code's multi-root workspace feature to manage both together!

