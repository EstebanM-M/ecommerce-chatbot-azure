"""
Sentiment Analysis Module
Analyzes user message sentiment using VADER
"""

from typing import Dict, Any
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from loguru import logger

from bot.config import config

# Optional: Import transformers only if available
try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logger.warning("transformers not installed - using VADER only (this is fine!)")


class SentimentAnalyzer:
    """Sentiment Analysis using pretrained models"""
    
    def __init__(self):
        """Initialize sentiment analyzer"""
        self.use_pretrained = config.USE_PRETRAINED_MODELS
        
        if self.use_pretrained:
            try:
                # Use lightweight VADER for fast sentiment analysis
                self.vader_analyzer = SentimentIntensityAnalyzer()
                logger.info("✅ VADER Sentiment Analyzer initialized")
                
                # Optionally use transformer model for better accuracy
                # Uncomment below to use DistilBERT (requires more resources)
                # self.transformer_analyzer = pipeline(
                #     "sentiment-analysis",
                #     model="distilbert-base-uncased-finetuned-sst-2-english"
                # )
                
            except Exception as e:
                logger.error(f"Error initializing sentiment analyzer: {e}")
                self.vader_analyzer = None
        else:
            logger.info("Using basic sentiment analysis (pretrained models disabled)")
            self.vader_analyzer = None
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of text
        
        Args:
            text: Input text to analyze
            
        Returns:
            dict: Sentiment analysis results
                - sentiment: 'Positive', 'Negative', or 'Neutral'
                - score: Confidence score (0-1)
                - compound: Compound sentiment score (-1 to 1)
        """
        if not text or not text.strip():
            return {
                "sentiment": "Neutral",
                "score": 0.5,
                "compound": 0.0
            }
        
        try:
            if self.vader_analyzer:
                # Use VADER sentiment analysis
                scores = self.vader_analyzer.polarity_scores(text)
                compound = scores['compound']
                
                # Classify sentiment based on compound score
                if compound >= 0.05:
                    sentiment = "Positive"
                    score = (compound + 1) / 2  # Normalize to 0-1
                elif compound <= -0.05:
                    sentiment = "Negative"
                    score = abs(compound)  # Use absolute value for negative
                else:
                    sentiment = "Neutral"
                    score = 0.5
                
                return {
                    "sentiment": sentiment,
                    "score": round(score, 4),
                    "compound": round(compound, 4),
                    "positive": round(scores['pos'], 4),
                    "negative": round(scores['neg'], 4),
                    "neutral": round(scores['neu'], 4)
                }
            else:
                # Fallback: Basic keyword-based sentiment
                return self._basic_sentiment_analysis(text)
                
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return {
                "sentiment": "Neutral",
                "score": 0.5,
                "compound": 0.0
            }
    
    def _basic_sentiment_analysis(self, text: str) -> Dict[str, Any]:
        """
        Basic keyword-based sentiment analysis fallback
        
        Args:
            text: Input text
            
        Returns:
            dict: Basic sentiment results
        """
        text_lower = text.lower()
        
        # Positive keywords
        positive_keywords = [
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
            'love', 'perfect', 'awesome', 'best', 'happy', 'thanks', 'thank you'
        ]
        
        # Negative keywords
        negative_keywords = [
            'bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 'angry',
            'disappointed', 'frustrating', 'problem', 'issue', 'broken', 'poor'
        ]
        
        positive_count = sum(1 for word in positive_keywords if word in text_lower)
        negative_count = sum(1 for word in negative_keywords if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = "Positive"
            score = min(0.7 + (positive_count * 0.1), 0.95)
        elif negative_count > positive_count:
            sentiment = "Negative"
            score = min(0.6 + (negative_count * 0.1), 0.9)
        else:
            sentiment = "Neutral"
            score = 0.5
        
        return {
            "sentiment": sentiment,
            "score": round(score, 4),
            "compound": 0.0,
            "method": "basic_keywords"
        }
    
    def get_sentiment_emoji(self, sentiment: str) -> str:
        """
        Get emoji representation of sentiment
        
        Args:
            sentiment: Sentiment label
            
        Returns:
            str: Emoji
        """
        emoji_map = {
            "Positive": "😊",
            "Negative": "😞",
            "Neutral": "😐"
        }
        return emoji_map.get(sentiment, "😐")
    
    def analyze_batch(self, texts: list[str]) -> list[Dict[str, Any]]:
        """
        Analyze sentiment for multiple texts
        
        Args:
            texts: List of text strings
            
        Returns:
            list: List of sentiment analysis results
        """
        return [self.analyze(text) for text in texts]


# Example usage for testing
if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    
    test_messages = [
        "I love this product! It's amazing!",
        "This is terrible. I'm very disappointed.",
        "Can you track my order?",
        "The quality is outstanding, highly recommend!",
        "Worst purchase ever. Not happy at all."
    ]
    
    print("=" * 60)
    print("SENTIMENT ANALYSIS TEST")
    print("=" * 60)
    
    for message in test_messages:
        result = analyzer.analyze(message)
        emoji = analyzer.get_sentiment_emoji(result["sentiment"])
        print(f"\nMessage: {message}")
        print(f"Sentiment: {result['sentiment']} {emoji}")
        print(f"Score: {result['score']:.4f}")
        if 'compound' in result:
            print(f"Compound: {result['compound']:.4f}")
    
    print("\n" + "=" * 60)