"""
E-commerce Chatbot - Main Application Entry Point
Azure Bot Framework with aiohttp server
"""

import sys
from aiohttp import web
from aiohttp.web import Request, Response
from botbuilder.core import BotFrameworkAdapterSettings, BotFrameworkAdapter
from botbuilder.schema import Activity
from loguru import logger

from bot.config import config
from bot.ecommerce_bot import EcommerceBot

# Use SQLite for local development (no Azure SQL needed)
# from bot.utils.db_helper import DatabaseHelper  # Azure SQL version
from bot.utils.db_helper_sqlite import DatabaseHelper  # SQLite version (easier!)


# Configure logger
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level=config.LOG_LEVEL
)


class BotApp:
    """Main Bot Application"""
    
    def __init__(self):
        """Initialize bot application"""
        # Print configuration summary
        config.print_config_summary()
        
        # Validate configuration
        is_valid, missing = config.validate_config()
        if not is_valid:
            logger.error(f"Missing required configurations: {missing}")
            logger.error("Please check your .env file and try again")
            sys.exit(1)
        
        # Check if running in local development mode
        is_local = not config.MICROSOFT_APP_ID or config.MICROSOFT_APP_ID == ""
        
        if is_local:
            logger.info("🔓 Running in LOCAL DEVELOPMENT mode (no authentication)")
        else:
            logger.info("🔐 Running in PRODUCTION mode (with authentication)")
        
        # Create adapter settings (empty strings disable auth validation)
        self.settings = BotFrameworkAdapterSettings(
            app_id=config.MICROSOFT_APP_ID or "",
            app_password=config.MICROSOFT_APP_PASSWORD or ""
        )
        
        # Create adapter
        self.adapter = BotFrameworkAdapter(self.settings)
        
        # Create database helper
        self.db_helper = DatabaseHelper()
        
        # Create bot instance
        self.bot = EcommerceBot(self.db_helper)
        
        # Error handler
        async def on_error(context, error):
            logger.error(f"Error in conversation: {error}")
            await context.send_activity("I apologize, but I encountered an error. Please try again.")
        
        self.adapter.on_turn_error = on_error
        
        logger.info("✅ Bot initialized successfully")
    
    async def messages(self, req: Request) -> Response:
        """
        Main endpoint for receiving messages from Azure Bot Service
        
        Args:
            req: HTTP request
            
        Returns:
            Response: HTTP response
        """
        # Check if request is authenticated
        if "application/json" in req.headers.get("Content-Type", ""):
            body = await req.json()
        else:
            return Response(status=415, text="Unsupported Media Type")
        
        activity = Activity().deserialize(body)
        auth_header = req.headers.get("Authorization", "")
        
        try:
            # Create callback for bot
            async def bot_callback(turn_context):
                await self.bot.on_turn(turn_context)
            
            # Process the activity
            response = await self.adapter.process_activity(
                activity,
                auth_header,
                bot_callback
            )
            
            if response:
                return Response(status=response.status, text=response.body)
            return Response(status=200)
            
        except Exception as e:
            logger.error(f"Error processing activity: {e}")
            return Response(status=500, text=str(e))
    
    async def health_check(self, req: Request) -> Response:
        """
        Health check endpoint for monitoring
        
        Args:
            req: HTTP request
            
        Returns:
            Response: Health status
        """
        # Check database connection
        try:
            db_status = await self.db_helper.check_connection()
            return web.json_response({
                "status": "healthy",
                "bot_name": config.BOT_NAME,
                "version": config.BOT_VERSION,
                "database": "connected" if db_status else "disconnected"
            })
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return web.json_response({
                "status": "unhealthy",
                "error": str(e)
            }, status=503)
    
    async def root(self, req: Request) -> Response:
        """
        Root endpoint with bot information
        
        Args:
            req: HTTP request
            
        Returns:
            Response: Bot information
        """
        return web.json_response({
            "bot_name": config.BOT_NAME,
            "version": config.BOT_VERSION,
            "status": "running",
            "endpoints": {
                "messages": "/api/messages",
                "health": "/health"
            }
        })
    
    def create_app(self) -> web.Application:
        """
        Create aiohttp application
        
        Returns:
            Application: Configured web application
        """
        app = web.Application()
        
        # Add routes
        app.router.add_get("/", self.root)
        app.router.add_get("/health", self.health_check)
        app.router.add_post("/api/messages", self.messages)
        
        logger.info(f"Routes configured:")
        logger.info(f"  GET  / - Root endpoint")
        logger.info(f"  GET  /health - Health check")
        logger.info(f"  POST /api/messages - Bot messages endpoint")
        
        return app


def main():
    """Main entry point"""
    logger.info("=" * 60)
    logger.info("STARTING E-COMMERCE CHATBOT")
    logger.info("=" * 60)
    
    try:
        # Create bot application
        bot_app = BotApp()
        
        # Create web application
        app = bot_app.create_app()
        
        # Start server
        logger.info(f"🚀 Starting server on {config.API_HOST}:{config.API_PORT}")
        logger.info("=" * 60)
        
        web.run_app(
            app,
            host=config.API_HOST,
            port=config.API_PORT
        )
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()