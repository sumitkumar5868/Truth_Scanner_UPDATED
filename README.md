# 🔍 Truth Scanner Pro v2.0

> **Enterprise-Grade AI Confidence Detection System**  
> Built for [Hackathon Name] - Detect overconfidence and misleading claims with advanced AI

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Configuration](#-configuration)
- [Development](#-development)
- [Deployment](#-deployment)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [Team](#-team)

---

## 🎯 Overview

**Truth Scanner Pro** is an advanced AI-powered system that detects overconfidence, misleading claims, and weak evidence in text. It combines pattern-based detection with machine learning to provide confidence scores and actionable insights.

### Use Cases
- 📰 **Journalism**: Verify claims in articles and news
- 🎓 **Education**: Check academic writing for proper citations
- 💼 **Business**: Analyze reports and presentations
- 🔬 **Research**: Validate scientific claims
- 💬 **Social Media**: Detect misinformation

---

## ✨ Features

### Core Capabilities
- ✅ **AI-Powered Detection**: Pattern-based confidence analysis
- 📊 **Real-time Analysis**: Instant text scanning
- 🎨 **Interactive Dashboard**: Beautiful web interface
- 🔐 **Secure API**: Authentication & rate limiting
- 💾 **Data Persistence**: SQLite database with history
- 📈 **Analytics**: Track usage and trends
- 📤 **Export Options**: JSON, CSV, PDF, Markdown

### Technical Features
- 🚀 **High Performance**: Optimized pattern matching
- 🔄 **RESTful API**: Easy integration
- 📱 **Responsive UI**: Works on all devices
- 🎯 **Modular Architecture**: Clean separation of concerns
- 🧪 **Test Coverage**: Comprehensive testing
- 📝 **Documentation**: Detailed guides

---

## 📁 Project Structure

```
Truth_Scanner_Organized/
│
├── 📁 backend/                  # Backend Python code
│   ├── 📁 api/                  # REST API endpoints
│   │   ├── __init__.py
│   │   └── api.py              # Flask API with auth & rate limiting
│   │
│   ├── 📁 models/               # ML Models & Core Logic
│   │   ├── __init__.py
│   │   └── truth_scanner.py    # Main detection engine
│   │
│   ├── 📁 database/             # Database Management
│   │   ├── __init__.py
│   │   └── db_manager.py       # SQLite operations
│   │
│   ├── 📁 utils/                # Utility Functions
│   │   ├── __init__.py
│   │   └── export_manager.py   # Export functionality
│   │
│   └── __init__.py
│
├── 📁 frontend/                 # Frontend Web Interface
│   ├── 📁 css/
│   │   └── style.css           # Styles (extracted)
│   ├── 📁 js/
│   │   └── app.js              # JavaScript (extracted)
│   └── index.html               # Main HTML page
│
├── 📁 config/                   # Configuration Files
│   └── config.py                # Centralized config management
│
├── 📁 docs/                     # Documentation
│   ├── DEPLOYMENT_GUIDE.md      # Deployment instructions
│   ├── FEATURES.md              # Feature documentation
│   └── UPGRADE_SUMMARY.md       # Version history
│
├── 📁 data/                     # Data Directory
│   ├── truth_scanner.db         # SQLite database (auto-created)
│   ├── backups/                 # Database backups
│   └── exports/                 # Exported reports
│
├── 📁 tests/                    # Test Suite
│   └── (test files)
│
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
└── README.md                    # This file
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Step 1: Clone the Repository
```bash
git clone https://github.com/sumitkumar5868/Truth_Scanner.git
cd Truth_Scanner_Organized
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your configuration
# Use nano, vim, or any text editor
nano .env
```

### Step 5: Initialize Database
```bash
python -c "from backend.database.db_manager import DatabaseManager; DatabaseManager().initialize()"
```

---

## ⚡ Quick Start

### Option 1: Run the Web Interface
```bash
# Start the Flask server
python run.py

# Open your browser
# Navigate to: http://localhost:5000
```

### Option 2: Use the API
```bash
# Start the API server
python -m backend.api.api

# Test the API
curl -X POST http://localhost:5000/api/analyze \
  -H "X-API-Key: ts_demo_key_12345" \
  -H "Content-Type: application/json" \
  -d '{"text": "This is definitely the best solution ever!"}'
```

### Option 3: Use as Python Library
```python
from backend.models.truth_scanner import TruthScannerPro

# Initialize scanner
scanner = TruthScannerPro()

# Analyze text
text = "Climate change is absolutely caused by human activity."
result = scanner.analyze_text(text)

# View results
print(f"Confidence Score: {result['confidence_score']}")
print(f"Risk Level: {result['risk_level']}")
```

---

## 📡 API Documentation

### Authentication
All API requests require an API key in the header:
```
X-API-Key: your_api_key_here
```

### Endpoints

#### 1. Analyze Text
```http
POST /api/analyze
Content-Type: application/json
X-API-Key: ts_demo_key_12345

{
  "text": "Your text to analyze here"
}
```

**Response:**
```json
{
  "confidence_score": 75.5,
  "risk_level": "high",
  "certainty_indicators": 8,
  "evidence_indicators": 2,
  "flags": ["overconfident language", "lacks citations"],
  "suggestions": ["Add citations", "Use qualifiers"],
  "analysis_time": 0.023
}
```

#### 2. Get History
```http
GET /api/history?limit=10
X-API-Key: ts_demo_key_12345
```

#### 3. Get Statistics
```http
GET /api/stats
X-API-Key: ts_demo_key_12345
```

#### 4. Export Report
```http
POST /api/export
Content-Type: application/json
X-API-Key: ts_demo_key_12345

{
  "analysis_id": "abc123",
  "format": "pdf"
}
```

### Rate Limits
- **Free Tier**: 100 requests/hour
- **Pro Tier**: 1,000 requests/hour
- **Enterprise**: Unlimited

---

## ⚙️ Configuration

### Environment Variables
Create a `.env` file based on `.env.example`:

```env
# Application
APP_ENV=development
APP_DEBUG=True
APP_PORT=5000

# Database
DATABASE_PATH=data/truth_scanner.db

# API Keys
API_KEY_DEMO=ts_demo_key_12345
API_KEY_PRO=ts_pro_key_67890

# Rate Limiting
RATE_LIMIT_FREE=100
RATE_LIMIT_PRO=1000
```

See `.env.example` for all available options.

---

## 💻 Development

### Running in Development Mode
```bash
# Enable debug mode in .env
APP_DEBUG=True

# Run with auto-reload
python run.py
```

### Code Style
We follow PEP 8 guidelines. Format your code:
```bash
pip install black flake8
black backend/
flake8 backend/
```

### Adding New Features
1. Create feature branch: `git checkout -b feature/your-feature`
2. Implement changes in appropriate module
3. Add tests in `tests/`
4. Update documentation
5. Submit pull request

---

## 🚢 Deployment

### Production Deployment
See [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) for detailed instructions.

Quick production setup:
```bash
# Set production environment
export APP_ENV=production
export APP_DEBUG=False

# Use production server (gunicorn)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Docker Deployment
```bash
# Build image
docker build -t truth-scanner .

# Run container
docker run -p 5000:5000 truth-scanner
```

---

## 🧪 Testing

### Run Tests
```bash
# Run all tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=backend tests/

# Run specific test
python -m pytest tests/test_scanner.py
```

### Manual Testing
```bash
# Test the scanner
python -c "from backend.models.truth_scanner import TruthScannerPro; \
           scanner = TruthScannerPro(); \
           print(scanner.analyze_text('This is definitely true!'))"
```

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork** the repository
2. **Create** a feature branch
3. **Commit** your changes
4. **Push** to your branch
5. **Open** a Pull Request

### Contribution Guidelines
- Follow PEP 8 coding standards
- Add tests for new features
- Update documentation
- Write clear commit messages

---

## 👥 Owner 

**Project Lead**: Sumit kumar
**Date**: 10/02/2026



---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Built with Python, Flask, and modern web technologies
- Inspired by the need for truth in digital communication
- Thanks to all contributors and supporters

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/sumitkumar5868/Truth_Scanner/issues)
- **Email**: [sumitytvlog3@gmail.com]


---

## 🗺️Future Roadmap

- [ ] Add machine learning model training
- [ ] Multi-language support
- [ ] Browser extension
- [ ] Mobile app
- [ ] Advanced analytics dashboard
- [ ] Integration with popular platforms

---

**Made with ❤️ for truth and transparency**
