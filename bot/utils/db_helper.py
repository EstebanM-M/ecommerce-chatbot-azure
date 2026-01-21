"""
Database Helper Utility
Handles all database operations for the chatbot
"""

import pyodbc
from typing import List, Dict, Any, Optional
from datetime import datetime
from loguru import logger

from bot.config import config


class DatabaseHelper:
    """Helper class for database operations"""
    
    def __init__(self):
        """Initialize database connection"""
        self.connection_string = config.get_sql_connection_string()
        self.conn = None
        self._connect()
    
    def _connect(self) -> None:
        """Establish database connection"""
        try:
            self.conn = pyodbc.connect(self.connection_string)
            logger.info("✅ Database connected successfully")
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            raise
    
    def _get_connection(self) -> pyodbc.Connection:
        """Get active database connection, reconnect if needed"""
        try:
            # Test connection
            cursor = self.conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            return self.conn
        except:
            # Reconnect if connection lost
            logger.warning("Database connection lost, reconnecting...")
            self._connect()
            return self.conn
    
    async def check_connection(self) -> bool:
        """
        Check if database connection is active
        
        Returns:
            bool: True if connected
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
            return True
        except Exception as e:
            logger.error(f"Database connection check failed: {e}")
            return False
    
    async def get_order_status(self, order_number: str) -> Optional[Dict[str, Any]]:
        """
        Get order status by order number
        
        Args:
            order_number: Order number
            
        Returns:
            dict: Order details or None
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "EXEC sp_GetOrderStatus @order_number=?",
                order_number
            )
            
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return {
                    "order_number": row.order_number,
                    "status": row.status,
                    "order_date": row.order_date,
                    "total_amount": float(row.total_amount),
                    "tracking_number": row.tracking_number,
                    "estimated_delivery": row.estimated_delivery,
                    "shipping_address": row.shipping_address,
                    "customer_email": row.email,
                    "customer_name": row.full_name
                }
            return None
            
        except Exception as e:
            logger.error(f"Error getting order status: {e}")
            return None
    
    async def search_products(
        self, query: str, category: Optional[str] = None, limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search for products
        
        Args:
            query: Search query
            category: Product category filter
            limit: Maximum results
            
        Returns:
            list: Product list
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            sql = """
                SELECT TOP (?) product_id, product_name, category, price, 
                       rating, description, stock_quantity
                FROM Products
                WHERE is_active = 1
                AND stock_quantity > 0
                AND (product_name LIKE ? OR description LIKE ?)
            """
            params = [limit, f"%{query}%", f"%{query}%"]
            
            if category:
                sql += " AND category = ?"
                params.append(category)
            
            sql += " ORDER BY rating DESC, reviews_count DESC"
            
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            cursor.close()
            
            products = []
            for row in rows:
                products.append({
                    "product_id": row.product_id,
                    "product_name": row.product_name,
                    "category": row.category,
                    "price": float(row.price),
                    "rating": float(row.rating) if row.rating else 0,
                    "description": row.description,
                    "stock_quantity": row.stock_quantity
                })
            
            return products
            
        except Exception as e:
            logger.error(f"Error searching products: {e}")
            return []
    
    async def get_popular_products(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get most popular products
        
        Args:
            limit: Maximum results
            
        Returns:
            list: Product list
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT TOP (?) product_id, product_name, category, price, 
                       rating, description, reviews_count
                FROM Products
                WHERE is_active = 1 AND stock_quantity > 0
                ORDER BY rating DESC, reviews_count DESC
            """, limit)
            
            rows = cursor.fetchall()
            cursor.close()
            
            products = []
            for row in rows:
                products.append({
                    "product_id": row.product_id,
                    "product_name": row.product_name,
                    "category": row.category,
                    "price": float(row.price),
                    "rating": float(row.rating) if row.rating else 0,
                    "description": row.description,
                    "reviews_count": row.reviews_count
                })
            
            return products
            
        except Exception as e:
            logger.error(f"Error getting popular products: {e}")
            return []
    
    async def search_faq(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Search FAQ database
        
        Args:
            query: User query
            
        Returns:
            dict: FAQ entry or None
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT TOP 1 faq_id, question, answer, category
                FROM FAQ
                WHERE is_active = 1
                AND (question LIKE ? OR answer LIKE ?)
                ORDER BY helpful_count DESC
            """, f"%{query}%", f"%{query}%")
            
            row = cursor.fetchone()
            cursor.close()
            
            if row:
                return {
                    "faq_id": row.faq_id,
                    "question": row.question,
                    "answer": row.answer,
                    "category": row.category
                }
            return None
            
        except Exception as e:
            logger.error(f"Error searching FAQ: {e}")
            return None
    
    async def increment_faq_asked(self, faq_id: int) -> None:
        """
        Increment FAQ asked counter
        
        Args:
            faq_id: FAQ ID
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE FAQ
                SET times_asked = times_asked + 1
                WHERE faq_id = ?
            """, faq_id)
            
            conn.commit()
            cursor.close()
            
        except Exception as e:
            logger.error(f"Error incrementing FAQ counter: {e}")
    
    async def get_conversation_by_session(self, session_id: str) -> Optional[int]:
        """
        Get conversation ID by session ID
        
        Args:
            session_id: Session identifier
            
        Returns:
            int: Conversation ID or None
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT conversation_id
                FROM Conversations
                WHERE session_id = ?
                AND ended_at IS NULL
            """, session_id)
            
            row = cursor.fetchone()
            cursor.close()
            
            return row.conversation_id if row else None
            
        except Exception as e:
            logger.error(f"Error getting conversation: {e}")
            return None
    
    async def create_conversation(
        self, user_id: str, session_id: str, channel: str
    ) -> int:
        """
        Create new conversation
        
        Args:
            user_id: User identifier
            session_id: Session identifier
            channel: Communication channel
            
        Returns:
            int: New conversation ID
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # For demo purposes, use a default user_id of 1 if user not in database
            # In production, you would create/retrieve actual user records
            
            cursor.execute("""
                INSERT INTO Conversations (user_id, session_id, channel)
                VALUES (1, ?, ?)
            """, session_id, channel)
            
            conn.commit()
            
            # Get the inserted ID
            cursor.execute("SELECT @@IDENTITY")
            conversation_id = cursor.fetchone()[0]
            cursor.close()
            
            logger.info(f"Created conversation {conversation_id} for session {session_id}")
            return int(conversation_id)
            
        except Exception as e:
            logger.error(f"Error creating conversation: {e}")
            raise
    
    async def save_message(
        self,
        conversation_id: int,
        sender_type: str,
        message_text: str,
        intent: Optional[str] = None,
        confidence_score: Optional[float] = None,
        sentiment: Optional[str] = None,
        sentiment_score: Optional[float] = None
    ) -> None:
        """
        Save message to database
        
        Args:
            conversation_id: Conversation ID
            sender_type: 'User' or 'Bot'
            message_text: Message text
            intent: Intent name
            confidence_score: Intent confidence
            sentiment: Sentiment label
            sentiment_score: Sentiment score
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                EXEC sp_LogMessage
                    @conversation_id=?,
                    @sender_type=?,
                    @message_text=?,
                    @intent=?,
                    @confidence_score=?,
                    @sentiment=?,
                    @sentiment_score=?
            """, 
                conversation_id,
                sender_type,
                message_text,
                intent,
                confidence_score,
                sentiment,
                sentiment_score
            )
            
            conn.commit()
            cursor.close()
            
        except Exception as e:
            logger.error(f"Error saving message: {e}")
    
    def close(self) -> None:
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
