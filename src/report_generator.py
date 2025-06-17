import json
import os
from datetime import datetime
from typing import Dict, Any

class ReportGenerator:
    """Generate comprehensive reports in multiple formats"""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_json_report(self, 
                           activity_analysis: Dict, 
                           topic_analysis: Dict, 
                           sentiment_analysis: Dict,
                           summary: str,
                           filename: str = None) -> str:
        """Generate comprehensive JSON report"""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"whatsapp_analysis_{timestamp}.json"
        
        report = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "report_type": "WhatsApp Chat Analysis",
                "version": "1.0"
            },
            "summary": summary,
            "activity_analysis": activity_analysis,
            "topic_analysis": topic_analysis,
            "sentiment_analysis": sentiment_analysis
        }
        
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        return filepath
    
    def generate_html_report(self,
                           activity_analysis: Dict,
                           topic_analysis: Dict,
                           sentiment_analysis: Dict,
                           summary: str,
                           visualizations: Dict = None,
                           filename: str = None) -> str:
        """Generate HTML report with embedded visualizations"""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"whatsapp_report_{timestamp}.html"
        
        html_content = self._create_html_template(
            activity_analysis, topic_analysis, sentiment_analysis, summary, visualizations
        )
        
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filepath
    
    def generate_text_report(self,
                           activity_analysis: Dict,
                           topic_analysis: Dict,
                           sentiment_analysis: Dict,
                           summary: str,
                           filename: str = None) -> str:
        """Generate plain text report"""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"whatsapp_summary_{timestamp}.txt"
        
        report_lines = [
            "=" * 60,
            "WHATSAPP GROUP CHAT ANALYSIS REPORT",
            "=" * 60,
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "EXECUTIVE SUMMARY",
            "-" * 20,
            summary,
            "",
            "ACTIVITY STATISTICS",
            "-" * 20,
            f"Total Messages: {activity_analysis['total_messages']:,}",
            f"Total Users: {activity_analysis['total_users']}",
            f"Date Range: {activity_analysis['date_range']['start']} to {activity_analysis['date_range']['end']}",
            f"Duration: {activity_analysis['date_range']['days']} days",
            f"Average Messages/Day: {activity_analysis['avg_messages_per_day']}",
            "",
            "TOP CONTRIBUTORS",
            "-" * 20
        ]
        
        # Add top users
        for i, (user, stats) in enumerate(list(activity_analysis['top_users'].items())[:10], 1):
            report_lines.append(
                f"{i:2d}. {user}: {stats['message_count']} messages "
                f"(avg length: {stats['avg_message_length']:.1f} chars)"
            )
        
        report_lines.extend([
            "",
            "ACTIVITY PATTERNS",
            "-" * 20,
            f"Most Active Day: {activity_analysis['most_active_day']['date']} "
            f"({activity_analysis['most_active_day']['messages']} messages)",
            f"Peak Hour: {activity_analysis['peak_hour']['hour']:02d}:00 "
            f"({activity_analysis['peak_hour']['messages']} messages)",
            ""
        ])
        
        # Add weekly pattern
        report_lines.append("Weekly Pattern:")
        for day, count in activity_analysis['weekly_pattern'].items():
            report_lines.append(f"  {day}: {count} messages")
        
        # Add topics
        if topic_analysis.get('keywords'):
            report_lines.extend([
                "",
                "KEY TOPICS & KEYWORDS",
                "-" * 20
            ])
            
            for i, keyword in enumerate(topic_analysis['keywords'][:15], 1):
                report_lines.append(f"{i:2d}. {keyword['word']} (score: {keyword['score']:.3f})")
        
        # Add sentiment analysis
        report_lines.extend([
            "",
            "SENTIMENT ANALYSIS",
            "-" * 20,
            f"Overall Sentiment: {sentiment_analysis['overall_sentiment']}",
            f"Average Sentiment Score: {sentiment_analysis['average_compound_score']}",
            "",
            "Sentiment Distribution:",
            f"  Positive: {sentiment_analysis['sentiment_distribution']['positive']:.1f}%",
            f"  Negative: {sentiment_analysis['sentiment_distribution']['negative']:.1f}%",
            f"  Neutral: {sentiment_analysis['sentiment_distribution']['neutral']:.1f}%",
            ""
        ])
        
        if sentiment_analysis['statistics']['most_positive_day']:
            report_lines.append(f"Most Positive Day: {sentiment_analysis['statistics']['most_positive_day']}")
        if sentiment_analysis['statistics']['most_negative_day']:
            report_lines.append(f"Most Negative Day: {sentiment_analysis['statistics']['most_negative_day']}")
        
        report_lines.extend([
            "",
            "=" * 60,
            "End of Report",
            "=" * 60
        ])
        
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        
        return filepath
    
    def _create_html_template(self, activity_analysis: Dict, topic_analysis: Dict, 
                            sentiment_analysis: Dict, summary: str, visualizations: Dict = None) -> str:
        """Create HTML template for the report"""
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WhatsApp Chat Analysis Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 1.1em;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 40px;
            background: #f8f9fa;
            border-radius: 15px;
            padding: 25px;
            border-left: 5px solid #25D366;
        }}
        
        .section h2 {{
            color: #2c3e50;
            margin-top: 0;
            font-size: 1.5em;
            display: flex;
            align-items: center;
        }}
        
        .section h2::before {{
            content: "📊";
            margin-right: 10px;
            font-size: 1.2em;
        }}
        
        .summary {{
            background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
            border-left-color: #2196f3;
            font-size: 1.1em;
            line-height: 1.7;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #25D366;
        }}
        
        .stat-label {{
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }}
        
        .top-users {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        
        .user-card {{
            background: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        
        .user-name {{
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .user-stats {{
            color: #666;
            font-size: 0.9em;
        }}
        
        .keywords {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 20px 0;
        }}
        
        .keyword-tag {{
            background: #25D366;
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: 500;
        }}
        
        .sentiment-overview {{
            display: flex;
            justify-content: space-around;
            align-items: center;
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
        }}
        
        .sentiment-item {{
            text-align: center;
        }}
        
        .sentiment-value {{
            font-size: 1.5em;
            font-weight: bold;
        }}
        
        .positive {{ color: #4caf50; }}
        .negative {{ color: #f44336; }}
        .neutral {{ color: #9e9e9e; }}
        
        .timestamp {{
            text-align: center;
            color: #666;
            font-size: 0.9em;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📱 WhatsApp Chat Analysis</h1>
            <p>Comprehensive Group Chat Intelligence Report</p>
        </div>
        
        <div class="content">
            <div class="section summary">
                <h2>Executive Summary</h2>
                <p>{summary}</p>
            </div>
            
            <div class="section">
                <h2>Activity Statistics</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value">{activity_analysis['total_messages']:,}</div>
                        <div class="stat-label">Total Messages</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{activity_analysis['total_users']}</div>
                        <div class="stat-label">Active Users</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{activity_analysis['date_range']['days']}</div>
                        <div class="stat-label">Days Active</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{activity_analysis['avg_messages_per_day']}</div>
                        <div class="stat-label">Avg Messages/Day</div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>Top Contributors</h2>
                <div class="top-users">
        """
        
        # Add top users
        for user, stats in list(activity_analysis['top_users'].items())[:8]:
            html += f"""
                    <div class="user-card">
                        <div class="user-name">{user}</div>
                        <div class="user-stats">
                            {stats['message_count']} messages<br>
                            Avg: {stats['avg_message_length']:.1f} chars
                        </div>
                    </div>
            """
        
        html += """
                </div>
            </div>
        """
        
        # Add keywords section
        if topic_analysis.get('keywords'):
            html += f"""
            <div class="section">
                <h2>Key Topics & Keywords</h2>
                <div class="keywords">
            """
            for keyword in topic_analysis['keywords'][:20]:
                html += f'<span class="keyword-tag">{keyword["word"]}</span>'
            
            html += """
                </div>
            </div>
            """
        
        # Add sentiment section
        html += f"""
            <div class="section">
                <h2>Sentiment Analysis</h2>
                <div class="sentiment-overview">
                    <div class="sentiment-item">
                        <div class="sentiment-value positive">{sentiment_analysis['sentiment_distribution']['positive']:.1f}%</div>
                        <div>Positive</div>
                    </div>
                    <div class="sentiment-item">
                        <div class="sentiment-value neutral">{sentiment_analysis['sentiment_distribution']['neutral']:.1f}%</div>
                        <div>Neutral</div>
                    </div>
                    <div class="sentiment-item">
                        <div class="sentiment-value negative">{sentiment_analysis['sentiment_distribution']['negative']:.1f}%</div>
                        <div>Negative</div>
                    </div>
                </div>
                <p><strong>Overall Sentiment:</strong> {sentiment_analysis['overall_sentiment']}</p>
                <p><strong>Average Score:</strong> {sentiment_analysis['average_compound_score']}</p>
            </div>
        """
        
        html += f"""
            <div class="timestamp">
                Report generated on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}
            </div>
        </div>
    </div>
</body>
</html>
        """
        
        return html
