#!/usr/bin/env python3
"""
WhatsApp Chat Analyzer - Command Line Interface
A comprehensive tool for analyzing WhatsApp group chat exports
"""

import argparse
import os
import sys
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import our modules
from whatsapp_parser import WhatsAppParser
from chat_analyzer import ChatAnalyzer
from chat_visualizer import ChatVisualizer
from report_generator import ReportGenerator

def main():
    parser = argparse.ArgumentParser(
        description="Analyze WhatsApp group chat exports",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py chat.txt                          # Basic analysis
  python main.py chat.txt --format json           # JSON output
  python main.py chat.txt --topics 10 --viz       # With visualizations
  python main.py chat.txt --output reports/       # Custom output directory
        """
    )
    
    parser.add_argument(
        'input_file',
        help='Path to WhatsApp chat export (.txt file)'
    )
    
    parser.add_argument(
        '--format',
        choices=['text', 'json', 'html'],
        default='text',
        help='Output format (default: text)'
    )
    
    parser.add_argument(
        '--output',
        default='reports',
        help='Output directory (default: reports)'
    )
    
    parser.add_argument(
        '--topics',
        type=int,
        default=5,
        help='Number of topics to extract (default: 5)'
    )
    
    parser.add_argument(
        '--viz',
        action='store_true',
        help='Generate visualizations (saves as HTML files)'
    )
    
    parser.add_argument(
        '--wordcloud',
        action='store_true',
        help='Generate word cloud (saves as PNG)'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress progress messages'
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.input_file):
        print(f"❌ Error: File '{args.input_file}' not found.")
        sys.exit(1)
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    if not args.quiet:
        print("📱 WhatsApp Chat Analyzer")
        print("=" * 50)
        print(f"Input file: {args.input_file}")
        print(f"Output format: {args.format}")
        print(f"Output directory: {args.output}")
        print()
    
    try:
        # Initialize components
        if not args.quiet:
            print("🔧 Initializing components...")
        
        parser_obj = WhatsAppParser()
        analyzer = ChatAnalyzer()
        visualizer = ChatVisualizer()
        report_gen = ReportGenerator(args.output)
        
        # Parse chat file
        if not args.quiet:
            print("📖 Parsing chat file...")
        
        df = parser_obj.parse_chat_file(args.input_file)
        
        if df.empty:
            print("❌ Error: Could not parse any messages from the file.")
            print("Please ensure it's a valid WhatsApp chat export.")
            sys.exit(1)
        
        if not args.quiet:
            print(f"✅ Successfully parsed {len(df)} messages from {df['user'].nunique()} users")
            print()
        
        # Perform analysis
        if not args.quiet:
            print("🧠 Analyzing chat patterns...")
        
        activity_analysis = analyzer.analyze_activity(df)
        topic_analysis = analyzer.extract_topics(df, args.topics)
        sentiment_analysis = analyzer.analyze_sentiment(df)
        summary = analyzer.generate_summary(df, activity_analysis, topic_analysis, sentiment_analysis)
        
        if not args.quiet:
            print("✅ Analysis complete!")
            print()
        
        # Generate visualizations
        visualizations = {}
        if args.viz:
            if not args.quiet:
                print("📊 Generating visualizations...")
            
            # Generate and save visualizations
            viz_dir = os.path.join(args.output, 'visualizations')
            os.makedirs(viz_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # User activity chart
            fig_users = visualizer.create_user_activity_chart(activity_analysis)
            if fig_users:
                users_path = os.path.join(viz_dir, f'user_activity_{timestamp}.html')
                fig_users.write_html(users_path)
                visualizations['user_activity'] = users_path
            
            # Daily timeline
            fig_timeline = visualizer.create_daily_timeline(df)
            if fig_timeline:
                timeline_path = os.path.join(viz_dir, f'daily_timeline_{timestamp}.html')
                fig_timeline.write_html(timeline_path)
                visualizations['timeline'] = timeline_path
            
            # Hourly heatmap
            fig_heatmap = visualizer.create_hourly_heatmap(df)
            if fig_heatmap:
                heatmap_path = os.path.join(viz_dir, f'hourly_heatmap_{timestamp}.html')
                fig_heatmap.write_html(heatmap_path)
                visualizations['heatmap'] = heatmap_path
            
            # Sentiment analysis
            fig_sentiment = visualizer.create_sentiment_distribution(sentiment_analysis)
            if fig_sentiment:
                sentiment_path = os.path.join(viz_dir, f'sentiment_distribution_{timestamp}.html')
                fig_sentiment.write_html(sentiment_path)
                visualizations['sentiment'] = sentiment_path
            
            if not args.quiet:
                print(f"📊 Visualizations saved to: {viz_dir}")
        
        # Generate word cloud
        if args.wordcloud:
            if not args.quiet:
                print("☁️ Generating word cloud...")
            
            wordcloud_path = os.path.join(args.output, f'wordcloud_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png')
            visualizer.create_wordcloud(df, wordcloud_path)
            
            if not args.quiet:
                print(f"☁️ Word cloud saved to: {wordcloud_path}")
        
        # Generate report
        if not args.quiet:
            print(f"📄 Generating {args.format.upper()} report...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if args.format == 'json':
            output_path = report_gen.generate_json_report(
                activity_analysis, topic_analysis, sentiment_analysis, summary,
                f'analysis_{timestamp}.json'
            )
        elif args.format == 'html':
            output_path = report_gen.generate_html_report(
                activity_analysis, topic_analysis, sentiment_analysis, summary,
                visualizations, f'report_{timestamp}.html'
            )
        else:  # text
            output_path = report_gen.generate_text_report(
                activity_analysis, topic_analysis, sentiment_analysis, summary,
                f'summary_{timestamp}.txt'
            )
        
        if not args.quiet:
            print(f"✅ Report saved to: {output_path}")
            print()
            print("📋 Quick Summary:")
            print("-" * 30)
            print(summary)
            print()
            print("🎉 Analysis complete! Check the output directory for detailed results.")
        else:
            print(output_path)
    
    except KeyboardInterrupt:
        print("\\n❌ Analysis interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        if not args.quiet:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
