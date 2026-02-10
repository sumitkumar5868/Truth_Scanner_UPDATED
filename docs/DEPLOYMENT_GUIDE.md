# Truth Scanner Pro - Deployment Guide

## Production Deployment Options

### Option 1: Simple Server (Development/Demo)

Perfect for demos, internal tools, and development.

#### Setup

```bash
# 1. Install dependencies
pip install flask

# 2. Run the API server
python3 truth_scanner_api.py

# Server starts on http://localhost:5000
```

#### Test

```bash
curl -X POST http://localhost:5000/v1/analyze \
  -H "Authorization: Bearer ts_demo_key_12345" \
  -H "Content-Type: application/json" \
  -d '{"text": "Test text here"}'
```

---

### Option 2: Production Server with Gunicorn

For production environments with higher traffic.

#### Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 truth_scanner_api:app

# Options:
# -w 4: 4 worker processes
# -b 0.0.0.0:5000: Bind to all interfaces on port 5000
# --timeout 120: Request timeout (seconds)
# --access-logfile -: Log to stdout
```

#### Systemd Service (Linux)

Create `/etc/systemd/system/truthscanner.service`:

```ini
[Unit]
Description=Truth Scanner Pro API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/truthscanner
Environment="PATH=/opt/truthscanner/venv/bin"
ExecStart=/opt/truthscanner/venv/bin/gunicorn \
    -w 4 \
    -b 0.0.0.0:5000 \
    --timeout 120 \
    --access-logfile /var/log/truthscanner/access.log \
    --error-logfile /var/log/truthscanner/error.log \
    truth_scanner_api:app

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable truthscanner
sudo systemctl start truthscanner
sudo systemctl status truthscanner
```

---

### Option 3: Docker Deployment

Containerized deployment for easy scaling.

#### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY truth_scanner_pro.py .
COPY truth_scanner_api.py .

# Create data directory
RUN mkdir -p /data

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "truth_scanner_api:app"]
```

#### Build and Run

```bash
# Build image
docker build -t truthscanner:latest .

# Run container
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/data:/data \
  --name truthscanner \
  truthscanner:latest

# Check logs
docker logs truthscanner

# Stop container
docker stop truthscanner
```

#### Docker Compose

`docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data:/data
      - ./logs:/var/log/truthscanner
    environment:
      - FLASK_ENV=production
      - DATABASE_PATH=/data/truth_scanner.db
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/v1/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

Run with:

```bash
docker-compose up -d
```

---

### Option 4: Kubernetes Deployment

For enterprise-scale deployments.

#### Deployment YAML

`kubernetes/deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: truthscanner
  labels:
    app: truthscanner
spec:
  replicas: 3
  selector:
    matchLabels:
      app: truthscanner
  template:
    metadata:
      labels:
        app: truthscanner
    spec:
      containers:
      - name: api
        image: truthscanner:latest
        ports:
        - containerPort: 5000
        env:
        - name: FLASK_ENV
          value: "production"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /v1/health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /v1/health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: truthscanner
spec:
  selector:
    app: truthscanner
  ports:
  - port: 80
    targetPort: 5000
  type: LoadBalancer
```

Deploy:

```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl get pods
kubectl get services
```

---

### Option 5: Cloud Platforms

#### AWS Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.11 truthscanner

# Create environment
eb create truthscanner-env

# Deploy
eb deploy

# Open in browser
eb open
```

#### Google Cloud Run

```bash
# Build and push image
gcloud builds submit --tag gcr.io/PROJECT_ID/truthscanner

# Deploy
gcloud run deploy truthscanner \
  --image gcr.io/PROJECT_ID/truthscanner \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Azure App Service

```bash
# Create resource group
az group create --name truthscanner-rg --location eastus

# Create app service plan
az appservice plan create --name truthscanner-plan --resource-group truthscanner-rg --sku B1 --is-linux

# Create web app
az webapp create --resource-group truthscanner-rg --plan truthscanner-plan --name truthscanner --runtime "PYTHON|3.11"

