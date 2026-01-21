# 🚀 Deployment Guide - E-commerce Chatbot

This guide will walk you through deploying the E-commerce Chatbot to Azure.

## 📋 Prerequisites

Before you begin, ensure you have:

1. **Azure Account** - [Sign up for free](https://azure.microsoft.com/free/) (includes $200 credit)
2. **Azure CLI** - [Install Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
3. **Docker Desktop** - [Install Docker](https://www.docker.com/products/docker-desktop)
4. **Git** - [Install Git](https://git-scm.com/downloads)
5. **Python 3.9+** - [Install Python](https://www.python.org/downloads/)

## 🎯 Deployment Overview

```
┌─────────────────────────────────────────────────────────┐
│                    AZURE DEPLOYMENT                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐    ┌──────────────────────┐          │
│  │ Azure Bot    │───▶│ Azure Container      │          │
│  │ Service      │    │ Instance (ACI)       │          │
│  └──────────────┘    └──────────────────────┘          │
│         │                      │                        │
│         │                      │                        │
│         ▼                      ▼                        │
│  ┌──────────────┐    ┌──────────────────────┐          │
│  │ Application  │    │ Azure SQL Database   │          │
│  │ Insights     │    │                      │          │
│  └──────────────┘    └──────────────────────┘          │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## 🔧 Step 1: Setup Azure Resources

### 1.1 Login to Azure

```bash
az login
az account set --subscription "YOUR_SUBSCRIPTION_ID"
```

### 1.2 Create Resource Group

```bash
# Create resource group
az group create \
  --name ecommerce-chatbot-rg \
  --location eastus

# Verify creation
az group show --name ecommerce-chatbot-rg
```

### 1.3 Create Azure SQL Database

```bash
# Create SQL Server
az sql server create \
  --name ecommerce-chatbot-sql \
  --resource-group ecommerce-chatbot-rg \
  --location eastus \
  --admin-user sqladmin \
  --admin-password "YourSecurePassword123!"

# Create database
az sql db create \
  --resource-group ecommerce-chatbot-rg \
  --server ecommerce-chatbot-sql \
  --name ecommerce_chatbot \
  --service-objective S0 \
  --zone-redundant false

# Configure firewall (allow Azure services)
az sql server firewall-rule create \
  --resource-group ecommerce-chatbot-rg \
  --server ecommerce-chatbot-sql \
  --name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0

# Add your IP for database setup
az sql server firewall-rule create \
  --resource-group ecommerce-chatbot-rg \
  --server ecommerce-chatbot-sql \
  --name AllowMyIP \
  --start-ip-address YOUR_IP_ADDRESS \
  --end-ip-address YOUR_IP_ADDRESS
```

### 1.4 Setup Database Schema

```bash
# Install sqlcmd if not already installed
# On macOS: brew install sqlcmd
# On Ubuntu: apt-get install mssql-tools

# Connect and run schema script
sqlcmd -S ecommerce-chatbot-sql.database.windows.net \
  -d ecommerce_chatbot \
  -U sqladmin \
  -P "YourSecurePassword123!" \
  -i sql/schema.sql

# Run seed data script
sqlcmd -S ecommerce-chatbot-sql.database.windows.net \
  -d ecommerce_chatbot \
  -U sqladmin \
  -P "YourSecurePassword123!" \
  -i sql/seed_data.sql
```

### 1.5 Create Azure Bot Service

```bash
# Create Azure Bot
az bot create \
  --resource-group ecommerce-chatbot-rg \
  --name ecommerce-chatbot \
  --location global \
  --kind registration \
  --sku F0

# Get bot credentials
az bot show \
  --resource-group ecommerce-chatbot-rg \
  --name ecommerce-chatbot
```

**Important**: Note down the `appId` from the output. You'll need to create an app password in the next step.

### 1.6 Create App Registration and Secret

```bash
# This will be done in Azure Portal
# Go to: Azure Portal > Azure Active Directory > App registrations > Your Bot
# Under "Certificates & secrets", create a new client secret
# Note down the secret VALUE (not the ID)
```

### 1.7 Create Application Insights (Optional)

```bash
# Create Application Insights
az monitor app-insights component create \
  --app ecommerce-chatbot-insights \
  --location eastus \
  --resource-group ecommerce-chatbot-rg \
  --application-type web

# Get instrumentation key
az monitor app-insights component show \
  --app ecommerce-chatbot-insights \
  --resource-group ecommerce-chatbot-rg \
  --query instrumentationKey
```

## 🐳 Step 2: Build and Push Docker Image

### 2.1 Create Azure Container Registry

```bash
# Create ACR
az acr create \
  --resource-group ecommerce-chatbot-rg \
  --name ecommerceacr \
  --sku Basic

# Login to ACR
az acr login --name ecommerceacr
```

### 2.2 Build and Push Image

```bash
# Build Docker image
docker build -t ecommerce-chatbot:latest .

# Tag image for ACR
docker tag ecommerce-chatbot:latest \
  ecommerceacr.azurecr.io/ecommerce-chatbot:latest

# Push to ACR
docker push ecommerceacr.azurecr.io/ecommerce-chatbot:latest
```

## ☁️ Step 3: Deploy to Azure Container Instances

### 3.1 Create .env file for deployment

Create a file named `.env.azure` with your production values:

```bash
MICROSOFT_APP_ID=your-app-id-here
MICROSOFT_APP_PASSWORD=your-app-password-here
SQL_SERVER=ecommerce-chatbot-sql.database.windows.net
SQL_DATABASE=ecommerce_chatbot
SQL_USERNAME=sqladmin
SQL_PASSWORD=YourSecurePassword123!
APPINSIGHTS_INSTRUMENTATION_KEY=your-instrumentation-key
```

### 3.2 Deploy Container

```bash
# Create ACI
az container create \
  --resource-group ecommerce-chatbot-rg \
  --name ecommerce-chatbot-container \
  --image ecommerceacr.azurecr.io/ecommerce-chatbot:latest \
  --registry-login-server ecommerceacr.azurecr.io \
  --registry-username ecommerceacr \
  --registry-password $(az acr credential show --name ecommerceacr --query "passwords[0].value" -o tsv) \
  --dns-name-label ecommerce-chatbot-api \
  --ports 3978 \
  --environment-variables \
    MICROSOFT_APP_ID="your-app-id" \
    SQL_SERVER="ecommerce-chatbot-sql.database.windows.net" \
    SQL_DATABASE="ecommerce_chatbot" \
    SQL_USERNAME="sqladmin" \
  --secure-environment-variables \
    MICROSOFT_APP_PASSWORD="your-app-password" \
    SQL_PASSWORD="YourSecurePassword123!" \
  --cpu 1 \
  --memory 1.5

# Get container FQDN
az container show \
  --resource-group ecommerce-chatbot-rg \
  --name ecommerce-chatbot-container \
  --query ipAddress.fqdn
```

## 🔗 Step 4: Configure Bot Messaging Endpoint

```bash
# Update bot with messaging endpoint
# The endpoint will be: https://YOUR-CONTAINER-FQDN:3978/api/messages

az bot update \
  --resource-group ecommerce-chatbot-rg \
  --name ecommerce-chatbot \
  --endpoint "https://ecommerce-chatbot-api.eastus.azurecontainer.io:3978/api/messages"
```

## 🌐 Step 5: Configure Web Chat Channel

1. Go to Azure Portal
2. Navigate to your Bot Service resource
3. Click on "Channels" in the left menu
4. Click on "Web Chat" 
5. Copy one of the secret keys
6. Update `frontend/index.html` with the secret key:

```javascript
const BOT_SECRET = 'YOUR_WEB_CHAT_SECRET_HERE';
```

## 📊 Step 6: Deploy Streamlit Dashboard (Optional)

### Option A: Deploy to Azure Container Instances

```bash
# Build dashboard image
docker build -f Dockerfile.dashboard -t ecommerce-dashboard:latest .

# Tag and push
docker tag ecommerce-dashboard:latest \
  ecommerceacr.azurecr.io/ecommerce-dashboard:latest
docker push ecommerceacr.azurecr.io/ecommerce-dashboard:latest

# Deploy
az container create \
  --resource-group ecommerce-chatbot-rg \
  --name ecommerce-dashboard-container \
  --image ecommerceacr.azurecr.io/ecommerce-dashboard:latest \
  --registry-login-server ecommerceacr.azurecr.io \
  --registry-username ecommerceacr \
  --registry-password $(az acr credential show --name ecommerceacr --query "passwords[0].value" -o tsv) \
  --dns-name-label ecommerce-dashboard \
  --ports 8501 \
  --command-line "streamlit run dashboard/app.py --server.port=8501 --server.address=0.0.0.0" \
  --environment-variables \
    SQL_SERVER="ecommerce-chatbot-sql.database.windows.net" \
    SQL_DATABASE="ecommerce_chatbot" \
    SQL_USERNAME="sqladmin" \
  --secure-environment-variables \
    SQL_PASSWORD="YourSecurePassword123!" \
  --cpu 1 \
  --memory 2
```

### Option B: Deploy to Azure App Service

```bash
# Create App Service Plan
az appservice plan create \
  --name ecommerce-dashboard-plan \
  --resource-group ecommerce-chatbot-rg \
  --is-linux \
  --sku B1

# Create Web App
az webapp create \
  --resource-group ecommerce-chatbot-rg \
  --plan ecommerce-dashboard-plan \
  --name ecommerce-dashboard-app \
  --deployment-container-image-name ecommerceacr.azurecr.io/ecommerce-dashboard:latest

# Configure Web App
az webapp config appsettings set \
  --resource-group ecommerce-chatbot-rg \
  --name ecommerce-dashboard-app \
  --settings \
    SQL_SERVER="ecommerce-chatbot-sql.database.windows.net" \
    SQL_DATABASE="ecommerce_chatbot" \
    SQL_USERNAME="sqladmin" \
    SQL_PASSWORD="YourSecurePassword123!"
```

## ✅ Step 7: Testing

### 7.1 Test Bot Endpoint

```bash
# Test health endpoint
curl https://ecommerce-chatbot-api.eastus.azurecontainer.io:3978/health
```

### 7.2 Test Web Chat

1. Open `frontend/index.html` in a browser
2. Start chatting with the bot
3. Try commands like:
   - "Track order ORD-2026-00001"
   - "I'm looking for a laptop"
   - "What's your return policy?"

### 7.3 Test Dashboard

Navigate to: `http://ecommerce-dashboard.eastus.azurecontainer.io:8501`

## 📈 Step 8: Monitoring and Logging

### View Application Insights

```bash
# View recent traces
az monitor app-insights query \
  --app ecommerce-chatbot-insights \
  --analytics-query "traces | take 50"
```

### View Container Logs

```bash
# View bot logs
az container logs \
  --resource-group ecommerce-chatbot-rg \
  --name ecommerce-chatbot-container

# Stream logs in real-time
az container logs \
  --resource-group ecommerce-chatbot-rg \
  --name ecommerce-chatbot-container \
  --follow
```

## 🔄 Step 9: CI/CD with GitHub Actions (Optional)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Azure

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Login to Azure
      uses: azure/login@v1
      with:
        creds: ${{ secrets.AZURE_CREDENTIALS }}
    
    - name: Build and push Docker image
      run: |
        az acr login --name ecommerceacr
        docker build -t ecommerceacr.azurecr.io/ecommerce-chatbot:latest .
        docker push ecommerceacr.azurecr.io/ecommerce-chatbot:latest
    
    - name: Restart container
      run: |
        az container restart \
          --resource-group ecommerce-chatbot-rg \
          --name ecommerce-chatbot-container
```

## 🧹 Cleanup (Optional)

To delete all resources:

```bash
az group delete --name ecommerce-chatbot-rg --yes --no-wait
```

## 💰 Cost Estimation

**Free Tier Resources:**
- Azure Bot Service (F0): FREE
- Azure SQL Database (Basic): ~$5/month
- Azure Container Instances: ~$15/month
- Application Insights: First 5GB/month FREE

**Estimated Monthly Cost: $20-30**

## 🆘 Troubleshooting

### Bot not responding?
- Check container logs: `az container logs --resource-group ecommerce-chatbot-rg --name ecommerce-chatbot-container`
- Verify messaging endpoint is correctly configured
- Ensure app credentials match

### Dashboard not loading data?
- Verify SQL connection string
- Check firewall rules on SQL Server
- Review container logs

### Database connection errors?
- Verify SQL Server firewall rules include Azure services
- Check credentials in environment variables
- Test connection with sqlcmd

## 📚 Additional Resources

- [Azure Bot Service Documentation](https://docs.microsoft.com/en-us/azure/bot-service/)
- [Bot Framework SDK](https://github.com/microsoft/botbuilder-python)
- [Azure Container Instances](https://docs.microsoft.com/en-us/azure/container-instances/)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

**Need Help?** Open an issue on GitHub or contact support.
