# VPS Deployment Guide

## Option 1: Simple VPS with Docker

### Prerequisites
- VPS with Ubuntu 22.04+ (DigitalOcean, Linode, Vultr)
- Domain name (optional but recommended)

### Steps

1. **Set up VPS and install Docker**
```bash
# SSH into your VPS
ssh root@your-server-ip

# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose-plugin -y
```

2. **Clone and configure your app**
```bash
# Clone repository
git clone <your-repo-url>
cd playdate-organiser

# Create production environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Edit environment files for production
nano backend/.env
```

3. **Production environment variables**
```bash
# backend/.env
DATABASE_URL=postgresql://postgres:your-secure-password@postgres:5432/playdate_db
SECRET_KEY=your-very-long-random-secret-key-here
BACKEND_CORS_ORIGINS=["https://yourdomain.com", "https://api.yourdomain.com"]

# frontend/.env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

4. **Create production docker-compose**
```yaml
# docker-compose.prod.yml
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: playdate_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://postgres:${POSTGRES_PASSWORD}@postgres:5432/playdate_db
      SECRET_KEY: ${SECRET_KEY}
      BACKEND_CORS_ORIGINS: ${BACKEND_CORS_ORIGINS}
    depends_on:
      - postgres
    restart: unless-stopped

  frontend:
    build: ./frontend
    environment:
      NEXT_PUBLIC_API_URL: ${NEXT_PUBLIC_API_URL}
    depends_on:
      - backend
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
```

5. **Deploy**
```bash
# Start the application
docker compose -f docker-compose.prod.yml up -d

# Check status
docker compose -f docker-compose.prod.yml ps
```

### Domain and SSL Setup

1. **Point domain to your VPS IP**
2. **Set up Nginx reverse proxy with SSL**
3. **Use Let's Encrypt for free SSL certificates**

```bash
# Install certbot
apt install certbot python3-certbot-nginx -y

# Get SSL certificate
certbot --nginx -d yourdomain.com -d api.yourdomain.com
```