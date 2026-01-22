# Docker Setup Guide for Twitchminert-GUI

This guide provides comprehensive instructions for building, running, and managing the Twitchminert-GUI application using Docker and Docker Compose.

## Prerequisites

- Docker (version 20.10+)
- Docker Compose (version 1.29+)
- Git (for cloning the repository)
- Text editor for .env configuration

## Understanding the Docker Architecture

### Dockerfile Overview

The Dockerfile uses a multi-stage build process:
- **Build Stage**: Installs build dependencies and Python packages
- **Runtime Stage**: Creates a minimal image with only runtime dependencies
- **Non-root User**: Runs as `twitchminert` user for security
- **Health Check**: Monitors container health with HTTP endpoint

### Docker Compose Configuration

The `docker-compose.yml` defines:
- **twitchminert-gui**: Main Flask application
- **db**: Database service
- **twitchminert-network**: Custom bridge network for service communication
- **Volumes**: Persistent storage for data, logs, and database

---

## Environment Configuration (.env)

### Step 1: Create .env File

Copy the example configuration:
```bash
cp .env.example .env
```

### Step 2: Configure Environment Variables

Edit `.env` and set your values:

```env
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# Security
SECRET_KEY=your-very-secure-random-key-here-change-in-production

# Twitch API Credentials
TWITCH_CLIENT_ID=your_twitch_client_id_here
TWITCH_CLIENT_SECRET=your_twitch_client_secret_here

# Database
DATABASE_URL=sqlite:///./data/app.db

# Logging
LOG_LEVEL=INFO
LOG_DIR=./logs
```

