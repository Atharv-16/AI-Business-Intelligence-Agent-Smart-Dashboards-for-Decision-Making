from agents.business_intelligence_agent import BusinessIntelligenceAgent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities.sql_database import SQLDatabase
from data.mock_analytics import generate_mock_analytics_data, get_analytics_summary
import os
from dotenv import load_dotenv

def init_database():
    # Load environment variables
    load_dotenv()
    
    # Initialize the database
    db_path = "sqlite:///./business_intelligence.db"
    db = SQLDatabase.from_uri(db_path)
    
    # Initialize the LLM (dummy instance for database initialization)
    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0.7,
        max_tokens=2048
    )
    
    # Initialize the agent to create the database schema
    agent = BusinessIntelligenceAgent(llm=model, db=db)
    
    # Generate mock data
    print("Generating mock data...")
    data = generate_mock_analytics_data(30)
    
    # Get and print summary
    summary = get_analytics_summary()
    print("\nSummary statistics:")
    print(f"Average Page Views: {summary['average_page_views']:.0f}")
    print(f"Average Unique Visitors: {summary['average_unique_visitors']:.0f}")
    print(f"Average Session Duration: {summary['average_session_duration']:.1f} minutes")
    print(f"Average Bounce Rate: {summary['average_bounce_rate']*100:.1f}%")
    print(f"Average Conversion Rate: {summary['average_conversion_rate']*100:.1f}%")
    print(f"Last Update: {summary['last_update']}")
    
    print("\nDatabase initialized successfully!")

if __name__ == "__main__":
    init_database() 