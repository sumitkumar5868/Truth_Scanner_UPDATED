
        // Detection Patterns
        const PATTERNS = {
            certainty: [
                /\b(definitely|certainly|absolutely|undoubtedly|unquestionably)\b/gi,
                /\b(always|never|all|none|every|everyone|nobody|nothing)\b/gi,
                /\b(clearly|obviously|evidently|manifestly|plainly)\b/gi,
                /\b(proven|established|known|fact|indisputable)\b/gi,
                /\b(will|must|cannot|impossible)\b/gi,
                /\b(universally|completely|entirely|totally|wholly)\b/gi
            ],
            evidence: [
                /https?:\/\/[^\s]+/gi,
                /\[[\d]+\]/g,
                /\([^)]*\d{4}[^)]*\)/g,
                /\b(according to|source:|per|based on|research shows|studies show|data suggests)\b/gi,
                /\b(might|could|may|possibly|likely|probably|appears|seems|suggests)\b/gi,
                /\b(approximately|roughly|around|about|estimate|potential)\b/gi
            ],
            claims: [
                /\d+(\.\d+)?\s*(percent|%|degrees?|times|years?|people|users)/gi,
                /\b\d{4}\b/g,
                /\b(causes?|leads? to|results? in|due to|because of)\b/gi,
                /\b(increase|decrease|rise|fall|grow|decline)\b.*\b(by|to)\b.*\d+/gi
            ]
        };

        // Settings
        let settings = {
            certaintyWeight: 50,
            evidenceWeight: 30,
            claimWeight: 20,
            highThreshold: 70,
            mediumThreshold: 40
        };

        // Statistics
        let stats = {
            totalAnalyses: 0,
            avgScore: 0,
            highRiskCount: 0,
            allScores: []
        };

        // History
        let analysisHistory = [];

        // Current result for export
        let currentResult = null;

        // Example texts
        const examples = {
            high: `Climate change is definitely caused by human activity. Scientists universally agree that global temperatures will certainly rise by 5 degrees by 2050. This is an established fact that everyone accepts. The evidence is absolutely clear and nobody disputes it.

All coastal cities will completely flood by 2040. This is proven beyond any doubt. Everyone knows that fossil fuels are the only cause.`,
            
            low: `According to the IPCC Assessment Report (2021), climate models suggest that global temperatures could rise between 1.5-4°C by 2100, though significant uncertainty remains in regional projections.

Research published in Nature Climate Change indicates that human activities are likely a major contributing factor, with greenhouse gas emissions appearing to correlate with observed warming trends (Smith et al., 2023).`
        };

        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            loadSettings();
            loadHistory();
            loadStats();
            updateCharCount();
            
            // Drag and drop
            const dropZone = document.getElementById('dropZone');
            if (dropZone) {
                dropZone.addEventListener('click', () => document.getElementById('fileInput').click());
                dropZone.addEventListener('dragover', (e) => {
                    e.preventDefault();
                    dropZone.classList.add('dragover');
                });
                dropZone.addEventListener('dragleave', () => {
                    dropZone.classList.remove('dragover');
                });
                dropZone.addEventListener('drop', (e) => {
                    e.preventDefault();
                    dropZone.classList.remove('dragover');
                    handleFiles(e.dataTransfer.files);
                });
            }

            // Character count
            document.getElementById('inputText').addEventListener('input', updateCharCount);
        });

        // Tab switching
        function switchTab(tabName) {
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            
            event.target.classList.add('active');
            document.getElementById('tab-' + tabName).classList.add('active');
        }

        // Update character count
        function updateCharCount() {
            const text = document.getElementById('inputText').value;
            document.getElementById('charCount').textContent = text.length;
            document.getElementById('wordCount').textContent = text.trim() ? text.trim().split(/\s+/).length : 0;
        }

        // Find matches
        function findMatches(text, patterns) {
            const matches = new Set();
            patterns.forEach(pattern => {
                const found = text.match(pattern);
                if (found) {
                    found.forEach(match => matches.add(match.toLowerCase()));
                }
            });
            return Array.from(matches);
        }

        // Analyze text
        function analyzeText() {
            const text = document.getElementById('inputText').value.trim();
            
            if (!text) {
                showNotification('Please enter text to analyze', 'error');
                return;
            }

            // Find matches
            const certaintyMatches = findMatches(text, PATTERNS.certainty);
            const evidenceMatches = findMatches(text, PATTERNS.evidence);
            const claimMatches = findMatches(text, PATTERNS.claims);

            // Calculate statistics
            const words = text.split(/\s+/).length;
            const sentences = text.split(/[.!?]+/).filter(s => s.trim()).length;

            // Calculate component scores
            const certaintyScore = Math.min(100, (certaintyMatches.length / Math.max(sentences, 1)) * 30);
            const evidenceScore = Math.min(100, (evidenceMatches.length / Math.max(sentences, 1)) * 20);
            const claimScore = Math.min(100, (claimMatches.length / Math.max(sentences, 1)) * 15);

            // Calculate final score
            const score = Math.round(
                certaintyScore * (settings.certaintyWeight / 100) +
                (100 - evidenceScore) * (settings.evidenceWeight / 100) +
                claimScore * (settings.claimWeight / 100)
            );

            // Determine risk
            let risk;
            if (score >= settings.highThreshold) {
                risk = 'HIGH RISK';
            } else if (score >= settings.mediumThreshold) {
                risk = 'MEDIUM RISK';
            } else {
                risk = 'LOW RISK';
            }

            // Create result object
            currentResult = {
                score,
                risk,
                ratio: `${certaintyMatches.length}:${evidenceMatches.length}`,
                certaintyMarkers: certaintyMatches,
                evidenceMarkers: evidenceMatches,
                claims: claimMatches,
                statistics: {
                    words,
                    sentences,
                    avgWordsPerSentence: (words / Math.max(sentences, 1)).toFixed(1)
                },
                interpretation: generateInterpretation(score, certaintyMatches.length, evidenceMatches.length, risk),
                text,
                timestamp: new Date().toISOString()
            };

            // Display results
            displayResults(currentResult);

            // Update stats
            updateStats(score, risk);

            // Save to history
            saveToHistory(currentResult);

            // Show highlighted text
            displayHighlightedText(text, certaintyMatches, evidenceMatches, claimMatches);

            showNotification('Analysis complete!', 'success');
        }

        // Generate interpretation
        function generateInterpretation(score, certaintyCount, evidenceCount, risk) {
            if (risk === 'HIGH RISK') {
                return `This text shows strong signs of confidence without evidence (${score}/100). It contains ${certaintyCount} certainty markers but only ${evidenceCount} evidence markers. The high ratio of assertive language to supporting evidence suggests the AI is making claims with inappropriate confidence. Users should verify these claims independently.`;
            } else if (risk === 'MEDIUM RISK') {
                return `This text shows moderate confidence levels (${score}/100). While it contains ${certaintyCount} certainty markers, there are ${evidenceCount} evidence markers providing some grounding. The claims should be verified, especially those marked with certainty language.`;
            } else {
                return `This text demonstrates good epistemic humility (${score}/100). With ${certaintyCount} certainty markers and ${evidenceCount} evidence markers, the text shows appropriate hedging and qualification. The AI appears to be expressing appropriate uncertainty about its claims.`;
            }
        }

        // Display results
        function displayResults(result) {
            const container = document.getElementById('resultsContainer');
            
            let riskClass = result.risk.includes('HIGH') ? 'high' : 
                           result.risk.includes('MEDIUM') ? 'medium' : 'low';
            
            container.innerHTML = `
                <div class="score-display">
                    <div class="score-circle">
                        <span class="score-value" style="color: var(--${riskClass === 'high' ? 'danger' : riskClass === 'medium' ? 'warning' : 'success'})">${result.score}</span>
                    </div>
                    <div class="score-label">Confidence Score</div>
                    <div class="risk-badge risk-${riskClass}">${result.risk}</div>
                    <div style="margin-top: 15px; color: #666;">
                        Ratio: ${result.ratio} (Certainty:Evidence)
                    </div>
                </div>

                <div class="detection-grid">
                    <div class="detection-card" style="border-left-color: var(--danger)">
                        <h3>
                            ⚠️ Certainty Markers
                            <span class="detection-count">${result.certaintyMarkers.length}</span>
                        </h3>
                        <ul class="detection-list">
                            ${result.certaintyMarkers.length > 0 ? 
                                result.certaintyMarkers.slice(0, 5).map(m => `<li>${m}</li>`).join('') :
                                '<li style="background: transparent; color: #999;">None detected</li>'}
                            ${result.certaintyMarkers.length > 5 ? `<li>... and ${result.certaintyMarkers.length - 5} more</li>` : ''}
                        </ul>
                    </div>

                    <div class="detection-card" style="border-left-color: var(--success)">
                        <h3>
                            ✅ Evidence Markers
                            <span class="detection-count">${result.evidenceMarkers.length}</span>
                        </h3>
                        <ul class="detection-list">
                            ${result.evidenceMarkers.length > 0 ? 
                                result.evidenceMarkers.slice(0, 5).map(m => `<li>${m}</li>`).join('') :
                                '<li style="background: transparent; color: #999;">None detected</li>'}
                            ${result.evidenceMarkers.length > 5 ? `<li>... and ${result.evidenceMarkers.length - 5} more</li>` : ''}
                        </ul>
                    </div>

                    <div class="detection-card" style="border-left-color: var(--warning)">
                        <h3>
                            🎯 Verifiable Claims
                            <span class="detection-count">${result.claims.length}</span>
                        </h3>
                        <ul class="detection-list">
                            ${result.claims.length > 0 ? 
                                result.claims.slice(0, 5).map(m => `<li>${m}</li>`).join('') :
                                '<li style="background: transparent; color: #999;">None detected</li>'}
                            ${result.claims.length > 5 ? `<li>... and ${result.claims.length - 5} more</li>` : ''}
                        </ul>
                    </div>
                </div>

                <div class="chart-container" style="margin-top: 25px;">
                    <h3 style="margin-bottom: 15px; color: var(--dark);">📊 Component Breakdown</h3>
                    <div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <span>Certainty Impact</span>
                            <span>${Math.round((result.certaintyMarkers.length / Math.max(result.statistics.sentences, 1)) * 30)}%</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${Math.round((result.certaintyMarkers.length / Math.max(result.statistics.sentences, 1)) * 30)}%; background: var(--danger)"></div>
                        </div>
                    </div>
                    <div style="margin-top: 15px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <span>Evidence Score</span>
                            <span>${Math.round((result.evidenceMarkers.length / Math.max(result.statistics.sentences, 1)) * 20)}%</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${Math.round((result.evidenceMarkers.length / Math.max(result.statistics.sentences, 1)) * 20)}%; background: var(--success)"></div>
                        </div>
                    </div>
                    <div style="margin-top: 15px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <span>Claim Density</span>
                            <span>${Math.round((result.claims.length / Math.max(result.statistics.sentences, 1)) * 15)}%</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${Math.round((result.claims.length / Math.max(result.statistics.sentences, 1)) * 15)}%; background: var(--warning)"></div>
                        </div>
                    </div>
                </div>

                <div style="background: var(--light); padding: 20px; border-radius: 10px; margin-top: 25px;">
                    <h3 style="margin-bottom: 10px; color: var(--dark);">💡 Interpretation</h3>
                    <p style="line-height: 1.6; color: #555;">${result.interpretation}</p>
                </div>

                <div style="background: white; padding: 20px; border-radius: 10px; margin-top: 15px; border: 2px solid var(--border);">
                    <h3 style="margin-bottom: 15px; color: var(--dark);">📈 Text Statistics</h3>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; text-align: center;">
                        <div>
                            <div style="font-size: 2em; font-weight: bold; color: var(--primary);">${result.statistics.words}</div>
                            <div style="color: #666; margin-top: 5px;">Words</div>
                        </div>
                        <div>
                            <div style="font-size: 2em; font-weight: bold; color: var(--primary);">${result.statistics.sentences}</div>
                            <div style="color: #666; margin-top: 5px;">Sentences</div>
                        </div>
                        <div>
                            <div style="font-size: 2em; font-weight: bold; color: var(--primary);">${result.statistics.avgWordsPerSentence}</div>
                            <div style="color: #666; margin-top: 5px;">Avg Words/Sentence</div>
                        </div>
                    </div>
                </div>
            `;

            document.getElementById('exportSection').style.display = 'block';
        }

        // Display highlighted text
        function displayHighlightedText(text, certainty, evidence, claims) {
            let highlighted = text;

            // Escape HTML
            highlighted = highlighted.replace(/</g, '&lt;').replace(/>/g, '&gt;');

            // Highlight certainty markers
            certainty.forEach(marker => {
                const regex = new RegExp(`\\b${marker}\\b`, 'gi');
                highlighted = highlighted.replace(regex, `<span class="highlight-certainty" title="Certainty marker">${marker}</span>`);
            });

            // Highlight evidence markers
            evidence.forEach(marker => {
                const regex = new RegExp(marker.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
                highlighted = highlighted.replace(regex, `<span class="highlight-evidence" title="Evidence marker">${marker}</span>`);
            });

            // Highlight claims
            claims.forEach(claim => {
                const regex = new RegExp(claim.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
                highlighted = highlighted.replace(regex, `<span class="highlight-claim" title="Verifiable claim">${claim}</span>`);
            });

            document.getElementById('highlightedText').innerHTML = highlighted;
            document.getElementById('highlightedSection').style.display = 'block';
        }

        // Update stats
        function updateStats(score, risk) {
            stats.allScores.push(score);
            stats.totalAnalyses++;
            stats.avgScore = Math.round(stats.allScores.reduce((a, b) => a + b, 0) / stats.allScores.length);
            if (risk === 'HIGH RISK') stats.highRiskCount++;

            document.getElementById('totalAnalyses').textContent = stats.totalAnalyses;
            document.getElementById('avgScore').textContent = stats.avgScore;
            document.getElementById('highRiskCount').textContent = stats.highRiskCount;

            localStorage.setItem('truthScannerStats', JSON.stringify(stats));
        }

        // Load stats
        function loadStats() {
            const saved = localStorage.getItem('truthScannerStats');
            if (saved) {
                stats = JSON.parse(saved);
                document.getElementById('totalAnalyses').textContent = stats.totalAnalyses;
                document.getElementById('avgScore').textContent = stats.avgScore;
                document.getElementById('highRiskCount').textContent = stats.highRiskCount;
            }
        }

        // Save to history
        function saveToHistory(result) {
            analysisHistory.unshift({
                ...result,
                preview: result.text.substring(0, 100) + '...'
            });
            
            if (analysisHistory.length > 50) analysisHistory = analysisHistory.slice(0, 50);
            
            localStorage.setItem('truthScannerHistory', JSON.stringify(analysisHistory));
            displayHistory();
        }

        // Display history
        function displayHistory() {
            const container = document.getElementById('historyContainer');
            
            if (analysisHistory.length === 0) {
                container.innerHTML = `
                    <div style="text-align: center; padding: 60px 20px; color: #999;">
                        <div style="font-size: 4em; margin-bottom: 20px;">📚</div>
                        <p style="font-size: 1.1em;">No analysis history yet</p>
                    </div>
                `;
                return;
            }

            container.innerHTML = analysisHistory.map((item, index) => {
                const riskClass = item.risk.includes('HIGH') ? 'high' : 
                                 item.risk.includes('MEDIUM') ? 'medium' : 'low';
                const date = new Date(item.timestamp).toLocaleString();
                
                return `
                    <div class="history-item" onclick="loadHistoryItem(${index})">
                        <div class="history-meta">
                            <span>📅 ${date}</span>
                            <span class="risk-badge risk-${riskClass}" style="padding: 5px 15px; font-size: 0.8em;">${item.risk}</span>
                        </div>
                        <div class="history-preview">${item.preview}</div>
                        <div style="margin-top: 10px; color: #666; font-size: 0.9em;">
                            Score: ${item.score}/100 | Ratio: ${item.ratio}
                        </div>
                    </div>
                `;
            }).join('');
        }

        // Load history item
        function loadHistoryItem(index) {
            const item = analysisHistory[index];
            document.getElementById('inputText').value = item.text;
            switchTab('single');
            document.querySelector('.tab-btn').click();
            analyzeText();
        }

        // Load history
        function loadHistory() {
            const saved = localStorage.getItem('truthScannerHistory');
            if (saved) {
                analysisHistory = JSON.parse(saved);
                displayHistory();
            }
        }

        // Clear history
        function clearHistory() {
            if (confirm('Are you sure you want to clear all history?')) {
                analysisHistory = [];
                localStorage.removeItem('truthScannerHistory');
                displayHistory();
                showNotification('History cleared', 'success');
            }
        }

        // Export history
        function exportHistory() {
            if (analysisHistory.length === 0) {
                showNotification('No history to export', 'error');
                return;
            }

            const dataStr = JSON.stringify(analysisHistory, null, 2);
            const dataBlob = new Blob([dataStr], { type: 'application/json' });
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = `truth-scanner-history-${new Date().toISOString().split('T')[0]}.json`;
            link.click();
            URL.revokeObjectURL(url);
            
            showNotification('History exported successfully', 'success');
        }

        // Export results
        function exportResults(format) {
            if (!currentResult) {
                showNotification('No analysis to export', 'error');
                return;
            }

            let content, filename, type;

            switch(format) {
                case 'json':
                    content = JSON.stringify(currentResult, null, 2);
                    filename = `truth-scanner-${Date.now()}.json`;
                    type = 'application/json';
                    break;
                
                case 'csv':
                    content = `Score,Risk,Ratio,Certainty Markers,Evidence Markers,Claims,Words,Sentences\n`;
                    content += `${currentResult.score},${currentResult.risk},${currentResult.ratio},${currentResult.certaintyMarkers.length},${currentResult.evidenceMarkers.length},${currentResult.claims.length},${currentResult.statistics.words},${currentResult.statistics.sentences}`;
                    filename = `truth-scanner-${Date.now()}.csv`;
                    type = 'text/csv';
                    break;
                
                case 'html':
                    content = generateHTMLReport(currentResult);
                    filename = `truth-scanner-report-${Date.now()}.html`;
                    type = 'text/html';
                    break;
                
                case 'txt':
                    content = generateTextReport(currentResult);
                    filename = `truth-scanner-${Date.now()}.txt`;
                    type = 'text/plain';
                    break;
            }

            const blob = new Blob([content], { type });
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = filename;
            link.click();
            URL.revokeObjectURL(url);

            showNotification(`Exported as ${format.toUpperCase()}`, 'success');
        }

        // Generate HTML report
        function generateHTMLReport(result) {
            return `<!DOCTYPE html>
<html>
<head>
    <title>Truth Scanner Report</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        .header { text-align: center; margin-bottom: 40px; }
        .score { font-size: 4em; font-weight: bold; color: ${result.risk.includes('HIGH') ? '#e63946' : result.risk.includes('MEDIUM') ? '#f77f00' : '#06d6a0'}; }
        .risk { background: ${result.risk.includes('HIGH') ? '#e63946' : result.risk.includes('MEDIUM') ? '#f77f00' : '#06d6a0'}; color: white; padding: 10px 20px; border-radius: 20px; display: inline-block; margin-top: 15px; }
        .section { margin: 30px 0; padding: 20px; background: #f8f9fa; border-radius: 10px; }
        .list { list-style: none; padding: 0; }
        .list li { padding: 8px; margin: 5px 0; background: white; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 Truth Scanner Report</h1>
        <div class="score">${result.score}/100</div>
        <div class="risk">${result.risk}</div>
        <p>Generated: ${new Date(result.timestamp).toLocaleString()}</p>
    </div>
    
    <div class="section">
        <h2>Summary</h2>
        <p><strong>Ratio:</strong> ${result.ratio} (Certainty:Evidence)</p>
        <p><strong>Words:</strong> ${result.statistics.words}</p>
        <p><strong>Sentences:</strong> ${result.statistics.sentences}</p>
    </div>
    
    <div class="section">
        <h2>⚠️ Certainty Markers (${result.certaintyMarkers.length})</h2>
        <ul class="list">
            ${result.certaintyMarkers.map(m => `<li>${m}</li>`).join('')}
        </ul>
    </div>
    
    <div class="section">
        <h2>✅ Evidence Markers (${result.evidenceMarkers.length})</h2>
        <ul class="list">
            ${result.evidenceMarkers.map(m => `<li>${m}</li>`).join('')}
        </ul>
    </div>
    
    <div class="section">
        <h2>💡 Interpretation</h2>
        <p>${result.interpretation}</p>
    </div>
    
    <div class="section">
        <h2>📄 Original Text</h2>
        <p>${result.text}</p>
    </div>
</body>
</html>`;
        }

        // Generate text report
        function generateTextReport(result) {
            return `TRUTH SCANNER ANALYSIS REPORT
${'='.repeat(60)}

SCORE: ${result.score}/100
RISK: ${result.risk}
RATIO: ${result.ratio} (Certainty:Evidence)
TIMESTAMP: ${new Date(result.timestamp).toLocaleString()}

TEXT STATISTICS:
- Words: ${result.statistics.words}
- Sentences: ${result.statistics.sentences}
- Avg Words/Sentence: ${result.statistics.avgWordsPerSentence}

CERTAINTY MARKERS (${result.certaintyMarkers.length}):
${result.certaintyMarkers.map(m => `- ${m}`).join('\n')}

EVIDENCE MARKERS (${result.evidenceMarkers.length}):
${result.evidenceMarkers.map(m => `- ${m}`).join('\n')}

VERIFIABLE CLAIMS (${result.claims.length}):
${result.claims.map(m => `- ${m}`).join('\n')}

INTERPRETATION:
${result.interpretation}

ORIGINAL TEXT:
${result.text}

${'='.repeat(60)}
Generated by Truth Scanner Pro
https://truthscanner.ai
`;
        }

        // Load example
        function loadExample(type) {
            document.getElementById('inputText').value = examples[type];
            updateCharCount();
        }

        // Clear input
        function clearInput() {
            document.getElementById('inputText').value = '';
            updateCharCount();
            document.getElementById('resultsContainer').innerHTML = `
                <div style="text-align: center; padding: 60px 20px; color: #999;">
                    <div style="font-size: 4em; margin-bottom: 20px;">🔍</div>
                    <p style="font-size: 1.1em;">Enter text and click "Analyze" to see results</p>
                </div>
            `;
            document.getElementById('highlightedSection').style.display = 'none';
            document.getElementById('exportSection').style.display = 'none';
        }

        // Handle file upload
        function handleFiles(files) {
            if (files.length === 0) return;

            const resultsContainer = document.getElementById('batchResults');
            resultsContainer.innerHTML = '<h3 style="margin-bottom: 20px;">Processing files...</h3>';

            const results = [];

            Array.from(files).forEach((file, index) => {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    const text = e.target.result;
                    
                    // Analyze
                    const certaintyMatches = findMatches(text, PATTERNS.certainty);
                    const evidenceMatches = findMatches(text, PATTERNS.evidence);
                    const claimMatches = findMatches(text, PATTERNS.claims);
                    const sentences = text.split(/[.!?]+/).filter(s => s.trim()).length;
                    
                    const certaintyScore = Math.min(100, (certaintyMatches.length / Math.max(sentences, 1)) * 30);
                    const evidenceScore = Math.min(100, (evidenceMatches.length / Math.max(sentences, 1)) * 20);
                    const claimScore = Math.min(100, (claimMatches.length / Math.max(sentences, 1)) * 15);
                    
                    const score = Math.round(
                        certaintyScore * (settings.certaintyWeight / 100) +
                        (100 - evidenceScore) * (settings.evidenceWeight / 100) +
                        claimScore * (settings.claimWeight / 100)
                    );

                    let risk;
                    if (score >= settings.highThreshold) risk = 'HIGH RISK';
                    else if (score >= settings.mediumThreshold) risk = 'MEDIUM RISK';
                    else risk = 'LOW RISK';

                    results.push({
                        filename: file.name,
                        score,
                        risk,
                        certaintyCount: certaintyMatches.length,
                        evidenceCount: evidenceMatches.length
                    });

                    // If all files processed
                    if (results.length === files.length) {
                        displayBatchResults(results);
                    }
                };
                
                reader.readAsText(file);
            });
        }

        // Display batch results
        function displayBatchResults(results) {
            const container = document.getElementById('batchResults');
            
            container.innerHTML = `
                <h3 style="margin-bottom: 20px;">📊 Batch Analysis Results (${results.length} files)</h3>
                ${results.map(result => {
                    const riskClass = result.risk.includes('HIGH') ? 'high' : 
                                     result.risk.includes('MEDIUM') ? 'medium' : 'low';
                    return `
                        <div class="batch-item ${riskClass}">
                            <div>
                                <div style="font-weight: 600; margin-bottom: 5px;">${result.filename}</div>
                                <div style="color: #666; font-size: 0.9em;">
                                    Certainty: ${result.certaintyCount} | Evidence: ${result.evidenceCount}
                                </div>
                            </div>
                            <div style="text-align: center;">
                                <div style="font-size: 2em; font-weight: bold; color: var(--${riskClass === 'high' ? 'danger' : riskClass === 'medium' ? 'warning' : 'success'})">${result.score}</div>
                                <div style="font-size: 0.8em; color: #666;">Score</div>
                            </div>
                            <div>
                                <span class="risk-badge risk-${riskClass}" style="padding: 8px 16px; font-size: 0.85em;">${result.risk}</span>
                            </div>
                        </div>
                    `;
                }).join('')}
                
                <div style="margin-top: 20px; text-align: center;">
                    <button class="btn-primary" onclick="exportBatchResults()">
                        📥 Export All Results
                    </button>
                </div>
            `;
        }

        // Export batch results
        function exportBatchResults() {
            showNotification('Batch export feature coming soon!', 'success');
        }

        // Slider updates
        function updateSlider(id, value) {
            document.getElementById(id + 'Value').textContent = value + (id.includes('Threshold') ? '+' : '%');
            settings[id] = parseInt(value);
        }

        // Reset settings
        function resetSettings() {
            settings = {
                certaintyWeight: 50,
                evidenceWeight: 30,
                claimWeight: 20,
                highThreshold: 70,
                mediumThreshold: 40
            };
            
            document.getElementById('certaintyWeight').value = 50;
            document.getElementById('evidenceWeight').value = 30;
            document.getElementById('claimWeight').value = 20;
            document.getElementById('highThreshold').value = 70;
            document.getElementById('mediumThreshold').value = 40;
            
            updateSlider('certaintyWeight', 50);
            updateSlider('evidenceWeight', 30);
            updateSlider('claimWeight', 20);
            updateSlider('highThreshold', 70);
            updateSlider('mediumThreshold', 40);
            
            showNotification('Settings reset to defaults', 'success');
        }

        // Save settings
        function saveSettings() {
            localStorage.setItem('truthScannerSettings', JSON.stringify(settings));
            showNotification('Settings saved successfully', 'success');
        }

        // Load settings
        function loadSettings() {
            const saved = localStorage.getItem('truthScannerSettings');
            if (saved) {
                settings = JSON.parse(saved);
                document.getElementById('certaintyWeight').value = settings.certaintyWeight;
                document.getElementById('evidenceWeight').value = settings.evidenceWeight;
                document.getElementById('claimWeight').value = settings.claimWeight;
                document.getElementById('highThreshold').value = settings.highThreshold;
                document.getElementById('mediumThreshold').value = settings.mediumThreshold;
                
                updateSlider('certaintyWeight', settings.certaintyWeight);
                updateSlider('evidenceWeight', settings.evidenceWeight);
                updateSlider('claimWeight', settings.claimWeight);
                updateSlider('highThreshold', settings.highThreshold);
                updateSlider('mediumThreshold', settings.mediumThreshold);
            }
        }

        // Show notification
        function showNotification(message, type) {
            const notification = document.getElementById('notification');
            notification.textContent = message;
            notification.className = `notification ${type} show`;
            
            setTimeout(() => {
                notification.classList.remove('show');
            }, 3000);
        }
    