### Important Notes:
- **Never commit .env to version control** (it's in .gitignore)
- Change `SECRET_KEY` to a strong random value for production
- Obtain `TWITCH_CLIENT_ID` and `TWITCH_CLIENT_SECRET` from Twitch Developer Console
- For production, use a more secure database (PostgreSQL instead of SQLite)

---

## Building the Docker Image

### Build from Repository

```bash
# Build with default tag
docker-compose build

# Build with custom tag
docker build -t twitchminert-gui:latest .

# Build with specific Python version
docker build --build-arg PYTHON_VERSION=3.11 -t twitchminert-gui:3.11 .

# Build without cache (fresh build)
docker-compose build --no-cache
```

### View Built Images

```bash
docker images | grep twitchminert
```

---

## Running the Application

### Using Docker Compose (Recommended)

```bash
# Start all services in background
docker-compose up -d

# Start with logging output
docker-compose up

# Start specific service
docker-compose up twitchminert-gui

# Start with verbose logging
docker-compose up --verbose
```

### Port Mapping

The application is accessible at:
- **HTTP**: `http://localhost:5000`
- **Health Check**: `http://localhost:5000/health`

To use a different port, modify `docker-compose.yml`:

```yaml
ports:
  - "8000:5000"  # Maps host port 8000 to container port 5000
```

Or use environment variable:

```bash
PORT=8000 docker-compose up -d
```

### Running Single Container

```bash
# Run Flask app directly
docker run -it \
  --name twitchminert-gui \
  -p 5000:5000 \
  --env-file .env \
  twitchminert-gui:latest

# Run with environment variables
docker run -d \
  --name twitchminert-gui \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret-key \
  -e TWITCH_CLIENT_ID=your-client-id \
  -e TWITCH_CLIENT_SECRET=your-secret \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  twitchminert-gui:latest
```

---

## Volume Management

### Persistent Volumes

The docker-compose setup creates three volumes:

```yaml
volumes:
  - ./data:/app/data       # Application data
  - ./logs:/app/logs       # Application logs
  - ./db:/db              # Database files
```

### Create Volume Directory

```bash
# Create directories if they don't exist
mkdir -p data logs db

# Set appropriate permissions (Linux/macOS)
chmod 755 data logs db
```

### Backup Volumes

```bash
# Backup data directory
tar -czf backup_data_$(date +%Y%m%d).tar.gz data/

# Backup entire setup
tar -czf backup_full_$(date +%Y%m%d).tar.gz data/ logs/ db/

# Restore from backup
tar -xzf backup_data_20260122.tar.gz
```

---

## Container Management

### View Running Containers

```bash
# List all running containers
docker-compose ps

# View container logs
docker-compose logs -f twitchminert-gui

# View logs from specific service
docker-compose logs db

# View last 50 lines
docker-compose logs --tail=50 twitchminert-gui
```

### Access Container Shell

```bash
# Access running container
docker-compose exec twitchminert-gui sh

# Or with specific user
docker-compose exec -u twitchminert twitchminert-gui bash
```

### Stop and Remove Containers

```bash
# Stop all services
docker-compose stop

# Stop specific service
docker-compose stop twitchminert-gui

# Remove stopped containers
docker-compose rm

# Remove with force
docker-compose rm -f

# Stop and remove everything
docker-compose down

# Remove volumes too (WARNING: data loss)
docker-compose down -v
```

---

## Health Checks and Monitoring

### Container Health Status

```bash
# Check container health
docker-compose ps

# View health history
docker inspect twitchminert-gui | grep -A 10 Health

# Manual health check
curl -f http://localhost:5000/health
```

### View Container Resources

```bash
# Monitor resource usage
docker stats twitchminert-gui

# View detailed container info
docker inspect twitchminert-gui
```

---

## Networking

### Internal Service Communication

Services communicate via the `twitchminert-network` bridge:

```bash
# View network
docker network inspect twitchminert-network

# Inside container, access other services:
# - twitchminert-gui:5000
# - db:5432 (if using PostgreSQL)
```

### Connect External Services

To connect to host services from container:

```bash
# Use host.docker.internal (Docker Desktop)
extra_hosts:
  - "host.docker.internal:host-gateway"

# Connect to host:
# http://host.docker.internal:port
```

---

## Production Deployment

### Security Checklist

- [ ] Change SECRET_KEY to strong random value
- [ ] Use HTTPS/SSL certificate
- [ ] Configure real database (PostgreSQL recommended)
- [ ] Set FLASK_ENV=production
- [ ] Enable health checks
- [ ] Configure logging and monitoring
- [ ] Set resource limits
- [ ] Use secrets management (Docker Secrets/Swarm)

### Production Configuration

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  twitchminert-gui:
    restart: on-failure:5
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 30s
```

### Run Production Setup

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs twitchminert-gui

# Check if port is already in use
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill process using port
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

### Environment Variables Not Loading

```bash
# Verify .env exists
ls -la .env

# Check .env syntax
cat .env

# Pass variables directly
docker-compose -e VARIABLE=value up -d
```

### Permission Errors

```bash
# Fix volume permissions
sudo chown -R 1000:1000 data/ logs/ db/
sudo chmod -R 755 data/ logs/ db/
```

### Database Connection Issues

```bash
# Check database container
docker-compose logs db

# Verify network connectivity
docker-compose exec twitchminert-gui curl http://db:5432

# Rebuild with no cache
docker-compose build --no-cache
```

---

## Cleanup

### Remove Unused Resources

```bash
# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Remove unused networks
docker network prune

# Full cleanup (WARNING: removes untagged images)
docker system prune

# With volumes
docker system prune -a --volumes
```

---

## Advanced Topics

### Custom Docker Build

```dockerfile
# Dockerfile.custom
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "run.py"]
```

Build with custom Dockerfile:

```bash
docker build -f Dockerfile.custom -t twitchminert-gui:custom .
```

### Docker Registry Push

```bash
# Login to Docker Hub
docker login

# Tag image
docker tag twitchminert-gui:latest username/twitchminert-gui:latest

# Push to registry
docker push username/twitchminert-gui:latest

# Pull from registry
docker pull username/twitchminert-gui:latest
```

---

## References

- [Docker Documentation](https://docs.docker.com)
- [Docker Compose Documentation](https://docs.docker.com/compose)
- [Flask Docker Best Practices](https://flask.palletsprojects.com/en/2.3.x/deploying/docker/)
- [Repository Dockerfile](./Dockerfile)
- [Repository docker-compose.yml](./docker-compose.yml)
