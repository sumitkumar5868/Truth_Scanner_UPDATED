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

class TruthScannerPro:
    """
    Enterprise-grade confidence detection engine with:
    - Pattern-based detection
    - ML-ready architecture
    - Performance optimization
    - Extensible plugin system
    """
    
    VERSION = "2.0.0"
    
    # Enhanced Detection Patterns
    CERTAINTY_PATTERNS = [
        r'\b(definitely|certainly|absolutely|undoubtedly|unquestionably)\b',
        r'\b(always|never|all|none|every|everyone|nobody|nothing|everywhere)\b',
        r'\b(clearly|obviously|evidently|manifestly|plainly|undeniably)\b',
        r'\b(proven|established|known|fact|indisputable|irrefutable)\b',
        r'\b(will|must|cannot|impossible|guaranteed|assured)\b',
        r'\b(universally|completely|entirely|totally|wholly|perfectly)\b',
        r'\b(inevitable|unavoidable|inescapable|certain to)\b',
        r'\b(without (question|doubt))\b'
    ]

    EVIDENCE_PATTERNS = [
        r'https?://[^\s]+',  # URLs
        r'\[[\d]+\]',  # [1] citations
        r'\([^)]*\d{4}[^)]*\)',  # (Author, 2020)
        r'\b(according to|source:|per|based on|research shows|studies? show|data suggests?)\b',
        r'\b(might|could|may|possibly|likely|probably|perhaps|potentially)\b',
        r'\b(appears?|seems?|suggests?|indicates?|implies?)\b',
        r'\b(approximately|roughly|around|about|estimate[sd]?|potential)\b',
        r'\b(some|many|several|various|numerous|multiple)\s+(researchers?|studies|experts?)\b',
        r'doi:\s*\d+\.\d+',  # DOI references
        r'\b[A-Z][a-z]+ et al\.\s*\(\d{4}\)\b'  # et al citations
    ]

    CLAIM_PATTERNS = [
        r'\d+(\.\d+)?\s*(percent|%|degrees?|times|years?|people|users|millions?|billions?)',
        r'\b\d{4}\b',  # Years
        r'\b(causes?|leads? to|results? in|due to|because of|triggered by)\b',
        r'\b(increase[sd]?|decrease[sd]?|rise[ns]?|f[ae]ll[s]?|grow[ns]?|decline[sd]?)\b.*\b(by|to)\b.*\d+',
        r'\b(correlation|causation|effect|impact|influence)\b.*\b(between|of)\b',
        r'\b\d+(\.\d+)?\s*times (more|less|higher|lower)\b',
        r'\bprove[sd]?\s+that\b',
        r'\bdemonstrate[sd]?\s+that\b'
    ]

    def __init__(self, config: Optional[Dict] = None):
        """Initialize scanner with optional configuration"""
        self.config = config or self._default_config()
        self.certainty_regex = [re.compile(p, re.IGNORECASE) for p in self.CERTAINTY_PATTERNS]
        self.evidence_regex = [re.compile(p, re.IGNORECASE) for p in self.EVIDENCE_PATTERNS]
        self.claim_regex = [re.compile(p, re.IGNORECASE) for p in self.CLAIM_PATTERNS]
        
    def _default_config(self) -> Dict:
        """Default configuration"""
        return {
            'certainty_weight': 0.5,
            'evidence_weight': 0.3,
            'claim_weight': 0.2,
            'high_threshold': 70,
            'medium_threshold': 40,
            'min_sentence_length': 5,
            'max_text_length': 1000000
        }
    
    def analyze(self, text: str, detailed: bool = True) -> Dict:
        """
        Analyze text for confidence without evidence
        
        Args:
            text: Input text to analyze
            detailed: Include detailed breakdown
            
        Returns:
            Dictionary with analysis results
        """
        # Validation
        if not text or len(text.strip()) == 0:
            raise ValueError("Empty text provided")
        
        if len(text) > self.config['max_text_length']:
            raise ValueError(f"Text exceeds maximum length of {self.config['max_text_length']}")
        
        # Find matches
        certainty_matches = self._find_matches(text, self.certainty_regex)
        evidence_matches = self._find_matches(text, self.evidence_regex)
        claim_matches = self._find_matches(text, self.claim_regex)
        
        # Calculate statistics
        stats = self._calculate_statistics(text)
        
        # Calculate component scores
        certainty_score = self._calculate_certainty_score(
            len(certainty_matches), 
            stats['sentences']
        )
        evidence_score = self._calculate_evidence_score(
            len(evidence_matches),
            stats['sentences']
        )
        claim_score = self._calculate_claim_score(
            len(claim_matches),
            stats['sentences']
        )
        
        # Calculate final score
        confidence_score = round(
            certainty_score * self.config['certainty_weight'] +
            (100 - evidence_score) * self.config['evidence_weight'] +
            claim_score * self.config['claim_weight']
        )
        
        # Determine risk level
        risk_level = self._determine_risk(confidence_score)
        
        # Build result
        result = {
            'version': self.VERSION,
            'score': confidence_score,
            'risk': risk_level,
            'ratio': f"{len(certainty_matches)}:{len(evidence_matches)}",
            'statistics': stats,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        
        if detailed:
            result.update({
                'certainty_markers': list(certainty_matches),
                'evidence_markers': list(evidence_matches),
                'claims': list(claim_matches),
                'scores': {
                    'certainty': round(certainty_score, 2),
                    'evidence': round(evidence_score, 2),
                    'claim': round(claim_score, 2)
                },
                'interpretation': self._generate_interpretation(
                    confidence_score,
                    len(certainty_matches),
                    len(evidence_matches),
                    len(claim_matches),
                    risk_level
                ),
                'recommendations': self._generate_recommendations(risk_level, result)
            })
        
        return result
    
    def _find_matches(self, text: str, regex_list: List) -> set:
        """Find all unique matches for given regex patterns"""
        matches = set()
        for regex in regex_list:
            found = regex.findall(text)
            for match in found:
                # Handle tuple matches (from groups)
                if isinstance(match, tuple):
                    match = match[0] if match[0] else match[1] if len(match) > 1 else ''
                if match:
                    matches.add(match.lower().strip())
        return matches
    
    def _calculate_statistics(self, text: str) -> Dict:
        """Calculate text statistics"""
        words = [w for w in text.split() if w.strip()]
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        
        # Filter very short sentences
        sentences = [s for s in sentences if len(s.split()) >= self.config['min_sentence_length']]
        
        return {
            'words': len(words),
            'sentences': len(sentences),
            'characters': len(text),
            'avg_words_per_sentence': round(len(words) / max(len(sentences), 1), 1),
            'avg_chars_per_word': round(len(text.replace(' ', '')) / max(len(words), 1), 1)
        }
    
    def _calculate_certainty_score(self, count: int, sentences: int) -> float:
        """Calculate certainty component score"""
        if sentences == 0:
            return 0
        density = count / sentences
        return min(100, density * 30)
    
    def _calculate_evidence_score(self, count: int, sentences: int) -> float:
        """Calculate evidence component score"""
        if sentences == 0:
            return 0
        density = count / sentences
        return min(100, density * 25)
    
    def _calculate_claim_score(self, count: int, sentences: int) -> float:
        """Calculate claim component score"""
        if sentences == 0:
            return 0
        density = count / sentences
        return min(100, density * 15)
    
    def _determine_risk(self, score: float) -> str:
        """Determine risk level from score"""
        if score >= self.config['high_threshold']:
            return "HIGH RISK"
        elif score >= self.config['medium_threshold']:
            return "MEDIUM RISK"
        else:
            return "LOW RISK"
    
    def _generate_interpretation(
        self, 
        score: float, 
        certainty_count: int,
        evidence_count: int,
        claim_count: int,
        risk: str
    ) -> str:
        """Generate human-readable interpretation"""
        if risk == "HIGH RISK":
            return (
                f"This text exhibits strong confidence without adequate evidence (score: {score}/100). "
                f"It contains {certainty_count} certainty markers but only {evidence_count} evidence markers, "
                f"indicating a {certainty_count}:{evidence_count} ratio of assertive language to supporting citations. "
                f"Additionally, {claim_count} verifiable claims were detected. This pattern suggests the AI is "
                f"making claims with inappropriate confidence. Users should independently verify all assertions "
                f"before trusting this content."
            )
        elif risk == "MEDIUM RISK":
            return (
                f"This text shows moderate confidence levels (score: {score}/100). "
                f"While it contains {certainty_count} certainty markers, there are {evidence_count} "
                f"evidence markers providing some grounding. The text includes {claim_count} verifiable claims. "
                f"Critical assertions should be verified, especially those marked with certainty language. "
                f"The AI is expressing some appropriate hedging but could improve citation practices."
            )
        else:
            return (
                f"This text demonstrates good epistemic humility (score: {score}/100). "
                f"With {certainty_count} certainty markers and {evidence_count} evidence markers, "
                f"the text shows appropriate hedging and qualification. {claim_count} verifiable claims "
                f"were detected with proper context. The AI appears to be expressing appropriate uncertainty "
                f"about its claims. However, always verify important information independently."
            )
    
    def _generate_recommendations(self, risk: str, result: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if risk == "HIGH RISK":
            recommendations.extend([
                "Verify all claims independently before using this information",
                "Look for primary sources and peer-reviewed research",
                "Cross-reference with multiple authoritative sources",
                "Be especially cautious with numerical claims and predictions",
                "Consider consulting domain experts"
            ])
        elif risk == "MEDIUM RISK":
            recommendations.extend([
                "Verify key claims, especially those affecting decisions",
                "Look for supporting evidence for main assertions",
                "Check if sources are cited and authoritative",
                "Be cautious with specific numbers and dates"
            ])
        else:
            recommendations.extend([
                "Content shows good practices but always verify critical information",
                "Check that cited sources are reputable and current",
                "Verify any claims that will inform important decisions"
            ])
        
        return recommendations

