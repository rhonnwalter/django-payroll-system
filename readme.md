A Django-based payroll management system that calculates employee pay, including overtime, with clean and professional configuration.

Features

-Employee management with unique IDs and usernames
-Payroll records with hours worked and overtime
-Automatic overtime rate calculation (1.25× hourly rate)
-Precision rounding for pay totals
-Secure environment variable handling via .env

1. Clone the Repository
   git clone https://github.com/your-username/django-payroll-system.git cd django-payroll-system

2. Install Dependencies
    pip install pipenv
    pipenv install

3. Activate the Virtual Environment
    pipenv shell

4. Configure Environment Variables
    Create a .env file in the project root:
    DJANGO_SECRET_KEY=your-secret-key
    DEBUG=True
    DATABASE_URL=sqlite:///db.sqlite3

5. Run Migrations
    python manage.py migrate

6. Start the Development Server
    python manage.py runserver
