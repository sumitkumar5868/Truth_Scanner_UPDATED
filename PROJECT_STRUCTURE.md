# 📁 Truth Scanner Pro - Project Structure

Complete guide to understanding the project organization and file structure.

---

## 🎯 Design Principles

The project follows these key principles:

1. **Separation of Concerns**: Frontend, backend, and configuration are clearly separated
2. **Modularity**: Each component has a specific responsibility
3. **Scalability**: Easy to add new features and extend functionality
4. **Maintainability**: Clean, organized code that's easy to understand
5. **Professional Standards**: Production-ready structure suitable for hackathons and real-world deployment

---

## 📂 Directory Overview

```
Truth_Scanner_Organized/
│
├── 📁 backend/              # All Python backend code
├── 📁 frontend/             # Web interface (HTML, CSS, JS)
├── 📁 config/               # Configuration management
├── 📁 docs/                 # Documentation files
├── 📁 data/                 # Runtime data (databases, exports)
├── 📁 tests/                # Test suite
│
├── 📄 run.py                # Main application entry point
├── 📄 requirements.txt      # Python dependencies
├── 📄 .env.example          # Environment variables template
├── 📄 .gitignore            # Git ignore rules
├── 📄 README.md             # Main documentation
└── 📄 ...                   # Other config files
```

---

## 🔍 Detailed Structure

### Backend (`/backend`)

The backend contains all Python code for the core application logic.

```
backend/
├── __init__.py              # Package initialization
│
├── 📁 api/                  # REST API Layer
│   ├── __init__.py
│   └── api.py              # Flask API with routes, auth, rate limiting
│
├── 📁 models/               # AI/ML Models & Core Logic
│   ├── __init__.py
│   └── truth_scanner.py    # Main detection engine with pattern matching
│
├── 📁 database/             # Database Layer
│   ├── __init__.py
│   └── db_manager.py       # SQLite operations, CRUD, schema management
│
└── 📁 utils/                # Utility Functions
    ├── __init__.py
    └── export_manager.py   # Export to JSON, CSV, PDF, Markdown
```

#### Key Components

**1. API Layer (`backend/api/api.py`)**
- RESTful endpoints
- API key authentication
- Rate limiting
- Request/response handling
- Error handling

**2. Models (`backend/models/truth_scanner.py`)**
- Pattern-based text analysis
- Confidence scoring algorithm
- Evidence detection
- Risk level calculation
- Text processing utilities

**3. Database (`backend/database/db_manager.py`)**
- SQLite database management
- Analysis history storage
- Statistics tracking
- Backup functionality
- Query optimization

**4. Utils (`backend/utils/export_manager.py`)**
- Multiple export formats
- Report generation
- Data formatting
- File management

---

### Frontend (`/frontend`)

Clean separation of HTML, CSS, and JavaScript.

```
frontend/
├── index.html              # Main HTML structure
├── 📁 css/
│   └── style.css          # All styles (extracted from original)
└── 📁 js/
    └── app.js             # All JavaScript (extracted from original)
```

#### Features
- **Responsive Design**: Works on all devices
- **Modern UI**: Clean, professional interface
- **Interactive**: Real-time analysis and feedback
- **Modular**: Separated concerns for easy maintenance

---

### Configuration (`/config`)

Centralized configuration management.

```
config/
├── __init__.py
└── config.py              # Environment-based configuration
```

**Features:**
- Environment variables support
- Multiple environments (dev, production, testing)
- Database configuration
- API settings
- Security settings

**Usage:**
```python
from config import get_config

config = get_config()
print(config.DATABASE_PATH)
```

---

### Documentation (`/docs`)

All project documentation.

```
docs/
├── DEPLOYMENT_GUIDE.md    # Production deployment instructions
├── FEATURES.md            # Detailed feature documentation
└── UPGRADE_SUMMARY.md     # Version history and changes
```

---

### Data (`/data`)

Runtime data storage (auto-created, not in version control).

```
data/
├── truth_scanner.db       # SQLite database (auto-created)
├── 📁 backups/            # Database backups
└── 📁 exports/            # Exported reports and analyses
```

**Note:** This directory is in `.gitignore` and created automatically on first run.

---

### Tests (`/tests`)

Comprehensive test suite.

```
tests/
├── __init__.py
└── test_scanner.py        # Sample tests for core functionality
```

**To add more tests:**
```python
# Create test_api.py
# Create test_database.py
# Create test_exports.py
```

---

## 🔧 Key Files

### Root Level Files

#### `run.py` - Application Entry Point
```python
# Main launcher
# - Loads configuration
# - Initializes directories
# - Starts Flask server
# - Handles graceful shutdown

python run.py
```

#### `requirements.txt` - Python Dependencies
```
Flask==2.0.1
# All project dependencies
```

#### `.env.example` - Environment Template
```env
# Copy to .env and customize
APP_ENV=development
APP_PORT=5000
# ... more settings
```

#### `.gitignore` - Version Control Rules
```
# Ignore sensitive and generated files
.env
*.db
__pycache__/
# ... more patterns
```

#### `README.md` - Main Documentation
Comprehensive guide with:
- Installation instructions
- Quick start guide
- API documentation
- Configuration options
- Development guide

#### `SETUP.md` - Quick Setup Guide
Streamlined 5-minute setup instructions for hackathon demos.

#### `API_EXAMPLES.md` - API Usage Guide
Complete API reference with examples in:
- Python
- JavaScript
- cURL
- Multiple frameworks

#### `CONTRIBUTING.md` - Contribution Guidelines
Standards for:
- Code style
- Testing
- Documentation
- Pull requests

#### `LICENSE` - MIT License
Open source license information.

