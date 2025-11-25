import os
from datetime import datetime

def generate_html_report(query, winner, report_content, audit_reason, block_hash, rewards, filename="financial_report.html"):
    """
    Generates a premium HTML report for the financial analysis.
    """
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FinChain Analysis Report</title>
    <style>
        :root {{
            --primary: #0f172a;
            --secondary: #1e293b;
            --accent: #3b82f6;
            --text: #e2e8f0;
            --success: #10b981;
            --card-bg: #1e293b;
        }}
        
        body {{
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background-color: var(--primary);
            color: var(--text);
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
        }}

        header {{
            text-align: center;
            margin-bottom: 60px;
            border-bottom: 1px solid #334155;
            padding-bottom: 40px;
        }}

        h1 {{
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(to right, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}

        .meta {{
            color: #94a3b8;
            font-size: 0.9rem;
        }}

        .card {{
            background-color: var(--card-bg);
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            border: 1px solid #334155;
        }}

        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            border-bottom: 1px solid #334155;
            padding-bottom: 15px;
        }}

        .card-title {{
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--accent);
        }}

        .winner-badge {{
            background-color: rgba(16, 185, 129, 0.2);
            color: var(--success);
            padding: 6px 12px;
            border-radius: 9999px;
            font-size: 0.875rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }}

        .report-content {{
            white-space: pre-wrap;
            color: #cbd5e1;
        }}

        .audit-section {{
            background-color: rgba(59, 130, 246, 0.1);
            border-left: 4px solid var(--accent);
            padding: 20px;
            margin-top: 20px;
            border-radius: 0 8px 8px 0;
        }}

        .blockchain-info {{
            font-family: 'JetBrains Mono', monospace;
            background-color: #000;
            padding: 15px;
            border-radius: 8px;
            font-size: 0.85rem;
            color: #22c55e;
            word-break: break-all;
        }}

        .token-reward {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-top: 10px;
            font-weight: 600;
            color: #fbbf24;
        }}

        footer {{
            text-align: center;
            margin-top: 60px;
            color: #64748b;
            font-size: 0.875rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>FinChain Analysis Report</h1>
            <div class="meta">Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | Query: "{query}"</div>
        </header>

        <div class="card">
            <div class="card-header">
                <div class="card-title">🏆 Winning Analysis</div>
                <div class="winner-badge">
                    <span>★</span> {winner}
                </div>
            </div>
            <div class="report-content">{report_content}</div>
        </div>

        <div class="card">
            <div class="card-header">
                <div class="card-title">⚖️ Auditor's Verdict</div>
            </div>
            <div class="audit-section">
                <strong>Why this report won:</strong><br>
                {audit_reason}
            </div>
        </div>

        <div class="card">
            <div class="card-header">
                <div class="card-title">🔗 Blockchain & Rewards</div>
            </div>
            <div class="blockchain-info">
                BLOCK HASH: {block_hash}
            </div>
            <div class="token-reward">
                <span>💰</span> {rewards}
            </div>
        </div>

        <footer>
            <p>Decentralized Traceable Financial Analysis Network (FinChain-Agent)</p>
        </footer>
    </div>
</body>
</html>
"""
    with open(filename, "w") as f:
        f.write(html_template)
    return os.path.abspath(filename)
