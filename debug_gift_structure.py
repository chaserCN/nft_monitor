"""Debug script to see full gift data structure."""
import asyncio
import json
from dotenv import load_dotenv
from portals_auth import PortalsAuthManager

load_dotenv()


async def debug_gift_structure():
    """Show full structure of a gift object."""
    print("="*60)
    print("DEBUGGING GIFT DATA STRUCTURE")
    print("="*60)

    # Get auth token
    manager = PortalsAuthManager()
    token = await manager.get_token()

    import portalsmp

    # Search for Ionic dryer
    print("\nSearching for Ionic dryer...")
    results = portalsmp.search(
        authData=token,
        gift_name="Ionic dryer",
        limit=3,
        sort="price_asc"
    )

    if results:
        print(f"\n✓ Found {len(results)} results\n")

        for i, gift in enumerate(results):
            print("="*60)
            print(f"GIFT #{i+1}")
            print("="*60)
            print(json.dumps(gift, indent=2, ensure_ascii=False))
            print()

            # Show all top-level keys
            print("Top-level keys:")
            for key in gift.keys():
                print(f"  - {key}: {type(gift[key]).__name__}")
            print()

    else:
        print("No results found")


if __name__ == "__main__":
    asyncio.run(debug_gift_structure())
