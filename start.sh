#!/bin/bash

echo "🚀 Starting SA Market..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Copy .env.example to .env if not exists
if [ ! -f backend/.env ]; then
    echo "📝 Creating backend/.env from backend/.env.example..."
    cp backend/.env.example backend/.env
    echo "⚠️  Please edit backend/.env with your configuration before continuing."
    read -p "Press Enter to continue..."
fi

# Start services
echo "🐳 Starting Docker containers..."
docker-compose up -d

echo ""
echo "✅ SA Market is starting!"
echo ""
echo "📌 Services:"
echo "  - Frontend:        http://localhost:3000"
echo "  - Backend API:     http://localhost:8000"
echo "  - API Docs:        http://localhost:8000/docs"
echo "  - MinIO Console:   http://localhost:9001"
echo "  - PostgreSQL:      localhost:5432"
echo "  - Redis:           localhost:6379"
echo ""
echo "📊 View logs:"
echo "  docker-compose logs -f"
echo ""
echo "🛑 Stop services:"
echo "  docker-compose down"
echo ""
