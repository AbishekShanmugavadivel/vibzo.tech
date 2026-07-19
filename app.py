import os
import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vibzo.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database and creates tables if they don't exist."""
    print(f"Initializing database at: {DB_PATH}")
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create quotes table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        service TEXT,
        message TEXT,
        budget TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create contacts table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create projects table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        project_type TEXT,
        budget TEXT,
        timeline TEXT,
        details TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create course_registrations table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS course_registrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        course_name TEXT,
        batch_preference TEXT,
        message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()
    print("Database check complete. All tables verified.")

import shutil

# Run database initialization
init_db()

# Create required directories if they don't exist
os.makedirs(os.path.join(app.root_path, 'templates'), exist_ok=True)
os.makedirs(os.path.join(app.root_path, 'static', 'css'), exist_ok=True)
os.makedirs(os.path.join(app.root_path, 'static', 'js'), exist_ok=True)
os.makedirs(os.path.join(app.root_path, 'static', 'images'), exist_ok=True)

# Copy generated mockup image on startup
source_img = r"C:\Users\Sakthi\.gemini\antigravity\brain\2b89b11e-6d8d-4885-a8a7-5c836ab61f6a\vibzo_hero_mockup_1784345049288.jpg"
dest_img = os.path.join(app.root_path, 'static', 'images', 'vibzo_hero_mockup.jpg')
if os.path.exists(source_img):
    try:
        shutil.copy(source_img, dest_img)
        print(f"Successfully copied mockup image to {dest_img}")
    except Exception as e:
        print(f"Error copying mockup image: {e}")
else:
    print(f"Mockup image source not found at {source_img}")

# Copy new 3D background image on startup
source_bg = r"C:\Users\Sakthi\.gemini\antigravity\brain\2b89b11e-6d8d-4885-a8a7-5c836ab61f6a\vibzo_3d_bg_1784345300110.jpg"
dest_bg = os.path.join(app.root_path, 'static', 'images', 'vibzo_3d_bg.jpg')
if os.path.exists(source_bg):
    try:
        shutil.copy(source_bg, dest_bg)
        print(f"Successfully copied 3D background image to {dest_bg}")
    except Exception as e:
        print(f"Error copying 3D background image: {e}")
else:
    print(f"3D background image source not found at {source_bg}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Fetch data from tables
    quotes = cursor.execute('SELECT * FROM quotes ORDER BY created_at DESC').fetchall()
    contacts = cursor.execute('SELECT * FROM contacts ORDER BY created_at DESC').fetchall()
    projects = cursor.execute('SELECT * FROM projects ORDER BY created_at DESC').fetchall()
    courses = cursor.execute('SELECT * FROM course_registrations ORDER BY created_at DESC').fetchall()
    
    conn.close()
    return render_template('admin.html', quotes=quotes, contacts=contacts, projects=projects, courses=courses)

@app.route('/api/quote', methods=['POST'])
def save_quote():
    try:
        data = request.json or request.form
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone', '')
        service = data.get('service', '')
        message = data.get('message', '')
        budget = data.get('budget', '')
        
        if not name or not email:
            return jsonify({'status': 'error', 'message': 'Name and Email are required fields.'}), 400
            
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO quotes (name, email, phone, service, message, budget) VALUES (?, ?, ?, ?, ?, ?)',
            (name, email, phone, service, message, budget)
        )
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success', 'message': 'Quote request received successfully!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/contact', methods=['POST'])
def save_contact():
    try:
        data = request.json or request.form
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone', '')
        message = data.get('message', '')
        
        if not name or not email or not message:
            return jsonify({'status': 'error', 'message': 'Name, Email, and Message are required fields.'}), 400
            
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO contacts (name, email, phone, message) VALUES (?, ?, ?, ?)',
            (name, email, phone, message)
        )
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success', 'message': 'Message sent successfully!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/project', methods=['POST'])
def save_project():
    try:
        data = request.json or request.form
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone', '')
        project_type = data.get('project_type', '')
        budget = data.get('budget', '')
        timeline = data.get('timeline', '')
        details = data.get('details', '')
        
        if not name or not email:
            return jsonify({'status': 'error', 'message': 'Name and Email are required.'}), 400
            
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO projects (name, email, phone, project_type, budget, timeline, details) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (name, email, phone, project_type, budget, timeline, details)
        )
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success', 'message': 'Project details submitted successfully!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/course', methods=['POST'])
def save_course():
    try:
        data = request.json or request.form
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone', '')
        course_name = data.get('course_name', '')
        batch_preference = data.get('batch_preference', '')
        message = data.get('message', '')
        
        if not name or not email or not course_name:
            return jsonify({'status': 'error', 'message': 'Name, Email, and Course Selection are required.'}), 400
            
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO course_registrations (name, email, phone, course_name, batch_preference, message) VALUES (?, ?, ?, ?, ?, ?)',
            (name, email, phone, course_name, batch_preference, message)
        )
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success', 'message': 'Course registration request submitted successfully!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
