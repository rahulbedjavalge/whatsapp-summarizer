#!/usr/bin/env python3
"""
Quick test script to verify WhatsApp Chat Analyzer functionality
"""

import os
import tempfile
from datetime import datetime

# Import our modules
from whatsapp_parser import WhatsAppParser
from chat_analyzer import ChatAnalyzer
from chat_visualizer import ChatVisualizer
from report_generator import ReportGenerator

def create_sample_chat():
    """Create a sample WhatsApp chat for testing"""
    sample_chat = """
1/15/2024, 10:30 AM - Alice: Hey everyone! How are you doing?
1/15/2024, 10:32 AM - Bob: Great! Working on the project
1/15/2024, 10:35 AM - Charlie: Same here, almost done with my part
1/15/2024, 11:00 AM - Alice: Awesome! Can we meet tomorrow?
1/15/2024, 11:05 AM - Bob: Sure, what time works for everyone?
1/15/2024, 11:10 AM - Charlie: How about 2 PM?
1/15/2024, 11:15 AM - Alice: Perfect! See you then 😊
1/15/2024, 11:20 AM - Bob: Looking forward to it!
1/16/2024, 2:00 PM - Alice: Hi everyone, ready for the meeting?
1/16/2024, 2:02 PM - Charlie: Yes! Let's start
1/16/2024, 2:05 PM - Bob: Great presentation today Alice!
1/16/2024, 2:10 PM - Alice: Thanks! Team work makes the dream work
1/16/2024, 2:15 PM - Charlie: Agreed! This project is going well
1/16/2024, 2:20 PM - Bob: Should we celebrate when we finish?
1/16/2024, 2:25 PM - Alice: Definitely! Pizza party? 🍕
1/16/2024, 2:30 PM - Charlie: Count me in! I love pizza
1/16/2024, 2:35 PM - Bob: Me too! Let's plan it for Friday
1/16/2024, 2:40 PM - Alice: Friday it is! Can't wait
"""
    return sample_chat.strip()

def test_analyzer():
    """Test the complete analysis pipeline"""
    print("🧪 Testing WhatsApp Chat Analyzer...")
    print("=" * 50)
    
    try:
        # Create temporary chat file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as tmp_file:
            tmp_file.write(create_sample_chat())
            tmp_file_path = tmp_file.name
        
        print(f"📝 Created sample chat file: {tmp_file_path}")
        
        # Initialize components
        print("🔧 Initializing components...")
        parser = WhatsAppParser()
        analyzer = ChatAnalyzer()
        visualizer = ChatVisualizer()
        report_gen = ReportGenerator("test_reports")
        
        # Parse chat
        print("📖 Parsing chat file...")
        df = parser.parse_chat_file(tmp_file_path)
        
        if df.empty:
            print("❌ Error: Could not parse chat file")
            return False
        
        print(f"✅ Successfully parsed {len(df)} messages from {df['user'].nunique()} users")
        
        # Analyze
        print("🧠 Analyzing chat patterns...")
        activity_analysis = analyzer.analyze_activity(df)
        topic_analysis = analyzer.extract_topics(df, 3)
        sentiment_analysis = analyzer.analyze_sentiment(df)
        summary = analyzer.generate_summary(df, activity_analysis, topic_analysis, sentiment_analysis)
        
        print("✅ Analysis complete!")
        
        # Generate report
        print("📄 Generating test report...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Generate HTML report
        html_path = report_gen.generate_html_report(
            activity_analysis, topic_analysis, sentiment_analysis, summary,
            filename=f'test_report_{timestamp}.html'
        )
        
        # Generate JSON report
        json_path = report_gen.generate_json_report(
            activity_analysis, topic_analysis, sentiment_analysis, summary,
            filename=f'test_analysis_{timestamp}.json'
        )
        
        print(f"✅ HTML report saved to: {html_path}")
        print(f"✅ JSON report saved to: {json_path}")
        
        # Display summary
        print("\n📋 Analysis Summary:")
        print("-" * 30)
        print(summary)
        
        # Cleanup
        os.unlink(tmp_file_path)
        
        print("\n🎉 All tests passed! The analyzer is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_analyzer()
    exit(0 if success else 1)
