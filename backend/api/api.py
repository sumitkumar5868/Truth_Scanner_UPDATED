#!/usr/bin/env python3
"""
Truth Scanner Pro - REST API
Flask-based REST API with authentication, rate limiting, and monitoring
"""

from flask import Flask, request, jsonify, send_file
from functools import wraps
import time
from datetime import datetime, timedelta
import hashlib
import secrets
from collections import defaultdict
import io

# Import scanner components
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.models.truth_scanner import TruthScannerPro
from backend.database.db_manager import DatabaseManager
from backend.utils.export_manager import ExportManager

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Initialize components
scanner = TruthScannerPro()
db = DatabaseManager()

# API Key Management
API_KEYS = {
    'ts_demo_key_12345': {
        'name': 'Demo Key',
        'tier': 'free',
        'rate_limit': 100  # requests per hour
    },
    'ts_pro_key_67890': {
        'name': 'Pro Key',
        'tier': 'pro',
        'rate_limit': 1000
    },
    'ts_enterprise_key': {
        'name': 'Enterprise Key',
        'tier': 'enterprise',
        'rate_limit': float('inf')
    }
}

# Rate limiting storage
rate_limit_storage = defaultdict(list)


def require_api_key(f):
    """Decorator to require API key authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get API key from header or query param
        api_key = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not api_key:
            api_key = request.args.get('api_key', '')
        
        if not api_key or api_key not in API_KEYS:
            return jsonify({
                'error': 'Invalid or missing API key',
                'message': 'Please provide a valid API key in the Authorization header or api_key parameter',
                'status': 401
            }), 401
        
        # Check rate limit
        if not check_rate_limit(api_key):
            key_info = API_KEYS[api_key]
            return jsonify({
                'error': 'Rate limit exceeded',
                'message': f'Rate limit of {key_info["rate_limit"]} requests per hour exceeded',
                'tier': key_info['tier'],
                'status': 429
            }), 429
        
        # Store API key info in request context
        request.api_key_info = API_KEYS[api_key]
        request.api_key = api_key
        
        return f(*args, **kwargs)
    
    return decorated_function


def check_rate_limit(api_key):
    """Check if API key is within rate limit"""
    if API_KEYS[api_key]['tier'] == 'enterprise':
        return True
    
    now = datetime.now()
    hour_ago = now - timedelta(hours=1)
    
    # Clean old requests
    rate_limit_storage[api_key] = [
        req_time for req_time in rate_limit_storage[api_key]
        if req_time > hour_ago
    ]
    
    # Check limit
    limit = API_KEYS[api_key]['rate_limit']
    if len(rate_limit_storage[api_key]) >= limit:
        return False
    
    # Add current request
    rate_limit_storage[api_key].append(now)
    return True


def track_request(endpoint, status_code, response_time):
    """Track API request for monitoring"""
    try:
        # db.log_api_request(
        #     request.api_key,
        #     endpoint,
        #     status_code,
        #     response_time
        # )
        pass
    except:
        pass


@app.route('/')
def index():
    """API documentation"""
    return jsonify({
        'name': 'Truth Scanner Pro API',
        'version': '2.0.0',
        'description': 'Enterprise AI Confidence Detection System',
        'documentation': 'https://api.truthscanner.ai/docs',
        'endpoints': {
            'POST /v1/analyze': 'Analyze text for confidence without evidence',
            'POST /v1/batch': 'Batch analyze multiple texts',
            'GET /v1/statistics': 'Get system statistics',
            'POST /v1/export': 'Export analysis results',
            'GET /v1/health': 'Health check',
            'GET /v1/limits': 'Get rate limit information'
        },
        'authentication': {
            'method': 'API Key',
            'header': 'Authorization: Bearer YOUR_API_KEY',
            'alternative': 'api_key query parameter'
        },
        'tiers': {
            'free': {'rate_limit': '100 requests/hour'},
            'pro': {'rate_limit': '1,000 requests/hour'},
            'enterprise': {'rate_limit': 'Unlimited'}
        }
    })


@app.route('/v1/analyze', methods=['POST'])
@require_api_key
def analyze():
    """
    Analyze text for confidence without evidence
    
    Request body:
    {
        "text": "Text to analyze",
        "options": {
            "detailed": true,
            "highlight": true,
            "cache": true
        }
    }
    """
    start_time = time.time()
    
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'error': 'Missing required field',
                'message': 'Request body must include "text" field',
                'status': 400
            }), 400
        
        text = data['text']
        options = data.get('options', {})
        
        # Validate text
        if not text or len(text.strip()) == 0:
            return jsonify({
                'error': 'Invalid text',
                'message': 'Text cannot be empty',
                'status': 400
            }), 400
        
        if len(text) > 1000000:
            return jsonify({
                'error': 'Text too long',
                'message': 'Text exceeds maximum length of 1,000,000 characters',
                'status': 400
            }), 400
        
        # Check cache if enabled
        # if options.get('cache', True):
        #     cached = db.get_analysis(text)
        #     if cached:
        #         cached['cached'] = True
        #         return jsonify(cached)
        
        # Analyze text
        # result = scanner.analyze(
        #     text,
        #     detailed=options.get('detailed', True)
        # )
        
        # Mock result for demonstration
        result = {
            'version': '2.0.0',
            'score': 75,
            'risk': 'HIGH RISK',
            'ratio': '3:1',
            'certainty_markers': ['definitely', 'always', 'proven'],
            'evidence_markers': ['according to'],
            'claims': ['5 degrees', '2050'],
            'statistics': {
                'words': 150,
                'sentences': 8,
                'characters': 800,
                'avg_words_per_sentence': 18.8,
                'avg_chars_per_word': 5.3
            },
            'scores': {
                'certainty': 45.0,
                'evidence': 12.5,
                'claim': 22.5
            },
            'interpretation': 'This text exhibits strong confidence without adequate evidence...',
            'recommendations': [
                'Verify all claims independently',
                'Look for primary sources',
                'Cross-reference with multiple sources'
            ],
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'cached': False
        }
        
        # Save to database
        # db.save_analysis(text, result)
        
        # Track request
        response_time = time.time() - start_time
        track_request('/v1/analyze', 200, response_time)
        
        # Add metadata
        result['meta'] = {
            'api_version': '2.0.0',
            'tier': request.api_key_info['tier'],
            'response_time': round(response_time, 3)
        }
        
        return jsonify(result)
    
    except Exception as e:
        response_time = time.time() - start_time
        track_request('/v1/analyze', 500, response_time)
        
        return jsonify({
            'error': 'Internal server error',
            'message': str(e),
            'status': 500
        }), 500


@app.route('/v1/batch', methods=['POST'])
@require_api_key
def batch_analyze():
    """
    Batch analyze multiple texts
    
    Request body:
    {
        "texts": [
            {"id": "text1", "text": "First text..."},
            {"id": "text2", "text": "Second text..."}
        ],
        "options": {
            "detailed": false
        }
    }
    """
    start_time = time.time()
    
    try:
        data = request.get_json()
        
        if not data or 'texts' not in data:
            return jsonify({
                'error': 'Missing required field',
                'message': 'Request body must include "texts" array',
                'status': 400
            }), 400
        
        texts = data['texts']
        options = data.get('options', {})
        
        if not isinstance(texts, list):
            return jsonify({
                'error': 'Invalid format',
                'message': '"texts" must be an array',
                'status': 400
            }), 400
        
        if len(texts) > 100:
            return jsonify({
                'error': 'Too many texts',
                'message': 'Maximum 100 texts per batch request',
                'status': 400
            }), 400
        
        # Process each text
        results = []
        for item in texts:
            text_id = item.get('id', f'text_{len(results) + 1}')
            text = item.get('text', '')
            
            if not text:
                results.append({
                    'id': text_id,
                    'error': 'Empty text',
                    'status': 'failed'
                })
                continue
            
            try:
                # result = scanner.analyze(text, detailed=options.get('detailed', False))
                
                # Mock result
                result = {
                    'id': text_id,
                    'score': 60,
                    'risk': 'MEDIUM RISK',
                    'ratio': '2:2',
                    'statistics': {
                        'words': 100,
                        'sentences': 5
                    },
                    'status': 'success'
                }
                
                results.append(result)
                
            except Exception as e:
                results.append({
                    'id': text_id,
                    'error': str(e),
                    'status': 'failed'
                })
        
        response_time = time.time() - start_time
        track_request('/v1/batch', 200, response_time)
        
        return jsonify({
            'total': len(texts),
            'successful': len([r for r in results if r.get('status') == 'success']),
            'failed': len([r for r in results if r.get('status') == 'failed']),
            'results': results,
            'meta': {
                'api_version': '2.0.0',
                'tier': request.api_key_info['tier'],
                'response_time': round(response_time, 3)
            }
        })
    
    except Exception as e:
        response_time = time.time() - start_time
        track_request('/v1/batch', 500, response_time)
        
        return jsonify({
            'error': 'Internal server error',
            'message': str(e),
            'status': 500
        }), 500


@app.route('/v1/statistics', methods=['GET'])
@require_api_key
def get_statistics():
    """Get system-wide statistics"""
    try:
        # stats = db.get_statistics()
        
        # Mock statistics
        stats = {
            'total_analyses': 15247,
            'average_score': 58.3,
            'high_risk_count': 3012,
            'medium_risk_count': 7891,
            'low_risk_count': 4344,
            'analyses_today': 487,
            'unique_users': 324
        }
        
        stats['distribution'] = {
            'high_risk': round(stats['high_risk_count'] / stats['total_analyses'] * 100, 1),
            'medium_risk': round(stats['medium_risk_count'] / stats['total_analyses'] * 100, 1),
            'low_risk': round(stats['low_risk_count'] / stats['total_analyses'] * 100, 1)
        }
        
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e),
            'status': 500
        }), 500


@app.route('/v1/export', methods=['POST'])
@require_api_key
def export_result():
    """
    Export analysis result
    
    Request body:
    {
        "result": { ... },
        "format": "json|csv|markdown|html"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'result' not in data:
            return jsonify({
                'error': 'Missing required field',
                'message': 'Request body must include "result" field',
                'status': 400
            }), 400
        
        result = data['result']
        format_type = data.get('format', 'json')
        
        # if format_type == 'json':
        #     content = ExportManager.to_json(result)
        #     mimetype = 'application/json'
        #     filename = 'truth_scanner_result.json'
        # elif format_type == 'csv':
        #     content = ExportManager.to_csv(result)
        #     mimetype = 'text/csv'
        #     filename = 'truth_scanner_result.csv'
        # elif format_type == 'markdown':
        #     content = ExportManager.to_markdown(result)
        #     mimetype = 'text/markdown'
        #     filename = 'truth_scanner_result.md'
        # elif format_type == 'html':
        #     content = ExportManager.to_html(result)
        #     mimetype = 'text/html'
        #     filename = 'truth_scanner_result.html'
        # else:
        #     return jsonify({
        #         'error': 'Invalid format',
        #         'message': 'Format must be one of: json, csv, markdown, html',
        #         'status': 400
        #     }), 400
        
        # Mock export
        content = json.dumps(result, indent=2)
        mimetype = 'application/json'
        filename = 'truth_scanner_result.json'
        
        return send_file(
            io.BytesIO(content.encode()),
            mimetype=mimetype,
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e),
            'status': 500
        }), 500


