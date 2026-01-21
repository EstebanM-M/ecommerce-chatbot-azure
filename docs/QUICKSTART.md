# ⚡ Quick Start Guide - E-commerce Chatbot

Get the chatbot running locally in under 10 minutes!

## 📦 What You'll Need

- **Python 3.9+** 
- **Azure Account** (Free tier works! Get $200 credit)
- **SQL Server** (Azure SQL Database or local SQL Server)

## 🚀 5-Minute Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/ecommerce-chatbot-azure.git
cd ecommerce-chatbot-azure
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Setup Azure Resources (10 minutes)

**Option A: Using Azure Portal (GUI)**

1. **Create Azure SQL Database:**
   - Go to [Azure Portal](https://portal.azure.com)
   - Click "Create a resource" → "SQL Database"
   - Create new server and database
   - Note: Server name, database name, username, password

2. **Create Azure Bot Service:**
   - Click "Create a resource" → "Azure Bot"
   - Choose "Bot Channels Registration"
   - Note: App ID and create App Password

3. **Run SQL Scripts:**
   - Open Azure Data Studio or SQL Server Management Studio
   - Connect to your Azure SQL Database
   - Execute `sql/schema.sql`
   - Execute `sql/seed_data.sql`

**Option B: Using Azure CLI (faster)**

```bash
# Login
az login

# Create everything
az group create --name chatbot-rg --location eastus

# Create SQL
az sql server create \
  --name myserver123 \
  --resource-group chatbot-rg \
  --admin-user sqladmin \
  --admin-password "SecurePass123!"

az sql db create \
  --resource-group chatbot-rg \
  --server myserver123 \
  --name ecommerce_chatbot \
  --service-objective S0

# Create Bot
az bot create \
  --resource-group chatbot-rg \
  --name mybot \
  --kind registration \
  --sku F0
```

### Step 4: Configure Environment Variables

```bash
# Copy example file
cp .env.example .env

# Edit .env with your values
nano .env  # or use your favorite editor
```

**Minimum required values:**
```bash
MICROSOFT_APP_ID=your-bot-app-id
MICROSOFT_APP_PASSWORD=your-bot-password
SQL_SERVER=yourserver.database.windows.net
SQL_DATABASE=ecommerce_chatbot
SQL_USERNAME=sqladmin
SQL_PASSWORD=YourPassword123!
```

### Step 5: Run the Bot! 🎉

```bash
# Start the bot
python -m bot.bot

# You should see:
# ✅ Bot initialized successfully
# 🚀 Starting server on 0.0.0.0:3978
```

### Step 6: Test Locally with Bot Framework Emulator

1. **Download Bot Framework Emulator:**
   - [Download here](https://github.com/Microsoft/BotFramework-Emulator/releases)

2. **Connect to your bot:**
   - Open Emulator
   - Click "Open Bot"
   - Enter endpoint: `http://localhost:3978/api/messages`
   - Enter App ID and Password from .env

3. **Start chatting!**
   - Try: "Track order ORD-2026-00001"
   - Try: "I'm looking for a laptop"

## 📊 Launch the Dashboard

In a **new terminal** (keep the bot running):

```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Start Streamlit dashboard
streamlit run dashboard/app.py

# Dashboard opens at: http://localhost:8501
```

## 🌐 Testing Web Chat Interface

1. **Get Web Chat Secret:**
   - Azure Portal → Your Bot → Channels → Web Chat
   - Copy one of the secret keys

2. **Update HTML file:**
   ```bash
   # Edit frontend/index.html
   # Replace: const BOT_SECRET = 'YOUR_BOT_SECRET_HERE';
   # With: const BOT_SECRET = 'your-actual-secret';
   ```

3. **Open in browser:**
   ```bash
   # Just open the file
   open frontend/index.html  # macOS
   # or double-click the file in Windows/Linux
   ```

## 🎯 Quick Test Scenarios

Try these commands in your bot:

### 📦 Order Tracking
```
User: Track my order
Bot: Could you provide your order number?
User: ORD-2026-00001
Bot: [Shows order status with tracking]
```

### 🔍 Product Search
```
User: I need a laptop for programming
Bot: [Shows recommended laptops with prices]
```

### ❓ FAQ
```
User: What's your return policy?
Bot: [Shows comprehensive return policy]
```

## 🐳 Docker Quick Start (Alternative)

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access:
# Bot: http://localhost:3978
# Dashboard: http://localhost:8501

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## 📱 Test on Mobile (Bonus)

1. Install **ngrok**: https://ngrok.com/download
2. Run ngrok:
   ```bash
   ngrok http 3978
   ```
3. Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)
4. Update Azure Bot messaging endpoint:
   ```bash
   az bot update \
     --resource-group chatbot-rg \
     --name mybot \
     --endpoint "https://abc123.ngrok.io/api/messages"
   ```
5. Open Web Chat on your phone!

## 🎓 What's Next?

### Customize Your Bot
- Edit intents in `bot/ecommerce_bot.py`
- Add new dialogs in `bot/dialogs/`
- Modify responses in `bot/utils/response_formatter.py`

### Improve ML Models
- Train custom sentiment model in `ml_models/sentiment/train.py`
- Build recommendation system in `ml_models/recommendations/train.py`

### Enhance Dashboard
- Add new pages in `dashboard/pages/`
- Create custom queries in `dashboard/utils/`

### Deploy to Production
- Follow `docs/DEPLOYMENT.md` for Azure deployment
- Setup CI/CD with GitHub Actions

## 🆘 Troubleshooting

### "Database connection failed"
```bash
# Test connection
sqlcmd -S yourserver.database.windows.net \
  -d ecommerce_chatbot \
  -U sqladmin \
  -P "YourPassword123!"

# Check firewall rules in Azure Portal
```

### "Bot not responding in Emulator"
```bash
# Verify bot is running
curl http://localhost:3978/health

# Check credentials match in .env and Emulator
```

### "Module not found"
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### "Port already in use"
```bash
# Change port in .env
API_PORT=3979

# Or kill existing process
# macOS/Linux: lsof -ti:3978 | xargs kill
# Windows: netstat -ano | findstr :3978
```

## 💡 Tips

1. **Use Bot Framework Emulator** for fastest testing
2. **Check health endpoint** `http://localhost:3978/health` to verify bot is running
3. **Monitor logs** in terminal to see what bot is doing
4. **SQL queries** are logged if LOG_LEVEL=DEBUG
5. **Dashboard auto-refreshes** data every time you switch pages

## 📚 Learning Resources

- **Bot Framework Tutorial**: https://docs.microsoft.com/en-us/azure/bot-service/
- **SQL Server Tutorial**: https://www.w3schools.com/sql/
- **Streamlit Tutorial**: https://docs.streamlit.io/
- **Python Async Tutorial**: https://realpython.com/async-io-python/

## 🎉 You're Ready!

Your chatbot is now running! Here's what to explore:

1. ✅ Chat with bot in Emulator
2. ✅ View analytics in Dashboard
3. ✅ Test different intents
4. ✅ Customize responses
5. ✅ Deploy to Azure (when ready)

**Happy Coding! 🚀**

---

**Questions?** Check the full documentation in `docs/` or open an issue on GitHub.
