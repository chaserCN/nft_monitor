"""Test TonAPI for getting NFT gift data."""
import requests
import json
from typing import Optional


def test_tonapi_nft_collections():
    """Test getting NFT collections from TonAPI."""
    print("="*60)
    print("Testing TonAPI - NFT Collections")
    print("="*60)

    base_url = "https://tonapi.io/v2"

    # Known Telegram Gifts collection address (example)
    # This is a placeholder - need to find actual gift collection addresses

    endpoints_to_try = [
        "/nft/collections",
        "/nft/searchItems?include_on_sale=true",
        "/accounts/-/nfts",
    ]

    headers = {
        "Accept": "application/json",
    }

    for endpoint in endpoints_to_try:
        url = f"{base_url}{endpoint}"
        print(f"\nTrying: {url}")

        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"Success! Keys: {list(data.keys()) if isinstance(data, dict) else 'list'}")
                print(f"Response preview: {json.dumps(data, indent=2)[:500]}")
            else:
                print(f"Error: {response.text[:200]}")

        except Exception as e:
            print(f"Error: {e}")


def test_tonapi_with_key(api_key: Optional[str] = None):
    """Test TonAPI with optional API key."""
    print("\n" + "="*60)
    print("Testing TonAPI with Authentication")
    print("="*60)

    if not api_key:
        print("⚠️  No API key provided")
        print("TonAPI Free tier: 1 request per second")
        print("Get API key at: https://tonconsole.com")
        print("\nTrying without API key...")

    base_url = "https://tonapi.io/v2"

    headers = {
        "Accept": "application/json",
    }

    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    # Try to search for gifts
    print(f"\nSearching for NFT items...")

    try:
        # Get trending collections
        url = f"{base_url}/nft/collections"
        response = requests.get(url, headers=headers, timeout=10, params={"limit": 10})

        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            collections = data.get('nft_collections', [])

            print(f"\n✓ Found {len(collections)} collections")

            for i, coll in enumerate(collections[:5]):
                name = coll.get('metadata', {}).get('name', 'Unknown')
                print(f"  {i+1}. {name}")

        elif response.status_code == 429:
            print("⚠️  Rate limit exceeded")
            print("Consider getting an API key for higher limits")
        else:
            print(f"Error: {response.text[:200]}")

    except Exception as e:
        print(f"Error: {e}")


def search_telegram_gifts_collection():
    """Try to find Telegram Gifts NFT collection."""
    print("\n" + "="*60)
    print("Searching for Telegram Gifts Collection")
    print("="*60)

    base_url = "https://tonapi.io/v2"

    # Telegram Gifts might be here - need to find the collection address
    # Let's try to search

    search_terms = ["telegram gift", "gift", "collectible"]

    for term in search_terms:
        print(f"\nSearching for: '{term}'")

        try:
            # Try different endpoints
            url = f"{base_url}/nft/searchItems"
            params = {
                "q": term,
                "limit": 10,
                "include_on_sale": True
            }

            response = requests.get(url, params=params, timeout=10)
            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                items = data.get('nft_items', [])

                if items:
                    print(f"✓ Found {len(items)} items")
                    for item in items[:3]:
                        metadata = item.get('metadata', {})
                        name = metadata.get('name', 'Unknown')
                        print(f"  - {name}")
                else:
                    print("  No items found")

            elif response.status_code == 404:
                print("  Endpoint not available")
            else:
                print(f"  Error: {response.text[:100]}")

        except Exception as e:
            print(f"  Error: {e}")


def check_getgems_api():
    """Check if GetGems has a public API."""
    print("\n" + "="*60)
    print("Testing GetGems API")
    print("="*60)

    # GetGems uses TonAPI backend, but might have own endpoints
    possible_urls = [
        "https://api.getgems.io/graphql",
        "https://getgems.io/api/nfts",
        "https://getgems.io/api/collections",
    ]

    for url in possible_urls:
        print(f"\nTrying: {url}")

        try:
            response = requests.get(url, timeout=10)
            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                print(f"✓ Success! Content type: {response.headers.get('content-type')}")
                print(f"Preview: {response.text[:200]}")
            else:
                print(f"Response: {response.text[:100]}")

        except Exception as e:
            print(f"Error: {e}")


def main():
    """Run all tests."""
    print("\n🔍 Testing Public TON NFT APIs\n")

    test_tonapi_nft_collections()
    test_tonapi_with_key()
    search_telegram_gifts_collection()
    check_getgems_api()

    print("\n" + "="*60)
    print("RECOMMENDATIONS")
    print("="*60)
    print("""
1. TonAPI (tonapi.io)
   - ✓ Public API available
   - ✓ Free tier: 1 req/sec (достаточно для мониторинга)
   - ✓ NFT endpoints available
   - ⚠️ Нужно найти адрес коллекции Telegram Gifts
   - 💡 Регистрация: https://tonconsole.com

2. GetGems
   - Использует TonAPI под капотом
   - Может иметь свои эндпоинты (нужно исследовать)

3. Alternative: Web Scraping
   - GetGems имеет веб-интерфейс
   - Можно парсить HTML (но менее надёжно)

4. Alternative: TON Blockchain напрямую
   - Читать данные из блокчейна TON
   - Требует знание смарт-контрактов

NEXT STEP: Нужно найти адрес коллекции Telegram Gifts в TON
    """)


if __name__ == "__main__":
    main()