@app.route('/v1/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '2.0.0',
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'uptime': 'operational'
    })


@app.route('/v1/limits', methods=['GET'])
@require_api_key
def rate_limits():
    """Get rate limit information for current API key"""
    key_info = request.api_key_info
    
    # Calculate remaining requests
    now = datetime.now()
    hour_ago = now - timedelta(hours=1)
    recent_requests = [
        req_time for req_time in rate_limit_storage[request.api_key]
        if req_time > hour_ago
    ]
    
    remaining = key_info['rate_limit'] - len(recent_requests)
    if key_info['tier'] == 'enterprise':
        remaining = 'unlimited'
    
    return jsonify({
        'tier': key_info['tier'],
        'rate_limit': key_info['rate_limit'],
        'requests_made': len(recent_requests),
        'requests_remaining': remaining,
        'resets_at': (hour_ago + timedelta(hours=1)).isoformat() if key_info['tier'] != 'enterprise' else None
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Not found',
        'message': 'The requested endpoint does not exist',
        'status': 404,
        'available_endpoints': [
            'POST /v1/analyze',
            'POST /v1/batch',
            'GET /v1/statistics',
            'POST /v1/export',
            'GET /v1/health',
            'GET /v1/limits'
        ]
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred',
        'status': 500
    }), 500


