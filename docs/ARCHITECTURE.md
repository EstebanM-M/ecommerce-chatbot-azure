# 🏗️ Architecture Documentation - E-commerce Chatbot

## System Overview

This document describes the architecture of the E-commerce Customer Support Chatbot system.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACES                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Web Chat    │  │ MS Teams     │  │  Mobile App  │          │
│  │  (HTML/JS)   │  │  Integration │  │  (Future)    │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                  │                  │                  │
│         └──────────────────┼──────────────────┘                  │
│                            │                                     │
└────────────────────────────┼─────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AZURE BOT FRAMEWORK                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────┐         │
│  │         Azure Bot Service (Channels)                │         │
│  │  - Web Chat Channel                                 │         │
│  │  - Microsoft Teams Channel                          │         │
│  │  - Direct Line API                                  │         │
│  └────────────────────┬───────────────────────────────┘         │
│                       │                                          │
└───────────────────────┼──────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BOT APPLICATION LAYER                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────┐       │
│  │              Bot Framework Adapter                    │       │
│  │  - Handles authentication                             │       │
│  │  - Processes activities                               │       │
│  │  - Error handling                                     │       │
│  └─────────────────────┬────────────────────────────────┘       │
│                        │                                         │
│                        ▼                                         │
│  ┌──────────────────────────────────────────────────────┐       │
│  │            EcommerceBot (Main Logic)                  │       │
│  │                                                        │       │
│  │  ┌────────────────────────────────────────────┐      │       │
│  │  │  Intent Recognition                         │      │       │
│  │  │  - Pattern matching                         │      │       │
│  │  │  - Keyword extraction                       │      │       │
│  │  │  - Entity extraction                        │      │       │
│  │  └────────────────────────────────────────────┘      │       │
│  │                                                        │       │
│  │  ┌────────────────────────────────────────────┐      │       │
│  │  │  Dialog Management                          │      │       │
│  │  │  - Order tracking dialog                    │      │       │
│  │  │  - Product search dialog                    │      │       │
│  │  │  - FAQ dialog                               │      │       │
│  │  └────────────────────────────────────────────┘      │       │
│  │                                                        │       │
│  └────────────────────┬───────────────────────────────────┘      │
│                       │                                          │
└───────────────────────┼──────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌─────────────┐ ┌────────────────┐
│  ML Models   │ │  Database   │ │  External      │
│  Layer       │ │  Layer      │ │  Services      │
└──────────────┘ └─────────────┘ └────────────────┘
```

## Component Details

### 1. Bot Application Layer

#### 1.1 Main Bot Class (`bot/ecommerce_bot.py`)
- **Responsibilities:**
  - Process incoming user messages
  - Recognize user intents
  - Route to appropriate dialog/handler
  - Generate contextual responses
  - Log conversations

- **Key Methods:**
  - `on_message_activity()`: Handle incoming messages
  - `_recognize_intent()`: Determine user intent
  - `_handle_intent()`: Route to intent handlers
  - `_save_message()`: Log to database

#### 1.2 Configuration (`bot/config.py`)
- **Purpose:** Centralized configuration management
- **Features:**
  - Environment variable loading
  - Validation of required configs
  - Connection string generation
  - Configuration summary printing

#### 1.3 Database Helper (`bot/utils/db_helper.py`)
- **Responsibilities:**
  - Manage SQL Server connections
  - Execute queries and stored procedures
  - Handle database errors gracefully
  - Provide data access methods

- **Key Methods:**
  - `get_order_status()`: Retrieve order information
  - `search_products()`: Search product catalog
  - `search_faq()`: Find FAQ answers
  - `save_message()`: Log conversation messages

#### 1.4 Response Formatter (`bot/utils/response_formatter.py`)
- **Purpose:** Format consistent, user-friendly responses
- **Features:**
  - Template-based responses
  - Dynamic content insertion
  - Multi-language support ready
  - Emoji and formatting

### 2. Machine Learning Layer

#### 2.1 Sentiment Analysis (`ml_models/sentiment/`)
- **Technology:** VADER Sentiment Analyzer
- **Purpose:** Analyze emotional tone of user messages
- **Outputs:**
  - Sentiment label (Positive/Negative/Neutral)
  - Confidence score (0-1)
  - Compound score (-1 to 1)

- **Use Cases:**
  - Detect frustrated customers
  - Trigger human escalation
  - Track satisfaction metrics
  - Personalize responses

#### 2.2 Product Recommendations (`ml_models/recommendations/`)
- **Approach:** Hybrid (Collaborative + Content-based)
- **Features:**
  - Product similarity calculation
  - User preference learning
  - Category associations
  - Ranking algorithms

- **Metrics:**
  - Recommendation score
  - Click-through rate
  - Conversion rate

### 3. Database Layer

#### 3.1 Schema Design

**Core Tables:**
- `Users`: Customer information
- `Products`: Product catalog
- `Orders`: Order records
- `Conversations`: Chat sessions
- `Messages`: Individual messages
- `FAQ`: Frequently asked questions

**Analytics Tables:**
- `ChatbotAnalytics`: Daily aggregated metrics
- `ProductRecommendations`: Recommendation tracking

**Views:**
- `vw_DailyConversationMetrics`: Daily conversation stats
- `vw_SentimentAnalysis`: Sentiment trends
- `vw_TopIntents`: Most common intents
- `vw_RecommendationPerformance`: ML performance

**Stored Procedures:**
- `sp_GetOrderStatus`: Retrieve order details
- `sp_LogMessage`: Save conversation message
- `sp_GetProductRecommendations`: Get product suggestions
- `sp_UpdateDailyAnalytics`: Update analytics tables

### 4. Analytics Dashboard

#### 4.1 Streamlit Application (`dashboard/app.py`)
- **Technology:** Streamlit + Plotly
- **Features:**
  - Real-time metrics visualization
  - Interactive charts and graphs
  - SQL query builder
  - Export capabilities

#### 4.2 Dashboard Pages
1. **Overview**: KPIs and summary metrics
2. **Conversations**: Trends and volume analysis
3. **Sentiment**: Emotion distribution and trends
4. **Intents**: Top user requests
5. **Products**: Recommendation performance

### 5. Frontend Layer

#### 5.1 Web Chat Interface (`frontend/index.html`)
- **Technology:** Bot Framework Web Chat SDK
- **Features:**
  - Responsive design
  - Modern UI with gradient styling
  - Message history
  - Typing indicators
  - Suggested actions support

## Data Flow

### Typical Conversation Flow

```
1. User sends message via Web Chat
   ↓
