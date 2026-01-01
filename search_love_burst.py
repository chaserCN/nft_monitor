"""Search for Ionic Dryer with Love Burst model - WORKING VERSION."""
import asyncio
import json
from dotenv import load_dotenv
from portals_auth import PortalsAuthManager

load_dotenv()


async def search_love_burst():
    """Search for Ionic Dryer with Love Burst model."""

    print("="*60)
    print("SEARCHING: IONIC DRYER - LOVE BURST")
    print("="*60)

    # Get auth
    manager = PortalsAuthManager()
    token = await manager.get_token()
    print("✓ Authenticated\n")

    import portalsmp

    # Get ALL gifts (API ignores filters)
    print("Fetching all available gifts...")
    all_gifts = portalsmp.search(
        authData=token,
        limit=100,  # Get more results
        sort="price_asc"
    )

    print(f"✓ Got {len(all_gifts)} gifts total\n")

    # Filter on our side
    print("Filtering for Ionic Dryer with Love Burst model...")

    love_burst_gifts = []

    for gift in all_gifts:
        gift_name = gift.get('name', '').lower()

        # Check if it's Ionic Dryer
        if 'ionic dryer' not in gift_name:
            continue

        # Check model in attributes
        attributes = gift.get('attributes', [])
        model_name = None

        for attr in attributes:
            if attr.get('type') == 'model':
                model_name = attr.get('value', '')
                break

        # Check if model is Love Burst
        if model_name and 'love burst' in model_name.lower():
            love_burst_gifts.append({
                'gift': gift,
                'model': model_name
            })

    print(f"✓ Found {len(love_burst_gifts)} Ionic Dryer - Love Burst gifts!\n")

    if love_burst_gifts:
        print("="*60)
        print(f"RESULTS: {len(love_burst_gifts)} GIFTS")
        print("="*60)

        # Sort by price
        love_burst_gifts.sort(key=lambda x: float(x['gift'].get('price', 999999)))

        for i, item in enumerate(love_burst_gifts):
            gift = item['gift']
            model = item['model']

            print(f"\n[{i+1}] {gift.get('tg_id', 'N/A')}")
            print(f"    Name: {gift.get('name')}")
            print(f"    Model: {model}")

            # Get other attributes
            attributes = gift.get('attributes', [])
            for attr in attributes:
                if attr.get('type') == 'symbol':
                    print(f"    Symbol: {attr.get('value')} (rarity: {attr.get('rarity_per_mille')/10:.1f}%)")
                elif attr.get('type') == 'backdrop':
                    print(f"    Backdrop: {attr.get('value')} (rarity: {attr.get('rarity_per_mille')/10:.1f}%)")

            print(f"    💰 Price: {gift.get('price')} TON")
            print(f"    📊 Floor: {gift.get('floor_price')} TON")

            owner = gift.get('owner')
            if owner:
                print(f"    👤 Listed: {gift.get('listed_at', '')[:10]}")

            print(f"    🔗 https://portals.tg/gift/{gift.get('id')}")
            print(f"    🖼️  {gift.get('photo_url', '')}")

        # Summary
        print("\n" + "="*60)
        print("PRICE SUMMARY")
        print("="*60)

        prices = [float(g['gift'].get('price', 0)) for g in love_burst_gifts]
        if prices:
            print(f"💰 Cheapest: {min(prices)} TON")
            print(f"💰 Most expensive: {max(prices)} TON")
            print(f"💰 Average: {sum(prices)/len(prices):.2f} TON")
            print(f"📊 Total listings: {len(love_burst_gifts)}")

    else:
        print("\n❌ No Ionic Dryer - Love Burst gifts found")
        print("\nTrying to see what Ionic Dryer models ARE available...")

        # Show what models exist
        ionic_dryers = [g for g in all_gifts if 'ionic dryer' in g.get('name', '').lower()]

        if ionic_dryers:
            print(f"\nFound {len(ionic_dryers)} Ionic Dryer gifts with these models:")
            models_seen = set()

            for gift in ionic_dryers[:20]:  # Show first 20
                attributes = gift.get('attributes', [])
                for attr in attributes:
                    if attr.get('type') == 'model':
                        model = attr.get('value')
                        if model not in models_seen:
                            models_seen.add(model)
                            print(f"  - {model}")


if __name__ == "__main__":
    asyncio.run(search_love_burst())
