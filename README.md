# 🎵 YouTube to MP3 Converter

A fast, reliable REST API service that converts YouTube videos to MP3 audio files. Built with FastAPI, Docker, and Kubernetes support.

![Python](https://img.shields.io/badge/python-v3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
![Kubernetes](https://img.shields.io/badge/kubernetes-supported-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🚀 **Fast API**: High-performance REST API built with FastAPI
- 🎵 **High Quality**: Extracts best available audio quality from YouTube
- 📦 **Containerized**: Docker-ready with production configurations
- ☸️ **Kubernetes Ready**: Complete Helm chart for deployment
- 🧪 **Well Tested**: Comprehensive test suite with 33+ tests
- 🔒 **Secure**: Non-root user, security contexts, input validation
- 📖 **Auto Documentation**: Interactive API docs with Swagger UI
- ⚡ **Streaming Response**: Efficient memory usage with streaming downloads
- 🛡️ **Error Handling**: Robust error handling and validation

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Build the image
docker build -t youtube-to-mp3 .

# Run the container
docker run -p 8000:8000 youtube-to-mp3

# Access the API
open http://localhost:8000/docs
```

### Local Development

```bash
# Clone the repository
git clone <your-repo-url>
cd youtube-to-mp3

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn youtube-to-mp3:app --host 0.0.0.0 --port 8000
```

## 📋 Prerequisites

- **Python 3.11+**
- **FFmpeg** (for audio processing)
- **Docker** (for containerized deployment)
- **Kubernetes + Helm** (for cluster deployment)

### System Dependencies

#### macOS
```bash
brew install ffmpeg
```

#### Ubuntu/Debian
```bash
sudo apt update && sudo apt install ffmpeg
```

#### Windows
Download from [FFmpeg official website](https://ffmpeg.org/download.html)

## 🛠️ Installation

### 1. Local Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd youtube-to-mp3

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install test dependencies (optional)
pip install -r requirements-test.txt
```

### 2. Docker Installation

```bash
# Build the Docker image
docker build -t youtube-to-mp3 .

# Run with Docker
docker run -d -p 8000:8000 --name youtube-converter youtube-to-mp3
```

### 3. Kubernetes Installation

```bash
# Install with Helm (see Helm Chart section for details)
helm install youtube-to-mp3 helm-chart/youtube-to-mp3/
```

## 🎯 Usage

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/convert/` | Convert YouTube video to MP3 |
| GET | `/docs` | Interactive API documentation |
| GET | `/redoc` | Alternative API documentation |

### Convert YouTube Video to MP3

**Request:**
```bash
curl -X POST "http://localhost:8000/convert/" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}' \
  --output audio.mp3
```

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Response:**
- **Content-Type**: `audio/mpeg`
- **Content-Disposition**: `attachment; filename="Video Title.mp3"`
- **Body**: MP3 audio file stream

### Supported URL Formats

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://m.youtube.com/watch?v=VIDEO_ID`

### Example with JavaScript

```javascript
const response = await fetch('http://localhost:8000/convert/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
  })
});

if (response.ok) {
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'audio.mp3';
  a.click();
}
```

### Example with Python

```python
import requests

response = requests.post(
    'http://localhost:8000/convert/',
    json={'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'}
)

if response.status_code == 200:
    with open('audio.mp3', 'wb') as f:
        f.write(response.content)
    print("Download completed!")
```

## 🧪 Testing

The project includes a comprehensive test suite with 33+ tests covering unit, integration, and performance testing.

### Run Tests

```bash
# Run all tests
./run_tests.sh -a

# Run specific test types
./run_tests.sh -s    # Simple tests (no dependencies)
./run_tests.sh -u    # Unit tests
./run_tests.sh -i    # Integration tests
./run_tests.sh -p    # Performance tests

# Run with coverage
./run_tests.sh -a -c

# Using pytest directly
pytest tests/ -v
pytest tests/test_unit.py -v
pytest tests/test_integration.py -v
```

### Test Summary

```bash
# Show test overview
./test_summary.sh
```

**Test Coverage:**
- ✅ **Unit Tests**: URLItem validation, app creation, error handling
- ✅ **Integration Tests**: API endpoints, HTTP responses, documentation
- ✅ **Performance Tests**: Response times, memory usage, concurrency
- ✅ **Simple Tests**: Basic functionality without external dependencies

## 🐳 Docker

### Build and Run

```bash
# Build the image
docker build -t youtube-to-mp3 .

# Run the container
docker run -p 8000:8000 youtube-to-mp3

# Run in background
docker run -d -p 8000:8000 --name youtube-converter youtube-to-mp3

# View logs
docker logs youtube-converter

# Stop and remove
docker stop youtube-converter && docker rm youtube-converter
```

### Docker Compose (Optional)

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  youtube-to-mp3:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENV=production
    restart: unless-stopped
```

Run with Docker Compose:
```bash
docker-compose up -d
```

## ☸️ Kubernetes Deployment

### Using Helm Chart

The project includes a complete Helm chart for Kubernetes deployment.

```bash
# Install with default values
helm install youtube-to-mp3 helm-chart/youtube-to-mp3/

# Install with custom values
helm install youtube-to-mp3 helm-chart/youtube-to-mp3/ -f custom-values.yaml

# Development deployment
helm install youtube-to-mp3-dev helm-chart/youtube-to-mp3/ -f helm-chart/values-dev.yaml

# Production deployment
helm install youtube-to-mp3-prod helm-chart/youtube-to-mp3/ -f helm-chart/values-prod.yaml
```

### Using Installation Script

```bash
# Development environment
./helm-chart/install.sh -e dev

# Production environment
./helm-chart/install.sh -e prod -n production

# Custom configuration
./helm-chart/install.sh -r my-converter -f my-values.yaml
```

### Manual Kubernetes Deployment

```bash
# Create namespace
kubectl create namespace youtube-to-mp3

# Deploy application
kubectl apply -f k8s/

# Port forward for testing
kubectl port-forward svc/youtube-to-mp3 8080:80

# Access application
open http://localhost:8080/docs
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `ENV` | Environment | `development` |

### Docker Environment Variables

```bash
docker run -p 8000:8000 \
  -e LOG_LEVEL=DEBUG \
  -e ENV=production \
  youtube-to-mp3
```

### Kubernetes Configuration

See `helm-chart/values.yaml` for all configuration options:

```yaml
# Resource limits
resources:
  limits:
    cpu: 1000m
    memory: 1Gi
  requests:
    cpu: 250m
    memory: 512Mi

# Autoscaling
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70

# Ingress
ingress:
  enabled: true
  hosts:
    - host: youtube-converter.yourdomain.com
      paths:
        - path: /
          pathType: Prefix
```

## 📊 Performance

### Benchmarks

- **Response Time**: < 5 seconds for invalid URLs
- **Conversion Time**: Depends on video length and quality
- **Memory Usage**: < 100MB increase per 50 requests
- **Concurrent Requests**: 95%+ success rate at 10+ req/sec
- **File Cleanup**: Automatic temporary file removal

### Optimization Tips

1. **Use Docker**: Consistent environment and dependencies
2. **Resource Limits**: Set appropriate CPU/memory limits in Kubernetes
3. **Caching**: Consider adding Redis for temporary file caching
4. **Load Balancing**: Use multiple replicas for high traffic
5. **Monitoring**: Implement health checks and metrics

## 🛡️ Security

### Built-in Security Features

- ✅ **Non-root User**: Container runs as unprivileged user
- ✅ **Input Validation**: Pydantic models validate all inputs
- ✅ **Error Handling**: No sensitive information in error messages
- ✅ **Resource Limits**: Prevents resource exhaustion
- ✅ **Temporary Files**: Automatic cleanup prevents disk filling

### Security Best Practices

```yaml
# Kubernetes security context
securityContext:
  allowPrivilegeEscalation: false
  capabilities:
    drop:
    - ALL
  readOnlyRootFilesystem: false
  runAsNonRoot: true
  runAsUser: 1000
```

### Rate Limiting (Recommended)

Add rate limiting with nginx ingress:

```yaml
annotations:
  nginx.ingress.kubernetes.io/rate-limit: "10"
  nginx.ingress.kubernetes.io/rate-limit-window: "1m"
```

## 🔧 Development

### Project Structure

```
youtube-to-mp3/
├── youtube-to-mp3.py          # Main application
├── requirements.txt           # Python dependencies
├── requirements-test.txt      # Test dependencies
├── Dockerfile                 # Docker configuration
├── .dockerignore             # Docker ignore file
├── pytest.ini               # Pytest configuration
├── run_tests.sh              # Test runner script
├── test_summary.sh           # Test summary script
├── tests/                    # Test suite
│   ├── test_unit.py          # Unit tests
│   ├── test_integration.py   # Integration tests
│   ├── test_performance.py   # Performance tests
│   ├── test_simple.py        # Simple tests
│   ├── test_minimal.py       # Minimal tests
│   └── conftest.py           # Test fixtures
└── helm-chart/               # Kubernetes Helm chart
    ├── youtube-to-mp3/       # Chart templates
    ├── values-dev.yaml       # Development values
    ├── values-prod.yaml      # Production values
    └── install.sh            # Installation script
```

### Adding New Features

1. **Add tests first** (TDD approach)
2. **Update the API** in `youtube-to-mp3.py`
3. **Update tests** to cover new functionality
4. **Update documentation** in README and API docs
5. **Test locally** with `./run_tests.sh -a`
6. **Build and test Docker** with `docker build -t youtube-to-mp3 .`

### Code Style

- **Python**: Follow PEP 8
- **FastAPI**: Use type hints and Pydantic models
- **Testing**: Write comprehensive tests for all features
- **Documentation**: Keep README and API docs updated

## 🔍 Troubleshooting

### Common Issues

#### 1. **Import Errors**
```bash
# Ensure correct MoviePy import
from moviepy.editor import AudioFileClip
```

#### 2. **FFmpeg Not Found**
```bash
# Install FFmpeg
brew install ffmpeg  # macOS
sudo apt install ffmpeg  # Ubuntu
```

#### 3. **YouTube URL Not Working**
- Check if the video exists and is accessible
- Ensure the URL format is correct
- Some videos may be geo-blocked or age-restricted

#### 4. **Docker Build Fails**
```bash
# Clear Docker cache and rebuild
docker system prune -a
docker build --no-cache -t youtube-to-mp3 .
```

#### 5. **Kubernetes Pod Not Starting**
```bash
# Check pod logs
kubectl logs deployment/youtube-to-mp3

# Check pod description
kubectl describe pod <pod-name>

# Check resources
kubectl top pods
```

### Debug Mode

Enable debug logging:

```bash
# Local development
LOG_LEVEL=DEBUG uvicorn youtube-to-mp3:app --reload

# Docker
docker run -p 8000:8000 -e LOG_LEVEL=DEBUG youtube-to-mp3

# Kubernetes
helm install youtube-to-mp3 helm-chart/youtube-to-mp3/ \
  --set env[0].name=LOG_LEVEL \
  --set env[0].value=DEBUG
```

### Health Checks

```bash
# Check API health
curl http://localhost:8000/docs

# Check in Kubernetes
kubectl get pods -l app.kubernetes.io/name=youtube-to-mp3
```

## 📈 Monitoring

### Health Check Endpoints

- **Docs**: `GET /docs` - API documentation
- **OpenAPI**: `GET /openapi.json` - API specification

### Metrics (Future Enhancement)

Consider adding:
- Prometheus metrics endpoint
- Request duration histograms
- Error rate counters
- Active download gauges

### Logging

The application logs:
- Download requests and video titles
- Error messages with context
- Performance metrics

## 🚀 Deployment

### Production Checklist

- [ ] **Environment Variables**: Set production values
- [ ] **Resource Limits**: Configure CPU/memory limits
- [ ] **Security**: Enable security contexts and policies
- [ ] **Monitoring**: Set up health checks and alerting
- [ ] **Scaling**: Configure horizontal pod autoscaling
- [ ] **Persistence**: Consider persistent storage for large files
- [ ] **Ingress**: Configure TLS and domain routing
- [ ] **Backup**: Plan for disaster recovery

### CI/CD Pipeline Example

```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          pip install -r requirements.txt
          pip install -r requirements-test.txt
          ./run_tests.sh -a

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build Docker image
        run: docker build -t youtube-to-mp3 .
      - name: Push to registry
        run: docker push your-registry/youtube-to-mp3

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Kubernetes
        run: |
          helm upgrade --install youtube-to-mp3 \
            helm-chart/youtube-to-mp3/ \
            --set image.tag=${{ github.sha }}
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Run the test suite**: `./run_tests.sh -a`
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/youtube-to-mp3.git
cd youtube-to-mp3

# Set up development environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-test.txt

# Run tests
./run_tests.sh -a

# Start development server
uvicorn youtube-to-mp3:app --reload --host 0.0.0.0 --port 8000
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Legal Notice

This tool is for educational and personal use only. Please respect YouTube's Terms of Service and copyright laws. Users are responsible for ensuring they have the right to download and convert content.

## 🙏 Acknowledgments

- **FastAPI**: For the excellent web framework
- **pytubefix**: For YouTube downloading capabilities
- **MoviePy**: For audio processing
- **Docker**: For containerization
- **Kubernetes**: For orchestration
- **FFmpeg**: For audio/video processing

## 📞 Support

If you encounter any issues or have questions:

1. **Check the troubleshooting section** above
2. **Run the test suite**: `./run_tests.sh -a`
3. **Check existing issues** in the repository
4. **Create a new issue** with detailed information

---

**Made with ❤️ and Python**

🎵 Convert responsibly and enjoy your music! 🎵