2. Azure Bot Service receives message
   ↓
3. Bot Framework Adapter processes activity
   ↓
4. EcommerceBot.on_message_activity() triggered
   ↓
5. Sentiment analysis performed on message
   ↓
6. Intent recognition executed
   ↓
7. Database queried for relevant data
   ↓
8. ML models provide recommendations (if needed)
   ↓
9. Response formatted using ResponseFormatter
   ↓
10. Message saved to database
    ↓
11. Response sent back to user
    ↓
12. Analytics updated asynchronously
```

## Security Architecture

### Authentication & Authorization
- **Bot Authentication**: OAuth 2.0 with Azure AD
- **Database**: SQL Server authentication with encrypted connection
- **API Keys**: Stored in Azure Key Vault (production)
- **Secrets Management**: Environment variables (development)

### Data Protection
- **In Transit**: TLS/HTTPS for all communications
- **At Rest**: Azure SQL Database encryption
- **PII Handling**: Anonymized logging
- **Compliance**: GDPR-ready data retention policies

## Scalability Considerations

### Horizontal Scaling
- **Bot Instances**: Azure Container Instances with load balancing
- **Database**: Azure SQL Database auto-scaling
- **Caching**: Redis cache for frequently accessed data (future)

### Performance Optimization
- **Connection Pooling**: Database connection reuse
- **Async Operations**: Non-blocking I/O for external calls
- **Query Optimization**: Indexed queries and stored procedures
- **Caching Strategy**: In-memory caching for static data

## Monitoring & Observability

### Application Insights
- **Metrics Tracked:**
  - Request volume
  - Response times
  - Error rates
  - Custom events (intents, user actions)

### Logging Strategy
- **Log Levels:**
  - ERROR: Critical failures
  - WARNING: Unexpected conditions
  - INFO: General informational messages
  - DEBUG: Detailed diagnostic information

### Health Checks
- **Bot Health**: `/health` endpoint
- **Database Health**: Connection validation
- **ML Models**: Model availability check

## Deployment Architecture

### Development
```
Local Machine
├── Python Bot (localhost:3978)
├── Streamlit Dashboard (localhost:8501)
└── Bot Framework Emulator
```

### Production (Azure)
```
Azure Cloud
├── Azure Bot Service (Global)
├── Azure Container Instances (Bot App)
├── Azure SQL Database
├── Azure Container Instances (Dashboard)
├── Application Insights
└── Azure Container Registry
```

## Technology Stack Summary

| Layer | Technology | Version |
|-------|-----------|---------|
| **Bot Framework** | Azure Bot SDK | 4.15.0 |
| **Language** | Python | 3.9+ |
| **Web Server** | aiohttp | 3.9.1 |
| **Database** | Azure SQL Server | Latest |
| **ORM** | pyodbc + SQLAlchemy | Latest |
| **ML/AI** | Transformers, VADER | Latest |
| **Dashboard** | Streamlit + Plotly | Latest |
| **Frontend** | Bot Framework Web Chat | Latest |
| **Containerization** | Docker | Latest |
| **CI/CD** | GitHub Actions | Latest |
| **Monitoring** | Application Insights | Latest |

## Extension Points

### Adding New Intents
1. Add pattern matching in `_recognize_intent()`
2. Create handler method `_handle_[intent_name]()`
3. Update `_handle_intent()` routing
4. Add response templates in `ResponseFormatter`

### Adding New Dialogs
1. Create dialog class in `bot/dialogs/`
2. Inherit from `ComponentDialog`
3. Register in bot initialization
4. Add tests

### Adding ML Models
1. Create model directory in `ml_models/`
2. Implement `train.py` and `inference.py`
3. Integrate with bot logic
4. Update configuration

### Adding Dashboard Pages
1. Create page in `dashboard/pages/`
2. Add SQL queries
3. Create visualizations
4. Register in main app

## Best Practices

1. **Code Organization**: Follow single responsibility principle
2. **Error Handling**: Always wrap external calls in try-catch
3. **Logging**: Log all important events with context
4. **Testing**: Write unit tests for critical paths
5. **Documentation**: Keep README and docs updated
6. **Security**: Never commit secrets to version control
7. **Performance**: Profile and optimize hot paths
8. **Monitoring**: Track key business metrics

## Future Enhancements

1. **Advanced NLU**: Azure LUIS or OpenAI GPT integration
2. **Multi-language**: i18n support
3. **Voice Support**: Speech-to-text integration
4. **Proactive Messaging**: Send updates to users
5. **A/B Testing**: Test different response strategies
6. **Advanced Analytics**: ML-powered insights
7. **Mobile App**: Native iOS/Android apps
8. **Integration**: CRM, ERP system connections

---

**Last Updated**: January 2026
**Version**: 1.0.0
