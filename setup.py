#!/usr/bin/env python3
"""
Simple setup script for WhatsApp Chat Analyzer
Handles dependency installation and NLTK data download
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False
    return True

def download_nltk_data():
    """Download required NLTK data"""
    print("📚 Downloading NLTK data...")
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('vader_lexicon', quiet=True)
        print("✅ NLTK data downloaded successfully!")
    except Exception as e:
        print(f"❌ Failed to download NLTK data: {e}")
        return False
    return True

def main():
    """Main setup function"""
    print("🚀 Setting up WhatsApp Chat Analyzer...")
    print("=" * 50)
    
    if not install_requirements():
        sys.exit(1)
    
    if not download_nltk_data():
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ Setup complete!")
    print("\n🎯 To start the application:")
    print("   streamlit run streamlit_app.py")
    print("\n📋 For command line usage:")
    print("   python main.py your_chat.txt")

if __name__ == "__main__":
    main()
