#!/usr/bin/env python3
"""
Truth Scanner Pro - Enterprise Backend
Advanced AI Confidence Detection with ML, API, and Database
"""

import re
import json
import sqlite3
from datetime import datetime
from collections import Counter
from typing import Dict, List, Tuple, Optional
import hashlib
import os

# Production-ready scanner with extensible architecture

class DatabaseManager:
    """SQLite database manager for storing analysis history"""
    
    def __init__(self, db_path: str = "truth_scanner.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text_hash TEXT UNIQUE,
                text TEXT,
                score INTEGER,
                risk TEXT,
                ratio TEXT,
                certainty_count INTEGER,
                evidence_count INTEGER,
                claim_count INTEGER,
                word_count INTEGER,
                sentence_count INTEGER,
                result_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                api_key TEXT,
                endpoint TEXT,
                status_code INTEGER,
                response_time REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_text_hash ON analyses(text_hash)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_created_at ON analyses(created_at)
        ''')
        
        conn.commit()
        conn.close()
    
    def save_analysis(self, text: str, result: Dict) -> int:
        """Save analysis result to database"""
        text_hash = hashlib.sha256(text.encode()).hexdigest()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO analyses 
                (text_hash, text, score, risk, ratio, certainty_count, evidence_count, 
                 claim_count, word_count, sentence_count, result_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                text_hash,
                text[:5000],  # Limit text storage
                result['score'],
                result['risk'],
                result['ratio'],
                len(result.get('certainty_markers', [])),
                len(result.get('evidence_markers', [])),
                len(result.get('claims', [])),
                result['statistics']['words'],
                result['statistics']['sentences'],
                json.dumps(result)
            ))
            
            analysis_id = cursor.lastrowid
            conn.commit()
            return analysis_id
            
        finally:
            conn.close()
    
    def get_analysis(self, text: str) -> Optional[Dict]:
        """Get cached analysis by text hash"""
        text_hash = hashlib.sha256(text.encode()).hexdigest()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'SELECT result_json FROM analyses WHERE text_hash = ?',
                (text_hash,)
            )
            row = cursor.fetchone()
            
            if row:
                return json.loads(row[0])
            return None
            
        finally:
            conn.close()
    
    def get_statistics(self) -> Dict:
        """Get aggregate statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT 
                    COUNT(*) as total,
                    AVG(score) as avg_score,
                    SUM(CASE WHEN risk = 'HIGH RISK' THEN 1 ELSE 0 END) as high_risk,
                    SUM(CASE WHEN risk = 'MEDIUM RISK' THEN 1 ELSE 0 END) as medium_risk,
                    SUM(CASE WHEN risk = 'LOW RISK' THEN 1 ELSE 0 END) as low_risk
                FROM analyses
            ''')
            
            row = cursor.fetchone()
            
            return {
                'total_analyses': row[0],
                'average_score': round(row[1], 1) if row[1] else 0,
                'high_risk_count': row[2],
                'medium_risk_count': row[3],
                'low_risk_count': row[4]
            }
            
        finally:
            conn.close()
    
    def log_api_request(self, api_key: str, endpoint: str, status_code: int, response_time: float):
        """Log API request for monitoring"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO api_requests (api_key, endpoint, status_code, response_time)
                VALUES (?, ?, ?, ?)
            ''', (api_key, endpoint, status_code, response_time))
            
            conn.commit()
            
        finally:
            conn.close()

