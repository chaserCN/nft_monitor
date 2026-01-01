"""Configuration module for NFT Gift Monitor Bot."""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration."""
    
    # Telegram Bot
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "")
    
    # Monitoring settings
    CHECK_INTERVAL_MINUTES = int(os.getenv("CHECK_INTERVAL_MINUTES", "5"))
    MAX_PRICE_TON = float(os.getenv("MAX_PRICE_TON", "100"))
    
    # Gift models to monitor
    GIFT_MODELS = [
        model.strip() 
        for model in os.getenv("GIFT_MODELS", "").split(",") 
        if model.strip()
    ]
    
    # API endpoints
    PORTALS_API_BASE = "https://api.portals.market"
    TONNEL_API_BASE = "https://api.tonnel.market"
    
    @classmethod
    def validate(cls):
        """Validate configuration."""
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is required")
        if not cls.TELEGRAM_CHANNEL_ID:
            raise ValueError("TELEGRAM_CHANNEL_ID is required")
        if not cls.GIFT_MODELS:
            raise ValueError("GIFT_MODELS must be specified")

