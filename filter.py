"""Filtering logic for gift listings."""
from typing import List
from marketplace_apis import GiftListing


class GiftFilter:
    """Filters gift listings based on criteria."""
    
    def __init__(self, models: List[str], max_price: float):
        """
        Initialize filter.
        
        Args:
            models: List of gift model names to include
            max_price: Maximum price in TON
        """
        self.models = [m.lower() for m in models] if models else []
        self.max_price = max_price
    
    def matches(self, listing: GiftListing) -> bool:
        """
        Check if listing matches filter criteria.
        
        Args:
            listing: GiftListing to check
            
        Returns:
            True if listing matches criteria
        """
        # Check model
        if self.models:
            listing_model = (listing.model or "").lower()
            if not any(model in listing_model for model in self.models):
                return False
        
        # Check price
        if listing.price_ton > self.max_price:
            return False
        
        return True
    
    def filter_listings(self, listings: List[GiftListing]) -> List[GiftListing]:
        """
        Filter list of listings.
        
        Args:
            listings: List of GiftListing objects
            
        Returns:
            Filtered list of GiftListing objects
        """
        return [listing for listing in listings if self.matches(listing)]

