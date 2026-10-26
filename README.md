# Employee Management System

A Django application for maintaining employee records. It provides account sign-up and login, an employee directory, and create, read, update, and delete operations.

## Features

- Sign up, sign in, and sign out
- Create, list, update, and delete employee records
- Employee details include name, joining date, age, contact information, education, skills, salary, and experience
- Form validation for employee fields, including non-negative salary and experience
- Responsive Bootstrap interface

## Requirements

- Python 3.10 or newer
- MySQL Server
- A MySQL client build environment if a compatible `mysqlclient` wheel is not available

## Setup

Open a terminal in the project root and create/activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the project dependencies:

```powershell
python -m pip install -r requirements.txt
```

Create a local `.env` file from the example:

```powershell
Copy-Item .env.example .env
```

Set the database connection values in `.env`:

```dotenv
DB_NAME=employee_management
DB_USER=root
DB_PASSWORD=your-mysql-password
DB_HOST=localhost
DB_PORT=3306
```

The application reads these values during Django settings initialization. `.env` is ignored by Git; do not commit credentials.

Create the database specified by `DB_NAME` in MySQL, then apply the migrations:

```powershell
python manage.py migrate
```

Optionally create an administrator account:

```powershell
python manage.py createsuperuser
```

Run the development server:

```powershell
python manage.py runserver
```

Open <http://127.0.0.1:8000/> in a browser.

## Tests and checks

```powershell
python manage.py check
python manage.py test
```

The test database uses the database backend configured for the project. The configured MySQL account must be able to create and drop test databases, or tests can be run with a local test-specific settings configuration.
