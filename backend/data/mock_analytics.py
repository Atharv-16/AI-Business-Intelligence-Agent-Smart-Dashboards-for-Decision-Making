import sqlite3
import random
from datetime import datetime, timedelta
import pandas as pd
from typing import Dict, Any, Optional

def generate_mock_analytics_data(days: int = 30, format: str = "json"):
    """Generate mock analytics data for the specified number of days."""
    conn = sqlite3.connect('business_intelligence.db')
    cursor = conn.cursor()

    # Clear existing data
    cursor.execute('DELETE FROM analytics_data')

    # Generate data for the last N days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    data = []
    current_date = start_date
    
    # Base values with some randomness
    base_page_views = 5000
    base_unique_visitors = 3000
    base_session_duration = 3.5  # minutes
    base_bounce_rate = 0.35  # 35%
    base_conversion_rate = 0.02  # 2%
    
    while current_date <= end_date:
        # Generate realistic variations
        # Weekdays have more traffic
        is_weekday = current_date.weekday() < 5
        weekday_multiplier = 1.2 if is_weekday else 0.8
        
        # Morning/afternoon variations
        hour = current_date.hour
        if 9 <= hour <= 17:  # Business hours
            time_multiplier = 1.3
        else:
            time_multiplier = 0.7
            
        # Generate data with realistic patterns
        page_views = int(base_page_views * weekday_multiplier * time_multiplier * random.uniform(0.9, 1.1))
        unique_visitors = int(base_unique_visitors * weekday_multiplier * time_multiplier * random.uniform(0.9, 1.1))
        session_duration = base_session_duration * random.uniform(0.8, 1.2)
        bounce_rate = base_bounce_rate * random.uniform(0.9, 1.1)
        conversion_rate = base_conversion_rate * random.uniform(0.9, 1.1)
        
        # Ensure values are within realistic bounds
        bounce_rate = min(max(bounce_rate, 0.1), 0.8)  # Between 10% and 80%
        conversion_rate = min(max(conversion_rate, 0.005), 0.1)  # Between 0.5% and 10%
        session_duration = min(max(session_duration, 1), 10)  # Between 1 and 10 minutes
        
        # Insert data into database
        cursor.execute('''
            INSERT INTO analytics_data 
            (date, page_views, unique_visitors, session_duration, bounce_rate, conversion_rate)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            current_date.strftime('%Y-%m-%d %H:%M:%S'),
            page_views,
            unique_visitors,
            session_duration,
            bounce_rate,
            conversion_rate
        ))
        
        data.append({
            'date': current_date.strftime('%Y-%m-%d %H:%M:%S'),
            'page_views': page_views,
            'unique_visitors': unique_visitors,
            'session_duration': session_duration,
            'bounce_rate': bounce_rate,
            'conversion_rate': conversion_rate
        })
        
        current_date += timedelta(hours=1)  # Generate hourly data
    
    conn.commit()
    conn.close()
    
    if format == "json":
        return data
    elif format == "dataframe":
        return pd.DataFrame(data)
    else:
        raise ValueError("Format must be either 'json' or 'dataframe'")

def get_analytics_summary():
    """Get summary statistics from the analytics data."""
    conn = sqlite3.connect('business_intelligence.db')
    cursor = conn.cursor()
    
    # Get summary statistics
    cursor.execute('''
        SELECT 
            AVG(page_views) as avg_page_views,
            AVG(unique_visitors) as avg_unique_visitors,
            AVG(session_duration) as avg_session_duration,
            AVG(bounce_rate) as avg_bounce_rate,
            AVG(conversion_rate) as avg_conversion_rate,
            MAX(date) as last_update
        FROM analytics_data
    ''')
    
    summary = cursor.fetchone()
    conn.close()
    
    return {
        'average_page_views': summary[0],
        'average_unique_visitors': summary[1],
        'average_session_duration': summary[2],
        'average_bounce_rate': summary[3],
        'average_conversion_rate': summary[4],
        'last_update': summary[5]
    }

# Example usage
if __name__ == "__main__":
    # Generate 30 days of mock data
    data = generate_mock_analytics_data(30)
    print("Generated mock data for 30 days")
    print("First 5 records:")
    print(data[:5])
    print("\nSummary statistics:")
    print(get_analytics_summary()) 