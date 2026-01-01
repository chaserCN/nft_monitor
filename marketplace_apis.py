"""Marketplace API clients for NFT gifts."""
import logging
import asyncio
from typing import List, Dict, Optional
from datetime import datetime
from portals_auth import PortalsAuthManager

logger = logging.getLogger(__name__)


class GiftListing:
    """Represents a gift listing from marketplace."""

    def __init__(self, data: Dict):
        self.id = data.get("id", "")
        self.model = data.get("model", "")
        self.price_ton = data.get("price_ton", 0.0)
        self.seller = data.get("seller", "")
        self.marketplace = data.get("marketplace", "")
        self.url = data.get("url", "")
        self.image_url = data.get("image_url", "")
        self.timestamp = data.get("timestamp", datetime.now().isoformat())

    def __repr__(self):
        return f"GiftListing(model={self.model}, price={self.price_ton} TON, marketplace={self.marketplace})"


class PortalsAPI:
    """Client for Portals marketplace API using portalsmp library."""

    def __init__(self, auth_data: str = ""):
        """
        Initialize Portals API client.

        Args:
            auth_data: Optional manual authentication token (overrides auto-auth)
        """
        # Initialize auth manager
        self.auth_manager = PortalsAuthManager(manual_token=auth_data)

        try:
            import portalsmp
            self.portalsmp = portalsmp
            self.available = True

            # Try to get a token to verify auth is configured
            try:
                self._get_auth_token()
                logger.info("Portals authentication configured successfully")
            except ValueError as e:
                logger.warning(f"Portals authentication not configured: {e}")
                self.available = False

        except ImportError:
            logger.error("portalsmp library not installed. Install with: pip install portalsmp")
            self.available = False
            self.portalsmp = None

    def _get_auth_token(self) -> str:
        """
        Get valid authentication token.

        Returns:
            Authentication token
        """
        return asyncio.run(self.auth_manager.get_token())

    def get_gifts(self, models: Optional[List[str]] = None) -> List[GiftListing]:
        """
        Fetch available gift listings from Portals.

        Args:
            models: Optional list of gift models to filter by

        Returns:
            List of GiftListing objects
        """
        if not self.available:
            logger.warning("Portals API not available")
            return []

        listings = []

        try:
            # Get fresh auth token (auto-refreshes if needed)
            auth_token = self._get_auth_token()

            # If specific models requested, search for each
            if models:
                for model in models:
                    try:
                        logger.info(f"Searching Portals for model: {model}")
                        results = self.portalsmp.search(
                            authData=auth_token,
                            name=model,
                            limit=50,
                            sort="price_asc"  # Cheapest first
                        )

                        if results:
                            logger.info(f"Found {len(results)} listings for '{model}'")
                            listings.extend(self._parse_search_results(results))

                    except Exception as e:
                        logger.error(f"Error searching for '{model}': {e}")
                        continue
            else:
                # Get floor prices to see what's available cheaply
                logger.info("Getting floor prices from Portals")
                floors = self.portalsmp.giftsFloors(authData=auth_token)

                # Sort by floor price and get cheapest items
                sorted_floors = sorted(floors, key=lambda x: x.get('floor_price', 0))

                # Get listings for cheapest gifts
                for item in sorted_floors[:20]:  # Top 20 cheapest
                    name = item.get('name', '')
                    try:
                        results = self.portalsmp.search(
                            authData=auth_token,
                            name=name,
                            limit=10,
                            sort="price_asc"
                        )

                        if results:
                            listings.extend(self._parse_search_results(results))

                    except Exception as e:
                        logger.debug(f"Error getting listings for '{name}': {e}")
                        continue

            logger.info(f"Successfully fetched {len(listings)} listings from Portals")

        except Exception as e:
            logger.error(f"Error fetching from Portals API: {e}")

            if "auth" in str(e).lower() or "token" in str(e).lower():
                logger.error("Authentication error. Your PORTALS_AUTH_DATA may be expired.")
                logger.error("Get a fresh token from web.telegram.org (see test_portals_simple.py)")

        return listings

    def _parse_search_results(self, results: List[Dict]) -> List[GiftListing]:
        """Parse search results into GiftListing objects."""
        listings = []

        for item in results:
            try:
                # Extract price
                price = float(item.get('price', 0))

                # Extract model information
                model_data = item.get('model', {})
                if isinstance(model_data, dict):
                    model_name = model_data.get('name', '')
                else:
                    model_name = str(model_data)

                # Gift name
                gift_name = item.get('name', '')

                # Combine for full model description
                full_model = f"{gift_name} ({model_name})" if model_name else gift_name

                # Owner/seller info
                owner = item.get('owner', {})
                if isinstance(owner, dict):
                    seller = owner.get('address', '') or owner.get('id', '')
                else:
                    seller = str(owner)

                # Gift ID
                gift_id = item.get('id', '') or item.get('tg_id', '')

                listing = GiftListing({
                    "id": str(gift_id),
                    "model": full_model,
                    "price_ton": price,
                    "seller": seller,
                    "marketplace": "Portals",
                    "url": f"https://portalsmarket.co/gift/{gift_id}",
                    "image_url": item.get('photo_url', '') or item.get('animation_url', ''),
                    "timestamp": item.get('listed_at', datetime.now().isoformat())
                })

                listings.append(listing)

            except Exception as e:
                logger.debug(f"Error parsing item: {e}")
                continue

        return listings


class TonnelAPI:
    """Client for Tonnel marketplace API."""

    def __init__(self):
        """Initialize Tonnel API client."""
        # Tonnel doesn't have a public API available yet
        # This is a placeholder for future implementation
        logger.info("Tonnel API client initialized (not yet implemented)")
        self.available = False

    def get_gifts(self, models: Optional[List[str]] = None) -> List[GiftListing]:
        """
        Fetch available gift listings from Tonnel.

        Args:
            models: Optional list of gift models to filter by

        Returns:
            List of GiftListing objects
        """
        # Tonnel API is not publicly available yet
        logger.debug("Tonnel API not yet implemented")
        return []


class MarketplaceAggregator:
    """Aggregates listings from multiple marketplaces."""

    def __init__(self, portals_auth: str = ""):
        """
        Initialize aggregator.

        Args:
            portals_auth: Portals authentication data
        """
        self.portals = PortalsAPI(portals_auth)
        self.tonnel = TonnelAPI()

    def get_all_gifts(self, models: Optional[List[str]] = None) -> List[GiftListing]:
        """
        Get gifts from all available marketplaces.

        Args:
            models: Optional list of gift models to filter by

        Returns:
            Combined list of GiftListing objects from all marketplaces
        """
        all_listings = []

        # Get from Portals
        portals_listings = self.portals.get_gifts(models)
        all_listings.extend(portals_listings)

        # Get from Tonnel (when available)
        tonnel_listings = self.tonnel.get_gifts(models)
        all_listings.extend(tonnel_listings)

        logger.info(f"Total listings from all marketplaces: {len(all_listings)}")

        return all_listings
