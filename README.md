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
2. Gemini API key
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
GEMINI_API_KEY=your_gemini_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///./business_intelligence.db

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Optional: Model Configuration
MODEL_NAME=gemini-pro
TEMPERATURE=0.7
MAX_TOKENS=1000
```

#### Initialize Database
```bash
python init_db.py
```

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

Once the backend server is running, you can access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Troubleshooting

### Common Issues

1. **Backend Server Won't Start**
   - Ensure Python 3.10+ is installed
   - Check if all dependencies are installed correctly
   - Verify the `.env` file exists and has correct values
   - Check if port 8000 is available

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
| GEMINI_API_KEY | Your Gemini API key | Yes | - |
| DATABASE_URL | Database connection string | Yes | sqlite:///./business_intelligence.db |
| HOST | Backend server host | No | 0.0.0.0 |
| PORT | Backend server port | No | 8000 |
| DEBUG | Debug mode | No | True |
| MODEL_NAME | Gemini model to use | No | gemini-pro |
| TEMPERATURE | Model temperature (0-1) | No | 0.7 |
| MAX_TOKENS | Maximum tokens per response | No | 1000 |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 