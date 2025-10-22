from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import os
from jose import JWTError, jwt
import bcrypt
from dotenv import load_dotenv
import uvicorn
import random

load_dotenv()

# Database setup
DATABASE_URL = "sqlite:///./data/study_point.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# JWT Security
security = HTTPBearer()

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String)  # student, parent, admin
    firstname = Column(String)
    lastname = Column(String)
    phone = Column(String)
    grade = Column(String, nullable=True)  # for students
    school = Column(String, nullable=True)  # for students
    student_code = Column(String, nullable=True)  # for students
    parent_student_code = Column(String, nullable=True)  # for parents
    created_at = Column(DateTime, default=datetime.utcnow)

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    subject = Column(String)
    grade = Column(String)
    difficulty = Column(String)
    time_limit = Column(Integer)
    file_name = Column(String)
    file_type = Column(String)  # react or json
    file_content = Column(Text)
    upload_date = Column(String)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)

class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer)
    task_id = Column(Integer)
    grade = Column(Integer)
    correct_answers = Column(Integer)
    total_questions = Column(Integer)
    time_spent = Column(Integer)  # in seconds
    submitted_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class UserCreate(BaseModel):
    username: str
    password: str
    role: str
    firstname: str
    lastname: str
    phone: str
    grade: Optional[str] = None
    school: Optional[str] = None
    student_code: Optional[str] = None
    parent_student_code: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    firstname: str
    lastname: str
    phone: str
    grade: Optional[str] = None
    school: Optional[str] = None
    student_code: Optional[str] = None
    parent_student_code: Optional[str] = None
    created_at: datetime

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    subject: str
    grade: str
    difficulty: str
    time_limit: Optional[int] = None
    file_name: Optional[str] = ""
    file_type: Optional[str] = "json"
    file_content: Optional[str] = ""
    upload_date: Optional[str] = None
    
    class Config:
        populate_by_name = True
        alias_generator = None
    
    # Accept both time_limit and timeLimit
    @classmethod
    def model_validate(cls, obj):
        if isinstance(obj, dict):
            if 'timeLimit' in obj and 'time_limit' not in obj:
                obj['time_limit'] = obj.pop('timeLimit')
        return super().model_validate(obj)

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    subject: str
    grade: str
    difficulty: str
    time_limit: Optional[int] = None
    file_name: Optional[str] = None
    file_type: Optional[str] = None
    file_content: Optional[str] = None
    upload_date: Optional[str] = None
    status: str
    created_at: datetime

class SubmissionCreate(BaseModel):
    student_id: int
    task_id: int
    grade: int
    correct_answers: int
    total_questions: int
    time_spent: int

class SubmissionResponse(BaseModel):
    id: int
    student_id: int
    task_id: int
    grade: int
    correct_answers: int
    total_questions: int
    time_spent: int
    submitted_at: datetime

# FastAPI app
app = FastAPI(title="StudyPoint API", version="1.0.0")

