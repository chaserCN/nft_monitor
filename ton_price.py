"""TON price fetcher using CoinGecko API."""
import asyncio
import aiohttp
from typing import Optional


class TonPriceFetcher:
    """Fetches TON price in UAH."""

    def __init__(self):
        self.api_url = "https://api.coingecko.com/api/v3/simple/price"
        self.cached_price = None
        self.cache_time = 0
        self.cache_duration = 300  # 5 minutes

    async def get_ton_price_uah(self) -> Optional[float]:
        """
        Get current TON price in UAH.

        Returns:
            TON price in UAH or None if failed
        """
        import time
        current_time = time.time()

        # Return cached price if still valid
        if self.cached_price and (current_time - self.cache_time) < self.cache_duration:
            return self.cached_price

        try:
            timeout = aiohttp.ClientTimeout(total=5)
            connector = aiohttp.TCPConnector(ssl=False)  # Disable SSL verification
            async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
                params = {
                    'ids': 'the-open-network',
                    'vs_currencies': 'uah'
                }
                async with session.get(self.api_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        price = data.get('the-open-network', {}).get('uah')

                        if price:
                            self.cached_price = float(price)
                            self.cache_time = current_time
                            return self.cached_price
        except Exception as e:
            print(f"Помилка отримання курсу TON: {e}")

        return self.cached_price  # Return old cached price if request failed

    def format_price_with_uah(self, ton_amount, ton_price_uah: Optional[float]) -> str:
        """
        Format price showing both TON and UAH.

        Args:
            ton_amount: Amount in TON (can be string or number)
            ton_price_uah: Current TON price in UAH

        Returns:
            Formatted price string
        """
        # Convert to float if it's a string
        try:
            ton_amount_float = float(ton_amount)
        except (ValueError, TypeError):
            return f"{ton_amount} TON"

        if ton_price_uah:
            uah_amount = ton_amount_float * ton_price_uah
            return f"{ton_amount} TON (~{uah_amount:,.0f} ₴)"
        else:
            return f"{ton_amount} TON"


# Example usage
async def main():
    fetcher = TonPriceFetcher()
    price = await fetcher.get_ton_price_uah()

    if price:
        print(f"TON price: {price:,.2f} ₴")
        print(f"Example: {fetcher.format_price_with_uah(42, price)}")
    else:
        print("Failed to fetch TON price")


if __name__ == "__main__":
    asyncio.run(main())
