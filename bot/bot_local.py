"""
Local Development Bot - NO AUTHENTICATION
Use this for testing locally without Bot Framework auth
"""

import sys
from aiohttp import web
from aiohttp.web import Request, Response
from loguru import logger
import json

from bot.ecommerce_bot import EcommerceBot
from bot.utils.db_helper_sqlite import DatabaseHelper

logger.remove()
logger.add(sys.stdout, level="INFO")


class SimpleTurnContext:
    """Simple turn context without Bot Framework"""
    
    def __init__(self, activity_data):
        self.activity = type('Activity', (), activity_data)
        self.responded = False
        self.response_text = ""
    
    async def send_activity(self, text):
        """Store response"""
        if isinstance(text, str):
            self.response_text = text
        else:
            self.response_text = text.text if hasattr(text, 'text') else str(text)
        self.responded = True


class LocalBotApp:
    """Simple bot app for local development"""
    
    def __init__(self):
        logger.info("=" * 60)
        logger.info("LOCAL DEVELOPMENT BOT (No Authentication)")
        logger.info("=" * 60)
        
        self.db = DatabaseHelper()
        self.bot = EcommerceBot(self.db)
        
        logger.info("✅ Local bot initialized")
    
    async def messages(self, req: Request) -> Response:
        """Handle messages without Bot Framework"""
        try:
            body = await req.json()
            
            # Extract message
            message_type = body.get("type", "")
            
            if message_type == "message":
                user_message = body.get("text", "")
                user_id = body.get("from", {}).get("id", "user123")
                
                logger.info(f"📥 Received: {user_message}")
                
                # Create simple turn context
                activity_data = {
                    "text": user_message,
                    "type": "message",
                    "from_property": type('User', (), {"id": user_id}),
                    "conversation": type('Conv', (), {"id": "local_conv"}),
                    "channel_id": "emulator"
                }
                
                turn_context = SimpleTurnContext(activity_data)
                
                # Process with bot
                await self.bot.on_message_activity(turn_context)
                
                # Return response WITH CORS headers
                if turn_context.responded:
                    logger.info(f"📤 Response: {turn_context.response_text[:50]}...")
                    response = web.json_response({
                        "type": "message",
                        "text": turn_context.response_text,
                        "from": {"id": "bot"},
                        "conversation": {"id": "local_conv"}
                    })
                    # Add CORS headers
                    response.headers['Access-Control-Allow-Origin'] = '*'
                    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
                    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
                    return response
                else:
                    response = Response(status=200)
                    response.headers['Access-Control-Allow-Origin'] = '*'
                    return response
            
            elif message_type == "conversationUpdate":
                # Handle welcome
                response = web.json_response({
                    "type": "message",
                    "text": "👋 Bot connected! Send me a message.",
                    "from": {"id": "bot"}
                })
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response
            
            response = Response(status=200)
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
            
        except Exception as e:
            logger.error(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            response = Response(status=500, text=str(e))
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
    
    async def health(self, req: Request) -> Response:
        """Health check"""
        response = web.json_response({"status": "healthy"})
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    
    async def options_handler(self, req: Request) -> Response:
        """Handle OPTIONS requests for CORS"""
        response = Response(status=200)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    
    def create_app(self):
        """Create web app"""
        app = web.Application()
        app.router.add_post("/api/messages", self.messages)
        app.router.add_options("/api/messages", self.options_handler)
        app.router.add_get("/health", self.health)
        app.router.add_options("/health", self.options_handler)
        logger.info("✅ Routes configured")
        return app


def main():
    logger.info("🚀 Starting LOCAL bot on http://localhost:3978")
    logger.info("=" * 60)
    
    app = LocalBotApp().create_app()
    web.run_app(app, host="0.0.0.0", port=3978, print=None)


if __name__ == "__main__":
    main()