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

class ExportManager:
    """Handle export to various formats"""
    
    @staticmethod
    def to_json(result: Dict, pretty: bool = True) -> str:
        """Export as JSON"""
        if pretty:
            return json.dumps(result, indent=2)
        return json.dumps(result)
    
    @staticmethod
    def to_csv(result: Dict) -> str:
        """Export as CSV"""
        headers = ['Score', 'Risk', 'Ratio', 'Certainty Count', 'Evidence Count', 
                   'Claim Count', 'Words', 'Sentences', 'Timestamp']
        
        values = [
            result['score'],
            result['risk'],
            result['ratio'],
            len(result.get('certainty_markers', [])),
            len(result.get('evidence_markers', [])),
            len(result.get('claims', [])),
            result['statistics']['words'],
            result['statistics']['sentences'],
            result['timestamp']
        ]
        
        csv_data = ','.join(headers) + '\n'
        csv_data += ','.join(str(v) for v in values)
        
        return csv_data
    
    @staticmethod
    def to_markdown(result: Dict) -> str:
        """Export as Markdown"""
        md = f"# Truth Scanner Analysis Report\n\n"
        md += f"**Score:** {result['score']}/100\n\n"
        md += f"**Risk Level:** {result['risk']}\n\n"
        md += f"**Ratio:** {result['ratio']} (Certainty:Evidence)\n\n"
        
        md += "## Statistics\n\n"
        md += f"- Words: {result['statistics']['words']}\n"
        md += f"- Sentences: {result['statistics']['sentences']}\n"
        md += f"- Avg words/sentence: {result['statistics']['avg_words_per_sentence']}\n\n"
        
        if 'certainty_markers' in result and result['certainty_markers']:
            md += "## Certainty Markers\n\n"
            for marker in result['certainty_markers']:
                md += f"- {marker}\n"
            md += "\n"
        
        if 'evidence_markers' in result and result['evidence_markers']:
            md += "## Evidence Markers\n\n"
            for marker in result['evidence_markers']:
                md += f"- {marker}\n"
            md += "\n"
        
        if 'interpretation' in result:
            md += "## Interpretation\n\n"
            md += result['interpretation'] + "\n\n"
        
        if 'recommendations' in result:
            md += "## Recommendations\n\n"
            for rec in result['recommendations']:
                md += f"- {rec}\n"
        
        md += f"\n---\n\n*Generated: {result['timestamp']}*\n"
        
        return md
    
    @staticmethod
    def to_html(result: Dict) -> str:
        """Export as HTML report"""
        risk_color = '#e63946' if 'HIGH' in result['risk'] else '#f77f00' if 'MEDIUM' in result['risk'] else '#06d6a0'
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Truth Scanner Report - {result['score']}/100</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 900px;
            margin: 50px auto;
            padding: 20px;
            background: #f8f9fa;
        }}
        .header {{
            text-align: center;
            background: white;
            padding: 40px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .score {{
            font-size: 5em;
            font-weight: bold;
            color: {risk_color};
            margin: 20px 0;
        }}
        .risk-badge {{
            display: inline-block;
            background: {risk_color};
            color: white;
            padding: 10px 30px;
            border-radius: 25px;
            font-weight: bold;
            font-size: 1.2em;
        }}
        .section {{
            background: white;
            padding: 30px;
            margin-bottom: 20px;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            color: #1e2761;
            margin-bottom: 20px;
            border-bottom: 3px solid {risk_color};
            padding-bottom: 10px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin: 20px 0;
        }}
        .stat-item {{
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 10px;
        }}
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: {risk_color};
        }}
        .stat-label {{
            color: #666;
            margin-top: 10px;
        }}
        .list {{
            list-style: none;
            padding: 0;
        }}
        .list li {{
            padding: 12px 15px;
            margin: 8px 0;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid {risk_color};
        }}
        .interpretation {{
            background: #e7f6f2;
            padding: 20px;
            border-radius: 10px;
            line-height: 1.8;
            border-left: 5px solid {risk_color};
        }}
        .footer {{
            text-align: center;
            color: #666;
            margin-top: 40px;
            padding: 20px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 Truth Scanner Pro</h1>
        <div class="score">{result['score']}</div>
        <div class="risk-badge">{result['risk']}</div>
        <p style="margin-top: 20px; color: #666;">
            Confidence:Evidence Ratio = {result['ratio']}
        </p>
    </div>

    <div class="section">
        <h2>📊 Text Statistics</h2>
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-value">{result['statistics']['words']}</div>
                <div class="stat-label">Words</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{result['statistics']['sentences']}</div>
                <div class="stat-label">Sentences</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{result['statistics']['avg_words_per_sentence']}</div>
                <div class="stat-label">Avg Words/Sentence</div>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>⚠️ Certainty Markers ({len(result.get('certainty_markers', []))})</h2>
        <ul class="list">
            {"".join(f"<li>{m}</li>" for m in result.get('certainty_markers', [])[:10])}
        </ul>
    </div>

    <div class="section">
        <h2>✅ Evidence Markers ({len(result.get('evidence_markers', []))})</h2>
        <ul class="list">
            {"".join(f"<li>{m}</li>" for m in result.get('evidence_markers', [])[:10])}
        </ul>
    </div>

    <div class="section">
        <h2>🎯 Verifiable Claims ({len(result.get('claims', []))})</h2>
        <ul class="list">
            {"".join(f"<li>{m}</li>" for m in result.get('claims', [])[:10])}
        </ul>
    </div>

    <div class="section">
        <h2>💡 Interpretation</h2>
        <div class="interpretation">
            {result.get('interpretation', 'No interpretation available')}
        </div>
    </div>

    {'<div class="section"><h2>📋 Recommendations</h2><ul class="list">' + "".join(f"<li>{r}</li>" for r in result.get('recommendations', [])) + '</ul></div>' if 'recommendations' in result else ''}

    <div class="footer">
        <p>Generated by <strong>Truth Scanner Pro v{result['version']}</strong></p>
        <p style="font-size: 0.9em; margin-top: 10px;">{result['timestamp']}</p>
    </div>
</body>
</html>"""
        return html


# Command-line interface
def cli_interface():
    """Enhanced command-line interface"""
    import sys
    
    scanner = TruthScannerPro()
    db = DatabaseManager()
    
    def print_banner():
        print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           🔍  TRUTH SCANNER PRO  🔍                          ║
║                                                              ║
║        Enterprise AI Confidence Detection System            ║
║                   Version 2.0.0                             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """)
    
    def print_results(result: Dict):
        """Print formatted results with colors"""
        score = result['score']
        risk = result['risk']
        
        # ANSI colors
        RED = '\033[91m'
        YELLOW = '\033[93m'
        GREEN = '\033[92m'
        BLUE = '\033[94m'
        CYAN = '\033[96m'
        RESET = '\033[0m'
        BOLD = '\033[1m'
        
        if score >= 70:
            color = RED
        elif score >= 40:
            color = YELLOW
        else:
            color = GREEN
        
        print("\n" + "="*70)
        print(f"{BOLD}ANALYSIS RESULTS{RESET}")
        print("="*70 + "\n")
        
        print(f"{color}╔════════════════════════════════════╗{RESET}")
        print(f"{color}║   CONFIDENCE SCORE: {score:3d}/100      ║{RESET}")
        print(f"{color}║   RISK LEVEL: {risk:18s}  ║{RESET}")
        print(f"{color}║   RATIO: {result['ratio']:24s}  ║{RESET}")
        print(f"{color}╚════════════════════════════════════╝{RESET}\n")
        
        print(f"{BOLD}📊 DETECTION DETAILS:{RESET}")
        print(f"   • Certainty Markers: {YELLOW}{len(result['certainty_markers'])}{RESET}")
        for marker in list(result['certainty_markers'])[:5]:
            print(f"     - {marker}")
        if len(result['certainty_markers']) > 5:
            print(f"     - ... and {len(result['certainty_markers']) - 5} more")
        
        print(f"\n   • Evidence Markers: {GREEN}{len(result['evidence_markers'])}{RESET}")
        for marker in list(result['evidence_markers'])[:5]:
            print(f"     - {marker}")
        if len(result['evidence_markers']) > 5:
            print(f"     - ... and {len(result['evidence_markers']) - 5} more")
        
        print(f"\n   • Verifiable Claims: {CYAN}{len(result['claims'])}{RESET}")
        for claim in list(result['claims'])[:5]:
            print(f"     - {claim}")
        if len(result['claims']) > 5:
            print(f"     - ... and {len(result['claims']) - 5} more")
        
        stats = result['statistics']
        print(f"\n{BOLD}📈 TEXT STATISTICS:{RESET}")
        print(f"   • Words: {stats['words']}")
        print(f"   • Sentences: {stats['sentences']}")
        print(f"   • Avg words/sentence: {stats['avg_words_per_sentence']}")
        
        print(f"\n{BOLD}💡 INTERPRETATION:{RESET}")
        print(f"   {result['interpretation']}\n")
        
        if 'recommendations' in result:
            print(f"{BOLD}📋 RECOMMENDATIONS:{RESET}")
            for i, rec in enumerate(result['recommendations'], 1):
                print(f"   {i}. {rec}")
        
        print("\n" + "="*70 + "\n")
    
    def interactive_mode():
        """Enhanced interactive mode"""
        print_banner()
        
        while True:
            print(f"\n{BOLD}OPTIONS:{RESET}")
            print("1. Analyze custom text")
            print("2. Analyze from file")
            print("3. View statistics")
            print("4. Export last result")
            print("5. Batch process directory")
            print("6. Configure settings")
            print("7. Exit")
            
            choice = input("\nSelect option (1-7): ").strip()
            
            if choice == '1':
                print("\nEnter text to analyze (press Ctrl+D or Ctrl+Z when done):")
                try:
                    lines = []
                    while True:
                        line = input()
                        lines.append(line)
                except EOFError:
                    pass
                
                text = '\n'.join(lines)
                
                if text.strip():
                    try:
                        result = scanner.analyze(text)
                        print_results(result)
                        db.save_analysis(text, result)
                        
                        # Store for export
                        with open('/tmp/last_result.json', 'w') as f:
                            json.dump(result, f, indent=2)
                    except Exception as e:
                        print(f"❌ Error: {e}")
            
            elif choice == '2':
                filepath = input("\nEnter file path: ").strip()
                try:
                    with open(filepath, 'r') as f:
                        text = f.read()
                    
                    result = scanner.analyze(text)
                    print_results(result)
                    db.save_analysis(text, result)
                    
                    # Auto-save
                    output_file = filepath + '.analysis.json'
                    with open(output_file, 'w') as f:
                        json.dump(result, f, indent=2)
                    print(f"✅ Results saved to: {output_file}")
                    
                except Exception as e:
                    print(f"❌ Error: {e}")
            
            elif choice == '3':
                stats = db.get_statistics()
                print(f"\n{BOLD}📊 DATABASE STATISTICS:{RESET}")
                print(f"   Total Analyses: {stats['total_analyses']}")
                print(f"   Average Score: {stats['average_score']}")
                print(f"   High Risk: {stats['high_risk_count']}")
                print(f"   Medium Risk: {stats['medium_risk_count']}")
                print(f"   Low Risk: {stats['low_risk_count']}")
            
            elif choice == '4':
                try:
                    with open('/tmp/last_result.json', 'r') as f:
                        result = json.load(f)
                    
                    print("\nExport formats:")
                    print("1. JSON")
                    print("2. CSV")
                    print("3. Markdown")
                    print("4. HTML")
                    
                    fmt_choice = input("\nSelect format (1-4): ").strip()
                    
                    if fmt_choice == '1':
                        output = ExportManager.to_json(result)
                        ext = 'json'
                    elif fmt_choice == '2':
                        output = ExportManager.to_csv(result)
                        ext = 'csv'
                    elif fmt_choice == '3':
                        output = ExportManager.to_markdown(result)
                        ext = 'md'
                    elif fmt_choice == '4':
                        output = ExportManager.to_html(result)
                        ext = 'html'
                    else:
                        print("Invalid choice")
                        continue
                    
                    filename = f"truth_scanner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
                    with open(filename, 'w') as f:
                        f.write(output)
                    print(f"✅ Exported to: {filename}")
                    
                except Exception as e:
                    print(f"❌ Error: {e}")
            
            elif choice == '5':
                dirpath = input("\nEnter directory path: ").strip()
                try:
                    import glob
                    files = glob.glob(os.path.join(dirpath, '*.txt'))
                    
                    print(f"\nFound {len(files)} text files")
                    results = []
                    
                    for filepath in files:
                        with open(filepath, 'r') as f:
                            text = f.read()
                        result = scanner.analyze(text, detailed=False)
                        result['filename'] = os.path.basename(filepath)
                        results.append(result)
                        print(f"✓ {os.path.basename(filepath)}: {result['score']}/100 ({result['risk']})")
                    
                    # Save batch results
                    batch_file = f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    with open(batch_file, 'w') as f:
                        json.dump(results, f, indent=2)
                    print(f"\n✅ Batch results saved to: {batch_file}")
                    
                except Exception as e:
                    print(f"❌ Error: {e}")
            
            elif choice == '6':
                print(f"\n{BOLD}CURRENT SETTINGS:{RESET}")
                print(f"   Certainty Weight: {scanner.config['certainty_weight'] * 100}%")
                print(f"   Evidence Weight: {scanner.config['evidence_weight'] * 100}%")
                print(f"   Claim Weight: {scanner.config['claim_weight'] * 100}%")
                print(f"   High Risk Threshold: {scanner.config['high_threshold']}")
                print(f"   Medium Risk Threshold: {scanner.config['medium_threshold']}")
                print("\n(Settings configuration coming in next version)")
            
            elif choice == '7':
                print("\nThank you for using Truth Scanner Pro! 🔍")
                break
            
            else:
                print("\n❌ Invalid option. Please try again.")
    
    # Run CLI
    if len(sys.argv) > 1:
        # File mode
        filepath = sys.argv[1]
        try:
            with open(filepath, 'r') as f:
                text = f.read()
            
            result = scanner.analyze(text)
            print_banner()
            print_results(result)
            
            # Auto-save
            output_file = filepath + '.analysis.json'
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"✅ Results saved to: {output_file}")
            
            db.save_analysis(text, result)
            
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    else:
        # Interactive mode
        interactive_mode()


if __name__ == "__main__":
    cli_interface()
