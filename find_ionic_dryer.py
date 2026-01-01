"""Find ALL Ionic Dryer gifts with pagination."""
import asyncio
import time
from dotenv import load_dotenv
from portals_auth import PortalsAuthManager

load_dotenv()


async def find_all_ionic_dryer():
    """Find all Ionic Dryer gifts using pagination."""

    print("="*60)
    print("SEARCHING ALL IONIC DRYER GIFTS")
    print("="*60)

    manager = PortalsAuthManager()
    token = await manager.get_token()
    print("✓ Authenticated\n")

    import portalsmp

    all_ionic_dryer = []
    offset = 0
    limit = 50
    max_pages = 20  # Maximum pages to fetch (1000 gifts)

    print("Fetching gifts with pagination...")
    print("(This may take a minute due to rate limits)\n")

    for page in range(max_pages):
        try:
            print(f"Page {page+1}: offset={offset}, limit={limit}... ", end="", flush=True)

            results = portalsmp.search(
                authData=token,
                offset=offset,
                limit=limit,
                sort="price_asc"
            )

            print(f"got {len(results)} gifts")

            if not results:
                print("No more results, stopping.")
                break

            # Filter for Ionic Dryer
            for gift in results:
                if 'ionic dryer' in gift.get('name', '').lower():
                    all_ionic_dryer.append(gift)

            offset += limit

            # Sleep to avoid rate limit
            time.sleep(1)

        except Exception as e:
            if "429" in str(e):
                print(f"\nRate limit hit, waiting 5 seconds...")
                time.sleep(5)
                continue
            else:
                print(f"\nError: {e}")
                break

    print(f"\n{'='*60}")
    print(f"FOUND {len(all_ionic_dryer)} IONIC DRYER GIFTS TOTAL")
    print("="*60)

    if all_ionic_dryer:
        # Group by model
        by_model = {}

        for gift in all_ionic_dryer:
            attributes = gift.get('attributes', [])
            model_name = "Unknown"

            for attr in attributes:
                if attr.get('type') == 'model':
                    model_name = attr.get('value', 'Unknown')
                    break

            if model_name not in by_model:
                by_model[model_name] = []
            by_model[model_name].append(gift)

        # Show models
        print("\nIonic Dryer models found:")
        for model, gifts in sorted(by_model.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"\n  {model}: {len(gifts)} gifts")

            # Show cheapest for each model
            gifts_sorted = sorted(gifts, key=lambda x: float(x.get('price', 999999)))
            cheapest = gifts_sorted[0]
            print(f"    Cheapest: {cheapest.get('price')} TON")

        # Show Love Burst specifically
        if "Love Burst" in by_model:
            print(f"\n{'='*60}")
            print(f"LOVE BURST DETAILS ({len(by_model['Love Burst'])} gifts)")
            print("="*60)

            love_burst_gifts = sorted(by_model['Love Burst'], key=lambda x: float(x.get('price', 999999)))

            for i, gift in enumerate(love_burst_gifts[:10]):  # Show first 10
                print(f"\n[{i+1}] {gift.get('tg_id')}")
                print(f"    💰 Price: {gift.get('price')} TON")
                print(f"    📊 Floor: {gift.get('floor_price')} TON")

                # Show all attributes
                for attr in gift.get('attributes', []):
                    attr_type = attr.get('type')
                    attr_value = attr.get('value')
                    rarity = attr.get('rarity_per_mille', 0) / 10
                    print(f"    {attr_type.title()}: {attr_value} ({rarity:.1f}%)")

                print(f"    🔗 https://portals.tg/gift/{gift.get('id')}")

            # Summary
            prices = [float(g.get('price', 0)) for g in love_burst_gifts]
            print(f"\n{'='*60}")
            print("LOVE BURST PRICE SUMMARY")
            print("="*60)
            print(f"💰 Cheapest: {min(prices)} TON")
            print(f"💰 Most expensive: {max(prices)} TON")
            print(f"💰 Average: {sum(prices)/len(prices):.2f} TON")
            print(f"📊 Total: {len(love_burst_gifts)} listings")

        else:
            print("\n❌ No Love Burst model found in Ionic Dryer gifts")

    else:
        print("\n❌ No Ionic Dryer gifts found at all")
        print("Possible reasons:")
        print("- All sold out")
        print("- Different name spelling")
        print("- Need to search more pages")


if __name__ == "__main__":
    asyncio.run(find_all_ionic_dryer())
