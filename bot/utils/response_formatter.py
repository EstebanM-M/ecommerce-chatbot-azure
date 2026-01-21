"""
Response Formatter Utility
Formats bot responses in a consistent, user-friendly manner
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, date


class ResponseFormatter:
    """Utility class for formatting bot responses"""
    
    @staticmethod
    def format_welcome_message() -> str:
        """
        Format welcome message
        
        Returns:
            str: Welcome message
        """
        return (
            "👋 Hello! Welcome to our e-commerce store! I'm your virtual assistant.\n\n"
            "I can help you with:\n"
            "• 📦 Track your orders\n"
            "• 🔍 Find products\n"
            "• 💡 Get product recommendations\n"
            "• ❓ Answer questions about shipping, returns, and more\n\n"
            "How can I assist you today?"
        )
    
    @staticmethod
    def format_help_message() -> str:
        """
        Format help message
        
        Returns:
            str: Help message
        """
        return (
            "I'm here to help! Here's what I can do:\n\n"
            "**Order Management:**\n"
            "• Track orders - Just say 'track my order' or provide your order number\n"
            "• Cancel orders - Say 'cancel my order'\n\n"
            "**Product Discovery:**\n"
            "• Search products - Tell me what you're looking for\n"
            "• Get recommendations - Ask 'recommend me a laptop'\n\n"
            "**Customer Service:**\n"
            "• Shipping information\n"
            "• Return policy\n"
            "• Payment methods\n"
            "• General FAQs\n\n"
            "Just type your question or request, and I'll do my best to help!"
        )
    
    @staticmethod
    def format_order_status(order: Dict[str, Any]) -> str:
        """
        Format order status response
        
        Args:
            order: Order details dictionary
            
        Returns:
            str: Formatted order status
        """
        status_emoji = {
            "Pending": "⏳",
            "Processing": "⚙️",
            "Shipped": "🚚",
            "Delivered": "✅",
            "Cancelled": "❌"
        }
        
        emoji = status_emoji.get(order["status"], "📦")
        
        message = f"{emoji} **Order Status: {order['status']}**\n\n"
        message += f"**Order Number:** {order['order_number']}\n"
        message += f"**Order Date:** {order['order_date'].strftime('%B %d, %Y')}\n"
        message += f"**Total Amount:** ${order['total_amount']:.2f}\n"
        
        if order["tracking_number"]:
            message += f"**Tracking Number:** {order['tracking_number']}\n"
        
        if order["estimated_delivery"]:
            if isinstance(order["estimated_delivery"], (datetime, date)):
                delivery_date = order["estimated_delivery"]
                if isinstance(delivery_date, datetime):
                    delivery_date = delivery_date.date()
                message += f"**Estimated Delivery:** {delivery_date.strftime('%B %d, %Y')}\n"
        
        if order["status"] == "Shipped":
            message += "\n📍 Your order is on its way!"
        elif order["status"] == "Delivered":
            message += "\n🎉 Your order has been delivered! We hope you enjoy your purchase!"
        elif order["status"] == "Processing":
            message += "\n⚙️ Your order is being prepared for shipment."
        
        message += "\n\nIs there anything else I can help you with?"
        
        return message
    
    @staticmethod
    def format_product_list(products: List[Dict[str, Any]], context: str = "") -> str:
        """
        Format product list response
        
        Args:
            products: List of product dictionaries
            context: Search context or query
            
        Returns:
            str: Formatted product list
        """
        if not products:
            return f"I couldn't find any products {context}. Please try a different search."
        
        intro = f"I found {len(products)} great product{'s' if len(products) > 1 else ''}"
        if context:
            intro += f" for {context}"
        intro += ":\n\n"
        
        message = intro
        
        for i, product in enumerate(products, 1):
            rating_stars = "⭐" * int(product.get("rating", 0))
            message += f"**{i}. {product['product_name']}**\n"
            message += f"   💰 ${product['price']:.2f}\n"
            message += f"   {rating_stars} {product.get('rating', 0):.1f}/5.0\n"
            
            if product.get("description"):
                desc = product["description"]
                if len(desc) > 80:
                    desc = desc[:80] + "..."
                message += f"   📝 {desc}\n"
            
            message += "\n"
        
        message += "Would you like more details about any of these products?"
        
        return message
    
    @staticmethod
    def format_product_recommendations(
        products: List[Dict[str, Any]], category: Optional[str] = None
    ) -> str:
        """
        Format product recommendations response
        
        Args:
            products: List of recommended products
            category: Product category
            
        Returns:
            str: Formatted recommendations
        """
        intro = "Based on your preferences, I recommend these products"
        if category:
            intro += f" in the {category} category"
        intro += ":\n\n"
        
        return ResponseFormatter.format_product_list(products, intro)
    
    @staticmethod
    def format_return_policy() -> str:
        """
        Format return policy response
        
        Returns:
            str: Return policy information
        """
        return (
            "**📦 Our Return Policy**\n\n"
            "We want you to be completely satisfied with your purchase!\n\n"
            "• ✅ **30-day money-back guarantee** on all products\n"
            "• ✅ Items must be in **original condition** with tags attached\n"
            "• ✅ Free return shipping on defective items\n"
            "• ✅ Refunds processed within **5-7 business days**\n\n"
            "**To initiate a return:**\n"
            "1. Go to 'My Orders' in your account\n"
            "2. Select the order and click 'Return Item'\n"
            "3. Choose your reason and print the return label\n"
            "4. Ship the item back to us\n\n"
            "Or contact our customer service team, and we'll help you through the process!\n\n"
            "Do you need help with a specific return?"
        )
    
    @staticmethod
    def format_shipping_info() -> str:
        """
        Format shipping information response
        
        Returns:
            str: Shipping information
        """
        return (
            "**🚚 Shipping Information**\n\n"
            "**Standard Shipping (5-7 business days):**\n"
            "• FREE on orders over $50\n"
            "• $5.99 on orders under $50\n\n"
            "**Express Shipping (2-3 business days):**\n"
            "• $15.00 flat rate\n\n"
            "**Overnight Shipping (1 business day):**\n"
            "• $25.00 flat rate\n\n"
            "**International Shipping:**\n"
            "• Available to 50+ countries\n"
            "• Rates vary by destination\n"
            "• Estimated delivery: 7-14 business days\n\n"
            "📦 All orders come with tracking information sent to your email!\n\n"
            "Need help with a specific order?"
        )
    
    @staticmethod
    def format_payment_methods() -> str:
        """
        Format payment methods response
        
        Returns:
            str: Payment methods information
        """
        return (
            "**💳 Accepted Payment Methods**\n\n"
            "We accept the following payment options:\n\n"
            "**Credit/Debit Cards:**\n"
            "• Visa\n"
            "• Mastercard\n"
            "• American Express\n"
            "• Discover\n\n"
            "**Digital Wallets:**\n"
            "• PayPal\n"
            "• Apple Pay\n"
            "• Google Pay\n\n"
            "🔒 All transactions are **secure and encrypted** for your protection.\n\n"
            "We do NOT store your full credit card information.\n\n"
            "Ready to make a purchase?"
        )
    
    @staticmethod
    def format_fallback_message() -> str:
        """
        Format fallback message for unrecognized intents
        
        Returns:
            str: Fallback message
        """
        return (
            "I'm not quite sure I understand. Could you rephrase that?\n\n"
            "I can help you with:\n"
            "• Tracking orders\n"
            "• Finding products\n"
            "• Shipping & return information\n"
            "• General questions\n\n"
            "Or type 'help' to see all my capabilities!"
        )
    
    @staticmethod
    def format_error_message() -> str:
        """
        Format error message
        
        Returns:
            str: Error message
        """
        return (
            "😓 I apologize, but I encountered an issue processing your request.\n\n"
            "Please try again, or contact our customer service team at:\n"
            "📧 support@ecommerce.com\n"
            "📞 1-800-555-0123 (Mon-Fri, 8 AM - 8 PM EST)"
        )
