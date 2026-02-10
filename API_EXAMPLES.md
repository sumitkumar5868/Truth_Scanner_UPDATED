# 📡 API Examples & Usage Guide

Complete guide to using the Truth Scanner Pro API with code examples in multiple languages.

---

## Table of Contents
- [Authentication](#authentication)
- [Python Examples](#python-examples)
- [JavaScript Examples](#javascript-examples)
- [cURL Examples](#curl-examples)
- [Response Format](#response-format)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)

---

## Authentication

All API requests require an API key sent in the `X-API-Key` header.

### Available API Keys (Default)
```
Demo:       ts_demo_key_12345      (100 req/hour)
Pro:        ts_pro_key_67890       (1000 req/hour)
Enterprise: ts_enterprise_key      (Unlimited)
```

---

## Python Examples

### Basic Analysis
```python
import requests

url = "http://localhost:5000/api/analyze"
headers = {
    "X-API-Key": "ts_demo_key_12345",
    "Content-Type": "application/json"
}
data = {
    "text": "This is absolutely the best solution ever created!"
}

response = requests.post(url, json=data, headers=headers)
result = response.json()

print(f"Confidence Score: {result['confidence_score']}")
print(f"Risk Level: {result['risk_level']}")
print(f"Suggestions: {result['suggestions']}")
```

### Batch Analysis
```python
import requests

texts = [
    "Climate change is definitely happening.",
    "Studies show that exercise may improve health.",
    "According to research (Smith, 2020), this approach works."
]

url = "http://localhost:5000/api/analyze"
headers = {
    "X-API-Key": "ts_demo_key_12345",
    "Content-Type": "application/json"
}

results = []
for text in texts:
    response = requests.post(url, json={"text": text}, headers=headers)
    results.append(response.json())

for i, result in enumerate(results, 1):
    print(f"\nText {i}:")
    print(f"  Score: {result['confidence_score']}")
    print(f"  Risk: {result['risk_level']}")
```

### Get Analysis History
```python
import requests

url = "http://localhost:5000/api/history"
headers = {"X-API-Key": "ts_demo_key_12345"}
params = {"limit": 10}

response = requests.get(url, headers=headers, params=params)
history = response.json()

print(f"Total analyses: {len(history['analyses'])}")
for analysis in history['analyses']:
    print(f"- {analysis['timestamp']}: Score {analysis['confidence_score']}")
```

### Export Analysis Report
```python
import requests

url = "http://localhost:5000/api/export"
headers = {
    "X-API-Key": "ts_demo_key_12345",
    "Content-Type": "application/json"
}
data = {
    "analysis_id": "abc123",
    "format": "json"  # Options: json, csv, pdf, markdown
}

response = requests.post(url, json=data, headers=headers)

# Save the file
with open("report.json", "wb") as f:
    f.write(response.content)
```

---

## JavaScript Examples

### Basic Analysis (Node.js)
```javascript
const axios = require('axios');

const analyzeText = async (text) => {
    try {
        const response = await axios.post(
            'http://localhost:5000/api/analyze',
            { text: text },
            {
                headers: {
                    'X-API-Key': 'ts_demo_key_12345',
                    'Content-Type': 'application/json'
                }
            }
        );
        
        console.log('Confidence Score:', response.data.confidence_score);
        console.log('Risk Level:', response.data.risk_level);
        console.log('Suggestions:', response.data.suggestions);
        
        return response.data;
    } catch (error) {
        console.error('Error:', error.response.data);
    }
};

analyzeText('This is definitely the only solution!');
```

### Basic Analysis (Browser)
```javascript
async function analyzeText(text) {
    const response = await fetch('http://localhost:5000/api/analyze', {
        method: 'POST',
        headers: {
            'X-API-Key': 'ts_demo_key_12345',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: text })
    });
    
    const result = await response.json();
    
    console.log('Confidence Score:', result.confidence_score);
    console.log('Risk Level:', result.risk_level);
    
    return result;
}

// Usage
analyzeText('This is absolutely the best approach ever!');
```

### React Example
```javascript
import React, { useState } from 'react';
import axios from 'axios';

function TruthScanner() {
    const [text, setText] = useState('');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const analyzeText = async () => {
        setLoading(true);
        try {
            const response = await axios.post(
                'http://localhost:5000/api/analyze',
                { text },
                {
                    headers: {
                        'X-API-Key': 'ts_demo_key_12345',
                        'Content-Type': 'application/json'
                    }
                }
            );
            setResult(response.data);
        } catch (error) {
            console.error('Error:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Enter text to analyze..."
            />
            <button onClick={analyzeText} disabled={loading}>
                {loading ? 'Analyzing...' : 'Analyze'}
            </button>
            
            {result && (
                <div>
                    <h3>Results:</h3>
                    <p>Score: {result.confidence_score}</p>
                    <p>Risk: {result.risk_level}</p>
                </div>
            )}
        </div>
    );
}

export default TruthScanner;
```

---

## cURL Examples

### Analyze Text
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "X-API-Key: ts_demo_key_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This is absolutely guaranteed to work!"
  }'
```

### Get History
```bash
curl -X GET "http://localhost:5000/api/history?limit=5" \
  -H "X-API-Key: ts_demo_key_12345"
```

### Get Statistics
```bash
curl -X GET http://localhost:5000/api/stats \
  -H "X-API-Key: ts_demo_key_12345"
```

### Export Report (JSON)
```bash
curl -X POST http://localhost:5000/api/export \
  -H "X-API-Key: ts_demo_key_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "analysis_id": "abc123",
    "format": "json"
  }' \
  --output report.json
```

### Export Report (PDF)
```bash
curl -X POST http://localhost:5000/api/export \
  -H "X-API-Key: ts_demo_key_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "analysis_id": "abc123",
    "format": "pdf"
  }' \
  --output report.pdf
```

---

## Response Format

### Successful Analysis Response
```json
{
    "status": "success",
    "analysis_id": "a1b2c3d4",
    "timestamp": "2024-02-10T17:30:00Z",
    "confidence_score": 75.5,
    "risk_level": "high",
    "certainty_indicators": 8,
    "evidence_indicators": 2,
    "word_count": 42,
    "sentence_count": 3,
    "flags": [
        "overconfident language",
        "lacks sufficient citations",
        "uses absolute terms"
    ],
    "suggestions": [
        "Add credible sources and citations",
        "Use more qualified language",
        "Provide evidence for claims"
    ],
    "highlighted_phrases": [
        {"phrase": "absolutely", "type": "certainty", "position": 15},
        {"phrase": "guaranteed", "type": "certainty", "position": 28}
    ],
    "analysis_time": 0.023
}
```

### History Response
```json
{
    "status": "success",
    "count": 10,
    "analyses": [
        {
            "analysis_id": "xyz789",
            "timestamp": "2024-02-10T17:25:00Z",
            "confidence_score": 65.0,
            "risk_level": "medium",
            "text_preview": "This study suggests that..."
        }
    ]
}
```

### Statistics Response
```json
{
    "status": "success",
    "total_analyses": 1547,
    "average_confidence": 62.3,
    "risk_distribution": {
        "low": 412,
        "medium": 856,
        "high": 279
    },
    "analyses_today": 45,
    "analyses_this_week": 312
}
```

---

## Error Handling

### Common Error Responses

#### Missing API Key (401)
```json
{
    "error": "API key is required",
    "status": 401
}
```

#### Invalid API Key (403)
```json
{
    "error": "Invalid API key",
    "status": 403
}
```

#### Rate Limit Exceeded (429)
```json
{
    "error": "Rate limit exceeded",
    "limit": 100,
    "reset_time": "2024-02-10T18:00:00Z",
    "status": 429
}
```

#### Missing Text (400)
```json
{
    "error": "Text field is required",
    "status": 400
}
```

#### Server Error (500)
```json
{
    "error": "Internal server error",
    "message": "An unexpected error occurred",
    "status": 500
}
```

### Python Error Handling Example
```python
import requests

try:
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()  # Raises HTTPError for bad status
    
    result = response.json()
    print(result)
    
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        print("Authentication failed: Invalid API key")
    elif e.response.status_code == 429:
        print("Rate limit exceeded. Please try again later.")
    else:
        print(f"HTTP error occurred: {e}")
        
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

---

## Rate Limiting

### Tier Limits
| Tier       | Requests/Hour | API Key              |
|------------|---------------|----------------------|
| Free       | 100           | ts_demo_key_12345    |
| Pro        | 1,000         | ts_pro_key_67890     |
| Enterprise | Unlimited     | ts_enterprise_key    |

### Rate Limit Headers
All responses include rate limit information:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1707584400
```

### Handling Rate Limits
```python
import time
import requests

def analyze_with_retry(text, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json={"text": text}, headers=headers)
            
            if response.status_code == 429:
                # Get reset time from headers
                reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
                wait_time = reset_time - int(time.time())
                
                print(f"Rate limited. Waiting {wait_time} seconds...")
                time.sleep(wait_time + 1)
                continue
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
    
    return None
```

---

## Advanced Usage

### Webhook Integration
```python
# Coming soon - Webhook support for async processing
```

### Batch Processing
```python
# Process multiple texts efficiently
def batch_analyze(texts, batch_size=10):
    results = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        for text in batch:
            result = analyze_text(text)
            results.append(result)
        time.sleep(1)  # Respect rate limits
    return results
```

---

## Testing the API

### Using Postman
1. Import the Postman collection (if available)
2. Set environment variables for API_KEY and BASE_URL
3. Run the requests

### Using Swagger/OpenAPI
Visit: `http://localhost:5000/api/docs` (if enabled)

---

## Support

For more examples and help:
- Check the [README.md](README.md)
- Review the [documentation](docs/)
- Open an issue on GitHub

Happy coding! 🚀
