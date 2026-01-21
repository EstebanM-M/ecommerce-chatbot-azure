"""
SQLite Database Helper - For Local Development
No Azure SQL required!
"""

import sqlite3
from typing import List, Dict, Any, Optional
from datetime import datetime
from loguru import logger
import os


class DatabaseHelper:
    """Helper class for SQLite database operations"""
    
    def __init__(self, db_path: str = "ecommerce_chatbot.db"):
        """Initialize SQLite database connection"""
        self.db_path = db_path
        self.conn = None
        self._connect()
        self._create_tables()
    
    def _connect(self) -> None:
        """Establish database connection"""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
            logger.info(f"✅ SQLite Database connected: {self.db_path}")
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            raise
    
    def _create_tables(self) -> None:
        """Create tables if they don't exist"""
        cursor = self.conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                email TEXT UNIQUE,
                full_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                category TEXT,
                price REAL,
                rating REAL,
                description TEXT,
                stock_quantity INTEGER DEFAULT 0,
                reviews_count INTEGER DEFAULT 0
            )
        """)
        
        # Orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                order_number TEXT UNIQUE,
                order_date TIMESTAMP,
                total_amount REAL,
                status TEXT,
                shipping_address TEXT,
                estimated_delivery DATE,
                tracking_number TEXT
            )
        """)
        
        # Conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Conversations (
                conversation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                session_id TEXT,
                channel TEXT,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ended_at TIMESTAMP,
                total_messages INTEGER DEFAULT 0,
                resolved INTEGER DEFAULT 0,
                satisfaction_score INTEGER
            )
        """)
        
        # Messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Messages (
                message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER,
                sender_type TEXT,
                message_text TEXT,
                intent TEXT,
                confidence_score REAL,
                sentiment TEXT,
                sentiment_score REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # FAQ table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS FAQ (
                faq_id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
                answer TEXT,
                category TEXT,
                times_asked INTEGER DEFAULT 0
            )
        """)
        
        self.conn.commit()
        
        # Insert sample data if empty
        cursor.execute("SELECT COUNT(*) FROM Products")
        if cursor.fetchone()[0] == 0:
            self._insert_sample_data()
        
        logger.info("✅ Database tables created/verified")
    
    def _insert_sample_data(self) -> None:
        """Insert sample data for testing"""
        cursor = self.conn.cursor()
        
        # Sample users
        cursor.execute("""
            INSERT INTO Users (username, email, full_name) 
            VALUES ('john_doe', 'john@example.com', 'John Doe')
        """)
        
        # Sample products
        products = [
            ('Dell XPS 15 Laptop', 'Laptops', 1299.99, 4.7, '15.6" FHD Display, Intel i7, 16GB RAM', 25, 234),
            ('MacBook Pro M3', 'Laptops', 1999.99, 4.9, '14" Retina Display, M3 Chip, 16GB RAM', 15, 567),
            ('iPhone 15 Pro', 'Smartphones', 999.99, 4.8, '6.1" Display, A17 Pro Chip, 128GB', 50, 891),
            ('Sony WH-1000XM5', 'Accessories', 349.99, 4.8, 'Wireless Noise-Cancelling Headphones', 60, 1234),
        ]
        
        cursor.executemany("""
            INSERT INTO Products (product_name, category, price, rating, description, stock_quantity, reviews_count)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, products)
        
        # Sample orders
        orders = [
            (1, 'ORD-2026-00001', '2026-01-15 10:30:00', 1349.98, 'Shipped', '123 Main St, New York, NY', '2026-01-22', 'TRK123456789'),
            (1, 'ORD-2026-00002', '2026-01-10 14:20:00', 999.99, 'Delivered', '123 Main St, New York, NY', '2026-01-15', 'TRK987654321'),
        ]
        
        cursor.executemany("""
            INSERT INTO Orders (user_id, order_number, order_date, total_amount, status, shipping_address, estimated_delivery, tracking_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, orders)
        
        # Sample FAQs
        faqs = [
            ('What is your return policy?', 'We offer a 30-day money-back guarantee on all products. Items must be in original condition.', 'Returns', 0),
            ('How long does shipping take?', 'Standard shipping takes 5-7 business days. Express shipping is available for $15.', 'Shipping', 0),
            ('What payment methods do you accept?', 'We accept Visa, Mastercard, American Express, PayPal, and Apple Pay.', 'Payment', 0),
        ]
        
        cursor.executemany("""
            INSERT INTO FAQ (question, answer, category, times_asked)
            VALUES (?, ?, ?, ?)
        """, faqs)
        
        self.conn.commit()
        logger.info("✅ Sample data inserted")
    
    async def check_connection(self) -> bool:
        """Check if database connection is active"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Database connection check failed: {e}")
            return False
    
    async def get_order_status(self, order_number: str) -> Optional[Dict[str, Any]]:
        """Get order status by order number"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT o.*, u.email, u.full_name
                FROM Orders o
                LEFT JOIN Users u ON o.user_id = u.user_id
                WHERE o.order_number = ?
            """, (order_number,))
            
            row = cursor.fetchone()
            if row:
                return {
                    "order_number": row["order_number"],
                    "status": row["status"],
                    "order_date": datetime.fromisoformat(row["order_date"]),
                    "total_amount": row["total_amount"],
                    "tracking_number": row["tracking_number"],
                    "estimated_delivery": row["estimated_delivery"],
                    "shipping_address": row["shipping_address"],
                    "customer_email": row["email"] if row["email"] else "N/A",
                    "customer_name": row["full_name"] if row["full_name"] else "N/A"
                }
            return None
        except Exception as e:
            logger.error(f"Error getting order status: {e}")
            return None
    
    async def search_products(self, query: str, category: Optional[str] = None, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for products"""
        try:
            cursor = self.conn.cursor()
            
            if category:
                cursor.execute("""
                    SELECT * FROM Products
                    WHERE (product_name LIKE ? OR description LIKE ?)
                    AND category = ?
                    AND stock_quantity > 0
                    ORDER BY rating DESC, reviews_count DESC
                    LIMIT ?
                """, (f"%{query}%", f"%{query}%", category, limit))
            else:
                cursor.execute("""
                    SELECT * FROM Products
                    WHERE (product_name LIKE ? OR description LIKE ?)
                    AND stock_quantity > 0
                    ORDER BY rating DESC, reviews_count DESC
                    LIMIT ?
                """, (f"%{query}%", f"%{query}%", limit))
            
            rows = cursor.fetchall()
            products = []
            for row in rows:
                products.append({
                    "product_id": row["product_id"],
                    "product_name": row["product_name"],
                    "category": row["category"],
                    "price": row["price"],
                    "rating": row["rating"],
                    "description": row["description"],
                    "stock_quantity": row["stock_quantity"]
                })
            
            return products
        except Exception as e:
            logger.error(f"Error searching products: {e}")
            return []
    
    async def get_popular_products(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get most popular products"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM Products
                WHERE stock_quantity > 0
                ORDER BY rating DESC, reviews_count DESC
                LIMIT ?
            """, (limit,))
            
            rows = cursor.fetchall()
            products = []
            for row in rows:
                products.append({
                    "product_id": row["product_id"],
                    "product_name": row["product_name"],
                    "category": row["category"],
                    "price": row["price"],
                    "rating": row["rating"],
                    "description": row["description"],
                    "reviews_count": row["reviews_count"]
                })
            
            return products
        except Exception as e:
            logger.error(f"Error getting popular products: {e}")
            return []
    
    async def search_faq(self, query: str) -> Optional[Dict[str, Any]]:
        """Search FAQ database"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM FAQ
                WHERE question LIKE ? OR answer LIKE ?
                ORDER BY times_asked DESC
                LIMIT 1
            """, (f"%{query}%", f"%{query}%"))
            
            row = cursor.fetchone()
            if row:
                return {
                    "faq_id": row["faq_id"],
                    "question": row["question"],
                    "answer": row["answer"],
                    "category": row["category"]
                }
            return None
        except Exception as e:
            logger.error(f"Error searching FAQ: {e}")
            return None
    
    async def increment_faq_asked(self, faq_id: int) -> None:
        """Increment FAQ asked counter"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE FAQ
                SET times_asked = times_asked + 1
                WHERE faq_id = ?
            """, (faq_id,))
            self.conn.commit()
        except Exception as e:
            logger.error(f"Error incrementing FAQ counter: {e}")
    
    async def get_conversation_by_session(self, session_id: str) -> Optional[int]:
        """Get conversation ID by session ID"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT conversation_id FROM Conversations
                WHERE session_id = ? AND ended_at IS NULL
            """, (session_id,))
            
            row = cursor.fetchone()
            return row["conversation_id"] if row else None
        except Exception as e:
            logger.error(f"Error getting conversation: {e}")
            return None
    
    async def create_conversation(self, user_id: str, session_id: str, channel: str) -> int:
        """Create new conversation"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO Conversations (user_id, session_id, channel)
                VALUES (1, ?, ?)
            """, (session_id, channel))
            
            self.conn.commit()
            logger.info(f"Created conversation for session {session_id}")
            return cursor.lastrowid
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
        """Save message to database"""
        try:
            cursor = self.conn.cursor()
            
            # Insert message
            cursor.execute("""
                INSERT INTO Messages (conversation_id, sender_type, message_text, intent, confidence_score, sentiment, sentiment_score)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (conversation_id, sender_type, message_text, intent, confidence_score, sentiment, sentiment_score))
            
            # Update conversation message count
            cursor.execute("""
                UPDATE Conversations
                SET total_messages = total_messages + 1
                WHERE conversation_id = ?
            """, (conversation_id,))
            
            self.conn.commit()
        except Exception as e:
            logger.error(f"Error saving message: {e}")
    
    def close(self) -> None:
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")