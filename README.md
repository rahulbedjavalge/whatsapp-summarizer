# WhatsApp Chat Analyzer 📱

A comprehensive Python tool for analyzing WhatsApp group chat exports. Get insights into user activity, trending topics, sentiment analysis, and generate beautiful visualizations with intelligent narrative summaries.

## 🚀 Features

- **📊 Activity Analysis**: Message counts, active users, peak times, daily/weekly patterns
- **🔥 Topic Extraction**: Key themes and popular keywords using NLP
- **😊 Sentiment Analysis**: Overall mood and emotional trends over time
- **📈 Visualizations**: Interactive charts, heatmaps, and word clouds
- **📄 Multiple Output Formats**: Text summary, JSON, HTML reports
- **🖥️ Web Interface**: Beautiful Streamlit web UI
- **🧠 Smart Narrative Summary**: Detailed insights about what's actually happening in your chat
- **🔒 Privacy First**: All processing happens locally

## 📸 Screenshots

### Web Interface
![WhatsApp Chat Analyzer Interface](https://github.com/rahulbedjavalge/whatsapp-summarizer/blob/main/screenshots/web-interface.png?raw=true)

*Beautiful Streamlit web interface with drag-and-drop file upload and real-time analysis*

### Interactive Visualizations
![Visualizations Dashboard](https://github.com/rahulbedjavalge/whatsapp-summarizer/blob/main/screenshots/visualizations.png?raw=true)

*Comprehensive visualizations including user activity charts, sentiment analysis, timeline graphs, and word clouds*

## 🎯 What's New - Enhanced Summary Feature

The analyzer now provides much more detailed and meaningful insights about your WhatsApp group chats!


## 🛠️ Quick Start

### 1. Installation
```bash
git clone <repository-url>
cd whatsapp-summarizer
pip install -r requirements.txt
```

### 2. Download NLTK data (first time only)
```python
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
```

### 3. Export Your WhatsApp Chat
1. Open your WhatsApp group chat
2. Tap on the group name (header)
3. Select "Export Chat"
4. Choose "Without Media"
5. Save the `.txt` file to your computer

## 🎯 Usage

### Web Interface (Recommended)
```bash
streamlit run streamlit_app.py
```
Then open your browser to `http://localhost:8501`

### Command Line Interface
```bash
# Basic analysis
python main.py your_chat.txt

# JSON output with visualizations
python main.py your_chat.txt --format json --viz --wordcloud

# Custom output directory
python main.py your_chat.txt --output results/ --topics 10
```

### Python Script
```python
from whatsapp_parser import WhatsAppParser
from chat_analyzer import ChatAnalyzer

# Parse chat file
parser = WhatsAppParser()
df = parser.parse_chat_file('your_chat.txt')

# Analyze
analyzer = ChatAnalyzer()
activity = analyzer.analyze_activity(df)
topics = analyzer.extract_topics(df)
sentiment = analyzer.analyze_sentiment(df)
summary = analyzer.generate_summary(df, activity, topics, sentiment)

print(summary)  # Now shows detailed narrative summary!
```

## 🧠 Understanding Your Chat Analysis

### 📊 Group Overview
- **Message Count**: Total number of messages analyzed
- **Participant Count**: Number of unique users who sent messages
- **Time Period**: Duration of the chat history
- **Daily Average**: How active the group is on average

### 👥 Most Active Members
- Shows top contributors with message counts
- **Privacy Protection**: Phone numbers are anonymized (e.g., "User 1234")
- **Average Character Length**: Indicates whether users send short/long messages

### 📈 Activity Patterns
- **Peak Hour**: When the group is most active during the day
- **Busiest Day**: The specific date with highest activity
- **Daily Average**: Messages per day over the entire period

### 🔥 Key Topics & Discussions
- **Primary Topics**: The main themes being discussed (high relevance)
- **Secondary Topics**: Supporting or related discussion themes
- **Smart Categorization**: Topics are automatically grouped by importance

### 😊 Mood & Sentiment Analysis
- **Overall Sentiment**: Whether the group tone is positive, negative, or neutral
- **Percentage Breakdown**: Detailed sentiment distribution
- **Trend Analysis**: How mood changes over time

### 💬 What's Happening in the Chat
This is the **NEW NARRATIVE SUMMARY** that tells you:
- **Purpose of the group** (work, family, friends, students, etc.)
- **Current discussions** and main concerns
- **Group dynamics** and communication patterns
- **Overall atmosphere** and tone

## 🎯 Chat Type Recognition

The analyzer automatically identifies different types of groups:

### 🎓 **Student/Education Groups**
Keywords: visa, student, university, study, exam, assignment
> "The group appears to be focused on student/visa related discussions and educational matters."

### 💼 **Work/Professional Groups**
Keywords: work, job, office, meeting, project, deadline
> "This seems to be a work-related group discussing professional matters and projects."

### 👨‍👩‍👧‍👦 **Family Groups**
Keywords: family, home, kids, mom, dad, dinner
> "The group appears to be a family chat sharing daily life updates and family matters."

### 🎉 **Social/Friends Groups**
Keywords: game, play, fun, party, friends, weekend
> "This looks like a social group focused on entertainment and friendship activities."

### Command Line Interface
```bash
# Basic analysis
python main.py your_chat.txt

# JSON output with visualizations
python main.py your_chat.txt --format json --viz --wordcloud

# Custom output directory
python main.py your_chat.txt --output results/ --topics 10
```

### Python Script
```python
from whatsapp_parser import WhatsAppParser
from chat_analyzer import ChatAnalyzer

# Parse chat file
parser = WhatsAppParser()
df = parser.parse_chat_file('your_chat.txt')

# Analyze
analyzer = ChatAnalyzer()
activity = analyzer.analyze_activity(df)
topics = analyzer.extract_topics(df)
sentiment = analyzer.analyze_sentiment(df)
summary = analyzer.generate_summary(df, activity, topics, sentiment)

print(summary)  # Now shows detailed narrative summary!
```

## 🎨 Output Formats

### 📊 Interactive Dashboard (Streamlit)
- Real-time analysis with interactive charts
- Upload and analyze immediately
- Download reports in multiple formats

### 📄 HTML Report
- Beautiful formatted report with embedded visualizations
- Perfect for sharing or archiving
- Includes all charts and graphs

### 📝 Text Summary
- Clean, readable format
- Great for quick insights
- Easy to copy/paste

### 🔧 JSON Export
- Machine-readable format
- Perfect for further analysis
- Complete data export

## 📈 Visualizations

The tool generates several types of visualizations:

- **User Activity Chart**: Bar chart showing most active contributors
- **Daily Timeline**: Message count trends over time
- **Hourly Heatmap**: Activity patterns by hour and day of week
- **Sentiment Timeline**: Mood changes over time
- **Word Cloud**: Visual representation of most common words
- **Weekly Patterns**: Activity distribution across days of the week

## 🔧 Command Line Options

```bash
python main.py --help

usage: main.py [-h] [--format {text,json,html}] [--output OUTPUT] 
               [--topics TOPICS] [--viz] [--wordcloud] [--quiet] 
               input_file

Options:
  input_file                    Path to WhatsApp chat export (.txt file)
  --format {text,json,html}     Output format (default: text)
  --output OUTPUT               Output directory (default: reports)
  --topics TOPICS               Number of topics to extract (default: 5)
  --viz                         Generate visualizations
  --wordcloud                   Generate word cloud
  --quiet                       Suppress progress messages
```

## 📁 Project Structure

```
whatsapp-summarizer/
├── main.py                 # Command line interface
├── streamlit_app.py        # Web interface
├── whatsapp_parser.py      # Chat file parsing
├── chat_analyzer.py        # Core analysis functions
├── chat_visualizer.py      # Visualization generation
├── report_generator.py     # Report formatting
├── requirements.txt        # Dependencies
├── screenshots/            # Demo images and interface screenshots
└── reports/               # Generated reports (auto-created)
    ├── visualizations/    # Chart files
    └── ...               # Report files
```

## 🔍 Supported Chat Formats

The parser supports various WhatsApp export formats:
- Different date formats (DD/MM/YYYY, MM/DD/YYYY, YYYY-MM-DD)
- 12-hour and 24-hour time formats
- Multiple languages
- System messages filtering

## 💡 Tips for Better Analysis

1. **Larger Chat Files**: More messages = better topic analysis and sentiment trends
2. **Time Period**: Longer timeframes show better activity patterns
3. **Multiple Formats**: Try different output formats for different use cases
4. **Visualizations**: Enable charts for better understanding of patterns
5. **Topic Count**: Adjust number of topics (5-15) based on group size and diversity

## 🛡️ Privacy & Security

- **Local Processing**: All analysis happens on your device
- **No Data Transmission**: Chat data never leaves your computer
- **Phone Number Protection**: Numbers are automatically anonymized in reports
- **No Storage**: Temporary files are automatically cleaned up
- **Open Source**: Full transparency of data handling

## 🆘 Troubleshooting

### Chat Not Parsing Correctly?
- Ensure it's a WhatsApp export (.txt file)
- Try re-exporting the chat
- Check file encoding (should be UTF-8)

### Strange User Names?
- This is normal for privacy protection
- Phone numbers are automatically anonymized
- Real names may not appear if users haven't set display names

### Missing Topics?
- Small chat files may not have enough content
- Try increasing the topic count parameter
- Ensure chat contains meaningful conversations (not just media/emoji)

## 🧪 Tech Stack

- **Python 3.7+**
- **pandas**: Data manipulation
- **NLTK/spaCy**: Natural language processing
- **scikit-learn**: Machine learning for topics
- **TextBlob/VADER**: Sentiment analysis
- **Plotly**: Interactive visualizations
- **Streamlit**: Web interface
- **WordCloud**: Text visualization

## 🔮 Advanced Features

- **Multi-language Support**: Analyzes chats in different languages
- **Smart Filtering**: Automatically removes system messages and spam
- **Trend Analysis**: Shows how topics and sentiment change over time
- **Visual Analytics**: Beautiful charts and word clouds
- **Batch Processing**: Analyze multiple chat files at once

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎉 Examples

### Student Group Analysis
```
💬 **WHAT'S HAPPENING IN THE CHAT**
The group appears to be focused on student/visa related discussions and educational matters. 
This is an active group with regular ongoing conversations. There are some concerns or 
frustrations being discussed regarding academic deadlines and application processes.
```

### Work Group Analysis
```
💬 **WHAT'S HAPPENING IN THE CHAT**
This seems to be a work-related group discussing professional matters and projects. 
The overall tone is quite positive and upbeat with team collaboration. Members are most 
active during business hours discussing meetings and project deadlines.
```

### Family Group Analysis
```
💬 **WHAT'S HAPPENING IN THE CHAT**
The group appears to be a family chat sharing daily life updates and family matters. 
This appears to be a smaller group with moderate activity. The overall tone is quite 
positive and upbeat with lots of emotional support and family bonding.
```

---

Made with ❤️ for better understanding of group dynamics and communication patterns.

**Need help?** Create an issue on the project repository or check the troubleshooting section above.
