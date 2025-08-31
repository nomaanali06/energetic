#!/bin/bash

# Energetic Backend Startup Script
# This script helps you get started with local development

echo "🚀 Starting Energetic Backend..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp env.example .env
    echo "📝 Please edit .env file and add your ANTHROPIC_API_KEY"
    echo "   Then run this script again."
    exit 1
fi

# Check if ANTHROPIC_API_KEY is set
if ! grep -q "ANTHROPIC_API_KEY=your_anthropic_api_key_here" .env; then
    echo "✅ Environment variables configured"
else
    echo "⚠️  Please set your ANTHROPIC_API_KEY in .env file"
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "🐳 Starting services with Docker Compose..."

# Start the services
docker-compose up -d

echo "⏳ Waiting for services to be ready..."

# Wait for database to be ready
echo "📊 Waiting for database..."
until docker-compose exec -T postgres pg_isready -U postgres > /dev/null 2>&1; do
    echo "   Database not ready yet..."
    sleep 2
done

echo "✅ Database is ready!"

# Wait for backend to be ready
echo "🔧 Waiting for backend..."
until curl -f http://localhost:8000/health > /dev/null 2>&1; do
    echo "   Backend not ready yet..."
    sleep 2
done

echo "✅ Backend is ready!"

echo ""
echo "🎉 Energetic Backend is now running!"
echo ""
echo "📍 Access points:"
echo "   • Frontend:        http://localhost:8000"
echo "   • API Docs:        http://localhost:8000/api/docs"
echo "   • Health Check:    http://localhost:8000/health"
echo "   • VNC:            localhost:5900"
echo "   • noVNC:          http://localhost:6080"
echo ""
echo "🔍 View logs:"
echo "   • Backend:         docker-compose logs -f backend"
echo "   • Database:        docker-compose logs -f postgres"
echo "   • VNC:            docker-compose logs -f vnc"
echo ""
echo "🛑 Stop services:    docker-compose down"
echo ""
