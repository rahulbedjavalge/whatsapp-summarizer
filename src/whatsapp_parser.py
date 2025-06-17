import re
import pandas as pd
from datetime import datetime
import emoji
from typing import List, Tuple, Optional

class WhatsAppParser:
    """Parser for WhatsApp chat export files"""
    
    def __init__(self):
        # Different date formats that WhatsApp uses
        self.date_patterns = [
            r'(\d{1,2}/\d{1,2}/\d{2,4}),?\s*(\d{1,2}:\d{2}(?::\d{2})?)\s*([APap][Mm])?\s*-\s*([^:]+):\s*(.*)',
            r'(\d{1,2}/\d{1,2}/\d{2,4}),?\s*(\d{1,2}:\d{2}(?::\d{2})?)\s*-\s*([^:]+):\s*(.*)',
            r'(\d{4}-\d{1,2}-\d{1,2}),?\s*(\d{1,2}:\d{2}(?::\d{2})?)\s*([APap][Mm])?\s*-\s*([^:]+):\s*(.*)',
            r'\[(\d{1,2}/\d{1,2}/\d{2,4}),?\s*(\d{1,2}:\d{2}(?::\d{2})?)\s*([APap][Mm])?\]\s*([^:]+):\s*(.*)'
        ]
    
    def parse_chat_file(self, file_path: str) -> pd.DataFrame:
        """Parse WhatsApp chat export file and return DataFrame"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='utf-8-sig') as file:
                content = file.read()
        
        messages = []
        lines = content.split('\n')
        
        current_message = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Try to match message pattern
            message_data = self._parse_message_line(line)
            
            if message_data:
                # If we have a previous message, save it
                if current_message:
                    messages.append(current_message)
                
                current_message = message_data
            else:
                # This is a continuation of the previous message
                if current_message:
                    current_message['message'] += ' ' + line
        
        # Don't forget the last message
        if current_message:
            messages.append(current_message)
        
        # Convert to DataFrame
        df = pd.DataFrame(messages)
        
        if not df.empty:
            # Clean and process the data
            df = self._clean_dataframe(df)
        
        return df
    
    def _parse_message_line(self, line: str) -> Optional[dict]:
        """Parse a single line to extract message components"""
        for pattern in self.date_patterns:
            match = re.match(pattern, line)
            if match:
                groups = match.groups()
                
                if len(groups) == 5:  # Pattern with AM/PM
                    date_str, time_str, am_pm, user, message = groups
                    if am_pm:
                        time_str += f" {am_pm}"
                elif len(groups) == 4:  # Pattern without AM/PM
                    date_str, time_str, user, message = groups
                    am_pm = None
                else:
                    continue
                
                # Parse datetime
                timestamp = self._parse_datetime(date_str, time_str)
                
                return {
                    'timestamp': timestamp,
                    'user': user.strip(),
                    'message': message.strip()
                }
        
        return None
    
    def _parse_datetime(self, date_str: str, time_str: str) -> datetime:
        """Parse date and time strings into datetime object"""
        # Clean the strings
        date_str = date_str.strip()
        time_str = time_str.strip()
        
        # Try different date formats
        date_formats = [
            '%d/%m/%Y', '%m/%d/%Y', '%d/%m/%y', '%m/%d/%y',
            '%Y-%m-%d', '%Y-%d-%m'
        ]
        
        time_formats = [
            '%H:%M:%S', '%H:%M', '%I:%M:%S %p', '%I:%M %p'
        ]
        
        # Try to parse date
        parsed_date = None
        for date_format in date_formats:
            try:
                parsed_date = datetime.strptime(date_str, date_format).date()
                break
            except ValueError:
                continue
        
        if not parsed_date:
            # Fallback to current date
            parsed_date = datetime.now().date()
          # Try to parse time
        parsed_time = None
        for time_format in time_formats:
            try:
                parsed_time = datetime.strptime(time_str, time_format).time()
                break
            except ValueError:
                continue
        
        if not parsed_time:
            # Fallback to midnight
            parsed_time = datetime.strptime('00:00', '%H:%M').time()
        
        return datetime.combine(parsed_date, parsed_time)
    
    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and process the DataFrame"""
        if df.empty:
            return df
            
        # Remove system messages
        system_messages = [
            'You deleted this message',
            'This message was deleted',
            'Messages and calls are end-to-end encrypted',
            'added', 'left', 'changed the group name to',
            'changed this group\'s icon', 'Security code changed'
        ]
        
        # Filter out system messages
        for msg in system_messages:
            df = df[~df['message'].str.contains(msg, case=False, na=False)]
        
        # Remove empty messages and null values
        df = df.dropna(subset=['message', 'user', 'timestamp'])
        df = df[df['message'].str.len() > 0]
        df = df[df['user'].str.len() > 0]
        
        if df.empty:
            return df
        
        # Sort by timestamp
        df = df.sort_values('timestamp').reset_index(drop=True)
        
        # Add derived columns safely
        try:
            df['date'] = df['timestamp'].dt.date
            df['hour'] = df['timestamp'].dt.hour
            df['day_of_week'] = df['timestamp'].dt.day_name()
            df['message_length'] = df['message'].str.len()
            
            # Clean emoji text
            df['clean_message'] = df['message'].apply(self._clean_text)
        except Exception as e:
            print(f"Error adding derived columns: {e}")
            # Add basic clean_message column if others fail
            df['clean_message'] = df['message'].apply(lambda x: str(x) if pd.notna(x) else "")
        
        return df
    
    def _clean_text(self, text: str) -> str:
        """Clean text by removing emojis and special characters"""
        # Convert emojis to text
        text = emoji.demojize(text)
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove mentions
        text = re.sub(r'@\w+', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text.strip()
