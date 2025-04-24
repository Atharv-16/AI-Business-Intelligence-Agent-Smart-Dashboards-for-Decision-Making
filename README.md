# AI Business Intelligence Agent: Smart Dashboards for Decision-Making

A multilingual Business Intelligence agent that provides actionable insights through natural language queries and smart visualizations.

## Features

- Natural language query interface
- Multilingual support (English, Mandarin, Cantonese)
- Integration with Google Analytics (mock data)
- Smart data visualization
- Actionable insights generation
- Follow-up question suggestions
- Learning from user interactions

## Project Structure

```
.
├── frontend/           # React frontend application
│   ├── public/        # Static files
│   ├── src/          # Source code
│   │   ├── components/  # React components
│   │   ├── pages/      # Page components
│   │   ├── services/   # API services
│   │   └── utils/      # Utility functions
├── backend/           # FastAPI backend server
│   ├── agents/       # AI agent logic
│   ├── analysis/     # Data analysis modules
│   ├── data/        # Data processing
│   │   └── mock_analytics.py  # Mock data generation
│   ├── visualization/ # Visualization modules
│   └── models/       # Model files (if using local models)
├── data/             # Mock data and data processing
├── docs/             # Documentation
└── tests/            # Test files
```

## Tech Stack

- Frontend: React, Plotly/ECharts
- Backend: FastAPI, Python 3.10+
- AI/ML: LangChain, Gemini
- Data Processing: Pandas, DuckDB
- Database: SQLite
- Visualization: Plotly, ECharts

## Prerequisites

### System Requirements
- Python 3.10 or higher
- Node.js 16 or higher
- npm 7 or higher
- Git
- At least 4GB RAM
- 10GB free disk space

### Required Accounts and API Keys
1. Google Cloud Platform account
   - Visit: https://console.cloud.google.com/
   - Create a new project
   - Enable the Gemini API
   - Create API credentials

2. Gemini API key
   - Go to Google Cloud Console
   - Navigate to "APIs & Services" > "Credentials"
   - Create an API key
   - Copy the key for later use

3. (Optional) Google Analytics account for real data integration

## Installation Guide

### 1. Clone the Repository
```bash
git clone [repository-url]
cd ai-business-intelligence-agent
```

### 2. Backend Setup

#### Create and Activate Virtual Environment
```bash
cd backend
python -m venv venv

# On Linux/Mac
source venv/bin/activate

# On Windows
.\venv\Scripts\activate
```

#### Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### Set Up Environment Variables
Create a `.env` file in the `backend` directory with the following content:
```env
# API Keys
GOOGLE_API_KEY=your_gemini_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///./business_intelligence.db

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Optional: Model Configuration
MODEL_NAME=gemini-1.5-pro
TEMPERATURE=0.7
MAX_TOKENS=2048
```

#### Initialize Database and Generate Mock Data
```bash
# This will create the database and generate mock data
python init_db.py
```

The mock data generation will:
1. Create the SQLite database
2. Generate 30 days of mock analytics data with the following columns:
   - `date`: Timestamp (YYYY-MM-DD HH:MM:SS)
   - `page_views`: Number of page views (integer)
   - `unique_visitors`: Number of unique visitors (integer)
   - `session_duration`: Average session duration in minutes (float)
   - `bounce_rate`: Percentage of visitors who leave without interaction (float, 0-1)
   - `conversion_rate`: Percentage of visitors who complete a desired action (float, 0-1)

The mock data includes realistic patterns:
- 20% more traffic on weekdays
- 30% more traffic during business hours (9 AM - 5 PM)
- Random variations within realistic bounds
- Hourly data points for granular analysis

### 3. Frontend Setup

#### Install Node.js Dependencies
```bash
cd frontend
npm install
```

#### Set Up Environment Variables
Create a `.env` file in the `frontend` directory:
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_GOOGLE_ANALYTICS_ID=your_ga_id_here
```

## Running the Application

### 1. Start the Backend Server
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend server will be available at `http://localhost:8000`

### 2. Start the Frontend Development Server
```bash
cd frontend
npm start
```

The frontend application will be available at `http://localhost:3000`

## API Documentation

### Available Endpoints

1. **Natural Language Query**
   - Endpoint: `POST /query`
   - Request Body:
     ```json
     {
       "text": "What was the average session duration last week?",
       "language": "en"
     }
     ```
   - Response:
     ```json
     {
       "response": "The average session duration last week was 3.5 minutes."
     }
     ```

