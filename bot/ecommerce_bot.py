"""
Main Bot Class for E-commerce Customer Support
Handles conversation flow, intent recognition, and responses
"""

from typing import List, Dict, Any
from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
from botbuilder.schema import ChannelAccount, Activity, ActivityTypes
from datetime import datetime
import re

from bot.utils.db_helper import DatabaseHelper
from bot.utils.response_formatter import ResponseFormatter
from ml_models.sentiment.inference import SentimentAnalyzer
from ml_models.recommendations.inference import ProductRecommender


class EcommerceBot(ActivityHandler):
    """
    E-commerce Customer Support Bot
    Handles various customer intents including order tracking,
    product search, and FAQ responses
    """

    def __init__(self, db_helper: DatabaseHelper):
        """
        Initialize the bot
        
        Args:
            db_helper: Database helper instance for SQL operations
        """
        super().__init__()
        self.db = db_helper
        self.formatter = ResponseFormatter()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.product_recommender = ProductRecommender()
        
        # Conversation state storage (in production, use Azure Bot State Service)
        self.conversation_state: Dict[str, Any] = {}

    async def on_message_activity(self, turn_context: TurnContext):
        """
        Handle incoming messages from users
        
        Args:
            turn_context: Turn context containing the user message
        """
        user_message = turn_context.activity.text.strip()
        user_id = turn_context.activity.from_property.id
        conversation_id = turn_context.activity.conversation.id

        # Log incoming message
        print(f"[{datetime.now()}] User {user_id}: {user_message}")

        # Analyze sentiment
        sentiment_result = self.sentiment_analyzer.analyze(user_message)
        
        # Get or create conversation in database
        conv_id = await self._get_or_create_conversation(
            user_id, conversation_id, turn_context.activity.channel_id
        )

        # Save user message to database
        await self._save_message(
            conv_id,
            "User",
            user_message,
            sentiment=sentiment_result["sentiment"],
            sentiment_score=sentiment_result["score"]
        )

        # Recognize intent and extract entities
        intent, entities, confidence = await self._recognize_intent(user_message)

        # Generate response based on intent
        response_text = await self._handle_intent(
            intent, entities, user_message, user_id, conv_id, turn_context
        )

        # Save bot response to database
        await self._save_message(
            conv_id,
            "Bot",
            response_text,
            intent=intent,
            confidence_score=confidence
        )

        # Send response to user
        await turn_context.send_activity(MessageFactory.text(response_text))

        # Log bot response
        print(f"[{datetime.now()}] Bot: {response_text[:100]}...")

    async def on_members_added_activity(
        self, members_added: List[ChannelAccount], turn_context: TurnContext
    ):
        """
        Greet new members when they join the conversation
        
        Args:
            members_added: List of new members
            turn_context: Turn context
        """
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                welcome_message = self.formatter.format_welcome_message()
                await turn_context.send_activity(MessageFactory.text(welcome_message))

    async def _recognize_intent(self, message: str) -> tuple[str, Dict[str, Any], float]:
        """
        Recognize user intent from message
        
        Args:
            message: User message text
            
        Returns:
            tuple: (intent_name, entities, confidence_score)
        """
        message_lower = message.lower()
        
        # Order tracking intent
        if any(keyword in message_lower for keyword in ["track", "order", "status", "where is my"]):
            # Extract order number if present
            order_pattern = r'ord-\d{4}-\d{5}|#?\d{5,}'
            order_match = re.search(order_pattern, message, re.IGNORECASE)
            entities = {"order_number": order_match.group(0) if order_match else None}
            return "track_order", entities, 0.95

        # Product search intent
        if any(keyword in message_lower for keyword in ["looking for", "need", "want", "buy", "purchase", "find"]):
            # Extract product category/name
            entities = {"search_query": message}
            return "product_search", entities, 0.88

        # Product recommendation intent
        if any(keyword in message_lower for keyword in ["recommend", "suggestion", "what should i", "best"]):
            entities = {"category": None}  # Can be enhanced with NER
            return "product_recommendation", entities, 0.90

        # Return policy intent
        if any(keyword in message_lower for keyword in ["return", "refund", "money back"]):
            return "return_policy", {}, 0.92

        # Shipping info intent
        if any(keyword in message_lower for keyword in ["shipping", "delivery", "ship"]):
            return "shipping_info", {}, 0.91

        # Payment methods intent
        if any(keyword in message_lower for keyword in ["payment", "pay", "credit card", "paypal"]):
            return "payment_methods", {}, 0.89

        # Cancel order intent
        if any(keyword in message_lower for keyword in ["cancel", "stop"]):
            return "cancel_order", {}, 0.87

        # Greeting intent
        if any(keyword in message_lower for keyword in ["hi", "hello", "hey", "good morning", "good afternoon"]):
            return "greeting", {}, 0.99

        # Goodbye intent
        if any(keyword in message_lower for keyword in ["bye", "goodbye", "thanks", "thank you", "see you"]):
            return "goodbye", {}, 0.94

        # Help intent
        if any(keyword in message_lower for keyword in ["help", "assist", "support"]):
            return "help", {}, 0.96

        # Default: unknown intent
        return "unknown", {"query": message}, 0.30

    async def _handle_intent(
        self,
        intent: str,
        entities: Dict[str, Any],
        message: str,
        user_id: str,
        conversation_id: int,
        turn_context: TurnContext
    ) -> str:
        """
        Handle different intents and generate appropriate responses
        
        Args:
            intent: Recognized intent
            entities: Extracted entities
            message: Original user message
            user_id: User identifier
            conversation_id: Database conversation ID
            turn_context: Turn context
            
        Returns:
            str: Response text
        """
        # Track order
        if intent == "track_order":
            order_number = entities.get("order_number")
            if order_number:
                return await self._handle_order_tracking(order_number)
            else:
                return "I'd be happy to help you track your order! Could you please provide your order number? It should look like ORD-2026-00001."

        # Product search
        elif intent == "product_search":
            search_query = entities.get("search_query", message)
            return await self._handle_product_search(search_query)

        # Product recommendation
        elif intent == "product_recommendation":
            category = entities.get("category")
            return await self._handle_product_recommendation(user_id, category)

        # Return policy
        elif intent == "return_policy":
            return self.formatter.format_return_policy()

        # Shipping info
        elif intent == "shipping_info":
            return self.formatter.format_shipping_info()

        # Payment methods
        elif intent == "payment_methods":
            return self.formatter.format_payment_methods()

        # Cancel order
        elif intent == "cancel_order":
            return "I can help you cancel your order. Please provide your order number, and I'll process the cancellation for you."

        # Greeting
        elif intent == "greeting":
            return self.formatter.format_welcome_message()

        # Goodbye
        elif intent == "goodbye":
            return "Thank you for chatting with us! Have a wonderful day! Feel free to return if you need any assistance. 😊"

        # Help
        elif intent == "help":
            return self.formatter.format_help_message()

        # Unknown intent - search FAQ
        else:
            faq_response = await self._search_faq(message)
            if faq_response:
                return faq_response
            else:
                return self.formatter.format_fallback_message()

    async def _handle_order_tracking(self, order_number: str) -> str:
        """
        Handle order tracking request
        
        Args:
            order_number: Order number to track
            
        Returns:
            str: Order status message
        """
        # Clean order number
        order_number = order_number.strip().upper()
        if not order_number.startswith("ORD-"):
            # Try to format it
            order_number = f"ORD-{order_number}" if order_number.replace("-", "").isdigit() else order_number

        # Query database for order status
        order = await self.db.get_order_status(order_number)
        
        if order:
            return self.formatter.format_order_status(order)
        else:
            return f"I couldn't find an order with number {order_number}. Please check the order number and try again, or contact customer service if you need assistance."

    async def _handle_product_search(self, query: str) -> str:
        """
        Handle product search request
        
        Args:
            query: Search query
            
        Returns:
            str: Product search results
        """
        # Extract potential category from query
        category_keywords = {
            "laptop": "Laptops",
            "computer": "Laptops",
            "phone": "Smartphones",
            "smartphone": "Smartphones",
            "headphone": "Accessories",
            "mouse": "Accessories",
            "book": "Books",
            "appliance": "Appliances"
        }
        
        category = None
        query_lower = query.lower()
        for keyword, cat in category_keywords.items():
            if keyword in query_lower:
                category = cat
                break

        # Search products
        products = await self.db.search_products(query, category, limit=3)
        
        if products:
            return self.formatter.format_product_list(products, query)
        else:
            return f"I couldn't find any products matching '{query}'. Could you try a different search term, or let me know what category you're interested in?"

    async def _handle_product_recommendation(self, user_id: str, category: str = None) -> str:
        """
        Handle product recommendation request
        
        Args:
            user_id: User identifier
            category: Optional category filter
            
        Returns:
            str: Product recommendations
        """
        # Get recommendations from ML model
        recommendations = await self.product_recommender.get_recommendations(
            user_id=user_id,
            category=category,
            n_recommendations=3
        )
        
        if recommendations:
            return self.formatter.format_product_recommendations(recommendations, category)
        else:
            # Fallback to popular products
            popular_products = await self.db.get_popular_products(limit=3)
            return self.formatter.format_product_list(popular_products, "our most popular items")

    async def _search_faq(self, query: str) -> str:
        """
        Search FAQ database for similar questions
        
        Args:
            query: User query
            
        Returns:
            str: FAQ answer or None
        """
        faq_result = await self.db.search_faq(query)
        
        if faq_result:
            # Increment times_asked counter
            await self.db.increment_faq_asked(faq_result["faq_id"])
            return faq_result["answer"]
        
        return None

    async def _get_or_create_conversation(
        self, user_id: str, session_id: str, channel: str
    ) -> int:
        """
        Get existing conversation or create new one
        
        Args:
            user_id: User identifier
            session_id: Conversation session ID
            channel: Communication channel
            
        Returns:
            int: Conversation ID from database
        """
        conv_id = await self.db.get_conversation_by_session(session_id)
        
        if not conv_id:
            conv_id = await self.db.create_conversation(user_id, session_id, channel)
        
        return conv_id

    async def _save_message(
        self,
        conversation_id: int,
        sender_type: str,
        message_text: str,
        intent: str = None,
        confidence_score: float = None,
        sentiment: str = None,
        sentiment_score: float = None
    ) -> None:
        """
        Save message to database
        
        Args:
            conversation_id: Database conversation ID
            sender_type: 'User' or 'Bot'
            message_text: Message content
            intent: Recognized intent (optional)
            confidence_score: Intent confidence (optional)
            sentiment: Sentiment label (optional)
            sentiment_score: Sentiment score (optional)
        """
        await self.db.save_message(
            conversation_id=conversation_id,
            sender_type=sender_type,
            message_text=message_text,
            intent=intent,
            confidence_score=confidence_score,
            sentiment=sentiment,
            sentiment_score=sentiment_score
        )
