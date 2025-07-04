from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import datetime
from typing import Dict, Any
import os

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=24)

jwt = JWTManager(app)
CORS(app)

# Database initialization
def init_db():
    conn = sqlite3.connect('feedback.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            role TEXT NOT NULL CHECK (role IN ('manager', 'employee')),
            manager_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (manager_id) REFERENCES users (id)
        )
    ''')
    
    # Create feedback table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            manager_id INTEGER NOT NULL,
            employee_id INTEGER NOT NULL,
            strengths TEXT NOT NULL,
            areas_to_improve TEXT NOT NULL,
            sentiment TEXT NOT NULL CHECK (sentiment IN ('positive', 'neutral', 'negative')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            acknowledged_at TIMESTAMP,
            FOREIGN KEY (manager_id) REFERENCES users (id),
            FOREIGN KEY (employee_id) REFERENCES users (id)
        )
    ''')
    
    # Insert demo data
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        # Create demo users
        manager_password = generate_password_hash('password123')
        employee_password = generate_password_hash('password123')
        
        cursor.execute('''
            INSERT INTO users (email, password_hash, name, role) 
            VALUES (?, ?, ?, ?)
        ''', ('manager@company.com', manager_password, 'John Manager', 'manager'))
        
        cursor.execute('''
            INSERT INTO users (email, password_hash, name, role, manager_id) 
            VALUES (?, ?, ?, ?, ?)
        ''', ('employee@company.com', employee_password, 'Jane Employee', 'employee', 1))
        
        cursor.execute('''
            INSERT INTO users (email, password_hash, name, role, manager_id) 
            VALUES (?, ?, ?, ?, ?)
        ''', ('employee2@company.com', employee_password, 'Bob Employee', 'employee', 1))
        
        # Create demo feedback
        cursor.execute('''
            INSERT INTO feedback (manager_id, employee_id, strengths, areas_to_improve, sentiment) 
            VALUES (?, ?, ?, ?, ?)
        ''', (1, 2, 'Excellent communication skills and always meets deadlines. Shows great initiative in team projects.', 
              'Could improve technical documentation and consider taking on more leadership responsibilities.', 'positive'))
        
        cursor.execute('''
            INSERT INTO feedback (manager_id, employee_id, strengths, areas_to_improve, sentiment) 
            VALUES (?, ?, ?, ?, ?)
        ''', (1, 3, 'Strong analytical skills and attention to detail. Great at problem-solving.', 
              'Could improve collaboration with remote team members and communication in meetings.', 'neutral'))
    
    conn.commit()
    conn.close()

# Helper function to get database connection
def get_db():
    return sqlite3.connect('feedback.db')

# Authentication routes
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, password_hash, name, role, manager_id FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    
    if not user or not check_password_hash(user[1], password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=user[0])
    
    return jsonify({
        'token': access_token,
        'user': {
            'id': user[0],
            'email': email,
            'name': user[2],
            'role': user[3],
            'manager_id': user[4]
        }
    })

@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, email, name, role, manager_id, created_at FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': user[0],
        'email': user[1],
        'name': user[2],
        'role': user[3],
        'manager_id': user[4],
        'created_at': user[5]
    })

# User routes
@app.route('/api/users/team', methods=['GET'])
@jwt_required()
def get_team_members():
    user_id = get_jwt_identity()
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if user is a manager
    cursor.execute('SELECT role FROM users WHERE id = ?', (user_id,))
    user_role = cursor.fetchone()[0]
    
    if user_role != 'manager':
        return jsonify({'error': 'Access denied'}), 403
    
    cursor.execute('''
        SELECT id, email, name, role, created_at 
        FROM users 
        WHERE manager_id = ? AND role = 'employee'
    ''', (user_id,))
    
    team_members = []
    for row in cursor.fetchall():
        team_members.append({
            'id': row[0],
            'email': row[1],
            'name': row[2],
            'role': row[3],
            'created_at': row[4]
        })
    
    conn.close()
    return jsonify(team_members)