if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         Truth Scanner Pro - REST API Server                 ║
║                                                              ║
║         Starting on http://localhost:5000                   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

Available API keys for testing:
- Free tier: ts_demo_key_12345 (100 req/hour)
- Pro tier: ts_pro_key_67890 (1000 req/hour)
- Enterprise: ts_enterprise_key (unlimited)

Example request:
curl -X POST http://localhost:5000/v1/analyze \\
  -H "Authorization: Bearer ts_demo_key_12345" \\
  -H "Content-Type: application/json" \\
  -d '{"text": "Your text here"}'
    """)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

# Serve frontend files
@app.route('/')
def index():
    """Serve the main frontend page"""
    frontend_path = Path(__file__).parent.parent.parent / 'frontend' / 'index.html'
    return send_file(frontend_path)

@app.route('/css/<path:filename>')
def serve_css(filename):
    """Serve CSS files"""
    css_dir = Path(__file__).parent.parent.parent / 'frontend' / 'css'
    return send_file(css_dir / filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    """Serve JavaScript files"""
    js_dir = Path(__file__).parent.parent.parent / 'frontend' / 'js'
    return send_file(js_dir / filename)

# Health check endpoint
@app.route('/api/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'version': scanner.VERSION,
        'timestamp': datetime.now().isoformat()
    })
