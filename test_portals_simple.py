"""Simple test to check Portals API with portalsmp library."""
import os
import sys
from dotenv import load_dotenv

load_dotenv()


def test_portals_with_auth():
    """Test Portals API with authentication."""
    print("="*60)
    print("Testing Portals Marketplace API")
    print("="*60)

    # Check if library is available
    try:
        import portalsmp
        print("✓ portalsmp library is installed\n")
    except ImportError:
        print("✗ portalsmp library not installed")
        print("Install with: pip3 install portalsmp")
        return

    # Get auth data from environment
    auth_data = os.getenv("PORTALS_AUTH_DATA", "")

    if not auth_data:
        print("⚠️  PORTALS_AUTH_DATA not found in .env file\n")
        print("To get authentication data:")
        print("1. Open https://web.telegram.org in your browser")
        print("2. Login to Telegram")
        print("3. Search for @portals_market_bot")
        print("4. Open the Portals mini app")
        print("5. Open DevTools (F12 or Cmd+Option+I)")
        print("6. Go to Network tab")
        print("7. Click around in the app")
        print("8. Find requests to portalsmarket.co")
        print("9. Look for 'Authorization' header")
        print("10. Copy the value (starts with 'tma ')")
        print("\nAdd to your .env file:")
        print("PORTALS_AUTH_DATA=tma eyJhbGc...<your_token_here>")
        return

    print(f"✓ Found auth data (length: {len(auth_data)} chars)\n")

    # Try to get collections (simplest call)
    print("Testing API call: collections()")
    print("-" * 60)

    try:
        collections = portalsmp.collections(authData=auth_data)
        print(f"✓ Success! Got {len(collections)} collections\n")

        # Show first few collections
        print("Sample collections:")
        for i, coll in enumerate(collections[:5]):
            name = coll.get('name', 'N/A')
            floor = coll.get('floor_price', 0)
            volume = coll.get('volume', 0)
            print(f"  {i+1}. {name}")
            print(f"     Floor: {floor} TON")
            print(f"     Volume: {volume}")

        return True

    except Exception as e:
        print(f"✗ Error calling API: {e}")
        print(f"\nError type: {type(e).__name__}")
        print("\nPossible issues:")
        print("- Auth token expired (tokens expire in 1-7 days)")
        print("- Auth token format incorrect")
        print("- Network connectivity issues")
        print("\nTry getting a fresh auth token from web.telegram.org")
        return False


def test_search_gifts():
    """Test searching for specific gifts."""
    print("\n" + "="*60)
    print("Testing Gift Search")
    print("="*60)

    try:
        import portalsmp
    except ImportError:
        print("portalsmp not installed")
        return

    auth_data = os.getenv("PORTALS_AUTH_DATA", "")
    if not auth_data:
        print("PORTALS_AUTH_DATA not set")
        return

    # Try searching for a common gift
    search_terms = ["delicious", "cake", "green star", "blue star"]

    for term in search_terms:
        print(f"\nSearching for: '{term}'")
        print("-" * 60)

        try:
            results = portalsmp.search(
                authData=auth_data,
                name=term,
                limit=5,
                sort="price_asc"  # Sort by price ascending
            )

            if results:
                print(f"✓ Found {len(results)} results\n")
                for i, gift in enumerate(results[:3]):
                    name = gift.get('name', 'N/A')
                    price = gift.get('price', 0)
                    model = gift.get('model', {})
                    model_name = model.get('name', 'N/A') if isinstance(model, dict) else 'N/A'

                    print(f"  {i+1}. {name}")
                    print(f"     Model: {model_name}")
                    print(f"     Price: {price} TON")
                break  # Found results, stop searching
            else:
                print(f"  No results for '{term}'")

        except Exception as e:
            print(f"  Error: {e}")


def test_floor_prices():
    """Test getting floor prices."""
    print("\n" + "="*60)
    print("Testing Floor Prices")
    print("="*60)

    try:
        import portalsmp
    except ImportError:
        print("portalsmp not installed")
        return

    auth_data = os.getenv("PORTALS_AUTH_DATA", "")
    if not auth_data:
        print("PORTALS_AUTH_DATA not set")
        return

    try:
        floors = portalsmp.giftsFloors(authData=auth_data)
        print(f"✓ Got floor prices for {len(floors)} items\n")

        # Sort by floor price
        sorted_floors = sorted(floors, key=lambda x: x.get('floor_price', 0))

        print("Cheapest gifts (by floor price):")
        for i, item in enumerate(sorted_floors[:10]):
            name = item.get('name', 'N/A')
            floor = item.get('floor_price', 0)
            print(f"  {i+1}. {name}: {floor} TON")

    except Exception as e:
        print(f"✗ Error: {e}")


def main():
    """Main test function."""
    print("\n🎁 Portals Marketplace API Test\n")

    # Test basic connection
    success = test_portals_with_auth()

    if success:
        # If basic test worked, try more features
        test_search_gifts()
        test_floor_prices()

        print("\n" + "="*60)
        print("✓ ALL TESTS COMPLETED")
        print("="*60)
        print("\nThe API is working! You can now use it in the monitor bot.")
        print("\nNext steps:")
        print("1. Update marketplace_apis.py to use portalsmp")
        print("2. Configure your .env file with bot token and channel ID")
        print("3. Set the gift models you want to monitor")
        print("4. Run: python3 main.py")
    else:
        print("\n" + "="*60)
        print("⚠️  SETUP REQUIRED")
        print("="*60)
        print("\nPlease get authentication data to continue.")


if __name__ == "__main__":
    main()
