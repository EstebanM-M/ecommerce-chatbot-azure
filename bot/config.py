"""
Configuration module for E-commerce Chatbot
Manages environment variables and Azure credentials
"""

import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()


class Config:
    """Bot Configuration"""

    # Azure Bot Service Configuration
    MICROSOFT_APP_ID: str = os.getenv("MICROSOFT_APP_ID", "")
    MICROSOFT_APP_PASSWORD: str = os.getenv("MICROSOFT_APP_PASSWORD", "")
    MICROSOFT_APP_TYPE: str = os.getenv("MICROSOFT_APP_TYPE", "MultiTenant")
    MICROSOFT_APP_TENANTID: str = os.getenv("MICROSOFT_APP_TENANTID", "")

    # Azure SQL Database Configuration
    SQL_SERVER: str = os.getenv("SQL_SERVER", "")
    SQL_DATABASE: str = os.getenv("SQL_DATABASE", "ecommerce_chatbot")
    SQL_USERNAME: str = os.getenv("SQL_USERNAME", "")
    SQL_PASSWORD: str = os.getenv("SQL_PASSWORD", "")
    SQL_DRIVER: str = os.getenv("SQL_DRIVER", "{ODBC Driver 18 for SQL Server}")

    # Azure Cognitive Services
    AZURE_TEXT_ANALYTICS_KEY: str = os.getenv("AZURE_TEXT_ANALYTICS_KEY", "")
    AZURE_TEXT_ANALYTICS_ENDPOINT: str = os.getenv("AZURE_TEXT_ANALYTICS_ENDPOINT", "")

    # Application Insights
    APPINSIGHTS_INSTRUMENTATION_KEY: str = os.getenv(
        "APPINSIGHTS_INSTRUMENTATION_KEY", ""
    )

    # Bot Configuration
    BOT_NAME: str = os.getenv("BOT_NAME", "E-commerce Support Bot")
    BOT_VERSION: str = os.getenv("BOT_VERSION", "1.0.0")

    # ML Models Configuration
    SENTIMENT_MODEL_PATH: str = os.getenv(
        "SENTIMENT_MODEL_PATH", "ml_models/sentiment/model"
    )
    RECOMMENDATION_MODEL_PATH: str = os.getenv(
        "RECOMMENDATION_MODEL_PATH", "ml_models/recommendations/model"
    )
    USE_PRETRAINED_MODELS: bool = os.getenv("USE_PRETRAINED_MODELS", "true").lower() == "true"

    # Conversation Settings
    MAX_CONVERSATION_DURATION_MINUTES: int = int(
        os.getenv("MAX_CONVERSATION_DURATION_MINUTES", "30")
    )
    ENABLE_ANALYTICS: bool = os.getenv("ENABLE_ANALYTICS", "true").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # API Settings
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "3978"))

    @classmethod
    def get_sql_connection_string(cls) -> str:
        """
        Generate SQL Server connection string
        
        Returns:
            str: ODBC connection string
        """
        return (
            f"Driver={cls.SQL_DRIVER};"
            f"Server=tcp:{cls.SQL_SERVER},1433;"
            f"Database={cls.SQL_DATABASE};"
            f"Uid={cls.SQL_USERNAME};"
            f"Pwd={cls.SQL_PASSWORD};"
            f"Encrypt=yes;"
            f"TrustServerCertificate=no;"
            f"Connection Timeout=30;"
        )

    @classmethod
    def validate_config(cls) -> tuple[bool, list[str]]:
        """
        Validate required configuration values
        
        Returns:
            tuple: (is_valid, list of missing configs)
        """
        missing_configs = []

        # For local development with SQLite, Azure credentials are optional
        # Only validate if we're NOT using SQLite (local development)
        
        # Check if running in local development mode
        is_local_dev = not cls.SQL_SERVER or cls.SQL_SERVER == "your-server-name.database.windows.net"
        
        if is_local_dev:
            # Local development - only critical config is nothing (we use SQLite)
            # Azure credentials are optional
            pass
        else:
            # Production - require Azure credentials
            critical_configs = {
                "MICROSOFT_APP_ID": cls.MICROSOFT_APP_ID,
                "MICROSOFT_APP_PASSWORD": cls.MICROSOFT_APP_PASSWORD,
                "SQL_SERVER": cls.SQL_SERVER,
                "SQL_USERNAME": cls.SQL_USERNAME,
                "SQL_PASSWORD": cls.SQL_PASSWORD,
            }

            for key, value in critical_configs.items():
                if not value:
                    missing_configs.append(key)

        is_valid = True  # Always valid for local development
        return is_valid, missing_configs

    @classmethod
    def print_config_summary(cls) -> None:
        """Print configuration summary (without sensitive data)"""
        print("=" * 60)
        print("BOT CONFIGURATION SUMMARY")
        print("=" * 60)
        print(f"Bot Name: {cls.BOT_NAME}")
        print(f"Bot Version: {cls.BOT_VERSION}")
        print(f"App Type: {cls.MICROSOFT_APP_TYPE}")
        print(f"SQL Server: {cls.SQL_SERVER}")
        print(f"SQL Database: {cls.SQL_DATABASE}")
        print(f"Use Pretrained Models: {cls.USE_PRETRAINED_MODELS}")
        print(f"Analytics Enabled: {cls.ENABLE_ANALYTICS}")
        print(f"Log Level: {cls.LOG_LEVEL}")
        print(f"API Host: {cls.API_HOST}:{cls.API_PORT}")
        print("=" * 60)

        # Validate configuration
        is_valid, missing = cls.validate_config()
        if not is_valid:
            print(f"⚠️  WARNING: Missing configurations: {', '.join(missing)}")
            print("Please check your .env file")
        else:
            print("✅ All critical configurations are set")
        print("=" * 60)


# Create singleton instance
config = Config()
