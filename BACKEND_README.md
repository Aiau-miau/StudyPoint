# StudyPoint Backend

A simple FastAPI backend for the StudyPoint educational platform with SQLite database and Docker support.

## Features

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLite** - Lightweight, file-based database
- **Docker** - Containerized deployment
- **CORS** - Configured for frontend communication
- **Authentication** - User registration and login with role-based access
- **Task Management** - Create, read, update, delete tasks
- **Submission Tracking** - Track student submissions and grades

## Quick Start

### Option 1: Using Docker (Recommended)

1. Make sure Docker is installed and running
2. Run the startup script:
   ```bash
   ./start.sh
   ```

### Option 2: Manual Setup

1. **Install Python dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Create data directory:**
   ```bash
   mkdir -p backend/data
   ```

3. **Initialize database:**
   ```bash
   cd backend
   python init_db.py
   ```

4. **Start the server:**
   ```bash
   python main.py
   ```

## API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - Login user
- `GET /api/users` - Get all users

### Tasks
- `POST /api/tasks` - Create new task
- `GET /api/tasks` - Get all tasks (optionally filter by grade)
- `DELETE /api/tasks/{task_id}` - Delete task

### Submissions
- `POST /api/submissions` - Create submission
- `GET /api/submissions` - Get all submissions
- `GET /api/submissions/student/{student_id}` - Get student submissions

## Sample Data

The database is initialized with sample data:

### Users
- **Admin**: username=`admin`, password=`admin123`
- **Student**: username=`student1`, password=`student123` (Student code: auto-generated)
- **Parent**: username=`parent1`, password=`parent123` (linked to student)

### Tasks
- Math estimation task for 4th grade
- Kazakh language words task for 4th grade

## Database Schema

### Users Table
- `id` - Primary key
- `username` - Unique username
- `password_hash` - SHA-256 hashed password
- `role` - student, parent, or admin
- `firstname`, `lastname` - User names
- `phone` - Phone number
- `grade` - Student grade (for students)
- `school` - School name (for students)
- `student_code` - Unique code (for students)
- `parent_student_code` - Student code (for parents)
- `created_at` - Registration timestamp

### Tasks Table
- `id` - Primary key
- `title` - Task title
- `description` - Task description
- `subject` - Subject (math, kazakh, etc.)
- `grade` - Target grade
- `difficulty` - easy, medium, hard
- `time_limit` - Time limit in minutes
- `file_name` - Uploaded file name
- `file_type` - react or json
- `file_content` - File content
- `upload_date` - Upload date
- `status` - active/inactive
- `created_at` - Creation timestamp

### Submissions Table
- `id` - Primary key
- `student_id` - Reference to user
- `task_id` - Reference to task
- `grade` - Final grade (0-100)
- `correct_answers` - Number of correct answers
- `total_questions` - Total questions
- `time_spent` - Time spent in seconds
- `submitted_at` - Submission timestamp

## Configuration

### Environment Variables
- `DATABASE_URL` - Database connection string (default: sqlite:///./data/study_point.db)

### CORS Settings
The API is configured to allow requests from:
- `http://localhost:3000`
- `http://localhost:5173` (Vue dev server)
- `http://127.0.0.1:5173`

## Development

### Running in Development Mode
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### API Documentation
Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Database Management
The SQLite database file is stored in `backend/data/study_point.db`. You can use any SQLite client to inspect or modify the data.

## Docker Commands

```bash
# Build and start all services
docker-compose up --build

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild specific service
docker-compose build backend
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   - Change ports in `docker-compose.yml` if 8000 or 5173 are occupied

2. **Database not found**
   - Make sure the `backend/data` directory exists
   - Run the initialization script: `python init_db.py`

3. **CORS errors**
   - Check that the frontend URL is in the CORS allowed origins
   - Make sure the frontend is running on the expected port

4. **Docker issues**
   - Make sure Docker is running
   - Try rebuilding: `docker-compose down && docker-compose up --build`

## Security Notes

- Passwords are hashed using SHA-256 (consider upgrading to bcrypt for production)
- No authentication tokens are implemented (add JWT for production)
- CORS is permissive for development (restrict for production)
- Database is file-based (consider PostgreSQL for production)

## Next Steps

For production deployment, consider:
1. Using a proper database (PostgreSQL)
2. Implementing JWT authentication
3. Adding input validation and sanitization
4. Setting up proper logging
5. Adding unit tests
6. Implementing rate limiting
7. Using environment variables for configuration


