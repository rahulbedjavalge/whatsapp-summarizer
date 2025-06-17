import streamlit as st
import pandas as pd
import os
import sys
import tempfile
from datetime import datetime
import plotly.graph_objects as go

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import our custom modules
from whatsapp_parser import WhatsAppParser
from chat_analyzer import ChatAnalyzer
from chat_visualizer import ChatVisualizer
from report_generator import ReportGenerator

# Page configuration
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #25D366 0%, #128C7E 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #25D366;
    }
    
    .stProgress .st-emotion-cache-1e6y48t {
        background-color: #25D366;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>📱 WhatsApp Chat Analyzer</h1>
        <p>Upload your WhatsApp group chat export and get comprehensive insights!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🛠️ Configuration")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload WhatsApp Chat Export (.txt)",
            type=['txt'],
            help="Export your WhatsApp chat by going to Group Info > Export Chat > Without Media"
        )
        
        st.markdown("---")
        
        # Analysis options
        st.subheader("Analysis Options")
        
        n_topics = st.slider("Number of Topics", 3, 10, 5)
        include_visualizations = st.checkbox("Generate Visualizations", True)
        include_wordcloud = st.checkbox("Generate Word Cloud", True)
        
        # Report format
        st.subheader("Report Format")
        report_format = st.selectbox(
            "Choose Output Format",
            ["Interactive Dashboard", "HTML Report", "JSON Report", "Text Summary"]
        )
    
    if uploaded_file is not None:
        # Process the uploaded file
        with st.spinner("🔄 Processing your chat file..."):
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            try:
                # Initialize components
                parser = WhatsAppParser()
                analyzer = ChatAnalyzer()
                visualizer = ChatVisualizer()
                report_gen = ReportGenerator()
                
                # Parse the chat
                df = parser.parse_chat_file(tmp_file_path)
                
                if df.empty:
                    st.error("❌ Could not parse the chat file. Please make sure it's a valid WhatsApp export.")
                    return
                
                st.success(f"✅ Successfully parsed {len(df)} messages!")
                
                # Perform analysis
                with st.spinner("🧠 Analyzing chat patterns..."):
                    activity_analysis = analyzer.analyze_activity(df)
                    topic_analysis = analyzer.extract_topics(df, n_topics)
                    sentiment_analysis = analyzer.analyze_sentiment(df)
                    summary = analyzer.generate_summary(df, activity_analysis, topic_analysis, sentiment_analysis)
                
                # Display results based on selected format
                if report_format == "Interactive Dashboard":
                    display_interactive_dashboard(df, activity_analysis, topic_analysis, sentiment_analysis, summary, visualizer, include_visualizations, include_wordcloud)
                
                elif report_format == "HTML Report":
                    html_path = report_gen.generate_html_report(activity_analysis, topic_analysis, sentiment_analysis, summary)
                    st.success(f"✅ HTML report generated: {html_path}")
                    
                    with open(html_path, 'r', encoding='utf-8') as f:
                        html_content = f.read()
                    
                    st.download_button(
                        label="📥 Download HTML Report",
                        data=html_content,
                        file_name=f"whatsapp_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                        mime="text/html"
                    )
                
                elif report_format == "JSON Report":
                    json_path = report_gen.generate_json_report(activity_analysis, topic_analysis, sentiment_analysis, summary)
                    
                    with open(json_path, 'r', encoding='utf-8') as f:
                        json_content = f.read()
                    
                    st.download_button(
                        label="📥 Download JSON Report",
                        data=json_content,
                        file_name=f"whatsapp_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                    
                    st.json(json_content)
                
                elif report_format == "Text Summary":
                    text_path = report_gen.generate_text_report(activity_analysis, topic_analysis, sentiment_analysis, summary)
                    
                    with open(text_path, 'r', encoding='utf-8') as f:
                        text_content = f.read()
                    
                    st.download_button(
                        label="📥 Download Text Report",
                        data=text_content,
                        file_name=f"whatsapp_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
                    
                    st.text_area("Summary Report", text_content, height=400)
                
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
            
            finally:
                # Clean up temporary file
                if os.path.exists(tmp_file_path):
                    os.unlink(tmp_file_path)
    
    else:
        # Instructions
        st.markdown("""
        ## 📋 How to Use
        
        1. **Export your WhatsApp chat:**
           - Open the group chat in WhatsApp
           - Tap on the group name
           - Select "Export Chat"
           - Choose "Without Media"
           
        2. **Upload the .txt file** using the file uploader in the sidebar
        
        3. **Configure analysis options** in the sidebar
        
        4. **Choose your preferred report format**
        
        5. **Analyze!** The app will process your chat and generate insights
        
        ## 🔒 Privacy Notice
        All processing happens locally on your device. Your chat data is not stored or transmitted anywhere.
        
        ## 📊 What You'll Get
        - **Activity Analysis**: Message counts, active users, peak times
        - **Topic Extraction**: Key themes and popular keywords
        - **Sentiment Analysis**: Overall mood and emotional trends
        - **Visualizations**: Charts, graphs, and word clouds
        - **Summary Report**: Human-readable insights
        """)

def display_interactive_dashboard(df, activity_analysis, topic_analysis, sentiment_analysis, summary, visualizer, include_visualizations, include_wordcloud):
    """Display interactive dashboard with all analysis results"""
      # Executive Summary
    st.header("📊 Executive Summary")
    st.markdown(summary)
    
    # Key Metrics
    st.header("📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Messages", f"{activity_analysis['total_messages']:,}")
    
    with col2:
        st.metric("Active Users", activity_analysis['total_users'])
    
    with col3:
        st.metric("Days Active", activity_analysis['date_range']['days'])
    
    with col4:
        st.metric("Avg Messages/Day", activity_analysis['avg_messages_per_day'])
    
    # Activity Analysis
    st.header("👥 Activity Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top Contributors")
        top_users_df = pd.DataFrame.from_dict(activity_analysis['top_users'], orient='index')
        st.dataframe(top_users_df.head(10))
    
    with col2:
        st.subheader("Peak Activity")
        st.write(f"**Most Active Day:** {activity_analysis['most_active_day']['date']}")
        st.write(f"**Peak Hour:** {activity_analysis['peak_hour']['hour']:02d}:00")
    
    # Visualizations
    if include_visualizations:
        st.header("📊 Visualizations")
        
        # User activity chart
        fig_users = visualizer.create_user_activity_chart(activity_analysis)
        if fig_users:
            st.plotly_chart(fig_users, use_container_width=True)
        
        # Create tabs for different visualizations
        tab1, tab2, tab3, tab4 = st.tabs(["Timeline", "Heatmap", "Weekly Pattern", "Sentiment"])
        
        with tab1:
            fig_timeline = visualizer.create_daily_timeline(df)
            if fig_timeline:
                st.plotly_chart(fig_timeline, use_container_width=True)
        
        with tab2:
            fig_heatmap = visualizer.create_hourly_heatmap(df)
            if fig_heatmap:
                st.plotly_chart(fig_heatmap, use_container_width=True)
        
        with tab3:
            fig_weekly = visualizer.create_weekly_pattern(activity_analysis)
            if fig_weekly:
                st.plotly_chart(fig_weekly, use_container_width=True)
        
        with tab4:
            col1, col2 = st.columns(2)
            
            with col1:
                fig_sentiment_dist = visualizer.create_sentiment_distribution(sentiment_analysis)
                if fig_sentiment_dist:
                    st.plotly_chart(fig_sentiment_dist, use_container_width=True)
            
            with col2:
                fig_sentiment_timeline = visualizer.create_sentiment_timeline(sentiment_analysis)
                if fig_sentiment_timeline:
                    st.plotly_chart(fig_sentiment_timeline, use_container_width=True)
    
    # Word Cloud
    if include_wordcloud:
        st.header("☁️ Word Cloud")
        try:
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                wordcloud_path = visualizer.create_wordcloud(df, tmp.name)
                if wordcloud_path:
                    st.image(wordcloud_path)
                    os.unlink(wordcloud_path)
        except Exception as e:
            st.warning(f"Could not generate word cloud: {str(e)}")
    
    # Topics Analysis
    st.header("🔥 Topics & Keywords")
    
    if topic_analysis.get('keywords'):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top Keywords")
            keywords_df = pd.DataFrame(topic_analysis['keywords'][:15])
            keywords_df['score'] = keywords_df['score'].round(3)
            st.dataframe(keywords_df, use_container_width=True)
        
        with col2:
            st.subheader("Keyword Cloud")
            keywords_text = " ".join([kw['word'] for kw in topic_analysis['keywords'][:30]])
            st.write(keywords_text)
    
    # Sentiment Analysis
    st.header("😊 Sentiment Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Overall Sentiment", sentiment_analysis['overall_sentiment'])
    
    with col2:
        st.metric("Positive %", f"{sentiment_analysis['sentiment_distribution']['positive']:.1f}%")
    
    with col3:
        st.metric("Negative %", f"{sentiment_analysis['sentiment_distribution']['negative']:.1f}%")
    
    # Raw Data Preview
    with st.expander("📋 Raw Data Preview"):
        st.dataframe(df.head(100))

if __name__ == "__main__":
    main()