# Add exception handler to log validation errors
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"\n=== VALIDATION ERROR ===")
    print(f"Path: {request.url.path}")
    print(f"Method: {request.method}")
    print(f"Errors: {exc.errors()}")
    print(f"Body: {exc.body}\n")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": str(exc.body)},
    )

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper functions for password hashing
def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    password_bytes = password[:72].encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    try:
        return bcrypt.checkpw(plain_password[:72].encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """Verify JWT token and extract user_id"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        return int(user_id) if user_id else None
    except JWTError:
        return None

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    """Get current authenticated user"""
    user_id = verify_token(credentials.credentials)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def generate_student_code() -> str:
    """Generate a unique 6-digit student code"""
    return str(random.randint(100000, 999999))

# Database initialization functions
def create_user_interactive(db: Session):
    """Interactive user creation"""
    username = input("Enter username: ").strip()
    
    if not username:
        print("Username cannot be empty!")
        return
    
    if db.query(User).filter(User.username == username).first():
        print("Username already exists!")
        return
    
    password = input("Enter password: ")
    if not password or len(password) < 6:
        print("Password must be at least 6 characters!")
        return
    
    role = input("Enter role (admin/student/parent): ").strip().lower()
    
    if role not in ["admin", "student", "parent"]:
        print("Invalid role! Choose from: admin, student, parent")
        return
    
    firstname = input("Enter first name: ").strip()
    lastname = input("Enter last name: ").strip()
    phone = input("Enter phone number: ").strip()

    user_data = {
        "username": username,
        "password_hash": hash_password(password),
        "role": role,
        "firstname": firstname,
        "lastname": lastname,
        "phone": phone,
    }

    if role == "student":
        student_code = generate_student_code()
        while db.query(User).filter(User.student_code == student_code).first():
            student_code = generate_student_code()
        user_data["student_code"] = student_code
        grade = input("Enter grade (optional, press Enter to skip): ").strip()
        school = input("Enter school (optional, press Enter to skip): ").strip()
        if grade:
            user_data["grade"] = grade
        if school:
            user_data["school"] = school
    elif role == "parent":
        student_code = input("Enter student code to link: ").strip()
        student_exists = db.query(User).filter(User.role == "student", User.student_code == student_code).first()
        if not student_exists:
            print("Student code not found!")
            return
        user_data["parent_student_code"] = student_code

    db_user = User(**user_data)
    db.add(db_user)
    db.commit()
    print(f"✓ User '{username}' created successfully!")
    if role == "student":
        print(f"  Student code: {user_data['student_code']}")

def create_task_interactive(db: Session):
    """Interactive task creation"""
    title = input("Enter task title: ").strip()
    description = input("Enter task description: ").strip()
    subject = input("Enter subject: ").strip()
    grade = input("Enter grade: ").strip()
    difficulty = input("Enter difficulty level (easy/medium/hard): ").strip().lower()
    
    if difficulty not in ["easy", "medium", "hard"]:
        print("Invalid difficulty! Using 'medium'")
        difficulty = "medium"
    
    try:
        time_limit = int(input("Enter time limit (in minutes): "))
    except ValueError:
        print("Invalid time limit! Using 30 minutes")
        time_limit = 30
    
    file_name = input("Enter file name: ").strip()
    file_type = input("Enter file type (react/json): ").strip().lower()
    
    if file_type not in ["react", "json"]:
        print("Invalid file type! Using 'json'")
        file_type = "json"
    
    file_content = input("Enter file content (or paste multi-line, end with blank line):\n").strip()

    task_data = {
        "title": title,
        "description": description,
        "subject": subject,
        "grade": grade,
        "difficulty": difficulty,
        "time_limit": time_limit,
        "file_name": file_name,
        "file_type": file_type,
        "file_content": file_content,
        "upload_date": datetime.now().strftime("%Y-%m-%d")
    }

    db_task = Task(**task_data)
    db.add(db_task)
    db.commit()
    print(f"✓ Task '{title}' created successfully!")

def init_database():
    """Initialize database with interactive user input"""
    db = SessionLocal()
    
    try:
        if db.query(User).first():
            print("✓ Database already initialized with data!")
            return
        
        print("\n=== StudyPoint Database Initialization ===\n")
        
        num_users = int(input("How many users do you want to create? "))
        for i in range(num_users):
            print(f"\n--- User {i+1}/{num_users} ---")
            create_user_interactive(db)

        num_tasks = int(input("\nHow many tasks do you want to create? "))
        for i in range(num_tasks):
            print(f"\n--- Task {i+1}/{num_tasks} ---")
            create_task_interactive(db)

        print("\n✓ Database initialized successfully!")
        
    except ValueError:
        print("Invalid input!")
        db.rollback()
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

# API Routes
@app.get("/")
async def root():
    return {"message": "StudyPoint API is running!", "version": "1.0.0"}

# User routes
@app.post("/api/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    if user.role == "parent" and user.parent_student_code:
        student_exists = db.query(User).filter(User.role == "student", User.student_code == user.parent_student_code).first()
        if not student_exists:
            raise HTTPException(status_code=400, detail="Student code not found")
    
    hashed_password = hash_password(user.password)
    
    student_code = None
    if user.role == "student":
        student_code = generate_student_code()
        while db.query(User).filter(User.student_code == student_code).first():
            student_code = generate_student_code()
    
    db_user = User(
        username=user.username,
        password_hash=hashed_password,
        role=user.role,
        firstname=user.firstname,
        lastname=user.lastname,
        phone=user.phone,
        grade=user.grade,
        school=user.school,
        student_code=student_code,
        parent_student_code=user.parent_student_code
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@app.post("/api/login", response_model=Token)
async def login_user(login: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == login.username, User.role == login.role).first()
    
    if not db_user or not verify_password(login.password, db_user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": str(db_user.id)}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

@app.get("/api/users", response_model=List[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/api/users/student/{student_code}", response_model=UserResponse)
async def get_student_by_code(student_code: str, db: Session = Depends(get_db)):
    student = db.query(User).filter(User.role == "student", User.student_code == student_code).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# Task routes
@app.post("/api/tasks", response_model=TaskResponse)
async def create_task(task: TaskCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    print(f"\n=== CREATE TASK REQUEST ===")
    print(f"User: {current_user.username} (Role: {current_user.role})")
    print(f"Received data: {task.dict()}")
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create tasks")
    
    # Set default upload_date if not provided
    upload_date = task.upload_date if task.upload_date else datetime.now().strftime("%m/%d/%Y")
    
    # Set default time_limit if not provided
    time_limit = task.time_limit if task.time_limit else 30
    
    print(f"Final upload_date: {upload_date}, time_limit: {time_limit}")
    
    try:
        db_task = Task(
            title=task.title,
            description=task.description or "",
            subject=task.subject,
            grade=task.grade,
            difficulty=task.difficulty,
            time_limit=time_limit,
            file_name=task.file_name or "",
            file_type=task.file_type or "json",
            file_content=task.file_content or "",
            upload_date=upload_date
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        print(f"✓ Task created successfully with ID: {db_task.id}\n")
        return db_task
    except Exception as e:
        print(f"✗ Error creating task: {str(e)}\n")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating task: {str(e)}")

@app.get("/api/tasks", response_model=List[TaskResponse])
async def get_tasks(grade: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Task).filter(Task.status == "active")
    if grade:
        query = query.filter(Task.grade == grade)
    return query.all()

@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete tasks")
    
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"}

# Submission routes
@app.post("/api/submissions", response_model=SubmissionResponse)
async def create_submission(submission: SubmissionCreate, db: Session = Depends(get_db)):
    db_submission = Submission(**submission.dict())
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission

@app.get("/api/submissions", response_model=List[SubmissionResponse])
async def get_submissions(student_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Submission)
    if student_id:
        query = query.filter(Submission.student_id == student_id)
    return query.all()

@app.get("/api/submissions/student/{student_id}", response_model=List[SubmissionResponse])
async def get_student_submissions(student_id: int, db: Session = Depends(get_db)):
    return db.query(Submission).filter(Submission.student_id == student_id).all()

if __name__ == "__main__":
    # Check if database needs initialization
    db = SessionLocal()
    has_users = db.query(User).first() is not None
    db.close()
    
    if not has_users:
        print("Database is empty. Running initialization...\n")
        init_database()
    
    # Start the server
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)