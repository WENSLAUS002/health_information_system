import mysql.connector

# --------------------------
# 1. Database Connection Setup
# --------------------------
db_config = {
    'user': 'root',          
    'password': 'wenslaus001',  
    'host': 'localhost',     
    'raise_on_warnings': True
}

# --------------------------
# 2. Connect to MySQL Server
# --------------------------
try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    print("Connected to MySQL server successfully.")

    # --------------------------
    # 3. Create Database
    # --------------------------
    cursor.execute("CREATE DATABASE IF NOT EXISTS health_system")
    print("Database 'health_system' created or already exists.")

    # Select the database
    cursor.execute("USE health_system")

    # --------------------------
    # 4. Create Tables
    # --------------------------

    # 4.1 Create 'programs' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS programs (
        program_id INT AUTO_INCREMENT PRIMARY KEY,
        program_name VARCHAR(255) NOT NULL UNIQUE,
        description TEXT
    )
    """)

    # 4.2 Create 'clients' table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        client_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        date_of_birth DATE,
        gender ENUM('Male', 'Female', 'Other'),
        phone_number VARCHAR(20),
        email VARCHAR(100),
        address TEXT
    )
    """)

    # 4.3 Create 'enrollments' table (many-to-many relationship)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS enrollments (
        enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
        client_id INT,
        program_id INT,
        date_enrolled DATE DEFAULT CURRENT_DATE,
        FOREIGN KEY (client_id) REFERENCES clients(client_id) ON DELETE CASCADE,
        FOREIGN KEY (program_id) REFERENCES programs(program_id) ON DELETE CASCADE,
        UNIQUE(client_id, program_id)  -- Prevent duplicate enrollments
    )
    """)
    
    # 1. General Appointment Booking (unsure form)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS general_appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 2. Consultation Appointment Form
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS consultation_appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            appointment_date TEXT NOT NULL,
            department TEXT NOT NULL,
            doctor TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 3. Volunteer Application Form
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS volunteer_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            volunteer_name TEXT NOT NULL,
            volunteer_email TEXT NOT NULL,
            volunteer_phone TEXT NOT NULL,
            volunteer_area TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 4. Internship Application Form
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS internship_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            intern_name TEXT NOT NULL,
            intern_email TEXT NOT NULL,
            intern_phone TEXT NOT NULL,
            intern_department TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 5. Job Application Form
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_name TEXT NOT NULL,
            job_email TEXT NOT NULL,
            job_phone TEXT NOT NULL,
            job_position TEXT NOT NULL,
            resume_file BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 6. Patient Registration
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patient_registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reg_name TEXT NOT NULL,
            reg_gender TEXT,
            reg_age INTEGER,
            reg_contact TEXT,
            reg_address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 7. Patient Admission
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patient_admissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            adm_sickness TEXT,
            adm_description TEXT,
            adm_doctor TEXT,
            doctor_signature TEXT,
            admission_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 8. Surgery Form
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS surgery_forms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sur_name TEXT,
            sur_surgery_type TEXT,
            sur_doctor TEXT,
            sur_consent TEXT,
            doctor_signature TEXT,
            surgery_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 9. Discharge Form
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS discharge_forms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dis_name TEXT,
            dis_treatment TEXT,
            dis_followup TEXT,
            dis_next_appointment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    print("Tables created successfully.")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # --------------------------
    # 5. Close connection
    # --------------------------
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection closed.")
