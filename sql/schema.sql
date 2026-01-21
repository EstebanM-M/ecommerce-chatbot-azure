-- E-commerce Chatbot Database Schema
-- Azure SQL Database

-- ============================================
-- 1. USERS TABLE
-- ============================================
CREATE TABLE Users (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(100) NOT NULL UNIQUE,
    email NVARCHAR(255) NOT NULL UNIQUE,
    full_name NVARCHAR(200),
    phone NVARCHAR(20),
    created_at DATETIME2 DEFAULT GETDATE(),
    last_login DATETIME2,
    is_active BIT DEFAULT 1,
    INDEX idx_email (email),
    INDEX idx_username (username)
);

-- ============================================
-- 2. PRODUCTS TABLE
-- ============================================
CREATE TABLE Products (
    product_id INT IDENTITY(1,1) PRIMARY KEY,
    product_name NVARCHAR(255) NOT NULL,
    category NVARCHAR(100),
    subcategory NVARCHAR(100),
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INT DEFAULT 0,
    description NVARCHAR(MAX),
    rating DECIMAL(3,2),
    reviews_count INT DEFAULT 0,
    created_at DATETIME2 DEFAULT GETDATE(),
    updated_at DATETIME2 DEFAULT GETDATE(),
    is_active BIT DEFAULT 1,
    INDEX idx_category (category),
    INDEX idx_price (price)
);

-- ============================================
-- 3. ORDERS TABLE
-- ============================================
CREATE TABLE Orders (
    order_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    order_number NVARCHAR(50) NOT NULL UNIQUE,
    order_date DATETIME2 DEFAULT GETDATE(),
    total_amount DECIMAL(10,2) NOT NULL,
    status NVARCHAR(50) NOT NULL, -- Pending, Processing, Shipped, Delivered, Cancelled
    shipping_address NVARCHAR(MAX),
    estimated_delivery DATE,
    actual_delivery DATE,
    tracking_number NVARCHAR(100),
    created_at DATETIME2 DEFAULT GETDATE(),
    updated_at DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    INDEX idx_order_number (order_number),
    INDEX idx_status (status),
    INDEX idx_user_id (user_id)
);

-- ============================================
-- 4. ORDER ITEMS TABLE
-- ============================================
CREATE TABLE OrderItems (
    order_item_id INT IDENTITY(1,1) PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    INDEX idx_order_id (order_id)
);

-- ============================================
-- 5. CONVERSATIONS TABLE
-- ============================================
CREATE TABLE Conversations (
    conversation_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT,
    session_id NVARCHAR(255) NOT NULL,
    channel NVARCHAR(50), -- WebChat, Teams, etc.
    started_at DATETIME2 DEFAULT GETDATE(),
    ended_at DATETIME2,
    total_messages INT DEFAULT 0,
    resolved BIT DEFAULT 0,
    escalated_to_human BIT DEFAULT 0,
    satisfaction_score INT, -- 1-5
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    INDEX idx_session_id (session_id),
    INDEX idx_started_at (started_at)
);

-- ============================================
-- 6. MESSAGES TABLE
-- ============================================
CREATE TABLE Messages (
    message_id INT IDENTITY(1,1) PRIMARY KEY,
    conversation_id INT NOT NULL,
    sender_type NVARCHAR(20) NOT NULL, -- User or Bot
    message_text NVARCHAR(MAX) NOT NULL,
    intent NVARCHAR(100),
    confidence_score DECIMAL(5,4),
    sentiment NVARCHAR(20), -- Positive, Neutral, Negative
    sentiment_score DECIMAL(5,4),
    timestamp DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (conversation_id) REFERENCES Conversations(conversation_id),
    INDEX idx_conversation_id (conversation_id),
    INDEX idx_timestamp (timestamp),
    INDEX idx_intent (intent)
);

-- ============================================
-- 7. INTENTS TABLE (For FAQ and intent tracking)
-- ============================================
CREATE TABLE Intents (
    intent_id INT IDENTITY(1,1) PRIMARY KEY,
    intent_name NVARCHAR(100) NOT NULL UNIQUE,
    category NVARCHAR(100),
    description NVARCHAR(MAX),
    response_template NVARCHAR(MAX),
    is_active BIT DEFAULT 1,
    created_at DATETIME2 DEFAULT GETDATE()
);

