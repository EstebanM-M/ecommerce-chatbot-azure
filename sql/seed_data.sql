-- Seed Data for E-commerce Chatbot Database
-- Sample data for testing and demonstration

-- ============================================
-- INSERT USERS
-- ============================================
INSERT INTO Users (username, email, full_name, phone, last_login) VALUES
('john_doe', 'john.doe@email.com', 'John Doe', '+1-555-0101', GETDATE()),
('jane_smith', 'jane.smith@email.com', 'Jane Smith', '+1-555-0102', GETDATE()),
('bob_wilson', 'bob.wilson@email.com', 'Bob Wilson', '+1-555-0103', GETDATE()),
('alice_brown', 'alice.brown@email.com', 'Alice Brown', '+1-555-0104', GETDATE()),
('charlie_davis', 'charlie.davis@email.com', 'Charlie Davis', '+1-555-0105', GETDATE());

-- ============================================
-- INSERT PRODUCTS
-- ============================================
INSERT INTO Products (product_name, category, subcategory, price, stock_quantity, description, rating, reviews_count) VALUES
-- Electronics - Laptops
('Dell XPS 15 Laptop', 'Electronics', 'Laptops', 1299.99, 25, '15.6" FHD Display, Intel i7, 16GB RAM, 512GB SSD', 4.7, 234),
('MacBook Pro M3', 'Electronics', 'Laptops', 1999.99, 15, '14" Retina Display, M3 Chip, 16GB RAM, 512GB SSD', 4.9, 567),
('HP Pavilion 14', 'Electronics', 'Laptops', 699.99, 40, '14" HD Display, Intel i5, 8GB RAM, 256GB SSD', 4.3, 189),
('Lenovo ThinkPad X1', 'Electronics', 'Laptops', 1499.99, 18, '14" FHD Display, Intel i7, 16GB RAM, 1TB SSD', 4.6, 312),

-- Electronics - Smartphones
('iPhone 15 Pro', 'Electronics', 'Smartphones', 999.99, 50, '6.1" Display, A17 Pro Chip, 128GB', 4.8, 891),
('Samsung Galaxy S24', 'Electronics', 'Smartphones', 899.99, 45, '6.2" AMOLED Display, Snapdragon 8 Gen 3, 256GB', 4.7, 723),
('Google Pixel 8', 'Electronics', 'Smartphones', 699.99, 35, '6.2" OLED Display, Tensor G3, 128GB', 4.6, 456),

-- Electronics - Accessories
('Sony WH-1000XM5 Headphones', 'Electronics', 'Accessories', 349.99, 60, 'Wireless Noise-Cancelling Headphones', 4.8, 1234),
('Apple AirPods Pro', 'Electronics', 'Accessories', 249.99, 75, 'Wireless Earbuds with Active Noise Cancellation', 4.7, 2341),
('Logitech MX Master 3S', 'Electronics', 'Accessories', 99.99, 100, 'Advanced Wireless Mouse', 4.6, 567),

-- Home & Kitchen
('Ninja Air Fryer', 'Home & Kitchen', 'Appliances', 129.99, 30, '5.5 Quart Capacity, 1750W', 4.5, 3456),
('Instant Pot Duo', 'Home & Kitchen', 'Appliances', 89.99, 40, '7-in-1 Multi-Use Pressure Cooker, 6 Quart', 4.7, 8901),
('Dyson V15 Vacuum', 'Home & Kitchen', 'Appliances', 649.99, 12, 'Cordless Stick Vacuum with Laser Detection', 4.8, 432),

-- Books
('Atomic Habits', 'Books', 'Self-Help', 16.99, 200, 'By James Clear - Transform Your Life', 4.9, 12345),
('The Lean Startup', 'Books', 'Business', 14.99, 150, 'By Eric Ries - Innovation & Entrepreneurship', 4.6, 2345),
('Deep Work', 'Books', 'Productivity', 15.99, 180, 'By Cal Newport - Focus in a Distracted World', 4.7, 3456),

