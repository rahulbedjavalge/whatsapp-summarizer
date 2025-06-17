# WhatsApp Chat Analyzer 📱

A comprehensive Python tool for analyzing WhatsApp group chat exports with beautiful visualizations and intelligent insights.

## 🚀 Quick Start

```bash
git clone https://github.com/rahulbedjavalge/whatsapp-summarizer.git
cd whatsapp-summarizer
python setup.py
streamlit run streamlit_app.py
```

Open your browser to `http://localhost:8501` and start analyzing!

## ✨ Features

- **📊 Smart Analysis**: Activity patterns, sentiment analysis, topic extraction
- **🎨 Beautiful Visualizations**: Interactive charts, heatmaps, word clouds  
- **📄 Multiple Formats**: Web interface, CLI, HTML/JSON exports
- **🔒 Privacy First**: All processing happens locally on your device
- **🧠 Intelligent Summaries**: Understand what's actually happening in your chat

## 📱 How to Export WhatsApp Chat

1. Open your WhatsApp group chat
2. Tap the group name → "Export Chat" → "Without Media"
3. Save the `.txt` file and upload it to the analyzer

## 🖥️ Usage Options

### Web Interface (Recommended)
```bash
streamlit run streamlit_app.py
```
- Drag & drop chat files
- Interactive visualizations
- Real-time analysis

### Command Line
```bash
python main.py your_chat.txt --format html --viz
```
- Batch processing
- Multiple output formats
- Scriptable workflow

## 📊 What You Get

### Smart Group Recognition
- **🎓 Student Groups**: "Focused on visa/university discussions"
- **💼 Work Groups**: "Team collaboration and project discussions"  
- **👨‍👩‍👧‍👦 Family Groups**: "Daily life updates and family bonding"
- **🎉 Social Groups**: "Entertainment and friendship activities"

### Comprehensive Analysis
- **Activity Patterns**: Most active users, peak times, daily trends
- **Topic Extraction**: Key themes and trending keywords
- **Sentiment Tracking**: Mood analysis and emotional trends
- **Visual Reports**: Interactive charts, graphs, and word clouds

## 📁 Clean Project Structure

```
whatsapp-summarizer/
├── src/                    # Core analysis modules
│   ├── whatsapp_parser.py  # Chat file parsing
│   ├── chat_analyzer.py    # Analysis engine
│   ├── chat_visualizer.py  # Visualization generator
│   └── report_generator.py # Report formatting
├── main.py                 # Command line interface  
├── streamlit_app.py        # Web interface
├── setup.py                # One-command setup
├── requirements.txt        # Dependencies
├── Dockerfile              # Docker support
└── README.md               # This file
```

## 🐳 Docker (Optional)

```bash
docker-compose up -d
```
Access at `http://localhost:8501`

## 🔧 Requirements

- Python 3.7+
- Dependencies: pandas, nltk, streamlit, plotly, scikit-learn
- NLTK data (downloaded automatically by setup.py)

## 🛡️ Privacy & Security

- **100% Local Processing**: Your data never leaves your computer
- **Phone Number Protection**: Automatically anonymized in reports
- **No Data Storage**: Temporary files cleaned up automatically
- **Open Source**: Full transparency of data handling

## 🆘 Quick Troubleshooting

- **Setup issues**: Run `python setup.py` again
- **Import errors**: Ensure you're in the project directory
- **Chat not parsing**: Re-export from WhatsApp without media
- **Missing visualizations**: Install requirements with `pip install -r requirements.txt`

---

**Simple. Clean. Powerful.** 🎯

Made with ❤️ for better understanding of group dynamics and communication patterns.
