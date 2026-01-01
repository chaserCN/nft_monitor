"""Test script to check NFT marketplace APIs."""
import requests
import json
import sys
from typing import Optional


def test_portals_api_direct():
    """Test Portals API with direct HTTP requests (requires auth)."""
    print("\n" + "="*60)
    print("Testing Portals API (Direct - requires authentication)")
    print("="*60)

    # Note: These endpoints require authentication
    # You need to get authData from web.telegram.org as described in docs

    base_url = "https://portals-market.com/api"

    # Test endpoints without auth (will likely fail, but shows what's needed)
    endpoints_to_test = [
        "/v1/gifts",
        "/gifts",
        "/collections",
        "/floor-prices",
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "application/json",
    }

    for endpoint in endpoints_to_test:
        url = f"{base_url}{endpoint}"
        try:
            print(f"\nTrying: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"Success! Response type: {type(data)}")
                    if isinstance(data, list) and len(data) > 0:
                        print(f"First item keys: {data[0].keys()}")
                    elif isinstance(data, dict):
                        print(f"Response keys: {data.keys()}")
                except Exception as e:
                    print(f"Response text (first 200 chars): {response.text[:200]}")
            else:
                print(f"Response: {response.text[:200]}")

        except Exception as e:
            print(f"Error: {e}")


def test_portals_with_library():
    """Test using portalsmp library."""
    print("\n" + "="*60)
    print("Testing Portals API with portalsmp library")
    print("="*60)

    try:
        import portalsmp
        print("✓ portalsmp library is installed")

        # This will fail without authData, but shows the pattern
        print("\nNote: To use this library, you need to:")
        print("1. Go to web.telegram.org")
        print("2. Open @portals bot mini app")
        print("3. Open DevTools → Network")
        print("4. Find 'Authorization' header in requests to portals-market.com")
        print("5. Copy the entire header value")
        print("\nThen use: portalsmp.search(authData='tma <your_token>')")

    except ImportError:
        print("✗ portalsmp library not installed")
        print("Install with: pip install portalsmp")


def test_fragment_api():
    """Test Fragment marketplace (official Telegram marketplace)."""
    print("\n" + "="*60)
    print("Testing Fragment API")
    print("="*60)

    # Fragment GraphQL endpoint
    url = "https://fragment.com/api"

    # Try to get gifts data
    query = """
    {
      gifts {
        id
        name
        price
        available
      }
    }
    """

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    try:
        print(f"\nTrying GraphQL: {url}")
        response = requests.post(
            url,
            json={"query": query},
            headers=headers,
            timeout=10
        )
        print(f"Status: {response.status_code}")
        print(f"Response (first 500 chars): {response.text[:500]}")

    except Exception as e:
        print(f"Error: {e}")


def test_getgems_api():
    """Test Getgems marketplace API."""
    print("\n" + "="*60)
    print("Testing Getgems API")
    print("="*60)

    base_url = "https://api.getgems.io"

    # Test different endpoints
    endpoints = [
        "/nft/items?collection_address=&sale_type=fix_price&sort=price_asc",
        "/collections",
        "/search?q=gift",
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "application/json",
    }

    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        try:
            print(f"\nTrying: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"Success! Response type: {type(data)}")
                    if isinstance(data, dict):
                        print(f"Response keys: {list(data.keys())[:10]}")
                except:
                    print(f"Response text (first 200 chars): {response.text[:200]}")
            else:
                print(f"Response: {response.text[:200]}")

        except Exception as e:
            print(f"Error: {e}")


def test_tonnel_api():
    """Test Tonnel marketplace API."""
    print("\n" + "="*60)
    print("Testing Tonnel API")
    print("="*60)

    # Try to find actual Tonnel API endpoints
    possible_urls = [
        "https://tonnel.network/api/gifts",
        "https://api.tonnel.network/gifts",
        "https://tonnel.network/api/v1/gifts",
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "application/json",
    }

    for url in possible_urls:
        try:
            print(f"\nTrying: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            print(f"Status: {response.status_code}")
            print(f"Response (first 200 chars): {response.text[:200]}")

        except Exception as e:
            print(f"Error: {e}")


def get_auth_instructions():
    """Print instructions for getting authentication."""
    print("\n" + "="*60)
    print("HOW TO GET AUTHENTICATION FOR PORTALS")
    print("="*60)
    print("""
1. Open web.telegram.org in your browser
2. Login to your Telegram account
3. Search for @portals bot
4. Open the Portals mini app
5. Open Browser DevTools (F12 or Cmd+Option+I on Mac)
6. Go to Network tab
7. Filter by 'portals-market.com'
8. Click around in the app to trigger API requests
9. Click on any request to portals-market.com
10. Look for 'Authorization' header in Request Headers
11. Copy the entire value (starts with 'tma ')
12. Save it to .env file as PORTALS_AUTH_DATA

Example:
PORTALS_AUTH_DATA=tma eyJhbGc...very.long.token...here

Then the bot will be able to fetch real prices!
    """)


def main():
    """Run all API tests."""
    print("NFT Marketplace API Testing")
    print("This script tests various NFT gift marketplace APIs")

    # Run tests
    test_portals_api_direct()
    test_portals_with_library()
    test_fragment_api()
    test_getgems_api()
    test_tonnel_api()

    # Show instructions
    get_auth_instructions()

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print("""
Based on research, the best approach is:

1. **Portals Marketplace** - Most popular, requires authentication
   - Use portalsmp library: pip install portalsmp
   - Get authData from web.telegram.org (see instructions above)
   - Can search, filter by price, get floor prices

2. **Alternative**: Use Telegram Bot API
   - More complex, requires running Telegram client
   - Can access official gift data

3. **Fragment/Getgems** - May have public APIs for some data
   - Need to investigate further

RECOMMENDED: Get Portals authData and use portalsmp library.
    """)


if __name__ == "__main__":
    main()
