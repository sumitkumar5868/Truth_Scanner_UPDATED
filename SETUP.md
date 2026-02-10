# 🚀 Quick Setup Guide

This guide will get you up and running with Truth Scanner Pro in under 5 minutes!

## Prerequisites
- Python 3.8 or higher installed
- Basic command line knowledge

## Step-by-Step Installation

### 1️⃣ Open Terminal/Command Prompt
Navigate to where you want to install the project.

### 2️⃣ Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment (Optional)
```bash
# Copy the example environment file
cp .env.example .env

# Edit if needed (optional for quick start)
# Default settings work fine for local development
```

### 5️⃣ Run the Application
```bash
python run.py
```

### 6️⃣ Open Your Browser
Navigate to: **http://localhost:5000**

That's it! You're ready to use Truth Scanner Pro! 🎉

---

## Quick Test

### Test the Web Interface
1. Open http://localhost:5000 in your browser
2. Enter some text like: "This is absolutely the best solution ever!"
3. Click "Analyze"
4. View your confidence analysis!

### Test the API
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "X-API-Key: ts_demo_key_12345" \
  -H "Content-Type: application/json" \
  -d '{"text": "This is definitely true!"}'
```

---

## Troubleshooting

### Port Already in Use?
Change the port in `.env`:
```
APP_PORT=8000
```

### Module Not Found Error?
Make sure you activated the virtual environment:
```bash
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

Then reinstall:
```bash
pip install -r requirements.txt
```

### Database Error?
The database is created automatically. If you encounter issues, delete the `data` folder and restart the application.

---

## Next Steps

- 📖 Read the [README.md](README.md) for comprehensive documentation
- 🚀 Check [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md) for production deployment
- 🎨 Explore the [docs/FEATURES.md](docs/FEATURES.md) for all features
- 💻 Review the API examples in [API_EXAMPLES.md](API_EXAMPLES.md)

---

## Need Help?

- Check the [README.md](README.md)
- Review the documentation in the `docs/` folder
- Open an issue on GitHub
- Contact the team

Happy scanning! 🔍
