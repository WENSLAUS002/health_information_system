from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# -------------------------------
# 1. Database Configuration
# -------------------------------
db_config = {
    'user': 'root',         
    'password': 'wenslaus001',  
    'host': 'localhost',
    'database': 'health_system'
}

# -------------------------------
# 2. Database Utility Functions
# -------------------------------

def get_db_connection():
    """Establishes and returns a new database connection."""
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

# -------------------------------
# 3. API Endpoints
# -------------------------------

@app.route('/programs', methods=['POST'])
def create_program():
    """
    Create a new health program.
    Example: {"program_name": "TB", "description": "Tuberculosis program"}
    """
    data = request.get_json()
    program_name = data.get('program_name')
    description = data.get('description')

    if not program_name:
        return jsonify({'error': 'Program name is required.'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO programs (program_name, description) 
            VALUES (%s, %s)
        """, (program_name, description))
        connection.commit()
        return jsonify({'message': f'Program "{program_name}" created successfully.'}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/clients', methods=['POST'])
def register_client():
    """
    Register a new client.
    Example: {"first_name": "John", "last_name": "Doe", "date_of_birth": "1990-01-01", "gender": "Male", "phone_number": "1234567890", "email": "john@example.com", "address": "123 Street"}
    """
    data = request.get_json()
    required_fields = ['first_name', 'last_name']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'First name and last name are required.'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO clients (first_name, last_name, date_of_birth, gender, phone_number, email, address)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data.get('first_name'),
            data.get('last_name'),
            data.get('date_of_birth'),
            data.get('gender'),
            data.get('phone_number'),
            data.get('email'),
            data.get('address')
        ))
        connection.commit()
        return jsonify({'message': 'Client registered successfully.'}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/enroll', methods=['POST'])
def enroll_client():
    """
    Enroll a client in one or more programs.
    Example: {"client_id": 1, "program_ids": [1, 2]}
    """
    data = request.get_json()
    client_id = data.get('client_id')
    program_ids = data.get('program_ids')

    if not client_id or not program_ids:
        return jsonify({'error': 'Client ID and Program IDs are required.'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        for program_id in program_ids:
            cursor.execute("""
                INSERT IGNORE INTO enrollments (client_id, program_id)
                VALUES (%s, %s)
            """, (client_id, program_id))
        connection.commit()
        return jsonify({'message': 'Client enrolled successfully.'}), 201
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/clients/search', methods=['GET'])
def search_clients():
    """
    Search for clients by name.
    Example: /clients/search?name=John
    """
    name_query = request.args.get('name')

    if not name_query:
        return jsonify({'error': 'Name query is required.'}), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT * FROM clients
            WHERE first_name LIKE %s OR last_name LIKE %s
        """, (f'%{name_query}%', f'%{name_query}%'))
        clients = cursor.fetchall()
        return jsonify(clients), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        connection.close()
        
# Route: General Appointment Booking
@app.route('/general_appointment', methods=['POST'])
def general_appointment():
    data = request.json
    name = data.get('name')
    email = data.get('email')

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO general_appointment (name, email) VALUES (%s, %s)"
    cursor.execute(sql, (name, email))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'General Appointment Booked Successfully'}), 201

# Route: Consultation Appointment
@app.route('/consultation_appointment', methods=['POST'])
def consultation_appointment():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """INSERT INTO consultation_appointment 
             (patient_name, email, phone, appointment_date, department, preferred_doctor) 
             VALUES (%s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (
        data.get('patient_name'),
        data.get('email'),
        data.get('phone'),
        data.get('appointment_date'),
        data.get('department'),
        data.get('preferred_doctor')
    ))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Consultation Appointment Scheduled Successfully'}), 201

# Route: Volunteer Application
@app.route('/volunteer_application', methods=['POST'])
def volunteer_application():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """INSERT INTO volunteer_application 
             (volunteer_name, volunteer_email, volunteer_phone, volunteer_area) 
             VALUES (%s, %s, %s, %s)"""
    cursor.execute(sql, (
        data.get('volunteer_name'),
        data.get('volunteer_email'),
        data.get('volunteer_phone'),
        data.get('volunteer_area')
    ))

@app.route('/clients/<int:client_id>', methods=['GET'])
def view_client_profile(client_id):
    """
    View a client's profile, including the programs they are enrolled in.
    Example: /clients/1
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Fetch client info
        cursor.execute("""
            SELECT * FROM clients WHERE client_id = %s
        """, (client_id,))
        client = cursor.fetchone()

        if not client:
            return jsonify({'error': 'Client not found.'}), 404

        # Fetch enrolled programs
        cursor.execute("""
            SELECT p.program_id, p.program_name, p.description
            FROM enrollments e
            JOIN programs p ON e.program_id = p.program_id
            WHERE e.client_id = %s
        """, (client_id,))
        programs = cursor.fetchall()

        client['enrolled_programs'] = programs
        return jsonify(client), 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500
    finally:
        cursor.close()
        connection.close()

# -------------------------------
# 4. Main
# -------------------------------

if __name__ == '__main__':
    app.run(debug=False)
