from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.agents import create_sql_agent
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from data.mock_analytics import generate_mock_analytics_data, get_analytics_summary
from agents.business_intelligence_agent import BusinessIntelligenceAgent
import sqlite3

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the LLM with Gemini
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=float(os.getenv("TEMPERATURE", "0.7")),
    max_tokens=None,
    timeout=30,
    max_retries=3,
    convert_system_message_to_human=True,
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }
)

# Initialize SQLite database
db_path = "sqlite:///./business_intelligence.db"
db = SQLDatabase.from_uri(db_path)

# Initialize the business intelligence agent
bi_agent = BusinessIntelligenceAgent(llm=model, db=db)

# Create custom prompt template with improved instructions
CUSTOM_PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "top_k"],
    template="""
    You are a helpful business intelligence assistant. Your task is to help users understand their business data.
    
    Available tables and their schemas:
    {table_info}
    
    Use the following format:
    
    Question: the input question
    Thought: you should always think about what to do
    Action: sql_db_query
    Action Input: the SQL query to execute
    Observation: the result of the action
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question
    
    Begin!
    
    Question: {input}
    Thought: Let me analyze the business data to answer this question.
    Action: sql_db_query
    Action Input: SELECT AVG(session_duration) FROM analytics_data
    Observation: {table_info}
    Thought: I now have the data to answer the question.
    Final Answer: Based on the data, the average session duration is [result] minutes.
    """
)

# Create SQL agent with custom prompt and improved error handling
agent = create_sql_agent(
    llm=model,
    toolkit=SQLDatabaseToolkit(db=db, llm=model),
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    prompt=CUSTOM_PROMPT,
    max_iterations=3
)

class Query(BaseModel):
    text: str
    language: Optional[str] = "en"

class AnalyticsQuery(BaseModel):
    days: Optional[int] = 30
    format: Optional[str] = "json"

class QueryResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@app.post("/query")
async def process_query(query: Query):
    """Process a natural language query and return insights."""
    try:
        response = bi_agent.process_query(query.text)
        return {"response": response}
    except Exception as e:
        print(f"Error in /query endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )

@app.get("/analytics")
async def get_analytics(days: int = 30):
    """Get analytics data for the specified number of days."""
    try:
        # Connect to SQLite database
        conn = sqlite3.connect('business_intelligence.db')
        cursor = conn.cursor()
        
        # Get data for the last N days
        cursor.execute('''
            SELECT date, page_views, unique_visitors, session_duration, bounce_rate, conversion_rate
            FROM analytics_data
            ORDER BY date DESC
            LIMIT ?
        ''', (days,))
        
        columns = [description[0] for description in cursor.description]
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        return {
            "success": True,
            "data": data,
            "error": None
        }
    except Exception as e:
        print(f"Error in /analytics endpoint: {str(e)}")
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }
    finally:
        conn.close()

@app.get("/analytics/summary")
async def get_analytics_summary():
    try:
        summary = get_analytics_summary()
        return {
            "success": True,
            "summary": summary,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "summary": None,
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 