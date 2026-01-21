"""
Product Recommendation Module
Provides product recommendations using collaborative filtering
and content-based approaches
"""

from typing import List, Dict, Any, Optional
import random
from loguru import logger

from bot.config import config


class ProductRecommender:
    """Product recommendation engine"""
    
    def __init__(self):
        """Initialize product recommender"""
        self.use_pretrained = config.USE_PRETRAINED_MODELS
        
        # In production, this would load a trained model
        # For demo purposes, we use a rule-based approach
        
        # Category-based product associations
        self.category_associations = {
            "Laptops": ["Accessories", "Books"],
            "Smartphones": ["Accessories"],
            "Accessories": ["Electronics"],
            "Appliances": ["Home & Kitchen"],
            "Books": ["Electronics"],
            "Sports & Outdoors": ["Home & Kitchen"]
        }
        
        # Price range preferences (can be learned from user history)
        self.price_ranges = {
            "budget": (0, 200),
            "mid_range": (200, 800),
            "premium": (800, 5000)
        }
        
        logger.info("✅ Product Recommender initialized")
    
    async def get_recommendations(
        self,
        user_id: str,
        category: Optional[str] = None,
        n_recommendations: int = 3,
        price_range: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get product recommendations for user
        
        Args:
            user_id: User identifier
            category: Product category filter
            n_recommendations: Number of recommendations
            price_range: 'budget', 'mid_range', or 'premium'
            
        Returns:
            list: Recommended products
        """
        # In production, this would:
        # 1. Fetch user purchase history
        # 2. Calculate user-item similarity
        # 3. Apply collaborative filtering
        # 4. Rank products
        
        # For demo purposes, return popular products with some randomization
        return []
    
    def calculate_similarity(
        self,
        product1: Dict[str, Any],
        product2: Dict[str, Any]
    ) -> float:
        """
        Calculate similarity between two products
        
        Args:
            product1: First product
            product2: Second product
            
        Returns:
            float: Similarity score (0-1)
        """
        similarity = 0.0
        
        # Category similarity (most important)
        if product1.get("category") == product2.get("category"):
            similarity += 0.5
        elif product2.get("category") in self.category_associations.get(product1.get("category", ""), []):
            similarity += 0.3
        
        # Price similarity
        price1 = product1.get("price", 0)
        price2 = product2.get("price", 0)
        
        if price1 and price2:
            price_diff = abs(price1 - price2)
            max_price = max(price1, price2)
            if max_price > 0:
                price_similarity = 1 - (price_diff / max_price)
                similarity += price_similarity * 0.3
        
        # Rating similarity
        rating1 = product1.get("rating", 0)
        rating2 = product2.get("rating", 0)
        
        if rating1 and rating2:
            rating_similarity = 1 - abs(rating1 - rating2) / 5.0
            similarity += rating_similarity * 0.2
        
        return min(similarity, 1.0)
    
    def get_complementary_products(
        self, product_category: str, n_products: int = 3
    ) -> List[str]:
        """
        Get complementary product categories
        
        Args:
            product_category: Product category
            n_products: Number of categories to return
            
        Returns:
            list: Complementary categories
        """
        complementary = self.category_associations.get(product_category, [])
        
        if len(complementary) < n_products:
            # Add all categories
            all_categories = list(self.category_associations.keys())
            remaining = [c for c in all_categories if c not in complementary and c != product_category]
            complementary.extend(random.sample(remaining, min(n_products - len(complementary), len(remaining))))
        
        return complementary[:n_products]
    
    def rank_products(
        self,
        products: List[Dict[str, Any]],
        user_preferences: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Rank products based on various factors
        
        Args:
            products: List of products
            user_preferences: User preference dictionary
            
        Returns:
            list: Ranked products
        """
        if not products:
            return []
        
        # Calculate score for each product
        for product in products:
            score = 0.0
            
            # Rating weight (40%)
            rating = product.get("rating", 0)
            score += (rating / 5.0) * 0.4
            
            # Reviews count weight (20%)
            reviews = product.get("reviews_count", 0)
            # Normalize reviews (assuming max 10000 reviews)
            normalized_reviews = min(reviews / 10000, 1.0)
            score += normalized_reviews * 0.2
            
            # Stock availability weight (20%)
            if product.get("stock_quantity", 0) > 0:
                score += 0.2
            
            # Price weight (20%) - prefer mid-range
            price = product.get("price", 0)
            if user_preferences and "preferred_price_range" in user_preferences:
                range_name = user_preferences["preferred_price_range"]
                min_price, max_price = self.price_ranges.get(range_name, (0, 10000))
                
                if min_price <= price <= max_price:
                    score += 0.2
                else:
                    # Partial credit if close to range
                    if price < min_price:
                        diff = min_price - price
                    else:
                        diff = price - max_price
                    
                    penalty = min(diff / max_price, 1.0)
                    score += 0.2 * (1 - penalty)
            else:
                # Default: prefer mid-range prices
                if 100 <= price <= 1000:
                    score += 0.2
                elif 50 <= price <= 1500:
                    score += 0.1
            
            product["recommendation_score"] = score
        
        # Sort by score
        ranked = sorted(products, key=lambda x: x.get("recommendation_score", 0), reverse=True)
        
        return ranked
    
    def explain_recommendation(self, product: Dict[str, Any]) -> str:
        """
        Generate explanation for why product was recommended
        
        Args:
            product: Product dictionary
            
        Returns:
            str: Explanation text
        """
        reasons = []
        
        rating = product.get("rating", 0)
        if rating >= 4.5:
            reasons.append(f"highly rated ({rating:.1f}/5.0)")
        
        reviews = product.get("reviews_count", 0)
        if reviews > 500:
            reasons.append(f"popular with {reviews:,} reviews")
        
        price = product.get("price", 0)
        if price < 100:
            reasons.append("affordable price")
        elif price > 1000:
            reasons.append("premium quality")
        
        if not reasons:
            reasons.append("matches your interests")
        
        explanation = f"Recommended because it's {', '.join(reasons)}"
        return explanation


# Example usage for testing
if __name__ == "__main__":
    recommender = ProductRecommender()
    
    # Test products
    test_products = [
        {
            "product_id": 1,
            "product_name": "Dell XPS 15",
            "category": "Laptops",
            "price": 1299.99,
            "rating": 4.7,
            "reviews_count": 234,
            "stock_quantity": 25
        },
        {
            "product_id": 2,
            "product_name": "MacBook Pro M3",
            "category": "Laptops",
            "price": 1999.99,
            "rating": 4.9,
            "reviews_count": 567,
            "stock_quantity": 15
        },
        {
            "product_id": 3,
            "product_name": "Sony WH-1000XM5",
            "category": "Accessories",
            "price": 349.99,
            "rating": 4.8,
            "reviews_count": 1234,
            "stock_quantity": 60
        }
    ]
    
    print("=" * 60)
    print("PRODUCT RECOMMENDATION TEST")
    print("=" * 60)
    
    # Test ranking
    ranked = recommender.rank_products(test_products)
    
    print("\nRanked Products:")
    for i, product in enumerate(ranked, 1):
        print(f"\n{i}. {product['product_name']}")
        print(f"   Score: {product.get('recommendation_score', 0):.4f}")
        print(f"   {recommender.explain_recommendation(product)}")
    
    # Test similarity
    print("\n" + "=" * 60)
    print("SIMILARITY TEST")
    print("=" * 60)
    similarity = recommender.calculate_similarity(test_products[0], test_products[1])
    print(f"\nSimilarity between {test_products[0]['product_name']} and {test_products[1]['product_name']}: {similarity:.4f}")
    
    similarity = recommender.calculate_similarity(test_products[0], test_products[2])
    print(f"Similarity between {test_products[0]['product_name']} and {test_products[2]['product_name']}: {similarity:.4f}")
    
    print("\n" + "=" * 60)
