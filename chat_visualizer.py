import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from wordcloud import WordCloud
from collections import Counter
import calendar

class ChatVisualizer:
    """Create visualizations for chat analysis"""
    
    def __init__(self):
        # Set style
        plt.style.use('default')
        sns.set_palette("husl")
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    def create_user_activity_chart(self, activity_analysis: dict, save_path: str = None) -> go.Figure:
        """Create bar chart of user activity"""
        top_users = activity_analysis['top_users']
        
        if not top_users:
            return None
        
        users = list(top_users.keys())[:10]
        message_counts = [top_users[user]['message_count'] for user in users]
        
        fig = go.Figure(data=[
            go.Bar(
                x=users,
                y=message_counts,
                marker_color='#25D366',
                text=message_counts,
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Most Active Users",
            xaxis_title="Users",
            yaxis_title="Number of Messages",
            template="plotly_white",
            height=500
        )
        
        fig.update_xaxes(tickangle=45)
        
        if save_path:
            fig.write_html(save_path)
        
        return fig
    
    def create_hourly_heatmap(self, df: pd.DataFrame, save_path: str = None) -> go.Figure:
        """Create heatmap of message activity by hour and day"""
        if df.empty:
            return None
        
        # Create hour-day matrix
        df['day_name'] = df['timestamp'].dt.day_name()
        hourly_data = df.groupby(['day_name', 'hour']).size().reset_index(name='count')
        
        # Create pivot table
        heatmap_data = hourly_data.pivot(index='day_name', columns='hour', values='count').fillna(0)
        
        # Reorder days
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_data = heatmap_data.reindex(day_order)
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=list(range(24)),
            y=day_order,
            colorscale='Greens',
            hoverongaps=False,
            colorbar=dict(title="Messages")
        ))
        
        fig.update_layout(
            title="Message Activity Heatmap (Hour vs Day)",
            xaxis_title="Hour of Day",
            yaxis_title="Day of Week",
            template="plotly_white",
            height=400
        )
        
        if save_path:
            fig.write_html(save_path)
        
        return fig
    
    def create_daily_timeline(self, df: pd.DataFrame, save_path: str = None) -> go.Figure:
        """Create timeline of daily message counts"""
        if df.empty:
            return None
        
        daily_counts = df.groupby('date').size().reset_index(name='count')
        daily_counts['date'] = pd.to_datetime(daily_counts['date'])
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=daily_counts['date'],
            y=daily_counts['count'],
            mode='lines+markers',
            name='Daily Messages',
            line=dict(color='#25D366', width=2),
            marker=dict(size=6)
        ))
        
        # Add trend line
        z = np.polyfit(range(len(daily_counts)), daily_counts['count'], 1)
        trend_line = np.poly1d(z)(range(len(daily_counts)))
        
        fig.add_trace(go.Scatter(
            x=daily_counts['date'],
            y=trend_line,
            mode='lines',
            name='Trend',
            line=dict(color='red', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title="Daily Message Activity Over Time",
            xaxis_title="Date",
            yaxis_title="Number of Messages",
            template="plotly_white",
            height=400
        )
        
        if save_path:
            fig.write_html(save_path)
        
        return fig
    
    def create_wordcloud(self, df: pd.DataFrame, save_path: str = None) -> str:
        """Create word cloud from messages"""
        if df.empty:
            return None
        
        # Combine all clean messages
        text = ' '.join(df['clean_message'].dropna())
        
        if not text.strip():
            return None
        
        # Create word cloud
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            max_words=100,
            colormap='Set3',
            relative_scaling=0.5
        ).generate(text)
        
        # Create matplotlib figure
        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Most Common Words', fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout(pad=0)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return save_path
    
    def create_sentiment_timeline(self, sentiment_analysis: dict, save_path: str = None) -> go.Figure:
        """Create sentiment timeline"""
        daily_sentiment = sentiment_analysis.get('daily_sentiment_trends', {})
        
        if not daily_sentiment:
            return None
        
        dates = list(daily_sentiment.keys())
        scores = list(daily_sentiment.values())
        
        # Convert string dates to datetime
        dates = pd.to_datetime(dates)
        
        fig = go.Figure()
        
        # Color based on sentiment
        colors = ['red' if score < -0.1 else 'green' if score > 0.1 else 'gray' for score in scores]
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=scores,
            mode='lines+markers',
            name='Daily Sentiment',
            line=dict(color='blue', width=2),
            marker=dict(size=8, color=colors)
        ))
        
        # Add neutral line
        fig.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Neutral")
        
        fig.update_layout(
            title="Daily Sentiment Trends",
            xaxis_title="Date",
            yaxis_title="Sentiment Score",
            template="plotly_white",
            height=400,
            yaxis=dict(range=[-1, 1])
        )
        
        if save_path:
            fig.write_html(save_path)
        
        return fig
    
    def create_sentiment_distribution(self, sentiment_analysis: dict, save_path: str = None) -> go.Figure:
        """Create pie chart of sentiment distribution"""
        sentiment_dist = sentiment_analysis.get('sentiment_distribution', {})
        
        if not sentiment_dist:
            return None
        
        labels = list(sentiment_dist.keys())
        values = list(sentiment_dist.values())
        colors = ['#00ff00', '#ff0000', '#808080']  # Green, Red, Gray
        
        fig = go.Figure(data=[go.Pie(
            labels=[label.capitalize() for label in labels],
            values=values,
            marker_colors=colors,
            textinfo='label+percent',
            textfont_size=12
        )])
        
        fig.update_layout(
            title="Sentiment Distribution",
            template="plotly_white",
            height=400
        )
        
        if save_path:
            fig.write_html(save_path)
        
        return fig
    
    def create_weekly_pattern(self, activity_analysis: dict, save_path: str = None) -> go.Figure:
        """Create bar chart of weekly activity pattern"""
        weekly_pattern = activity_analysis.get('weekly_pattern', {})
        
        if not weekly_pattern:
            return None
        
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        values = [weekly_pattern.get(day, 0) for day in days]
        
        fig = go.Figure(data=[
            go.Bar(
                x=days,
                y=values,
                marker_color=['#ff9999' if day in ['Saturday', 'Sunday'] else '#66b3ff' for day in days],
                text=values,
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Weekly Activity Pattern",
            xaxis_title="Day of Week",
            yaxis_title="Number of Messages",
            template="plotly_white",
            height=400
        )
        
        if save_path:
            fig.write_html(save_path)
        
        return fig
    
    def create_user_comparison(self, activity_analysis: dict, save_path: str = None) -> go.Figure:
        """Create comparison chart of top users with multiple metrics"""
        top_users = activity_analysis['top_users']
        
        if not top_users:
            return None
        
        users = list(top_users.keys())[:8]
        message_counts = [top_users[user]['message_count'] for user in users]
        avg_lengths = [top_users[user]['avg_message_length'] for user in users]
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Message Count', 'Average Message Length'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Message count
        fig.add_trace(
            go.Bar(x=users, y=message_counts, name="Messages", marker_color='#25D366'),
            row=1, col=1
        )
        
        # Average message length
        fig.add_trace(
            go.Bar(x=users, y=avg_lengths, name="Avg Length", marker_color='#128C7E'),
            row=1, col=2
        )
        
        fig.update_layout(
            title="User Activity Comparison",
            template="plotly_white",
            height=500,
            showlegend=False
        )
        
        fig.update_xaxes(tickangle=45)
        
        if save_path:
            fig.write_html(save_path)
        
        return fig
