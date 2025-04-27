# Health Information System

## Overview
The Health Information System is a web application designed to manage clients, health programs, and various healthcare services such as appointments and volunteer applications. This system is being developed as part of an internship project and aims to streamline client registration, program management, and appointment scheduling for healthcare providers.

## Features
- **Client Management**: Register new clients with personal details and manage their health program enrollments.
- **Health Program Management**: Create and update health programs, ensuring that clients can enroll in the relevant programs.
- **Appointment Scheduling**: Manage different types of appointments, including consultation, surgeries, and general bookings.
- **Volunteer and Internship Applications**: Handle volunteer and internship requests for healthcare personnel.
- **Discharge and Admission Records**: Manage patient admission, discharge forms, and surgery consent documentation.
  
## Tech Stack
- **Frontend**: HTML, CSS (Responsive Design)
- **Backend**: Python, Flask (API integration with frontend)
- **Database**: MySQL (for client records, health programs, appointments)
- **Libraries**: 
    - `mysql-connector` for MySQL database interactions
    - `Flask` for Python backend web framework

## Database Design
The following key tables are part of the Health Information System:
1. **clients**: Stores personal information for clients.
2. **programs**: Stores details about health programs available.
3. **enrollments**: Tracks which clients are enrolled in which health programs.
4. **appointments**: Manages appointment bookings, including consultations, surgeries, and general bookings.
5. **volunteer_applications**: Stores information about volunteer applicants.
6. **internship_applications**: Manages internship applications for students or trainees.
7. **patient_admissions**: Manages patient admission records.
8. **discharge_forms**: Tracks patient discharge details.

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/health-information-system.git
cd health-information-system
