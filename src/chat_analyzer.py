import pandas as pd
import numpy as np
from collections import Counter
from datetime import datetime, timedelta
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
from typing import Dict, List, Tuple

class ChatAnalyzer:
    """Comprehensive chat analysis including activity, topics, and sentiment"""
    
    def __init__(self):
        self.setup_nltk()
        self.lemmatizer = WordNetLemmatizer()
        self.vader_analyzer = SentimentIntensityAnalyzer()
        
    def setup_nltk(self):
        """Download required NLTK data"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
            
        try:
            nltk.data.find('tokenizers/punkt_tab')
        except LookupError:
            nltk.download('punkt_tab')
            
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
            
        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('wordnet')
    
    def analyze_activity(self, df: pd.DataFrame) -> Dict:
        """Analyze user activity patterns"""
        analysis = {}
        
        # Basic stats
        analysis['total_messages'] = len(df)
        analysis['total_users'] = df['user'].nunique()
        analysis['date_range'] = {
            'start': df['timestamp'].min().strftime('%Y-%m-%d'),
            'end': df['timestamp'].max().strftime('%Y-%m-%d'),
            'days': (df['timestamp'].max() - df['timestamp'].min()).days + 1
        }
        
        # Top active users
        user_stats = df.groupby('user').agg({
            'message': 'count',
            'message_length': ['mean', 'sum']
        }).round(2)
        user_stats.columns = ['message_count', 'avg_message_length', 'total_characters']
        user_stats = user_stats.sort_values('message_count', ascending=False)
        
        analysis['top_users'] = user_stats.head(10).to_dict('index')
        
        # Daily activity
        daily_activity = df.groupby('date')['message'].count()
        analysis['most_active_day'] = {
            'date': str(daily_activity.idxmax()),
            'messages': int(daily_activity.max())
        }
        
        # Hourly activity
        hourly_activity = df.groupby('hour')['message'].count()
        analysis['peak_hour'] = {
            'hour': int(hourly_activity.idxmax()),
            'messages': int(hourly_activity.max())
        }
        
        # Weekly patterns
        weekly_activity = df.groupby('day_of_week')['message'].count()
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekly_activity = weekly_activity.reindex(day_order)
        analysis['weekly_pattern'] = weekly_activity.to_dict()
        
        # Average messages per day
        analysis['avg_messages_per_day'] = round(
            analysis['total_messages'] / analysis['date_range']['days'], 2
        )
        
        return analysis
    
    def extract_topics(self, df: pd.DataFrame, n_topics: int = 5) -> Dict:
        """Extract key topics using TF-IDF and LDA"""
        # Combine all messages
        all_text = ' '.join(df['clean_message'].dropna())
        
        # Preprocess text
        processed_text = self._preprocess_for_topics(all_text)
        
        if not processed_text:
            return {'topics': [], 'keywords': []}
        
        # Split into documents (each message as a document)
        documents = df['clean_message'].dropna().apply(self._preprocess_for_topics)
        documents = [doc for doc in documents if doc]
        
        if len(documents) < 2:
            return {'topics': [], 'keywords': []}
        
        # TF-IDF for keywords
        try:
            tfidf = TfidfVectorizer(
                max_features=100,
                stop_words='english',
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.8
            )
            tfidf_matrix = tfidf.fit_transform(documents)
            
            # Get feature names and scores
            feature_names = tfidf.get_feature_names_out()
            scores = tfidf_matrix.sum(axis=0).A1
            
            # Top keywords
            keyword_scores = list(zip(feature_names, scores))
            keyword_scores.sort(key=lambda x: x[1], reverse=True)
            top_keywords = keyword_scores[:20]
            
            # LDA for topics
            lda = LatentDirichletAllocation(
                n_components=min(n_topics, len(documents)//2),
                random_state=42,
                max_iter=10
            )
            lda.fit(tfidf_matrix)
              # Extract topics
            topics = []
            feature_names = tfidf.get_feature_names_out()
            
            for topic_idx, topic in enumerate(lda.components_):
                top_words = [feature_names[i] for i in topic.argsort()[-10:][::-1]]
                topics.append({
                    'topic_id': topic_idx,
                    'keywords': top_words,
                    'weight': float(topic.max())
                })
            
            return {
                'topics': topics,
                'keywords': [{'word': word, 'score': float(score)} for word, score in top_keywords]
            }
            
        except Exception as e:
            print(f"Topic extraction error: {e}")
            return {'topics': [], 'keywords': []}
    
    def analyze_sentiment(self, df: pd.DataFrame) -> Dict:
        """Analyze sentiment of messages"""
        sentiments = []
        valid_indices = []
        
        # Process each message and keep track of valid indices
        for idx, message in enumerate(df['clean_message']):
            if pd.notna(message) and len(str(message).strip()) > 0:
                try:
                    # TextBlob sentiment
                    blob = TextBlob(str(message))
                    textblob_sentiment = {
                        'polarity': blob.sentiment.polarity,
                        'subjectivity': blob.sentiment.subjectivity
                    }
                    
                    # VADER sentiment
                    vader_scores = self.vader_analyzer.polarity_scores(str(message))
                    
                    sentiments.append({
                        'textblob_polarity': textblob_sentiment['polarity'],
                        'textblob_subjectivity': textblob_sentiment['subjectivity'],
                        'vader_positive': vader_scores['pos'],
                        'vader_negative': vader_scores['neg'],
                        'vader_neutral': vader_scores['neu'],
                        'vader_compound': vader_scores['compound']
                    })
                    valid_indices.append(idx)
                except Exception as e:
                    print(f"Error processing message at index {idx}: {e}")
                    continue
        
        if not sentiments:
            return {'overall_sentiment': 'Neutral', 'sentiment_distribution': {}, 'daily_sentiment_trends': {}, 'statistics': {}}
        
        # Convert to DataFrame for analysis
        sentiment_df = pd.DataFrame(sentiments)
        
        # Overall sentiment analysis
        avg_compound = sentiment_df['vader_compound'].mean()
        
        if avg_compound >= 0.05:
            overall_sentiment = 'Positive'
        elif avg_compound <= -0.05:
            overall_sentiment = 'Negative'
        else:
            overall_sentiment = 'Neutral'
        
        # Sentiment distribution
        positive_count = len(sentiment_df[sentiment_df['vader_compound'] >= 0.05])
        negative_count = len(sentiment_df[sentiment_df['vader_compound'] <= -0.05])
        neutral_count = len(sentiment_df) - positive_count - negative_count
        
        total = len(sentiment_df)
        sentiment_distribution = {
            'positive': round((positive_count / total) * 100, 2),
            'negative': round((negative_count / total) * 100, 2),
            'neutral': round((neutral_count / total) * 100, 2)
        }
        
        # Daily sentiment trends - only use valid messages
        sentiment_trends = {}
        try:
            if len(df) > 0 and len(valid_indices) > 0:
                # Create a temporary dataframe with only valid sentiment messages
                valid_df = df.iloc[valid_indices].copy()
                valid_df['sentiment_score'] = sentiment_df['vader_compound'].values
                
                if not valid_df.empty:
                    daily_sentiment = valid_df.groupby('date')['sentiment_score'].mean()
                    sentiment_trends = {str(k): float(v) for k, v in daily_sentiment.to_dict().items()}
                    
                    most_positive_day = str(daily_sentiment.idxmax()) if not daily_sentiment.empty else None
                    most_negative_day = str(daily_sentiment.idxmin()) if not daily_sentiment.empty else None
                else:
                    most_positive_day = None
                    most_negative_day = None
            else:
                most_positive_day = None
                most_negative_day = None
        except Exception as e:
            print(f"Error calculating daily sentiment trends: {e}")
            sentiment_trends = {}
            most_positive_day = None
            most_negative_day = None
        
        return {
            'overall_sentiment': overall_sentiment,
            'average_compound_score': round(avg_compound, 3),
            'sentiment_distribution': sentiment_distribution,
            'daily_sentiment_trends': sentiment_trends,            'statistics': {
                'avg_polarity': round(sentiment_df['textblob_polarity'].mean(), 3),
                'avg_subjectivity': round(sentiment_df['textblob_subjectivity'].mean(), 3),
                'most_positive_day': most_positive_day,
                'most_negative_day': most_negative_day
            }
        }
    
    def generate_summary(self, df: pd.DataFrame, activity_analysis: Dict, topic_analysis: Dict, sentiment_analysis: Dict) -> str:
        """Generate a human-readable summary with detailed narrative"""
        if len(df) == 0:
            return "No messages found to analyze."
        
        # Basic stats
        total_messages = activity_analysis['total_messages']
        total_users = activity_analysis['total_users']
        date_range = activity_analysis['date_range']
        
        # Generate detailed narrative summary
        narrative_summary = self._generate_narrative_summary(df, topic_analysis, sentiment_analysis)
        
        # Format basic stats with line breaks
        summary = f"""📊 **GROUP OVERVIEW**
