#!/bin/bash

# StudyPoint Startup Script

echo "🚀 Starting StudyPoint Application..."

# Create data directory if it doesn't exist
mkdir -p backend/data

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Build and start services
echo "📦 Building and starting services..."
docker-compose up --build -d

# Wait for backend to be ready
echo "⏳ Waiting for backend to be ready..."
sleep 10

# Initialize database with sample data
echo "🗄️  Initializing database..."
docker-compose exec backend python init_db.py

echo "✅ StudyPoint is now running!"
echo ""
echo "🌐 Frontend: http://localhost:5173"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Sample accounts:"
echo "  Admin: username=admin, password=admin123"
echo "  Student: username=student1, password=student123"
echo "  Parent: username=parent1, password=parent123"
echo ""
echo "To stop the application, run: docker-compose down"


