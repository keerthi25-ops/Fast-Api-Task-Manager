# Task Manager API

A simple Task Manager web application built with FastAPI backend and basic HTML/CSS/JavaScript frontend.

## Features

- User registration and authentication with JWT tokens
- Password hashing with bcrypt
- CRUD operations for tasks
- Users can only access their own tasks
- Basic filtering by completion status
- Pagination support
- SQLite database (easily configurable for PostgreSQL)

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, Pydantic
- **Database**: SQLite (configurable)
- **Authentication**: JWT tokens with python-jose
- **Password Hashing**: bcrypt with passlib
- **Frontend**: Plain HTML, CSS, JavaScript

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd task-manager
```

2. Create a virtual environment:
```bash
python -m venv env
# On Windows:
env\Scripts\activate
# On macOS/Linux:
source env/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Run the application:
```bash
uvicorn backend.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **API Docs**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative Docs**: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token

### Tasks
- `POST /tasks/` - Create a new task
- `GET /tasks/` - Get all user's tasks (with optional filtering)
- `GET /tasks/{id}` - Get a specific task
- `PUT /tasks/{id}` - Update a task
- `DELETE /tasks/{id}` - Delete a task

## Environment Variables

Create a `.env` file with:

```env
SECRET_KEY=your-secret-key-here-change-this-in-production
DATABASE_URL=sqlite:///./taskmanager.db
```

## Running Tests

```bash
pytest backend/app/tests/
```

## Deployment

### Local Development
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### Production
Use a production ASGI server like Gunicorn with Uvicorn workers:

```bash
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Frontend

The basic frontend is available at `backend/app/frontend/index.html`. Simply open this file in a web browser to use the application.

## Project Structure

```
task-manager/
├── backend/
│   ├── main.py                 # FastAPI application
│   └── app/
│       ├── __init__.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py       # Settings and configuration
│       │   └── security.py     # JWT and password utilities
│       ├── db/
│       │   ├── __init__.py
│       │   └── database.py     # Database connection
│       ├── models/
│       │   ├── __init__.py
│       │   ├── user.py         # User model
│       │   └── task.py         # Task model
│       ├── routers/
│       │   ├── __init__.py
│       │   ├── auth.py         # Authentication endpoints
│       │   └── tasks.py        # Task CRUD endpoints
│       ├── schemas/
│       │   ├── __init__.py
│       │   ├── user.py         # User Pydantic schemas
│       │   └── task.py         # Task Pydantic schemas
│       └── tests/
│           ├── __init__.py
│           ├── conftest.py     # Test configuration
│           ├── test_auth.py    # Authentication tests
│           └── test_tasks.py   # Task tests
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## Database Schema

### Users Table
- id: Primary key
- username: Unique username
- email: Unique email
- hashed_password: Bcrypt hashed password

### Tasks Table
- id: Primary key
- title: Task title
- description: Task description (optional)
- completed: Boolean completion status
- created_at: Creation timestamp
- updated_at: Last update timestamp
- owner_id: Foreign key to users table

## Security Features

- JWT token-based authentication
- Password hashing with bcrypt
- User isolation (users can only access their own tasks)
- CORS middleware configured
- Input validation with Pydantic

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).