-- Sports & Outdoors
('Yeti Rambler 30oz', 'Sports & Outdoors', 'Drinkware', 39.99, 100, 'Vacuum Insulated Tumbler', 4.8, 5678),
('Nike Air Zoom Pegasus', 'Sports & Outdoors', 'Running Shoes', 129.99, 50, "Men's Road Running Shoes", 4.6, 1234),
('Under Armour Gym Bag', 'Sports & Outdoors', 'Bags', 49.99, 75, 'Undeniable 4.0 Duffle Bag', 4.5, 890);

-- ============================================
-- INSERT ORDERS
-- ============================================
INSERT INTO Orders (user_id, order_number, order_date, total_amount, status, shipping_address, estimated_delivery, tracking_number) VALUES
(1, 'ORD-2026-00001', DATEADD(DAY, -5, GETDATE()), 1349.98, 'Shipped', '123 Main St, New York, NY 10001', DATEADD(DAY, 2, GETDATE()), 'TRK123456789'),
(1, 'ORD-2026-00002', DATEADD(DAY, -15, GETDATE()), 89.99, 'Delivered', '123 Main St, New York, NY 10001', DATEADD(DAY, -8, GETDATE()), 'TRK987654321'),
(2, 'ORD-2026-00003', DATEADD(DAY, -3, GETDATE()), 999.99, 'Processing', '456 Oak Ave, Los Angeles, CA 90001', DATEADD(DAY, 4, GETDATE()), NULL),
(3, 'ORD-2026-00004', DATEADD(DAY, -1, GETDATE()), 249.99, 'Pending', '789 Pine Rd, Chicago, IL 60601', DATEADD(DAY, 5, GETDATE()), NULL),
(4, 'ORD-2026-00005', DATEADD(DAY, -20, GETDATE()), 649.99, 'Delivered', '321 Elm St, Houston, TX 77001', DATEADD(DAY, -13, GETDATE()), 'TRK456789123'),
(5, 'ORD-2026-00006', GETDATE(), 1999.99, 'Processing', '654 Maple Dr, Phoenix, AZ 85001', DATEADD(DAY, 5, GETDATE()), NULL);

-- ============================================
-- INSERT ORDER ITEMS
-- ============================================
INSERT INTO OrderItems (order_id, product_id, quantity, unit_price, subtotal) VALUES
-- Order 1
(1, 1, 1, 1299.99, 1299.99),
(1, 8, 1, 349.99, 349.99),
-- Order 2
(2, 12, 1, 89.99, 89.99),
-- Order 3
(3, 5, 1, 999.99, 999.99),
-- Order 4
(4, 9, 1, 249.99, 249.99),
-- Order 5
(5, 13, 1, 649.99, 649.99),
-- Order 6
(6, 2, 1, 1999.99, 1999.99);

-- ============================================
-- INSERT INTENTS
-- ============================================
INSERT INTO Intents (intent_name, category, description, response_template) VALUES
('track_order', 'Order Management', 'User wants to track their order status', 'Let me check the status of your order. Could you please provide your order number?'),
('product_search', 'Product Discovery', 'User is looking for a specific product', 'I''d be happy to help you find the perfect product! What are you looking for?'),
('product_recommendation', 'Product Discovery', 'User wants product recommendations', 'I can recommend some great products for you! What category are you interested in?'),
('return_policy', 'Customer Service', 'User asks about return policy', 'Our return policy allows returns within 30 days of delivery. Would you like to start a return?'),
('shipping_info', 'Customer Service', 'User asks about shipping information', 'We offer free standard shipping on orders over $50. Express shipping is available for $15.'),
('payment_methods', 'Customer Service', 'User asks about payment options', 'We accept all major credit cards, PayPal, and Apple Pay.'),
('cancel_order', 'Order Management', 'User wants to cancel an order', 'I can help you cancel your order. Please provide your order number.'),
('greeting', 'Conversation', 'User greets the bot', 'Hello! Welcome to our e-commerce store. How can I assist you today?'),
('goodbye', 'Conversation', 'User ends conversation', 'Thank you for chatting with us! Have a great day!'),
('help', 'Conversation', 'User needs help', 'I can help you with: order tracking, product search, returns, shipping info, and more!');

