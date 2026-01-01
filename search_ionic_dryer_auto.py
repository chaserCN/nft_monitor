"""Search for Ionic dryer Love Burst gifts with automatic authentication."""
import sys
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()


async def get_auth_token():
    """Get authentication token automatically."""
    from portals_auth import PortalsAuthManager

    manager = PortalsAuthManager()

    # Check if we have credentials
    if not manager.has_auto_auth() and not manager.has_manual_auth():
        print("="*60)
        print("FIRST TIME SETUP REQUIRED")
        print("="*60)
        print("\nTo use automatic authentication, you need Telegram API credentials.")
        print("\nSTEPS:")
        print("1. Open https://my.telegram.org/auth")
        print("2. Login with your phone number")
        print("3. Go to 'API development tools'")
        print("4. Create an application (any name)")
        print("5. Copy api_id and api_hash")
        print("\nThen either:")
        print("  A) Set environment variables:")
        print("     export TELEGRAM_API_ID=your_api_id")
        print("     export TELEGRAM_API_HASH=your_api_hash")
        print("\n  B) Add to .env file:")
        print("     TELEGRAM_API_ID=your_api_id")
        print("     TELEGRAM_API_HASH=your_api_hash")

        # Ask if user wants to enter now
        print("\n" + "="*60)
        try:
            response = input("Do you have api_id and api_hash ready? (y/n): ").strip().lower()
            if response == 'y':
                api_id = input("Enter api_id: ").strip()
                api_hash = input("Enter api_hash: ").strip()

                # Set in environment for this session
                os.environ["TELEGRAM_API_ID"] = api_id
                os.environ["TELEGRAM_API_HASH"] = api_hash

                # Recreate manager with new credentials
                manager = PortalsAuthManager()
            else:
                print("\nCome back when you have the credentials!")
                return None
        except KeyboardInterrupt:
            print("\n\nCancelled.")
            return None

    # Get token (will auto-refresh if needed)
    try:
        token = await manager.get_token()
        print("\n✓ Authentication successful!")
        return token
    except Exception as e:
        print(f"\n✗ Authentication failed: {e}")
        return None


async def search_ionic_dryer():
    """Search for Ionic dryer Love Burst on Portals."""

    print("="*60)
    print("SEARCHING FOR IONIC DRYER - LOVE BURST")
    print("="*60)

    # Get authentication token automatically
    print("\nGetting authentication token...")
    auth_token = await get_auth_token()

    if not auth_token:
        print("\n⚠️  Cannot proceed without authentication.")
        return

    try:
        import portalsmp
        print("✓ portalsmp library loaded\n")
    except ImportError:
        print("✗ portalsmp not installed")
        print("Install with: pip3 install portalsmp")
        return

    # Search strategies
    search_strategies = [
        {"gift_name": "Ionic dryer", "model": "Love Burst"},
        {"gift_name": "Ionic dryer"},
        {"model": "Love Burst"},
        {"gift_name": "love burst"},
    ]

    all_results = []

    for i, params in enumerate(search_strategies):
        query_desc = ", ".join([f"{k}='{v}'" for k, v in params.items()])
        print(f"\nSearch #{i+1}: {query_desc}")
        print("-" * 60)

        try:
            results = portalsmp.search(
                authData=auth_token,
                limit=50,
                sort="price_asc",  # Cheapest first
                **params
            )

            if results:
                print(f"✓ Found {len(results)} listings")

                # Filter for Love Burst model
                love_burst_results = [
                    r for r in results
                    if 'love burst' in str(r.get('model', {}).get('name', '')).lower()
                    or 'love burst' in str(r.get('name', '')).lower()
                ]

                if love_burst_results:
                    print(f"  ({len(love_burst_results)} are Love Burst model)")
                    all_results.extend(love_burst_results)
                else:
                    # Add all results if we can't filter
                    all_results.extend(results)

            else:
                print(f"  No results")

        except Exception as e:
            print(f"✗ Error: {e}")

            if "auth" in str(e).lower() or "401" in str(e) or "403" in str(e):
                print("\n⚠️  Authentication error!")
                print("Token might be expired. Will auto-refresh on next run.")
                return

    # Remove duplicates
    seen_ids = set()
    unique_results = []
    for r in all_results:
        gift_id = r.get('id') or r.get('tg_id')
        if gift_id and gift_id not in seen_ids:
            seen_ids.add(gift_id)
            unique_results.append(r)

    if unique_results:
        print("\n" + "="*60)
        print(f"FOUND {len(unique_results)} IONIC DRYER LOVE BURST GIFTS")
        print("="*60)

        # Sort by price
        unique_results.sort(key=lambda x: float(x.get('price', 999999)))

        # Display results
        for i, gift in enumerate(unique_results):
            print(f"\n[{i+1}] Gift ID: {gift.get('id') or gift.get('tg_id')}")

            # Name
            name = gift.get('name', 'Unknown')
            print(f"    Name: {name}")

            # Model
            model_data = gift.get('model', {})
            if isinstance(model_data, dict):
                model_name = model_data.get('name', 'Unknown')
                model_rarity = model_data.get('percent', 'N/A')
                print(f"    Model: {model_name} ({model_rarity}% rarity)")

            # Symbol
            symbol_data = gift.get('symbol', {})
            if isinstance(symbol_data, dict):
                symbol_name = symbol_data.get('name', '')
                if symbol_name:
                    print(f"    Symbol: {symbol_name}")

            # Backdrop
            backdrop_data = gift.get('backdrop', {})
            if isinstance(backdrop_data, dict):
                backdrop_name = backdrop_data.get('name', '')
                if backdrop_name:
                    print(f"    Backdrop: {backdrop_name}")

            # Price
            price = gift.get('price', 0)
            print(f"    💰 Price: {price} TON")

            # Floor price
            floor = gift.get('floor_price', 0)
            if floor:
                print(f"    📊 Floor: {floor} TON")

            # Owner
            owner = gift.get('owner', {})
            if isinstance(owner, dict):
                owner_addr = owner.get('address', '')[:10]
                if owner_addr:
                    print(f"    👤 Owner: {owner_addr}...")

            # URL
            gift_id = gift.get('id') or gift.get('tg_id')
            url = f"https://portalsmarket.co/gift/{gift_id}"
            print(f"    🔗 URL: {url}")

        # Summary
        print("\n" + "="*60)
        print("PRICE SUMMARY")
        print("="*60)

        prices = [float(g.get('price', 0)) for g in unique_results if g.get('price')]
        if prices:
            print(f"Cheapest: {min(prices)} TON")
            print(f"Most expensive: {max(prices)} TON")
            print(f"Average: {sum(prices)/len(prices):.2f} TON")
            print(f"Total listings: {len(unique_results)}")

    else:
        print("\n" + "="*60)
        print("NO RESULTS FOUND")
        print("="*60)
        print("\nPossible reasons:")
        print("- No Ionic dryer Love Burst gifts currently listed on Portals")
        print("- All listings might be sold out")
        print("- Try checking on Fragment or GetGems manually")


def main():
    """Main function."""
    asyncio.run(search_ionic_dryer())


if __name__ == "__main__":
    main()
