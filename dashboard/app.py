"""
E-commerce Chatbot Analytics Dashboard
Streamlit application for visualizing chatbot performance and insights
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pyodbc
from typing import Dict, Any, List
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bot.config import config


# Page configuration
st.set_page_config(
    page_title="E-commerce Chatbot Analytics",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


class DashboardDatabase:
    """Database connection handler for dashboard"""
    
    def __init__(self):
        """Initialize database connection"""
        try:
            self.conn = pyodbc.connect(config.get_sql_connection_string())
        except Exception as e:
            st.error(f"❌ Database connection failed: {e}")
            st.stop()
    
    def query(self, sql: str, params: tuple = ()) -> pd.DataFrame:
        """
        Execute SQL query and return DataFrame
        
        Args:
            sql: SQL query string
            params: Query parameters
            
        Returns:
            DataFrame: Query results
        """
        try:
            return pd.read_sql(sql, self.conn, params=params)
        except Exception as e:
            st.error(f"Query error: {e}")
            return pd.DataFrame()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


@st.cache_resource
def get_db():
    """Get cached database connection"""
    return DashboardDatabase()


def load_overview_metrics(db: DashboardDatabase, days: int = 7) -> Dict[str, Any]:
    """
    Load overview metrics
    
    Args:
        db: Database connection
        days: Number of days to analyze
        
    Returns:
        dict: Metrics dictionary
    """
    cutoff_date = datetime.now() - timedelta(days=days)
    
    # Total conversations
    total_conv_query = """
        SELECT COUNT(*) as total
        FROM Conversations
        WHERE started_at >= ?
    """
    total_conv = db.query(total_conv_query, (cutoff_date,))
    
    # Resolution rate
    resolution_query = """
        SELECT 
            CAST(SUM(CASE WHEN resolved = 1 THEN 1.0 ELSE 0 END) / NULLIF(COUNT(*), 0) * 100 AS DECIMAL(5,2)) as resolution_rate
        FROM Conversations
        WHERE started_at >= ?
    """
    resolution_rate = db.query(resolution_query, (cutoff_date,))
    
    # Average satisfaction
    satisfaction_query = """
        SELECT 
            AVG(CAST(satisfaction_score AS FLOAT)) as avg_satisfaction
        FROM Conversations
        WHERE started_at >= ? AND satisfaction_score IS NOT NULL
    """
    avg_satisfaction = db.query(satisfaction_query, (cutoff_date,))
    
    # Total messages
    messages_query = """
        SELECT COUNT(*) as total
        FROM Messages m
        JOIN Conversations c ON m.conversation_id = c.conversation_id
        WHERE c.started_at >= ?
    """
    total_messages = db.query(messages_query, (cutoff_date,))
    
    return {
        "total_conversations": int(total_conv.iloc[0]['total']) if not total_conv.empty else 0,
        "resolution_rate": float(resolution_rate.iloc[0]['resolution_rate']) if not resolution_rate.empty and resolution_rate.iloc[0]['resolution_rate'] is not None else 0,
        "avg_satisfaction": float(avg_satisfaction.iloc[0]['avg_satisfaction']) if not avg_satisfaction.empty and avg_satisfaction.iloc[0]['avg_satisfaction'] is not None else 0,
        "total_messages": int(total_messages.iloc[0]['total']) if not total_messages.empty else 0
    }


def load_conversation_trends(db: DashboardDatabase, days: int = 30) -> pd.DataFrame:
    """Load conversation trends over time"""
    cutoff_date = datetime.now() - timedelta(days=days)
    
    query = """
        SELECT 
            CAST(started_at AS DATE) as date,
            COUNT(*) as conversations,
            SUM(total_messages) as messages,
            AVG(CAST(satisfaction_score AS FLOAT)) as avg_satisfaction
        FROM Conversations
        WHERE started_at >= ?
        GROUP BY CAST(started_at AS DATE)
        ORDER BY CAST(started_at AS DATE)
    """
    
    return db.query(query, (cutoff_date,))


def load_sentiment_distribution(db: DashboardDatabase, days: int = 7) -> pd.DataFrame:
    """Load sentiment distribution"""
    cutoff_date = datetime.now() - timedelta(days=days)
    
    query = """
        SELECT 
            m.sentiment,
            COUNT(*) as count,
            AVG(m.sentiment_score) as avg_score
        FROM Messages m
        JOIN Conversations c ON m.conversation_id = c.conversation_id
        WHERE c.started_at >= ?
        AND m.sender_type = 'User'
        AND m.sentiment IS NOT NULL
        GROUP BY m.sentiment
    """
    
    return db.query(query, (cutoff_date,))


def load_top_intents(db: DashboardDatabase, days: int = 7, limit: int = 10) -> pd.DataFrame:
    """Load top intents"""
    cutoff_date = datetime.now() - timedelta(days=days)
    
    query = f"""
        SELECT TOP ({limit})
            m.intent,
            COUNT(*) as count,
            AVG(m.confidence_score) as avg_confidence
        FROM Messages m
        JOIN Conversations c ON m.conversation_id = c.conversation_id
        WHERE c.started_at >= ?
        AND m.intent IS NOT NULL
        GROUP BY m.intent
        ORDER BY COUNT(*) DESC
    """
    
    return db.query(query, (cutoff_date,))


def load_recommendation_performance(db: DashboardDatabase) -> pd.DataFrame:
    """Load product recommendation performance"""
    query = """
        SELECT * FROM vw_RecommendationPerformance
        ORDER BY times_recommended DESC
    """
    
    return db.query(query)


def main():
    """Main dashboard application"""
    
    # Title
    st.title("🤖 E-commerce Chatbot Analytics Dashboard")
    st.markdown("---")
    
    # Sidebar
    st.sidebar.title("⚙️ Settings")
    
    # Date range selector
    date_range = st.sidebar.selectbox(
        "Select Time Period",
        ["Last 7 Days", "Last 30 Days", "Last 90 Days", "All Time"],
        index=0
    )
    
    days_map = {
        "Last 7 Days": 7,
        "Last 30 Days": 30,
        "Last 90 Days": 90,
        "All Time": 365 * 10  # Large number for all data
    }
    
    selected_days = days_map[date_range]
    
    # Refresh button
    if st.sidebar.button("🔄 Refresh Data"):
        st.cache_resource.clear()
        st.rerun()
    
    # Database connection
    db = get_db()
    
    # Load overview metrics
    with st.spinner("Loading metrics..."):
        metrics = load_overview_metrics(db, selected_days)
    
    # Display key metrics
    st.header("📊 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Conversations",
            f"{metrics['total_conversations']:,}",
            delta=None
        )
    
    with col2:
        st.metric(
            "Resolution Rate",
            f"{metrics['resolution_rate']:.1f}%",
            delta=None
        )
    
    with col3:
        st.metric(
            "Avg Satisfaction",
            f"{metrics['avg_satisfaction']:.2f}/5.0",
            delta=None
        )
    
    with col4:
        st.metric(
            "Total Messages",
            f"{metrics['total_messages']:,}",
            delta=None
        )
    
    st.markdown("---")
    
    # Conversation trends
    st.header("📈 Conversation Trends")
    
    trends_df = load_conversation_trends(db, selected_days)
    
    if not trends_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            fig_conv = px.line(
                trends_df,
                x='date',
                y='conversations',
                title='Daily Conversations',
                markers=True
            )
            fig_conv.update_layout(
                xaxis_title="Date",
                yaxis_title="Number of Conversations",
                hovermode='x unified'
            )
            st.plotly_chart(fig_conv, use_container_width=True)
        
        with col2:
            fig_msg = px.line(
                trends_df,
                x='date',
                y='messages',
                title='Daily Messages',
                markers=True,
                color_discrete_sequence=['#FF6B6B']
            )
            fig_msg.update_layout(
                xaxis_title="Date",
                yaxis_title="Number of Messages",
                hovermode='x unified'
            )
            st.plotly_chart(fig_msg, use_container_width=True)
    else:
        st.info("No conversation data available for the selected period.")
    
    st.markdown("---")
    
    # Sentiment analysis
    st.header("😊 Sentiment Analysis")
    
    sentiment_df = load_sentiment_distribution(db, selected_days)
    
    if not sentiment_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            # Sentiment pie chart
            colors = {
                'Positive': '#4CAF50',
                'Neutral': '#FFC107',
                'Negative': '#F44336'
            }
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=sentiment_df['sentiment'],
                values=sentiment_df['count'],
                marker=dict(colors=[colors.get(s, '#888888') for s in sentiment_df['sentiment']])
            )])
            fig_pie.update_layout(title='Sentiment Distribution')
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Sentiment bar chart
            fig_bar = px.bar(
                sentiment_df,
                x='sentiment',
                y='count',
                color='sentiment',
                title='Messages by Sentiment',
                color_discrete_map=colors
            )
            fig_bar.update_layout(
                xaxis_title="Sentiment",
                yaxis_title="Number of Messages",
                showlegend=False
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Sentiment table
        st.subheader("Sentiment Details")
        st.dataframe(
            sentiment_df.style.format({
                'count': '{:,}',
                'avg_score': '{:.4f}'
            }),
            use_container_width=True
        )
    else:
        st.info("No sentiment data available for the selected period.")
    
    st.markdown("---")
    
    # Top intents
    st.header("🎯 Top User Intents")
    
    intents_df = load_top_intents(db, selected_days, 10)
    
    if not intents_df.empty:
        fig_intents = px.bar(
            intents_df,
            x='count',
            y='intent',
            orientation='h',
            title='Most Frequent User Intents',
            text='count'
        )
        fig_intents.update_layout(
            xaxis_title="Number of Occurrences",
            yaxis_title="Intent",
            yaxis={'categoryorder': 'total ascending'}
        )
        fig_intents.update_traces(textposition='outside')
        st.plotly_chart(fig_intents, use_container_width=True)
        
        # Intent details table
        st.subheader("Intent Details")
        st.dataframe(
            intents_df.style.format({
                'count': '{:,}',
                'avg_confidence': '{:.4f}'
            }),
            use_container_width=True
        )
    else:
        st.info("No intent data available for the selected period.")
    
    st.markdown("---")
    
    # Product recommendations
    st.header("💡 Product Recommendation Performance")
    
    recommendations_df = load_recommendation_performance(db)
    
    if not recommendations_df.empty:
        # Top recommended products
        top_recommended = recommendations_df.head(10)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_rec = px.bar(
                top_recommended,
                x='times_recommended',
                y='product_name',
                orientation='h',
                title='Top Recommended Products',
                text='times_recommended'
            )
            fig_rec.update_layout(
                xaxis_title="Times Recommended",
                yaxis_title="Product",
                yaxis={'categoryorder': 'total ascending'}
            )
            fig_rec.update_traces(textposition='outside')
            st.plotly_chart(fig_rec, use_container_width=True)
        
        with col2:
            fig_ctr = px.scatter(
                recommendations_df,
                x='click_through_rate',
                y='conversion_rate',
                size='times_recommended',
                hover_name='product_name',
                title='Click-Through Rate vs Conversion Rate',
                labels={
                    'click_through_rate': 'Click-Through Rate (%)',
                    'conversion_rate': 'Conversion Rate (%)'
                }
            )
            st.plotly_chart(fig_ctr, use_container_width=True)
        
        # Recommendations table
        st.subheader("All Recommendation Performance")
        st.dataframe(
            recommendations_df.style.format({
                'times_recommended': '{:,}',
                'click_count': '{:,}',
                'purchase_count': '{:,}',
                'click_through_rate': '{:.2f}%',
                'conversion_rate': '{:.2f}%'
            }),
            use_container_width=True
        )
    else:
        st.info("No recommendation data available yet.")
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
    <div style='text-align: center; color: #888; padding: 20px;'>
        <p>E-commerce Chatbot Analytics Dashboard v1.0</p>
        <p>Data refreshed every 5 minutes</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