-- ============================================
-- INSERT FAQ
-- ============================================
INSERT INTO FAQ (question, answer, category, times_asked, helpful_count) VALUES
('What is your return policy?', 'We offer a 30-day money-back guarantee on all products. Items must be in original condition with tags attached. To initiate a return, please contact our customer service or use the "Return Order" option in your account.', 'Returns', 245, 198),
('How long does shipping take?', 'Standard shipping takes 5-7 business days. Express shipping (2-3 days) is available for $15. Free standard shipping on orders over $50.', 'Shipping', 567, 489),
('What payment methods do you accept?', 'We accept Visa, Mastercard, American Express, Discover, PayPal, Apple Pay, and Google Pay.', 'Payment', 123, 110),
('How can I track my order?', 'Once your order ships, you''ll receive a tracking number via email. You can also track your order in the "My Orders" section of your account.', 'Order Tracking', 891, 823),
('Can I change my shipping address?', 'Yes, you can change your shipping address before the order ships. Please contact customer service immediately with your order number and new address.', 'Order Management', 78, 65),
('Do you offer international shipping?', 'Yes, we ship to over 50 countries worldwide. International shipping rates and delivery times vary by destination.', 'Shipping', 156, 134),
('How do I cancel my order?', 'Orders can be cancelled within 1 hour of placement. Go to "My Orders" and click "Cancel Order". After this window, please contact customer service.', 'Order Management', 234, 201),
('What if my product arrives damaged?', 'We''re sorry to hear that! Please take photos of the damage and contact us within 48 hours. We''ll send a replacement or issue a full refund immediately.', 'Returns', 67, 62),
('Do you price match?', 'Yes! We match prices from authorized retailers. Submit a price match request within 7 days of purchase with proof of the lower price.', 'Pricing', 89, 78),
('How can I contact customer service?', 'You can reach us via chat (9 AM - 9 PM EST), email (support@ecommerce.com), or phone (1-800-555-0123) Monday-Friday 8 AM - 8 PM EST.', 'Customer Service', 345, 312);

-- ============================================
-- INSERT SAMPLE CONVERSATIONS
-- ============================================
INSERT INTO Conversations (user_id, session_id, channel, started_at, ended_at, total_messages, resolved, escalated_to_human, satisfaction_score) VALUES
(1, 'session_001', 'WebChat', DATEADD(HOUR, -2, GETDATE()), DATEADD(HOUR, -1, GETDATE()), 8, 1, 0, 5),
(2, 'session_002', 'WebChat', DATEADD(HOUR, -5, GETDATE()), DATEADD(HOUR, -4, GETDATE()), 12, 1, 0, 4),
(3, 'session_003', 'WebChat', DATEADD(HOUR, -10, GETDATE()), DATEADD(HOUR, -9, GETDATE()), 6, 1, 0, 5),
(1, 'session_004', 'WebChat', DATEADD(DAY, -1, GETDATE()), DATEADD(DAY, -1, GETDATE()), 15, 0, 1, 3),
(4, 'session_005', 'WebChat', DATEADD(DAY, -2, GETDATE()), DATEADD(DAY, -2, GETDATE()), 10, 1, 0, 4);