-- ============================================
-- 8. PRODUCT RECOMMENDATIONS TABLE
-- ============================================
CREATE TABLE ProductRecommendations (
    recommendation_id INT IDENTITY(1,1) PRIMARY KEY,
    conversation_id INT NOT NULL,
    product_id INT NOT NULL,
    recommendation_type NVARCHAR(50), -- Collaborative, Content-based, Hybrid
    score DECIMAL(5,4),
    was_clicked BIT DEFAULT 0,
    was_purchased BIT DEFAULT 0,
    created_at DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (conversation_id) REFERENCES Conversations(conversation_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    INDEX idx_conversation_id (conversation_id)
);

-- ============================================
-- 9. FAQ TABLE
-- ============================================
CREATE TABLE FAQ (
    faq_id INT IDENTITY(1,1) PRIMARY KEY,
    question NVARCHAR(500) NOT NULL,
    answer NVARCHAR(MAX) NOT NULL,
    category NVARCHAR(100),
    times_asked INT DEFAULT 0,
    helpful_count INT DEFAULT 0,
    not_helpful_count INT DEFAULT 0,
    is_active BIT DEFAULT 1,
    created_at DATETIME2 DEFAULT GETDATE(),
    updated_at DATETIME2 DEFAULT GETDATE(),
    INDEX idx_category (category)
);

-- ============================================
-- 10. CHATBOT ANALYTICS TABLE
-- ============================================
CREATE TABLE ChatbotAnalytics (
    analytics_id INT IDENTITY(1,1) PRIMARY KEY,
    date DATE NOT NULL,
    total_conversations INT DEFAULT 0,
    total_messages INT DEFAULT 0,
    unique_users INT DEFAULT 0,
    avg_conversation_duration DECIMAL(10,2), -- in seconds
    resolution_rate DECIMAL(5,2), -- percentage
    escalation_rate DECIMAL(5,2), -- percentage
    avg_satisfaction_score DECIMAL(3,2),
    positive_sentiment_rate DECIMAL(5,2),
    negative_sentiment_rate DECIMAL(5,2),
    neutral_sentiment_rate DECIMAL(5,2),
    created_at DATETIME2 DEFAULT GETDATE(),
    INDEX idx_date (date)
);

-- ============================================
-- VIEWS FOR ANALYTICS
-- ============================================

-- View: Daily Conversation Metrics
CREATE VIEW vw_DailyConversationMetrics AS
SELECT 
    CAST(started_at AS DATE) AS conversation_date,
    COUNT(*) AS total_conversations,
    COUNT(DISTINCT user_id) AS unique_users,
    SUM(total_messages) AS total_messages,
    AVG(total_messages) AS avg_messages_per_conversation,
    SUM(CASE WHEN resolved = 1 THEN 1 ELSE 0 END) AS resolved_conversations,
    SUM(CASE WHEN escalated_to_human = 1 THEN 1 ELSE 0 END) AS escalated_conversations,
    AVG(CAST(satisfaction_score AS DECIMAL(3,2))) AS avg_satisfaction
FROM Conversations
WHERE started_at IS NOT NULL
GROUP BY CAST(started_at AS DATE);

-- View: Sentiment Analysis Summary
CREATE VIEW vw_SentimentAnalysis AS
SELECT 
    CAST(m.timestamp AS DATE) AS message_date,
    m.sentiment,
    COUNT(*) AS message_count,
    AVG(m.sentiment_score) AS avg_sentiment_score
FROM Messages m
WHERE m.sender_type = 'User' AND m.sentiment IS NOT NULL
GROUP BY CAST(m.timestamp AS DATE), m.sentiment;

-- View: Top Intents
CREATE VIEW vw_TopIntents AS
SELECT 
    intent,
    COUNT(*) AS intent_count,
    AVG(confidence_score) AS avg_confidence
FROM Messages
WHERE intent IS NOT NULL
GROUP BY intent;

-- View: Product Recommendation Performance
CREATE VIEW vw_RecommendationPerformance AS
SELECT 
    p.product_name,
    p.category,
    COUNT(pr.recommendation_id) AS times_recommended,
    SUM(CASE WHEN pr.was_clicked = 1 THEN 1 ELSE 0 END) AS click_count,
    SUM(CASE WHEN pr.was_purchased = 1 THEN 1 ELSE 0 END) AS purchase_count,
    CAST(SUM(CASE WHEN pr.was_clicked = 1 THEN 1 ELSE 0 END) AS FLOAT) / 
        NULLIF(COUNT(pr.recommendation_id), 0) * 100 AS click_through_rate,
    CAST(SUM(CASE WHEN pr.was_purchased = 1 THEN 1 ELSE 0 END) AS FLOAT) / 
        NULLIF(COUNT(pr.recommendation_id), 0) * 100 AS conversion_rate
FROM ProductRecommendations pr
JOIN Products p ON pr.product_id = p.product_id
GROUP BY p.product_name, p.category;

-- ============================================
-- STORED PROCEDURES
-- ============================================

-- Procedure: Get Order Status
CREATE PROCEDURE sp_GetOrderStatus
    @order_number NVARCHAR(50)
AS
BEGIN
    SELECT 
        o.order_number,
        o.status,
        o.order_date,
        o.total_amount,
        o.tracking_number,
        o.estimated_delivery,
        o.shipping_address,
        u.email,
        u.full_name
    FROM Orders o
    JOIN Users u ON o.user_id = u.user_id
    WHERE o.order_number = @order_number;
END;

-- Procedure: Log Conversation Message
CREATE PROCEDURE sp_LogMessage
    @conversation_id INT,
    @sender_type NVARCHAR(20),
    @message_text NVARCHAR(MAX),
    @intent NVARCHAR(100) = NULL,
    @confidence_score DECIMAL(5,4) = NULL,
    @sentiment NVARCHAR(20) = NULL,
    @sentiment_score DECIMAL(5,4) = NULL
AS
BEGIN
    INSERT INTO Messages (conversation_id, sender_type, message_text, intent, confidence_score, sentiment, sentiment_score)
    VALUES (@conversation_id, @sender_type, @message_text, @intent, @confidence_score, @sentiment, @sentiment_score);
    
    -- Update conversation message count
    UPDATE Conversations
    SET total_messages = total_messages + 1
    WHERE conversation_id = @conversation_id;
END;

-- Procedure: Get Product Recommendations
CREATE PROCEDURE sp_GetProductRecommendations
    @user_id INT,
    @category NVARCHAR(100) = NULL,
    @top_n INT = 5
AS
BEGIN
    SELECT TOP (@top_n)
        p.product_id,
        p.product_name,
        p.category,
        p.price,
        p.rating,
        p.description
    FROM Products p
    WHERE p.is_active = 1
        AND (@category IS NULL OR p.category = @category)
        AND p.stock_quantity > 0
    ORDER BY p.rating DESC, p.reviews_count DESC;
END;

-- Procedure: Update Analytics Daily
CREATE PROCEDURE sp_UpdateDailyAnalytics
    @target_date DATE
AS
BEGIN
    MERGE INTO ChatbotAnalytics AS target
    USING (
        SELECT 
            @target_date AS date,
            COUNT(DISTINCT c.conversation_id) AS total_conversations,
            SUM(c.total_messages) AS total_messages,
            COUNT(DISTINCT c.user_id) AS unique_users,
            AVG(DATEDIFF(SECOND, c.started_at, c.ended_at)) AS avg_conversation_duration,
            CAST(SUM(CASE WHEN c.resolved = 1 THEN 1 ELSE 0 END) AS FLOAT) / 
                NULLIF(COUNT(*), 0) * 100 AS resolution_rate,
            CAST(SUM(CASE WHEN c.escalated_to_human = 1 THEN 1 ELSE 0 END) AS FLOAT) / 
                NULLIF(COUNT(*), 0) * 100 AS escalation_rate,
            AVG(CAST(c.satisfaction_score AS DECIMAL(3,2))) AS avg_satisfaction_score,
            (SELECT CAST(COUNT(*) AS FLOAT) / NULLIF((SELECT COUNT(*) FROM Messages WHERE CAST(timestamp AS DATE) = @target_date AND sender_type = 'User'), 0) * 100
             FROM Messages WHERE CAST(timestamp AS DATE) = @target_date AND sender_type = 'User' AND sentiment = 'Positive') AS positive_sentiment_rate,
            (SELECT CAST(COUNT(*) AS FLOAT) / NULLIF((SELECT COUNT(*) FROM Messages WHERE CAST(timestamp AS DATE) = @target_date AND sender_type = 'User'), 0) * 100
             FROM Messages WHERE CAST(timestamp AS DATE) = @target_date AND sender_type = 'User' AND sentiment = 'Negative') AS negative_sentiment_rate,
            (SELECT CAST(COUNT(*) AS FLOAT) / NULLIF((SELECT COUNT(*) FROM Messages WHERE CAST(timestamp AS DATE) = @target_date AND sender_type = 'User'), 0) * 100
             FROM Messages WHERE CAST(timestamp AS DATE) = @target_date AND sender_type = 'User' AND sentiment = 'Neutral') AS neutral_sentiment_rate
        FROM Conversations c
        WHERE CAST(c.started_at AS DATE) = @target_date
    ) AS source
    ON target.date = source.date
    WHEN MATCHED THEN
        UPDATE SET 
            total_conversations = source.total_conversations,
            total_messages = source.total_messages,
            unique_users = source.unique_users,
            avg_conversation_duration = source.avg_conversation_duration,
            resolution_rate = source.resolution_rate,
            escalation_rate = source.escalation_rate,
            avg_satisfaction_score = source.avg_satisfaction_score,
            positive_sentiment_rate = source.positive_sentiment_rate,
            negative_sentiment_rate = source.negative_sentiment_rate,
            neutral_sentiment_rate = source.neutral_sentiment_rate
    WHEN NOT MATCHED THEN
        INSERT (date, total_conversations, total_messages, unique_users, avg_conversation_duration, 
                resolution_rate, escalation_rate, avg_satisfaction_score,
                positive_sentiment_rate, negative_sentiment_rate, neutral_sentiment_rate)
        VALUES (source.date, source.total_conversations, source.total_messages, source.unique_users,
                source.avg_conversation_duration, source.resolution_rate, source.escalation_rate,
                source.avg_satisfaction_score, source.positive_sentiment_rate, 
                source.negative_sentiment_rate, source.neutral_sentiment_rate);
END;

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================

-- Additional composite indexes for common queries
CREATE INDEX idx_messages_conversation_timestamp ON Messages(conversation_id, timestamp);
CREATE INDEX idx_conversations_user_started ON Conversations(user_id, started_at);
CREATE INDEX idx_orders_user_status ON Orders(user_id, status);
CREATE INDEX idx_products_category_price ON Products(category, price);
