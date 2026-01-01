"""Search for Ionic dryer Love Burst gifts."""
import sys
import os


def search_ionic_dryer(auth_token=None):
    """Search for Ionic dryer Love Burst on Portals."""

    # Get auth token from parameter, environment, or ask user
    if not auth_token:
        auth_token = os.getenv("PORTALS_AUTH_DATA", "")

    if not auth_token:
        print("="*60)
        print("AUTHENTICATION REQUIRED")
        print("="*60)
        print("\nNo authentication token provided.")
        print("\nOptions:")
        print("1. Pass token as argument:")
        print("   python3 search_ionic_dryer.py 'tma <your_token>'")
        print("\n2. Set in .env file:")
        print("   PORTALS_AUTH_DATA=tma <your_token>")
        print("\n3. Get token from web.telegram.org:")
        print("   See GET_AUTH_TOKEN.md for instructions")
        return

    print("="*60)
    print("SEARCHING FOR IONIC DRYER - LOVE BURST")
    print("="*60)

    try:
        import portalsmp
        print("✓ portalsmp library loaded\n")
    except ImportError:
        print("✗ portalsmp not installed")
        print("Install with: pip3 install portalsmp")
        return

    # Search queries to try
    search_queries = [
        "Ionic dryer Love Burst",
        "Love Burst",
        "Ionic dryer",
        "love burst",
    ]

    all_results = []

    for query in search_queries:
        print(f"\nSearching for: '{query}'")
        print("-" * 60)

        try:
            results = portalsmp.search(
                authData=auth_token,
                name=query,
                limit=50,
                sort="price_asc"  # Cheapest first
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
                print("Your token might be expired or invalid.")
                print("Get a fresh token from web.telegram.org")
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
    # Check if token provided as argument
    auth_token = None
    if len(sys.argv) > 1:
        auth_token = sys.argv[1]

    search_ionic_dryer(auth_token)


if __name__ == "__main__":
    main()
