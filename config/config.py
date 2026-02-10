"""
Truth Scanner Pro - Configuration Management
Centralized configuration for the entire application
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration class"""
    
    # Application Settings
    APP_ENV = os.getenv('APP_ENV', 'development')
    DEBUG = os.getenv('APP_DEBUG', 'True').lower() == 'true'
    PORT = int(os.getenv('APP_PORT', 5000))
    HOST = os.getenv('APP_HOST', '0.0.0.0')
    
    # Project Root
    BASE_DIR = Path(__file__).parent
    
    # Database Configuration
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/truth_scanner.db')
    DATABASE_BACKUP_DIR = os.getenv('DATABASE_BACKUP_DIR', 'data/backups')
    
    # API Configuration
    API_KEYS = {
        os.getenv('API_KEY_DEMO', 'ts_demo_key_12345'): {
            'name': 'Demo Key',
            'tier': 'free',
            'rate_limit': int(os.getenv('RATE_LIMIT_FREE', 100))
        },
        os.getenv('API_KEY_PRO', 'ts_pro_key_67890'): {
            'name': 'Pro Key',
            'tier': 'pro',
            'rate_limit': int(os.getenv('RATE_LIMIT_PRO', 1000))
        },
        os.getenv('API_KEY_ENTERPRISE', 'ts_enterprise_key'): {
            'name': 'Enterprise Key',
            'tier': 'enterprise',
            'rate_limit': int(os.getenv('RATE_LIMIT_ENTERPRISE', 9999999))
        }
    }
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/truth_scanner.log')
    
    # Model Configuration
    MODEL_VERSION = os.getenv('MODEL_VERSION', '2.0.0')
    CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', 0.5))
    
    # Export Settings
    EXPORT_DIR = os.getenv('EXPORT_DIR', 'data/exports')
    MAX_EXPORT_SIZE = int(os.getenv('MAX_EXPORT_SIZE', 10485760))  # 10MB default
    
    @classmethod
    def init_app(cls):
        """Initialize application directories"""
        directories = [
            cls.DATABASE_BACKUP_DIR,
            cls.EXPORT_DIR,
            'logs',
            'data'
        ]
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DATABASE_PATH = 'data/test_truth_scanner.db'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get configuration based on environment"""
    env = os.getenv('APP_ENV', 'development')
    return config.get(env, config['default'])
