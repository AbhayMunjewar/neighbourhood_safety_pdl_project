from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory
from flask_mysqldb import MySQL
import bcrypt
import os
from config import Config

app = Flask(__name__, template_folder='../frontend', static_folder='../frontend')
app.config.from_object(Config)

mysql = MySQL(app)

# Import routes
from routes import auth, dashboard, incidents

# Register blueprints
app.register_blueprint(auth.bp)
app.register_blueprint(dashboard.bp)
app.register_blueprint(incidents.bp)

# Serve static files
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)