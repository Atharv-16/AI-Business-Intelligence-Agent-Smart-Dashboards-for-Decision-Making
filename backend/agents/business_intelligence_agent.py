from typing import Dict, Any, List
from langchain.agents import AgentExecutor
from langchain.tools import Tool
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain.agents import create_sql_agent
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sqlite3
import os
import random

class BusinessIntelligenceAgent:
    def __init__(self, llm: ChatGoogleGenerativeAI, db: SQLDatabase):
        self.llm = llm
        self.db = db
        self._initialize_database()  # Initialize database first
        
    def _initialize_database(self):
        """Initialize the SQLite database with required tables."""
        try:
            # Connect to SQLite database
            conn = sqlite3.connect('business_intelligence.db')
            cursor = conn.cursor()

            # Create analytics_data table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analytics_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    page_views INTEGER,
                    unique_visitors INTEGER,
                    session_duration REAL,
                    bounce_rate REAL,
                    conversion_rate REAL
                )
            ''')

            # Check if we need to insert sample data
            cursor.execute("SELECT COUNT(*) FROM analytics_data")
            count = cursor.fetchone()[0]
            
            if count == 0:
                # Insert sample data for the last 30 days
                today = datetime.now()
                for i in range(30):
                    date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
                    cursor.execute('''
                        INSERT INTO analytics_data 
                        (date, page_views, unique_visitors, session_duration, bounce_rate, conversion_rate)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        date,
                        random.randint(800, 1200),  # page_views
                        random.randint(400, 600),   # unique_visitors
                        round(random.uniform(2.0, 5.0), 1),  # session_duration
                        round(random.uniform(0.2, 0.4), 2),  # bounce_rate
                        round(random.uniform(0.01, 0.03), 2)  # conversion_rate
                    ))

            conn.commit()
            print("Database initialized successfully with sample data")
        except Exception as e:
            print(f"Error initializing database: {str(e)}")
            raise
        finally:
            conn.close()
    
    def analyze_trends(self, data: Dict[str, Any]) -> str:
        """Analyze trends in business metrics over time."""
        try:
            df = pd.DataFrame(data)
            df['date'] = pd.to_datetime(df['date'])
            
            # Calculate trends
            trends = {}
            for metric in ['page_views', 'unique_visitors', 'conversion_rate']:
                if metric in df.columns:
                    trend = np.polyfit(range(len(df)), df[metric], 1)[0]
                    trends[metric] = "increasing" if trend > 0 else "decreasing"
            
            return f"Trend Analysis: {trends}"
        except Exception as e:
            return f"Error analyzing trends: {str(e)}"
    
    def detect_anomalies(self, data: Dict[str, Any]) -> str:
        """Detect anomalies in business metrics."""
        try:
            df = pd.DataFrame(data)
            
            # Calculate z-scores
            anomalies = {}
            for metric in ['page_views', 'unique_visitors', 'conversion_rate']:
                if metric in df.columns:
                    z_scores = np.abs((df[metric] - df[metric].mean()) / df[metric].std())
                    anomalies[metric] = df[z_scores > 2][['date', metric]].to_dict('records')
            
            return f"Anomalies Detected: {anomalies}"
        except Exception as e:
            return f"Error detecting anomalies: {str(e)}"
    
    def generate_insights(self, data: Dict[str, Any]) -> str:
        """Generate actionable insights from data."""
        try:
            df = pd.DataFrame(data)
            
            insights = []
            
            # Analyze user behavior
            if 'bounce_rate' in df.columns:
                avg_bounce_rate = df['bounce_rate'].mean()
                if avg_bounce_rate > 0.5:
                    insights.append("High bounce rate detected. Consider improving landing page engagement.")
            
            # Analyze conversion trends
            if 'conversion_rate' in df.columns:
                conversion_growth = (df['conversion_rate'].iloc[-1] - df['conversion_rate'].iloc[0]) / df['conversion_rate'].iloc[0] * 100
                if conversion_growth > 0:
                    insights.append(f"Positive conversion growth of {conversion_growth:.2f}% observed.")
                else:
                    insights.append(f"Negative conversion growth of {conversion_growth:.2f}% observed.")
            
            return "Actionable Insights:\n" + "\n".join(insights)
        except Exception as e:
            return f"Error generating insights: {str(e)}"
    
    def process_query(self, query: str) -> str:
        """Process a business intelligence query and return a natural language response."""
        try:
            # Generate SQL query using the language model
            sql_prompt = ChatPromptTemplate.from_messages([
                ("user", """You are a SQL expert. Generate a SQL query for SQLite to answer this business intelligence question.
                The analytics_data table has the following columns:
                - date (TEXT): Date and time of the record
                - page_views (INTEGER): Number of page views
                - unique_visitors (INTEGER): Number of unique visitors
                - session_duration (REAL): Average session duration in minutes
                - bounce_rate (REAL): Bounce rate as a decimal (e.g., 0.35 for 35%)
                - conversion_rate (REAL): Conversion rate as a decimal (e.g., 0.02 for 2%)
                
                For date comparisons, use the date() function.
                For today's data, use date('now').
                For last month, use date('now', '-1 month').
                
                Question: {query}
                Please provide only the SQL query without any explanation or markdown formatting.""")
            ])
            sql_chain = sql_prompt | self.llm
            sql_response = sql_chain.invoke({"query": query})
            
            # Extract and clean the SQL query
            sql_query = sql_response.content.strip()
            sql_query = sql_query.replace('```sql', '').replace('```', '').strip()
            print(f"Generated SQL query: {sql_query}")
            
            try:
                # Execute the SQL query
                result = self.db.run(sql_query)
                print(f"Query result: {result}")
                
                if not result:
                    return "No data found for the specified query."
                
                # Generate natural language response
                response_prompt = ChatPromptTemplate.from_messages([
                    ("user", """You are a business intelligence expert. Provide a clear and concise answer based on these SQL results.
                    Format numbers appropriately (e.g., 1,234 instead of 1234).
                    For rates, show as percentages (e.g., 35% instead of 0.35).
                    For durations, show in minutes.
                    
                    Question: {query}
                    SQL Query: {sql_query}
                    Results: {result}
                    
                    Please provide a clear answer to the question based on this data.""")
                ])
                response_chain = response_prompt | self.llm
                response = response_chain.invoke({
                    "query": query,
                    "sql_query": sql_query,
                    "result": result
                })
                
                return response.content
                
            except Exception as db_error:
                print(f"Database error: {str(db_error)}")
                return f"Error executing query: {str(db_error)}"
            
        except Exception as e:
            print(f"General error: {str(e)}")
            return f"Error processing query: {str(e)}" 