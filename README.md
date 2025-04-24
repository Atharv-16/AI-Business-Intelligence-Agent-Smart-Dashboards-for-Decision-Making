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
├── backend/           # FastAPI backend server
├── data/             # Mock data and data processing
├── agents/           # AI agent logic and processing
├── docs/             # Documentation
└── tests/            # Test files
```

## Tech Stack

- Frontend: React, Plotly/ECharts
- Backend: FastAPI, Python 3.10+
- AI/ML: LangChain, Qwen/DeepSeek
- Data Processing: Pandas, DuckDB
- Database: SQLite
- Visualization: Plotly, ECharts

## Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js 16+
- Git

### Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd ai-business-intelligence-agent
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

3. Create a `.env` file in the `backend` directory with the following variables:

```
# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///./business_intelligence.db

# Optional: Model Configuration
MODEL_NAME=gpt-4  # or gpt-3.5-turbo
TEMPERATURE=0.7
MAX_TOKENS=1000
```

### Running the Application

1. Start the backend server:
```bash
cd backend
uvicorn main:app --reload
```

2. Start the frontend development server:
```bash
cd frontend
npm start
```

## License

MIT License

## Contact

For questions and support, please contact:
- Email: hackathon@holonai.ai
- Discord: https://discord.gg/J8uw6mWBqF 

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| OPENAI_API_KEY | Your OpenAI API key | Yes | - |
| DATABASE_URL | Database connection string | Yes | sqlite:///./business_intelligence.db |
| MODEL_NAME | OpenAI model to use | No | gpt-4 |
| TEMPERATURE | Model temperature (0-1) | No | 0.7 |
| MAX_TOKENS | Maximum tokens per response | No | 1000 |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 