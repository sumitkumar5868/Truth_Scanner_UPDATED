#!/usr/bin/env python3
"""
Truth Scanner Pro - Application Entry Point
Main launcher for the Truth Scanner application
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from backend.api.api import app
from config.config import get_config

def main():
    """Main application launcher"""
    # Get configuration
    config = get_config()
    
    # Initialize application directories
    config.init_app()
    
    # Print startup information
    print("=" * 60)
    print("🔍 Truth Scanner Pro v2.0")
    print("=" * 60)
    print(f"Environment: {config.APP_ENV}")
    print(f"Debug Mode: {config.DEBUG}")
    print(f"Host: {config.HOST}")
    print(f"Port: {config.PORT}")
    print("=" * 60)
    print(f"\n🚀 Starting server...")
    print(f"📍 Open your browser and navigate to:")
    print(f"   http://localhost:{config.PORT}")
    print(f"\n💡 Press CTRL+C to stop the server")
    print("=" * 60 + "\n")
    
    # Run the Flask application
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)