# Deploy code
az webapp up --name truthscanner --resource-group truthscanner-rg
```

---

## Nginx Reverse Proxy

For production, use Nginx as a reverse proxy.

#### Configuration

`/etc/nginx/sites-available/truthscanner`:

```nginx
server {
    listen 80;
    server_name api.truthscanner.ai;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;

    # Logging
    access_log /var/log/nginx/truthscanner_access.log;
    error_log /var/log/nginx/truthscanner_error.log;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Static files (if serving web interface)
    location /static {
        alias /opt/truthscanner/static;
        expires 1d;
    }
}
```

Enable:

```bash
sudo ln -s /etc/nginx/sites-available/truthscanner /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d api.truthscanner.ai
```

---

## Environment Variables

Set these in production:

```bash
# Flask
export FLASK_ENV=production
export FLASK_SECRET_KEY=your-secret-key-here

# Database
export DATABASE_PATH=/data/truth_scanner.db

# API
export API_KEY_SALT=random-salt-here

# Logging
export LOG_LEVEL=INFO
export LOG_FILE=/var/log/truthscanner/app.log

# Rate Limiting
export RATE_LIMIT_STORAGE=redis  # or memory
export REDIS_URL=redis://localhost:6379/0
```

---

## Database Setup

### SQLite (Default)

```python
# Already configured in truth_scanner_pro.py
# Database file: truth_scanner.db
# No additional setup needed
```

### PostgreSQL (Enterprise)

For high-traffic deployments:

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb truthscanner

# Create user
sudo -u postgres createuser truthscanner -P

# Grant privileges
sudo -u postgres psql
GRANT ALL PRIVILEGES ON DATABASE truthscanner TO truthscanner;
```

Update connection string:

```python
DATABASE_URL = "postgresql://truthscanner:password@localhost/truthscanner"
```

---

## Monitoring & Logging

### Application Logs

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/truthscanner/app.log'),
        logging.StreamHandler()
    ]
)
```

### Prometheus Metrics

Add to `truth_scanner_api.py`:

```python
from prometheus_client import Counter, Histogram, generate_latest

REQUEST_COUNT = Counter('truthscanner_requests_total', 'Total requests')
REQUEST_LATENCY = Histogram('truthscanner_request_latency_seconds', 'Request latency')

@app.route('/metrics')
def metrics():
    return generate_latest()
```

### Health Checks

Already implemented at `/v1/health`:

```bash
curl http://localhost:5000/v1/health
```

---

## Performance Optimization

### Caching with Redis

```python
import redis

cache = redis.Redis(host='localhost', port=6379, db=0)

def get_cached_result(text_hash):
    cached = cache.get(f'analysis:{text_hash}')
    if cached:
        return json.loads(cached)
    return None

def cache_result(text_hash, result):
    cache.setex(
        f'analysis:{text_hash}',
        3600,  # 1 hour TTL
        json.dumps(result)
    )
```

### Database Connection Pooling

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    'sqlite:///truth_scanner.db',
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)
```

### Load Balancing

Use HAProxy or Nginx:

```nginx
upstream truthscanner_backend {
    least_conn;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
    server 127.0.0.1:5003;
    server 127.0.0.1:5004;
}

server {
    location / {
        proxy_pass http://truthscanner_backend;
    }
}
```

---

## Security Best Practices

### 1. API Key Rotation

```python
import secrets

def generate_api_key():
    return 'ts_' + secrets.token_urlsafe(32)

def rotate_api_keys():
    # Implement key rotation logic
    pass
```

### 2. Rate Limiting

Already implemented in API. Adjust as needed:

```python
API_KEYS = {
    'key': {
        'rate_limit': 100,  # requests per hour
        'burst': 10         # burst allowance
    }
}
```

### 3. Input Sanitization

```python
import bleach

def sanitize_text(text):
    # Remove HTML tags
    text = bleach.clean(text, strip=True)
    # Limit length
    text = text[:1000000]
    return text
```

### 4. HTTPS Only

Force HTTPS in Nginx:

```nginx
server {
    listen 80;
    server_name api.truthscanner.ai;
    return 301 https://$server_name$request_uri;
}
```

---

## Backup & Recovery

### Database Backups

