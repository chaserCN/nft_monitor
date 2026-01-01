"""Telegram bot for sending notifications."""
import logging
from telegram import Bot
from telegram.error import TelegramError
from marketplace_apis import GiftListing

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Handles Telegram notifications."""
    
    def __init__(self, bot_token: str, channel_id: str):
        """
        Initialize Telegram notifier.
        
        Args:
            bot_token: Telegram bot token
            channel_id: Channel username or ID (e.g., @channel or -1001234567890)
        """
        self.bot = Bot(token=bot_token)
        self.channel_id = channel_id
    
    def format_listing_message(self, listing: GiftListing) -> str:
        """
        Format gift listing as message.
        
        Args:
            listing: GiftListing to format
            
        Returns:
            Formatted message string
        """
        message = f"🎁 <b>Новый подарок доступен!</b>\n\n"
        message += f"📦 <b>Модель:</b> {listing.model}\n"
        message += f"💰 <b>Цена:</b> {listing.price_ton:.2f} TON\n"
        message += f"🏪 <b>Маркетплейс:</b> {listing.marketplace}\n"
        message += f"👤 <b>Продавец:</b> {listing.seller[:10]}...\n\n"
        message += f"🔗 <a href='{listing.url}'>Купить на {listing.marketplace}</a>"
        
        return message
    
    async def send_notification(self, listing: GiftListing) -> bool:
        """
        Send notification about new listing.
        
        Args:
            listing: GiftListing to notify about
            
        Returns:
            True if sent successfully
        """
        try:
            message = self.format_listing_message(listing)
            
            # Send message with optional image
            if listing.image_url:
                await self.bot.send_photo(
                    chat_id=self.channel_id,
                    photo=listing.image_url,
                    caption=message,
                    parse_mode="HTML"
                )
            else:
                await self.bot.send_message(
                    chat_id=self.channel_id,
                    text=message,
                    parse_mode="HTML"
                )
            
            logger.info(f"Notification sent for listing {listing.id}")
            return True
            
        except TelegramError as e:
            logger.error(f"Failed to send Telegram notification: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending notification: {e}")
            return False
    
    async def send_notifications(self, listings: list[GiftListing]) -> int:
        """
        Send multiple notifications.
        
        Args:
            listings: List of GiftListing objects
            
        Returns:
            Number of successfully sent notifications
        """
        sent_count = 0
        for listing in listings:
            if await self.send_notification(listing):
                sent_count += 1
        
        return sent_count