This WhatsApp group had {total_messages:,} messages from {total_users} participants between {date_range['start']} and {date_range['end']} ({date_range['days']} days).

👥 **MOST ACTIVE MEMBERS**
{self._format_top_users(activity_analysis['top_users'])}

📈 **ACTIVITY PATTERNS**
Peak activity was at {activity_analysis['peak_hour']['hour']:02d}:00 hours, with the busiest day being {activity_analysis['most_active_day']['date']}.
The group averaged {activity_analysis['avg_messages_per_day']} messages per day.

🔥 **KEY TOPICS & DISCUSSIONS**
{self._format_topics_summary(topic_analysis, df)}

😊 **OVERALL MOOD & SENTIMENT**
{sentiment_analysis['overall_sentiment']} ({sentiment_analysis['sentiment_distribution']['positive']:.1f}% positive, {sentiment_analysis['sentiment_distribution']['negative']:.1f}% negative, {sentiment_analysis['sentiment_distribution']['neutral']:.1f}% neutral).

💬 **WHAT'S HAPPENING IN THE CHAT**
{narrative_summary}"""
        
        return summary
    
    def _format_top_users(self, top_users: Dict) -> str:
        """Format top users information"""
        if not top_users:
            return "No active users found."
        
        user_lines = []
        for i, (user, stats) in enumerate(list(top_users.items())[:5], 1):
            # Clean up phone numbers for display
            display_name = user
            if user.startswith('+') and len(user) > 10:
                display_name = f"User {user[-4:]}"  # Show last 4 digits
            
            user_lines.append(f"{i}. {display_name}: {stats['message_count']} messages (avg {stats['avg_message_length']:.1f} chars)")
        
        return "\n".join(user_lines)
    
    def _format_topics_summary(self, topic_analysis: Dict, df: pd.DataFrame) -> str:
        """Generate detailed topics summary"""
        if not topic_analysis.get('keywords'):
            return "No specific topics identified."
        
        top_keywords = topic_analysis['keywords'][:8]
        topic_summary = []
        
        # Group keywords by relevance
        high_relevance = [kw for kw in top_keywords if kw['score'] > 0.15]
        medium_relevance = [kw for kw in top_keywords if 0.05 < kw['score'] <= 0.15]
        
        if high_relevance:
            topic_summary.append(f"Primary topics: {', '.join([kw['word'] for kw in high_relevance])}")
        
        if medium_relevance:
            topic_summary.append(f"Secondary topics: {', '.join([kw['word'] for kw in medium_relevance])}")
        
        return "\n".join(topic_summary) if topic_summary else "Various general discussions"
    
    def _generate_narrative_summary(self, df: pd.DataFrame, topic_analysis: Dict, sentiment_analysis: Dict) -> str:
        """Generate a narrative summary of what's happening in the chat"""
        try:
            narrative_parts = []
            
            # Analyze message content patterns
            if not df.empty and 'message' in df.columns:
                # Get sample messages for context (avoiding phone numbers)
                sample_messages = df[df['message'].str.len() > 20]['message'].head(10).tolist()
                
                # Analyze common themes from keywords
                keywords = topic_analysis.get('keywords', [])
                if keywords:
                    primary_topics = [kw['word'] for kw in keywords[:3]]
                    
                    # Generate context based on topics
                    if any(word in ['visa', 'student', 'university', 'study'] for word in primary_topics):
                        narrative_parts.append("The group appears to be focused on student/visa related discussions and educational matters.")
                    
                    elif any(word in ['work', 'job', 'office', 'meeting', 'project'] for word in primary_topics):
                        narrative_parts.append("This seems to be a work-related group discussing professional matters and projects.")
                    
                    elif any(word in ['family', 'home', 'kids', 'mom', 'dad'] for word in primary_topics):
                        narrative_parts.append("The group appears to be a family chat sharing daily life updates and family matters.")
                    
                    elif any(word in ['game', 'play', 'fun', 'party', 'friends'] for word in primary_topics):
                        narrative_parts.append("This looks like a social group focused on entertainment and friendship activities.")
                    
                    else:
                        # Generic description based on top topics
                        if len(primary_topics) >= 2:
                            narrative_parts.append(f"The main discussions revolve around {primary_topics[0]} and {primary_topics[1]} related topics.")
                
                # Analyze communication patterns
                if len(df) > 100:
                    narrative_parts.append("This is an active group with regular ongoing conversations.")
                elif len(df) > 50:
                    narrative_parts.append("The group has moderate activity with periodic discussions.")
                else:
                    narrative_parts.append("This appears to be a smaller or newer group with limited activity.")
                
                # Sentiment context
                sentiment_dist = sentiment_analysis.get('sentiment_distribution', {})
                if sentiment_dist.get('positive', 0) > 50:
                    narrative_parts.append("The overall tone is quite positive and upbeat.")
                elif sentiment_dist.get('negative', 0) > 30:
                    narrative_parts.append("There are some concerns or frustrations being discussed.")
                else:
                    narrative_parts.append("The conversations maintain a neutral, informational tone.")
                
                # Activity timing context
                narrative_parts.append("Members are most active during afternoon hours, suggesting this might be a casual discussion group.")
            
            return " ".join(narrative_parts) if narrative_parts else "The group contains general conversations and interactions between members."
            
        except Exception as e:
            return f"Unable to generate detailed narrative summary due to: {str(e)}"
    
    def _preprocess_for_topics(self, text: str) -> str:
        """Preprocess text for topic extraction"""
        if not text or pd.isna(text):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and short words
        stop_words = set(stopwords.words('english'))
        stop_words.update(['group', 'chat', 'message', 'whatsapp', 'lol', 'haha', 'ok', 'okay', 'yes', 'no'])
        
        tokens = [token for token in tokens if token not in stop_words and len(token) > 2]
        
        # Lemmatize
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        
        return ' '.join(tokens)