# Feedback routes
@app.route('/api/feedback', methods=['GET'])
@jwt_required()
def get_feedback():
    user_id = get_jwt_identity()
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Check user role
    cursor.execute('SELECT role FROM users WHERE id = ?', (user_id,))
    user_role = cursor.fetchone()[0]
    
    if user_role == 'manager':
        cursor.execute('''
            SELECT f.id, f.manager_id, f.employee_id, f.strengths, f.areas_to_improve, 
                   f.sentiment, f.created_at, f.updated_at, f.acknowledged_at,
                   m.name as manager_name, e.name as employee_name
            FROM feedback f
            JOIN users m ON f.manager_id = m.id
            JOIN users e ON f.employee_id = e.id
            WHERE f.manager_id = ?
            ORDER BY f.created_at DESC
        ''', (user_id,))
    else:
        cursor.execute('''
            SELECT f.id, f.manager_id, f.employee_id, f.strengths, f.areas_to_improve, 
                   f.sentiment, f.created_at, f.updated_at, f.acknowledged_at,
                   m.name as manager_name, e.name as employee_name
            FROM feedback f
            JOIN users m ON f.manager_id = m.id
            JOIN users e ON f.employee_id = e.id
            WHERE f.employee_id = ?
            ORDER BY f.created_at DESC
        ''', (user_id,))
    
    feedback_list = []
    for row in cursor.fetchall():
        feedback_list.append({
            'id': row[0],
            'manager_id': row[1],
            'employee_id': row[2],
            'strengths': row[3],
            'areas_to_improve': row[4],
            'sentiment': row[5],
            'created_at': row[6],
            'updated_at': row[7],
            'acknowledged_at': row[8],
            'manager_name': row[9],
            'employee_name': row[10]
        })
    
    conn.close()
    return jsonify(feedback_list)

@app.route('/api/feedback', methods=['POST'])
@jwt_required()
def submit_feedback():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if user is a manager
    cursor.execute('SELECT role FROM users WHERE id = ?', (user_id,))
    user_role = cursor.fetchone()[0]
    
    if user_role != 'manager':
        return jsonify({'error': 'Access denied'}), 403
    
    # Validate employee is under this manager
    cursor.execute('SELECT id FROM users WHERE id = ? AND manager_id = ?', 
                   (data['employee_id'], user_id))
    if not cursor.fetchone():
        return jsonify({'error': 'Employee not found or not under your management'}), 404
    
    cursor.execute('''
        INSERT INTO feedback (manager_id, employee_id, strengths, areas_to_improve, sentiment)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, data['employee_id'], data['strengths'], data['areas_to_improve'], data['sentiment']))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Feedback submitted successfully'}), 201

@app.route('/api/feedback/<int:feedback_id>', methods=['PUT'])
@jwt_required()
def update_feedback(feedback_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if feedback belongs to this manager
    cursor.execute('SELECT manager_id FROM feedback WHERE id = ?', (feedback_id,))
    feedback = cursor.fetchone()
    
    if not feedback or feedback[0] != user_id:
        return jsonify({'error': 'Feedback not found or access denied'}), 404
    
    cursor.execute('''
        UPDATE feedback 
        SET strengths = ?, areas_to_improve = ?, sentiment = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (data['strengths'], data['areas_to_improve'], data['sentiment'], feedback_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Feedback updated successfully'})

@app.route('/api/feedback/<int:feedback_id>/acknowledge', methods=['POST'])
@jwt_required()
def acknowledge_feedback(feedback_id):
    user_id = get_jwt_identity()
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if feedback belongs to this employee
    cursor.execute('SELECT employee_id FROM feedback WHERE id = ?', (feedback_id,))
    feedback = cursor.fetchone()
    
    if not feedback or feedback[0] != user_id:
        return jsonify({'error': 'Feedback not found or access denied'}), 404
    
    cursor.execute('''
        UPDATE feedback 
        SET acknowledged_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (feedback_id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Feedback acknowledged successfully'})

# Dashboard routes
@app.route('/api/dashboard/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    user_id = get_jwt_identity()
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if user is a manager
    cursor.execute('SELECT role FROM users WHERE id = ?', (user_id,))
    user_role = cursor.fetchone()[0]
    
    if user_role != 'manager':
        return jsonify({'error': 'Access denied'}), 403
    
    # Get team members count
    cursor.execute('SELECT COUNT(*) FROM users WHERE manager_id = ?', (user_id,))
    total_team_members = cursor.fetchone()[0]
    
    # Get total feedback count
    cursor.execute('SELECT COUNT(*) FROM feedback WHERE manager_id = ?', (user_id,))
    total_feedback = cursor.fetchone()[0]
    
    # Get recent feedback count (last 30 days)
    cursor.execute('''
        SELECT COUNT(*) FROM feedback 
        WHERE manager_id = ? AND created_at > datetime('now', '-30 days')
    ''', (user_id,))
    recent_feedback = cursor.fetchone()[0]
    
    # Get sentiment distribution
    cursor.execute('''
        SELECT sentiment, COUNT(*) 
        FROM feedback 
        WHERE manager_id = ? 
        GROUP BY sentiment
    ''', (user_id,))
    
    sentiment_dist = {'positive': 0, 'neutral': 0, 'negative': 0}
    for row in cursor.fetchall():
        sentiment_dist[row[0]] = row[1]
    
    conn.close()
    
    return jsonify({
        'total_team_members': total_team_members,
        'total_feedback': total_feedback,
        'recent_feedback': recent_feedback,
        'sentiment_distribution': sentiment_dist
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)