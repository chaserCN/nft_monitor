"""Search for multiple gifts with multiple models and price limit."""
import asyncio
import time
from dotenv import load_dotenv
from portals_auth import PortalsAuthManager

load_dotenv()


async def search_gifts():
    """Search for specific gifts and models with pagination."""

    print("="*60)
    print("SEARCHING MULTIPLE GIFTS & MODELS")
    print("="*60)

    # Search criteria - specific gift+model combinations
    wanted_combinations = [
        ("Ionic Dryer", "Love Burst"),
        ("Spring Basket", "Ritual Goat"),
        ("Jolly Chimp", "La Baboon"),
    ]
    max_price = 31  # TON

    # Extract unique gifts and models for API query
    gift_names = list(set(gift for gift, _ in wanted_combinations))
    models = list(set(model for _, model in wanted_combinations))

    print(f"\nWanted combinations: {len(wanted_combinations)}")
    for gift, model in wanted_combinations:
        print(f"  - {gift} + {model}")
    print(f"\nMax price: {max_price} TON")
    print(f"\nAPI will search for: {len(gift_names)} gifts OR {len(models)} models")
    print(f"Then filter on client side to match exact combinations\n")

    # Get authentication
    manager = PortalsAuthManager()
    token = await manager.get_token()
    print("✓ Authenticated\n")

    import portalsmp

    # Search with pagination (API uses OR logic, so we get all gifts OR all models)
    print("Searching Portals Marketplace with pagination...")
    all_results = []
    offset = 0
    limit = 20
    max_pages = 20  # Maximum 20 pages (400 results) since we're using OR

    for page in range(max_pages):
        print(f"  Page {page+1}: offset={offset}... ", end="", flush=True)

        try:
            results = portalsmp.search(
                authData=token,
                gift_name=gift_names,
                model=models,
                max_price=max_price,
                offset=offset,
                limit=limit,
                sort="price_asc"  # Sort by price (cheapest first)
            )

            print(f"got {len(results)} gifts")

            if not results:
                print("  No more results")
                break

            all_results.extend(results)
            offset += limit

            # Stop if this was the last page
            if len(results) < limit:
                print("  Last page reached")
                break

            # Sleep to avoid rate limit
            time.sleep(1)

        except Exception as e:
            if "429" in str(e):
                print("\n  Rate limit, waiting 5 seconds...")
                time.sleep(5)
                continue
            else:
                print(f"\n  Error: {e}")
                break

    print(f"\n✓ Got {len(all_results)} gifts from API")

    # CLIENT-SIDE FILTERING: Keep only wanted gift+model combinations
    print("Filtering for exact gift+model combinations...")

    filtered_results = []
    for gift in all_results:
        gift_name = gift.get('name', '')
        attrs = gift.get('attributes', [])
        model = next((a['value'] for a in attrs if a['type'] == 'model'), '')

        # Check if this combination is in our wanted list
        if (gift_name, model) in wanted_combinations:
            filtered_results.append(gift)

    all_results = filtered_results
    print(f"✓ Filtered to {len(all_results)} gifts matching wanted combinations!\n")

    if all_results:
        # Group by gift name and model
        by_gift = {}
        for gift in all_results:
            gift_name = gift.get('name', 'Unknown')
            attrs = gift.get('attributes', [])
            model = next((a['value'] for a in attrs if a['type'] == 'model'), 'Unknown')

            key = f"{gift_name} - {model}"
            if key not in by_gift:
                by_gift[key] = []
            by_gift[key].append(gift)

        # Show summary by gift/model
        print("="*60)
        print(f"FOUND {len(all_results)} GIFTS")
        print("="*60)

        for key, gifts in sorted(by_gift.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"\n{key}: {len(gifts)} listings")

            # Sort by price
            gifts_sorted = sorted(gifts, key=lambda x: float(x.get('price', 999999)))
            cheapest = gifts_sorted[0]
            most_expensive = gifts_sorted[-1]

            print(f"  💰 Price range: {cheapest.get('price')} - {most_expensive.get('price')} TON")
            print(f"  📊 Floor: {cheapest.get('floor_price')} TON")
            print(f"  🔗 Cheapest: https://portals.tg/gift/{cheapest.get('id')}")

        # Show top 20 cheapest overall
        print("\n" + "="*60)
        print("TOP 20 CHEAPEST GIFTS")
        print("="*60)

        all_sorted = sorted(all_results, key=lambda x: float(x.get('price', 999999)))

        for i, gift in enumerate(all_sorted[:20]):
            attrs = gift.get('attributes', [])
            model = next((a['value'] for a in attrs if a['type'] == 'model'), 'N/A')
            symbol = next((a['value'] for a in attrs if a['type'] == 'symbol'), 'N/A')
            backdrop = next((a['value'] for a in attrs if a['type'] == 'backdrop'), 'N/A')

            # Rarities
            model_rarity = next((a['rarity_per_mille']/10 for a in attrs if a['type'] == 'model'), 0)
            symbol_rarity = next((a['rarity_per_mille']/10 for a in attrs if a['type'] == 'symbol'), 0)
            backdrop_rarity = next((a['rarity_per_mille']/10 for a in attrs if a['type'] == 'backdrop'), 0)

            print(f"\n[{i+1}] {gift.get('name')} #{gift.get('external_collection_number')}")
            print(f"    💰 Price: {gift.get('price')} TON")
            print(f"    🎨 Model: {model} ({model_rarity:.1f}%)")
            print(f"    🔣 Symbol: {symbol} ({symbol_rarity:.1f}%)")
            print(f"    🖼️  Backdrop: {backdrop} ({backdrop_rarity:.1f}%)")
            print(f"    🔗 https://portals.tg/gift/{gift.get('id')}")

        # Overall statistics
        print("\n" + "="*60)
        print("OVERALL STATISTICS")
        print("="*60)

        prices = [float(g.get('price', 0)) for g in all_results]
        print(f"💰 Cheapest: {min(prices)} TON")
        print(f"💰 Most expensive: {max(prices)} TON")
        print(f"💰 Average: {sum(prices)/len(prices):.2f} TON")
        print(f"📊 Total listings: {len(all_results)}")
        print(f"🎁 Unique gift/model combinations: {len(by_gift)}")

    else:
        print("❌ No gifts found matching criteria")


if __name__ == "__main__":
    asyncio.run(search_gifts())