#### `Dockerfile` - Container Configuration
Multi-stage build for production deployment.

#### `docker-compose.yml` - Orchestration
Easy deployment with Docker Compose.

---

## 🔄 Data Flow

### Request Flow
```
User Browser
    ↓
Frontend (index.html + app.js)
    ↓
API (backend/api/api.py)
    ↓
Truth Scanner (backend/models/truth_scanner.py)
    ↓
Database (backend/database/db_manager.py)
    ↓
Export (backend/utils/export_manager.py)
```

### Analysis Flow
```
1. User submits text → Frontend
2. Frontend sends POST → API endpoint
3. API validates request → Checks auth & rate limits
4. API calls scanner → TruthScannerPro.analyze_text()
5. Scanner processes → Pattern matching, scoring
6. Scanner returns results → Confidence score, flags, suggestions
7. API stores in DB → DatabaseManager.save_analysis()
8. API returns to frontend → JSON response
9. Frontend displays → Results visualization
```

---

## 🚀 Adding New Features

### Adding a New API Endpoint

1. **Update `backend/api/api.py`:**
```python
@app.route('/api/new-feature', methods=['POST'])
@require_api_key
@rate_limit
def new_feature():
    data = request.get_json()
    # Your logic here
    return jsonify(result)
```

2. **Update documentation:**
   - Add to `API_EXAMPLES.md`
   - Update `README.md` if needed

### Adding a New Model/Feature

1. **Create new file:**
```bash
touch backend/models/new_feature.py
```

2. **Implement the feature:**
```python
class NewFeature:
    def process(self, data):
        # Implementation
        pass
```

3. **Update `__init__.py`:**
```python
from .new_feature import NewFeature
__all__ = ['TruthScanner', 'NewFeature']
```

4. **Add tests:**
```bash
touch tests/test_new_feature.py
```

### Adding Frontend Features

1. **Update HTML** (`frontend/index.html`)
2. **Add styles** (`frontend/css/style.css`)
3. **Add logic** (`frontend/js/app.js`)
4. **Test thoroughly**

---

## 📦 Module Dependencies

```
run.py
  └── backend.api.api
      ├── backend.models.truth_scanner
      ├── backend.database.db_manager
      ├── backend.utils.export_manager
      └── config.config
```

---

## 🔒 Security Considerations

### Sensitive Files (Not in Version Control)
- `.env` - Environment variables
- `data/*.db` - Database files
- `data/backups/*` - Database backups
- `data/exports/*` - Exported data
- `logs/*.log` - Log files

### API Security
- API key authentication
- Rate limiting by tier
- Input validation
- Error handling

### Database Security
- Parameterized queries (SQL injection prevention)
- Regular backups
- Access control

---

## 🎯 Best Practices

### File Organization
✅ **DO:**
- Keep related code together
- Use clear, descriptive names
- Follow Python package conventions
- Separate concerns (HTML, CSS, JS)
- Document complex logic

❌ **DON'T:**
- Mix frontend and backend code
- Use generic names (utils.py, helpers.py)
- Put everything in one file
- Duplicate code across modules

### Import Organization
```python
# Standard library
import os
import json

# Third-party
from flask import Flask
import requests

# Local
from backend.models import TruthScanner
from config import get_config
```

---

## 🛠️ Development Workflow

1. **Setup**: `python -m venv venv && source venv/bin/activate`
2. **Install**: `pip install -r requirements.txt`
3. **Configure**: `cp .env.example .env`
4. **Develop**: Make changes in appropriate modules
5. **Test**: `python -m pytest tests/`
6. **Run**: `python run.py`
7. **Deploy**: Follow `docs/DEPLOYMENT_GUIDE.md`

---

## 📊 File Size Guidelines

- **Frontend Files**: Keep CSS < 100KB, JS < 200KB
- **Backend Modules**: Keep each file < 500 lines
- **Documentation**: Break into multiple files if > 1000 lines
- **Database**: Regular cleanup of old analyses

---

## 🔍 Finding Things Quickly

### Need to find...

**API endpoints?**
→ `backend/api/api.py`

**Text analysis logic?**
→ `backend/models/truth_scanner.py`

**Database queries?**
→ `backend/database/db_manager.py`

**Export functionality?**
→ `backend/utils/export_manager.py`

**Configuration settings?**
→ `config/config.py` or `.env`

**Frontend styles?**
→ `frontend/css/style.css`

**Frontend logic?**
→ `frontend/js/app.js`

**Usage examples?**
→ `API_EXAMPLES.md`

**Setup instructions?**
→ `SETUP.md` or `README.md`

---

## 🎓 Learning Resources

### Understanding the Structure
1. Start with `README.md` for overview
2. Read `SETUP.md` for quick start
3. Explore `backend/models/truth_scanner.py` for core logic
4. Review `backend/api/api.py` for API design
5. Check `frontend/` for UI implementation

### Code Examples
- `tests/test_scanner.py` - Testing patterns
- `API_EXAMPLES.md` - API usage
- `run.py` - Application initialization

---

## 🚀 Quick Reference

### Running the Application
```bash
python run.py                          # Development mode
APP_ENV=production python run.py       # Production mode
```

### Testing
```bash
python -m pytest tests/                # All tests
python -m pytest tests/test_scanner.py # Specific test
```

### Code Quality
```bash
black backend/                         # Format code
flake8 backend/                        # Check style
```

### Docker
```bash
docker build -t truth-scanner .        # Build image
docker-compose up                      # Run with compose
```

---

## 📞 Support

For questions about the structure:
1. Check this document
2. Review `README.md`
3. Open an issue on GitHub
4. Contact the team

---

**Understanding the structure helps you navigate and extend the project efficiently!** 🎯
