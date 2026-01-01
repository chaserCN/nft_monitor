"""Automatic authentication manager for Portals Marketplace."""
import os
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Optional

logger = logging.getLogger(__name__)


class PortalsAuthManager:
    """Manages Portals authentication with automatic token refresh."""

    def __init__(self, manual_token: Optional[str] = None):
        """
        Initialize auth manager.

        Args:
            manual_token: Optional manual token from .env (PORTALS_AUTH_DATA)
        """
        self.manual_token = manual_token or os.getenv("PORTALS_AUTH_DATA", "")
        self.auto_token = None
        self.token_expires_at = None
        self.token_refresh_failed = False

        # Telegram API credentials for automatic auth
        self.api_id = os.getenv("TELEGRAM_API_ID", "")
        self.api_hash = os.getenv("TELEGRAM_API_HASH", "")

    def has_auto_auth(self) -> bool:
        """Check if automatic authentication is configured."""
        return bool(self.api_id and self.api_hash)

    def has_manual_auth(self) -> bool:
        """Check if manual token is provided."""
        return bool(self.manual_token)

    def is_token_expired(self) -> bool:
        """Check if current auto token is expired."""
        if not self.token_expires_at:
            return True
        return datetime.now() >= self.token_expires_at

    async def refresh_token(self) -> bool:
        """
        Refresh authentication token using Telegram API.

        Returns:
            True if successful, False otherwise
        """
        if not self.has_auto_auth():
            logger.warning("Auto-auth not configured (missing TELEGRAM_API_ID/API_HASH)")
            return False

        try:
            logger.info("Refreshing Portals authentication token...")

            # Import here to avoid dependency if not using auto-auth
            from portalsmp import update_auth

            # Get new token
            self.auto_token = await update_auth(
                api_id=int(self.api_id),
                api_hash=self.api_hash
            )

            # Set expiration (tokens typically last 5-7 days, refresh every 5 days to be safe)
            self.token_expires_at = datetime.now() + timedelta(days=5)

            logger.info(f"✓ Token refreshed successfully. Expires: {self.token_expires_at}")
            self.token_refresh_failed = False

            return True

        except ImportError:
            logger.error("portalsmp library not installed. Install with: pip install portalsmp")
            self.token_refresh_failed = True
            return False

        except Exception as e:
            logger.error(f"Failed to refresh token: {e}")
            logger.error("You may need to delete account.session and re-authenticate")
            self.token_refresh_failed = True
            return False

    async def get_token(self) -> str:
        """
        Get valid authentication token.

        Priority:
        1. Auto-refreshed token (if configured and valid)
        2. Manual token from .env
        3. Attempt to refresh if auto-auth configured

        Returns:
            Valid authentication token

        Raises:
            ValueError: If no valid token available
        """
        # Try to use auto-refreshed token
        if self.has_auto_auth():
            # Check if we have a valid auto token
            if self.auto_token and not self.is_token_expired():
                logger.debug("Using cached auto token")
                return self.auto_token

            # Try to refresh
            if not self.token_refresh_failed:
                success = await self.refresh_token()
                if success and self.auto_token:
                    return self.auto_token

        # Fallback to manual token
        if self.has_manual_auth():
            logger.info("Using manual token from PORTALS_AUTH_DATA")
            return self.manual_token

        # No valid token available
        error_msg = """
No valid Portals authentication available.

Please configure ONE of the following:

OPTION 1 (Recommended): Automatic authentication
  1. Get Telegram API credentials at https://my.telegram.org/auth
  2. Add to .env file:
     TELEGRAM_API_ID=your_api_id
     TELEGRAM_API_HASH=your_api_hash
  3. On first run, you'll be asked for phone number and SMS code
  4. Token will auto-refresh every 5 days

OPTION 2: Manual token
  1. Get token from web.telegram.org (see GET_AUTH_TOKEN.md)
  2. Add to .env file:
     PORTALS_AUTH_DATA=tma <your_token>
  3. You'll need to update this manually every 1-7 days

See AUTHENTICATION_EXPLAINED.md for detailed instructions.
        """
        raise ValueError(error_msg)

    def get_token_sync(self) -> str:
        """
        Synchronous wrapper for get_token().

        Returns:
            Valid authentication token

        Raises:
            ValueError: If no valid token available
        """
        return asyncio.run(self.get_token())

    def get_auth_status(self) -> dict:
        """
        Get current authentication status.

        Returns:
            Dictionary with auth status information
        """
        status = {
            "has_auto_auth": self.has_auto_auth(),
            "has_manual_auth": self.has_manual_auth(),
            "auto_token_valid": bool(self.auto_token and not self.is_token_expired()),
            "token_expires_at": self.token_expires_at.isoformat() if self.token_expires_at else None,
            "token_refresh_failed": self.token_refresh_failed,
        }

        if status["has_auto_auth"]:
            if status["auto_token_valid"]:
                status["auth_method"] = "automatic (active)"
            else:
                status["auth_method"] = "automatic (needs refresh)"
        elif status["has_manual_auth"]:
            status["auth_method"] = "manual token"
        else:
            status["auth_method"] = "none (not configured)"

        return status

    def print_status(self):
        """Print authentication status to console."""
        status = self.get_auth_status()

        print("\n" + "="*60)
        print("PORTALS AUTHENTICATION STATUS")
        print("="*60)

        print(f"\nAuth Method: {status['auth_method']}")
        print(f"Auto-auth configured: {'✓' if status['has_auto_auth'] else '✗'}")
        print(f"Manual token configured: {'✓' if status['has_manual_auth'] else '✗'}")

        if status['auto_token_valid']:
            print(f"\n✓ Auto token is valid")
            print(f"  Expires: {status['token_expires_at']}")
        elif status['has_auto_auth']:
            print(f"\n⚠️  Auto token needs refresh")

        if status['token_refresh_failed']:
            print(f"\n✗ Last token refresh failed")
            print("  Check your Telegram API credentials")

        if not status['has_auto_auth'] and not status['has_manual_auth']:
            print("\n⚠️  No authentication configured!")
            print("  See AUTHENTICATION_EXPLAINED.md for setup instructions")

        print()


# Convenience function for backward compatibility
async def get_portals_token() -> str:
    """
    Get a valid Portals authentication token.

    Returns:
        Valid authentication token
    """
    manager = PortalsAuthManager()
    return await manager.get_token()
