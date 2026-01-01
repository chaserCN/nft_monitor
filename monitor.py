"""Main monitoring logic."""
import asyncio
import logging
from typing import Set, List
from datetime import datetime
from marketplace_apis import MarketplaceAggregator, GiftListing
from filter import GiftFilter
from telegram_bot import TelegramNotifier
from config import Config

logger = logging.getLogger(__name__)


class GiftMonitor:
    """Monitors NFT gifts and sends notifications."""
    
    def __init__(self):
        """Initialize monitor."""
        self.aggregator = MarketplaceAggregator()
        self.filter = GiftFilter(Config.GIFT_MODELS, Config.MAX_PRICE_TON)
        self.notifier = TelegramNotifier(
            Config.TELEGRAM_BOT_TOKEN,
            Config.TELEGRAM_CHANNEL_ID
        )
        self.seen_listings: Set[str] = set()
    
    def get_listing_key(self, listing: GiftListing) -> str:
        """
        Generate unique key for listing.
        
        Args:
            listing: GiftListing object
            
        Returns:
            Unique string key
        """
        return f"{listing.marketplace}:{listing.id}"
    
    def filter_new_listings(self, listings: List[GiftListing]) -> List[GiftListing]:
        """
        Filter out already seen listings.
        
        Args:
            listings: List of GiftListing objects
            
        Returns:
            List of new (unseen) listings
        """
        new_listings = []
        for listing in listings:
            key = self.get_listing_key(listing)
            if key not in self.seen_listings:
                new_listings.append(listing)
                self.seen_listings.add(key)
        
        return new_listings
    
    async def check_and_notify(self):
        """Check for new gifts and send notifications."""
        try:
            logger.info("Starting gift check...")
            
            # Fetch all gifts
            all_listings = self.aggregator.get_all_gifts(Config.GIFT_MODELS)
            logger.info(f"Found {len(all_listings)} total listings")
            
            # Filter by criteria
            filtered_listings = self.filter.filter_listings(all_listings)
            logger.info(f"Found {len(filtered_listings)} listings matching criteria")
            
            # Filter out already seen
            new_listings = self.filter_new_listings(filtered_listings)
            logger.info(f"Found {len(new_listings)} new listings")
            
            # Send notifications
            if new_listings:
                sent_count = await self.notifier.send_notifications(new_listings)
                logger.info(f"Sent {sent_count} notifications")
            else:
                logger.info("No new listings to notify about")
            
        except Exception as e:
            logger.error(f"Error in check_and_notify: {e}", exc_info=True)
    
    async def run_continuous(self):
        """Run monitoring continuously."""
        logger.info("Starting continuous monitoring...")
        logger.info(f"Check interval: {Config.CHECK_INTERVAL_MINUTES} minutes")
        logger.info(f"Monitoring models: {Config.GIFT_MODELS}")
        logger.info(f"Max price: {Config.MAX_PRICE_TON} TON")
        
        while True:
            try:
                await self.check_and_notify()
                await asyncio.sleep(Config.CHECK_INTERVAL_MINUTES * 60)
            except KeyboardInterrupt:
                logger.info("Monitoring stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in continuous monitoring: {e}", exc_info=True)
                await asyncio.sleep(60)  # Wait 1 minute before retry