-- ============================================
-- INSERT SAMPLE MESSAGES
-- ============================================
INSERT INTO Messages (conversation_id, sender_type, message_text, intent, confidence_score, sentiment, sentiment_score) VALUES
-- Conversation 1
(1, 'User', 'Hi, I need to track my order', 'track_order', 0.95, 'Neutral', 0.50),
(1, 'Bot', 'I''d be happy to help you track your order! Could you please provide your order number?', NULL, NULL, NULL, NULL),
(1, 'User', 'ORD-2026-00001', 'track_order', 0.98, 'Neutral', 0.52),
(1, 'Bot', 'Your order ORD-2026-00001 is currently shipped and in transit. Expected delivery: in 2 days. Tracking: TRK123456789', NULL, NULL, NULL, NULL),
(1, 'User', 'Great, thank you!', 'goodbye', 0.92, 'Positive', 0.85),
(1, 'Bot', 'You''re welcome! Have a great day!', NULL, NULL, NULL, NULL),

-- Conversation 2
(2, 'User', 'Hello', 'greeting', 0.99, 'Positive', 0.75),
(2, 'Bot', 'Hello! Welcome to our store. How can I assist you today?', NULL, NULL, NULL, NULL),
(2, 'User', 'I''m looking for a laptop for programming', 'product_search', 0.88, 'Neutral', 0.55),
(2, 'Bot', 'I have some great laptops for programming! Based on your needs, I recommend: 1. Dell XPS 15 - $1,299.99 (excellent performance), 2. MacBook Pro M3 - $1,999.99 (top-tier), 3. Lenovo ThinkPad X1 - $1,499.99 (business-grade)', NULL, NULL, NULL, NULL),
(2, 'User', 'Tell me more about the Dell XPS 15', 'product_search', 0.91, 'Neutral', 0.58),
(2, 'Bot', 'The Dell XPS 15 features a 15.6" FHD display, Intel i7 processor, 16GB RAM, and 512GB SSD. It has a 4.7 rating with 234 reviews. Perfect for programming with excellent battery life!', NULL, NULL, NULL, NULL),
(2, 'User', 'Sounds perfect, thanks!', 'goodbye', 0.94, 'Positive', 0.88),

-- Conversation 3
(3, 'User', 'What''s your return policy?', 'return_policy', 0.96, 'Neutral', 0.50),
(3, 'Bot', 'We offer a 30-day money-back guarantee on all products. Items must be in original condition. Would you like to start a return?', NULL, NULL, NULL, NULL),
(3, 'User', 'No, just wanted to know. Thank you!', 'goodbye', 0.89, 'Positive', 0.72),
(3, 'Bot', 'You''re welcome! Feel free to reach out if you need anything else!', NULL, NULL, NULL, NULL);

-- ============================================
-- INSERT SAMPLE PRODUCT RECOMMENDATIONS
-- ============================================
INSERT INTO ProductRecommendations (conversation_id, product_id, recommendation_type, score, was_clicked, was_purchased) VALUES
(2, 1, 'Collaborative', 0.92, 1, 0),
(2, 4, 'Content-based', 0.87, 1, 0),
(2, 10, 'Hybrid', 0.78, 0, 0);

-- ============================================
-- UPDATE ANALYTICS (Run daily analytics for last 7 days)
-- ============================================
DECLARE @i INT = 0;
WHILE @i < 7
BEGIN
    EXEC sp_UpdateDailyAnalytics @target_date = CAST(DATEADD(DAY, -@i, GETDATE()) AS DATE);
    SET @i = @i + 1;
END;

-- ============================================
-- VERIFICATION QUERIES
-- ============================================
SELECT 'Total Users' AS Metric, COUNT(*) AS Count FROM Users
UNION ALL
SELECT 'Total Products', COUNT(*) FROM Products
UNION ALL
SELECT 'Total Orders', COUNT(*) FROM Orders
UNION ALL
SELECT 'Total Conversations', COUNT(*) FROM Conversations
UNION ALL
SELECT 'Total Messages', COUNT(*) FROM Messages
UNION ALL
SELECT 'Total FAQs', COUNT(*) FROM FAQ;
