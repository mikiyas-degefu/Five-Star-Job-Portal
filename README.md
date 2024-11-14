# Centralized Job Portal System

A centralized job portal system designed to connect job seekers with companies. This platform provides a company admin panel for managing job postings, tracking applicants, and more. It aims to simplify the job-seeking and recruitment process by offering a robust, easy-to-use interface for both applicants and company administrators.

## Features

- **Job Seekers**: Browse job listings, apply for positions, and track application status.
- **Company Admin Panel**: Manage job postings, review applications, track applicant status, and communicate with potential hires.
- **Responsive Design**: Works seamlessly on both desktop and mobile devices.
- **Real-time Interactions**: Enhanced with AJAX for smooth and dynamic user experiences.
- **User Authentication**: Secure login system for both job seekers and company administrators.

## Technologies

This project is built with the following technologies:

- **Django**: Used as the primary web framework for building backend functionalities.
- **Django REST Framework**: Provides the API to manage and retrieve job-related data.
- **jQuery**: Enhances interactivity and real-time interactions with AJAX.
- **Django Templates**: Used to create and render dynamic HTML pages.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

- **Python** (3.x)
- **Django** (latest version)
- **Django REST Framework**
- **jQuery**

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/MikiyasMebrate/Five-Star-Job-Portal.git
2. Navigate to the project directory:

   ```bash
   cd Five-Star-Job-Portal


3. Create a virtual environment:

   ```bash
   python -m venv venv

4. Create a virtual environment:

   ```bash
   python -m venv venv

5. Activate the virtual environment:
- On Windows:
   ``` bash
   venv\Scripts\activate

- On MacOS/Linux:
   ``` bash
   source venv/bin/activate

6. Install required packages:
   ```bash
   pip install -r requirements.txt

7. Run database migrations:
   ```bash
   python manage.py migrate

8. Create a superuser to access the admin panel:
   ```bash
   python manage.py createsuperuser

9. Start the development server:
   ```bash
   python manage.py runserver


## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.