```bash
# Backup script
#!/bin/bash
BACKUP_DIR=/backups/truthscanner
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup
sqlite3 /data/truth_scanner.db ".backup '${BACKUP_DIR}/backup_${DATE}.db'"

# Compress
gzip ${BACKUP_DIR}/backup_${DATE}.db

# Delete old backups (keep 30 days)
find ${BACKUP_DIR} -name "*.gz" -mtime +30 -delete
```

### Automated Backups

Add to crontab:

```bash
0 2 * * * /opt/truthscanner/backup.sh
```

---

## Scaling Considerations

### Horizontal Scaling

1. **Stateless API servers** ✅
2. **Shared database** (PostgreSQL/MySQL)
3. **Distributed caching** (Redis Cluster)
4. **Load balancer** (Nginx/HAProxy)

### Vertical Scaling

- Increase worker processes
- Optimize database queries
- Add indexes
- Use connection pooling

### Auto-scaling (Kubernetes)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: truthscanner-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: truthscanner
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

---

## Testing in Production

### Smoke Tests

```bash
#!/bin/bash

echo "Testing health endpoint..."
curl -f http://localhost:5000/v1/health || exit 1

echo "Testing analyze endpoint..."
curl -f -X POST http://localhost:5000/v1/analyze \
  -H "Authorization: Bearer ts_demo_key_12345" \
  -H "Content-Type: application/json" \
  -d '{"text": "Test"}' || exit 1

echo "All tests passed!"
```

### Load Testing

```bash
# Install Apache Bench
sudo apt install apache2-utils

# Run load test
ab -n 1000 -c 10 -p payload.json -T application/json \
  -H "Authorization: Bearer ts_demo_key_12345" \
  http://localhost:5000/v1/analyze
```

---

## Troubleshooting

### Common Issues

**1. Port already in use**
```bash
# Find process
sudo lsof -i :5000
# Kill process
kill -9 PID
```

**2. Database locked**
```bash
# Check for locks
sudo fuser /data/truth_scanner.db
# Stop all processes using DB
sudo fuser -k /data/truth_scanner.db
```

**3. Permission denied**
```bash
# Fix permissions
sudo chown -R www-data:www-data /opt/truthscanner
sudo chmod -R 755 /opt/truthscanner
```

**4. High memory usage**
```bash
# Check memory
free -h
# Restart service
sudo systemctl restart truthscanner
```

---

## Maintenance

### Regular Tasks

**Daily:**
- Check logs for errors
- Monitor API usage
- Review rate limit hits

**Weekly:**
- Database vacuum (SQLite)
- Clear old cached data
- Review performance metrics

**Monthly:**
- Rotate API keys
- Update dependencies
- Review security patches
- Backup verification

---

## Cost Estimation

### Small Deployment (< 1M requests/month)

- **Server:** $5-20/month (DigitalOcean, Linode)
- **Domain:** $12/year
- **SSL:** Free (Let's Encrypt)
- **Total:** ~$10-25/month

### Medium Deployment (1-10M requests/month)

- **Servers:** $50-200/month (Load balanced)
- **Database:** $25-50/month (Managed PostgreSQL)
- **CDN:** $20-50/month
- **Monitoring:** $20/month
- **Total:** ~$115-320/month

### Large Deployment (10M+ requests/month)

- **Kubernetes Cluster:** $300-1000/month
- **Database:** $200-500/month (High availability)
- **CDN:** $100-300/month
- **Monitoring:** $100/month
- **Total:** ~$700-1900/month

---

## Support

For deployment assistance:
- **Email:** deploy@truthscanner.ai
- **Docs:** https://docs.truthscanner.ai/deployment
- **Discord:** https://discord.gg/truthscanner

---

**Production Checklist:**

- [ ] Environment variables configured
- [ ] Database initialized
- [ ] SSL certificate installed
- [ ] Nginx/reverse proxy configured
- [ ] Monitoring setup
- [ ] Backups automated
- [ ] Health checks working
- [ ] Load testing completed
- [ ] Documentation updated
- [ ] Team trained

---

© 2026 Truth Scanner Pro - Deployment Guide