2. **Get Analytics Data**
   - Endpoint: `GET /analytics?days=30`
   - Query Parameters:
     - `days`: Number of days of data to retrieve (default: 30)
   - Response:
     ```json
     {
       "success": true,
       "data": [
         {
           "date": "2024-04-24 10:00:00",
           "page_views": 5234,
           "unique_visitors": 3123,
           "session_duration": 3.5,
           "bounce_rate": 0.35,
           "conversion_rate": 0.02
         }
       ],
       "error": null
     }
     ```

3. **Get Analytics Summary**
   - Endpoint: `GET /analytics/summary`
   - Response:
     ```json
     {
       "success": true,
       "summary": {
         "average_page_views": 5234.5,
         "average_unique_visitors": 3123.2,
         "average_session_duration": 3.5,
         "average_bounce_rate": 0.35,
         "average_conversion_rate": 0.02,
         "last_update": "2024-04-24 10:00:00"
       },
       "error": null
     }
     ```

### Accessing API Documentation
Once the backend server is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Mock Data Management

### Regenerating Mock Data
To regenerate the mock data:
1. Stop the backend server
2. Run `python init_db.py` again
3. Restart the backend server

### Mock Data Patterns
The mock data generator creates realistic patterns:
1. **Time-based Variations**
   - Weekdays: 20% more traffic
   - Weekends: 20% less traffic
   - Business hours (9 AM - 5 PM): 30% more traffic
   - Non-business hours: 30% less traffic

2. **Data Ranges**
   - Page Views: 2000-8000 per hour
   - Unique Visitors: 1000-5000 per hour
   - Session Duration: 1-10 minutes
   - Bounce Rate: 10%-80%
   - Conversion Rate: 0.5%-10%

3. **Random Variations**
   - Each metric has random variations within ±10% of the base value
   - Values are constrained to realistic ranges

## Troubleshooting

### Common Issues

1. **Backend Server Won't Start**
   - Ensure Python 3.10+ is installed
   - Check if all dependencies are installed correctly
   - Verify the `.env` file exists and has correct values
   - Check if port 8000 is available
   - Ensure the database is initialized with `init_db.py`

2. **Frontend Won't Start**
   - Ensure Node.js 16+ is installed
   - Try clearing npm cache: `npm cache clean --force`
   - Delete node_modules and reinstall: `rm -rf node_modules && npm install`

3. **Database Issues**
   - Delete the existing database file and reinitialize: `rm business_intelligence.db && python init_db.py`
   - Check database permissions

4. **API Connection Issues**
   - Verify the backend server is running
   - Check if CORS is properly configured
   - Verify API endpoints in frontend environment variables

5. **Gemini API Issues**
   - Verify your API key is correct
   - Check your Google Cloud Console for API quota limits
   - Ensure the Gemini API is enabled in your project

### Getting Help

If you encounter any issues:
1. Check the console logs for both frontend and backend
2. Review the API documentation
3. Check the GitHub issues page
4. Contact support at hackathon@holonai.ai

## Development Guidelines

### Code Style
- Backend: Follow PEP 8 guidelines
- Frontend: Follow ESLint configuration
- Use meaningful commit messages
- Document new features and changes

### Testing
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Create a Pull Request

## License

MIT License

## Contact

For questions and support:
- Email: hackathon@holonai.ai
- Discord: https://discord.gg/J8uw6mWBqF 

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| GOOGLE_API_KEY | Your Google API key | Yes | - |
| DATABASE_URL | Database connection string | Yes | sqlite:///./business_intelligence.db |
| HOST | Backend server host | No | 0.0.0.0 |
| PORT | Backend server port | No | 8000 |
| DEBUG | Debug mode | No | True |
| MODEL_NAME | Gemini model to use | No | gemini-1.5-pro |
| TEMPERATURE | Model temperature (0-1) | No | 0.7 |
| MAX_TOKENS | Maximum tokens per response | No | 2048 |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

# Demo Video


https://github.com/user-attachments/assets/3e7788a0-cf7f-4d1c-a221-28039cb5e08a

# PDF Report
[Untitled document (1).pdf](https://github.com/user-attachments/files/19899579/Untitled.document.1.pdf)


