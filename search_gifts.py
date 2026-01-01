"""Script to search for specific NFT gift models."""
import logging
import sys
from marketplace_apis import MarketplaceAggregator
from filter import GiftFilter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def search_gifts(collection: str, model: str, max_price: float = None):
    aggregator = MarketplaceAggregator()
    listings = aggregator.get_all_gifts([model, f"{collection} {model}"])
    
    filter_obj = GiftFilter([model], max_price or 999999)
    filtered = filter_obj.filter_listings(listings)
    filtered.sort(key=lambda x: x.price_ton)
    
    print(f"Найдено: {len(filtered)}")
    for listing in filtered:
        print(f"{listing.model} - {listing.price_ton} TON - {listing.marketplace}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python search_gifts.py <collection> <model> [max_price]")
        sys.exit(1)
    
    collection = sys.argv[1]
    model = sys.argv[2]
    max_price = float(sys.argv[3]) if len(sys.argv) > 3 else None
    search_gifts(collection, model, max_price)

