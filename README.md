# 🤖 E-commerce Customer Support Chatbot - Azure Implementation

![Azure](https://img.shields.io/badge/Azure-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

Enterprise-grade chatbot solution for e-commerce customer support with ML-powered sentiment analysis, product recommendations, and real-time analytics dashboard.

## 📋 Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Deployment](#deployment)
- [Analytics Dashboard](#analytics-dashboard)

## ✨ Features

### Chatbot Capabilities
- 🔍 **Order Tracking**: Real-time order status queries
- 📦 **Product Recommendations**: ML-powered suggestions based on user preferences
- ❓ **FAQ Support**: Automated responses to common questions
- 😊 **Sentiment Analysis**: Real-time emotion detection for customer satisfaction
- 👤 **Human Escalation**: Smart routing to human agents when needed
- 🌐 **Multi-channel**: Web Chat, Microsoft Teams integration ready

### Analytics Dashboard
- 📊 **Real-time Metrics**: Conversation volume, resolution rate, CSAT scores
- 📈 **Sentiment Trends**: Track customer satisfaction over time
- 🏆 **Top Issues**: Identify most common customer problems
- 💡 **Product Insights**: Popular products and recommendation performance
- 📉 **SQL-powered Reports**: Custom queries and data visualization

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────┐
│   User Input    │────────▶│   Azure Bot      │
│   (Web/Teams)   │         │   Framework      │
└─────────────────┘         └────────┬─────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    │                │                │
            ┌───────▼──────┐ ┌──────▼───────┐ ┌─────▼──────┐
            │ NLU/Intent   │ │  ML Models   │ │ Azure SQL  │
            │ Recognition  │ │  - Sentiment │ │  Database  │
            │              │ │  - Recommend │ │            │
            └──────────────┘ └──────────────┘ └─────┬──────┘
                                                     │
                                              ┌──────▼────────┐
                                              │   Streamlit   │
                                              │   Dashboard   │
                                              └───────────────┘
```

## 🛠️ Tech Stack

### Core Technologies
- **Bot Framework**: Azure Bot Service SDK (Python)
- **Cloud Platform**: Microsoft Azure
- **Database**: Azure SQL Database
- **ML/AI**: 
  - Sentiment Analysis (DistilBERT/RoBERTa)
  - Product Recommendations (Collaborative Filtering)
- **Frontend**: 
  - Bot Framework Web Chat
  - Streamlit Dashboard
- **DevOps**: Docker, Azure Container Instances, GitHub Actions

### Python Libraries
- `botbuilder-core`: Bot Framework SDK
- `azure-cognitiveservices-language-textanalytics`: Azure AI Services
- `pyodbc`: SQL Server connectivity
- `transformers`: Hugging Face models
- `streamlit`: Analytics dashboard
- `pandas`, `plotly`: Data analysis and visualization

## 📁 Project Structure

```
ecommerce-chatbot-azure/
├── bot/                          # Azure Bot Framework application
│   ├── __init__.py
│   ├── bot.py                    # Main bot logic
│   ├── config.py                 # Configuration management
│   ├── dialogs/                  # Conversation dialogs
│   │   ├── order_tracking.py
│   │   ├── product_search.py
│   │   └── faq_dialog.py
│   ├── models/                   # Data models
│   │   ├── conversation.py
│   │   └── user.py
│   └── utils/                    # Utility functions
│       ├── db_helper.py
│       └── response_formatter.py
│
├── ml_models/                    # Machine Learning components
│   ├── sentiment/
│   │   ├── train.py
│   │   ├── inference.py
│   │   └── model_config.py
│   └── recommendations/
│       ├── train.py
│       ├── inference.py
│       └── collaborative_filter.py
│
├── dashboard/                    # Streamlit Analytics Dashboard
│   ├── app.py                    # Main dashboard application
│   ├── pages/
│   │   ├── overview.py
│   │   ├── sentiment_analysis.py
│   │   └── product_insights.py
│   └── utils/
│       └── data_loader.py
│
├── sql/                          # Database schema and queries
│   ├── schema.sql
│   ├── seed_data.sql
│   └── stored_procedures.sql
│
├── frontend/                     # Web Chat interface
│   ├── index.html
│   └── styles.css
│
├── tests/                        # Unit and integration tests
│   ├── test_bot.py
│   ├── test_ml_models.py
│   └── test_database.py
│
├── docs/                         # Documentation
│   ├── ARCHITECTURE.md
│   ├── DEPLOYMENT.md
│   └── API.md
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml             # GitHub Actions pipeline
│
├── Dockerfile                    # Container configuration
├── docker-compose.yml            # Local development setup
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
└── README.md                     # This file
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.9+
- Docker Desktop
- Azure Account (Free tier available)
- Git

### 1. Clone Repository
```bash
git clone https://github.com/EstebanM-M/ecommerce-chatbot-azure.git
cd ecommerce-chatbot-azure
```

### 2. Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Azure Resources Setup
```bash
# Create Azure resources (detailed in docs/DEPLOYMENT.md)
# - Azure Bot Service
# - Azure SQL Database
# - Azure Container Registry
# - Application Insights
```

### 4. Database Setup
```bash
# Run SQL scripts
sqlcmd -S your-server.database.windows.net -d ecommerce_chatbot -U your-user -P your-password -i sql/schema.sql
sqlcmd -S your-server.database.windows.net -d ecommerce_chatbot -U your-user -P your-password -i sql/seed_data.sql
```

### 5. Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your Azure credentials
# AZURE_BOT_APP_ID=your-app-id
# AZURE_BOT_APP_PASSWORD=your-app-password
# AZURE_SQL_CONNECTION_STRING=your-connection-string
```

### 6. Run Locally
```bash
# Start the bot
python -m bot.bot

# In another terminal, start the dashboard
streamlit run dashboard/app.py

# Open frontend/index.html in browser for Web Chat
```

## 🎯 Usage

### Chatbot Interactions
```
User: "Track my order #12345"
Bot: "Your order #12345 is currently in transit. Expected delivery: Jan 25, 2026"

User: "I need a laptop for programming"
Bot: "Based on your needs, I recommend:
     1. Dell XPS 15 - $1,299
     2. MacBook Pro M3 - $1,999
     Would you like more details?"
```

### Dashboard Access
Navigate to `http://localhost:8501` to view:
- Real-time conversation metrics
- Sentiment analysis trends
- Product recommendation performance
- SQL query builder for custom reports

## 📊 Analytics Dashboard

The Streamlit dashboard provides:

1. **Overview Page**: Key metrics, conversation volume, resolution rate
2. **Sentiment Analysis**: Customer satisfaction trends, emotion distribution
3. **Product Insights**: Top products, recommendation accuracy, conversion rates
4. **Custom Queries**: SQL query interface for advanced analytics

## 🐳 Docker Deployment

```bash
# Build image
docker build -t ecommerce-chatbot .

# Run with docker-compose
docker-compose up -d

# Access services
# Bot: http://localhost:3978
# Dashboard: http://localhost:8501
```

## 🔄 CI/CD Pipeline

GitHub Actions workflow automatically:
1. Runs tests on push
2. Builds Docker image
3. Deploys to Azure Container Instances
4. Updates Application Insights

## 📈 Key Metrics

- **Response Time**: < 2 seconds average
- **Intent Recognition Accuracy**: > 85%
- **Sentiment Analysis Accuracy**: > 90%
- **User Satisfaction**: Measured via CSAT surveys
- **Automation Rate**: % of conversations resolved without human intervention

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run specific test suite
pytest tests/test_bot.py -v

# Run with coverage
pytest --cov=bot --cov=ml_models tests/
```

## 📝 Documentation

- [Architecture Details](docs/ARCHITECTURE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [API Reference](docs/API.md)

## 🤝 Contributing

This is a portfolio project, but feedback and suggestions are welcome!

## 📄 License

MIT License

## 👤 Author

**Esteban Bernal**
- LinkedIn: [Esteban Morales](https://www.linkedin.com/in/esteban-morales-mahecha/)
- GitHub: [@EstebanM-M](https://github.com/EstebanM-M)

## 🙏 Acknowledgments

- Azure Bot Framework documentation
- Hugging Face Transformers library
- Streamlit community

---

**Note**: This project demonstrates enterprise-grade chatbot development with Azure, ML integration, and full-stack deployment capabilities for e-commerce customer support scenarios.
