"""Gift search functionality."""
import asyncio
import time
from typing import List, Tuple, Optional
from portals_auth import PortalsAuthManager
from ton_price import TonPriceFetcher


class GiftSearcher:
    """Handles searching for gifts on Portals Marketplace."""

    def __init__(self):
        self.auth_manager = PortalsAuthManager()
        self.price_fetcher = TonPriceFetcher()

    async def search_gifts(
        self,
        wanted_combinations: List[Tuple[str, str]],
        max_price: int,
        max_pages: int = 20
    ) -> List[dict]:
        """
        Search for gifts matching wanted combinations.

        Args:
            wanted_combinations: List of (gift_name, model) tuples
            max_price: Maximum price in TON
            max_pages: Maximum pages to fetch

        Returns:
            List of gift dictionaries matching criteria
        """
        # Get authentication token
        token = await self.auth_manager.get_token()

        import portalsmp

        # Extract unique gifts and models for API query
        gift_names = list(set(gift for gift, _ in wanted_combinations))
        models = list(set(model for _, model in wanted_combinations))

        # Search with pagination (API uses OR logic)
        all_results = []
        offset = 0
        limit = 20

        for page in range(max_pages):
            try:
                results = portalsmp.search(
                    authData=token,
                    gift_name=gift_names,
                    model=models,
                    max_price=max_price,
                    offset=offset,
                    limit=limit,
                    sort="price_asc"  # Cheapest first
                )

                if not results:
                    break

                all_results.extend(results)
                offset += limit

                # Stop if this was the last page
                if len(results) < limit:
                    break

                # Sleep to avoid rate limit
                time.sleep(0.5)

            except Exception as e:
                if "429" in str(e):
                    # Rate limit, wait and retry
                    time.sleep(5)
                    continue
                else:
                    print(f"Error searching gifts: {e}")
                    break

        # CLIENT-SIDE FILTERING: Keep only wanted gift+model combinations
        filtered_results = []
        for gift in all_results:
            gift_name = gift.get('name', '')
            attrs = gift.get('attributes', [])
            model = next((a['value'] for a in attrs if a['type'] == 'model'), '')

            # Check if this combination is in our wanted list
            if (gift_name, model) in wanted_combinations:
                filtered_results.append(gift)

        return filtered_results

    @staticmethod
    def format_gift_info(gift: dict) -> dict:
        """
        Extract and format gift information.

        Returns dict with formatted fields for easy display.
        """
        attrs = gift.get('attributes', [])

        # Extract attributes
        model = next((a['value'] for a in attrs if a['type'] == 'model'), 'N/A')
        symbol = next((a['value'] for a in attrs if a['type'] == 'symbol'), 'N/A')
        backdrop = next((a['value'] for a in attrs if a['type'] == 'backdrop'), 'N/A')

        # Extract rarities
        model_rarity = next((a['rarity_per_mille']/10 for a in attrs if a['type'] == 'model'), 0)
        symbol_rarity = next((a['rarity_per_mille']/10 for a in attrs if a['type'] == 'symbol'), 0)
        backdrop_rarity = next((a['rarity_per_mille']/10 for a in attrs if a['type'] == 'backdrop'), 0)

        return {
            'id': gift.get('id'),
            'name': gift.get('name'),
            'number': gift.get('external_collection_number'),
            'price': gift.get('price'),
            'floor_price': gift.get('floor_price'),
            'model': model,
            'model_rarity': model_rarity,
            'symbol': symbol,
            'symbol_rarity': symbol_rarity,
            'backdrop': backdrop,
            'backdrop_rarity': backdrop_rarity,
            'url': f"https://portals.tg/gift/{gift.get('id')}",
            'photo_url': gift.get('photo_url', ''),
        }

    async def format_gift_caption(self, info: dict) -> str:
        """Format gift information as Telegram caption with UAH price."""
        # Get TON price in UAH
        ton_price_uah = await self.price_fetcher.get_ton_price_uah()
        price_str = self.price_fetcher.format_price_with_uah(info['price'], ton_price_uah)

        caption = f"""🎁 {info['name']} #{info['number']}

💰 Ціна: {price_str}

🎨 Модель: {info['model']} ({info['model_rarity']:.1f}%)
🔣 Символ: {info['symbol']} ({info['symbol_rarity']:.1f}%)
🖼️ Фон: {info['backdrop']} ({info['backdrop_rarity']:.1f}%)

🔗 {info['url']}"""
        return caption
