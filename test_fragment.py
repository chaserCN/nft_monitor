"""Test Fragment API for Telegram Gifts."""
import requests
import json


def test_fragment_graphql():
    """Test Fragment GraphQL API."""
    print("="*60)
    print("Testing Fragment.com GraphQL API")
    print("="*60)

    url = "https://fragment.com/api"

    # Try different GraphQL queries for gifts
    queries = [
        # Query 1: Get gifts marketplace data
        {
            "name": "Gifts marketplace",
            "query": """
            query {
              gifts {
                id
                name
                price
                image
                available
              }
            }
            """
        },
        # Query 2: Get items (generic)
        {
            "name": "Items query",
            "query": """
            query {
              items {
                id
                title
                price
              }
            }
            """
        },
        # Query 3: Get collectibles
        {
            "name": "Collectibles query",
            "query": """
            query {
              collectibles(type: "gift") {
                id
                name
                price
              }
            }
            """
        },
    ]

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }

    for q in queries:
        print(f"\n[{q['name']}]")
        print(f"Query: {q['query'][:100]}...")

        try:
            response = requests.post(
                url,
                json={"query": q["query"]},
                headers=headers,
                timeout=10
            )

            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"✓ Success!")
                    print(f"Response: {json.dumps(data, indent=2)[:500]}")

                    # If we got data, this query works!
                    if data.get('data'):
                        print("\n🎉 THIS QUERY WORKS!")
                        return data

                except Exception as e:
                    print(f"JSON parse error: {e}")
                    print(f"Response text: {response.text[:200]}")
            else:
                print(f"Error response: {response.text[:200]}")

        except Exception as e:
            print(f"Request error: {e}")

    return None


def test_fragment_rest():
    """Test Fragment REST API endpoints."""
    print("\n" + "="*60)
    print("Testing Fragment.com REST API")
    print("="*60)

    base_url = "https://fragment.com"

    endpoints = [
        "/api/gifts",
        "/api/collectibles",
        "/api/items",
        "/api/marketplace/gifts",
        "/gifts",
    ]

    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }

    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        print(f"\nTrying: {url}")

        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"Status: {response.status_code}")

            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')

                if 'json' in content_type:
                    try:
                        data = response.json()
                        print(f"✓ JSON response!")
                        print(f"Data: {json.dumps(data, indent=2)[:300]}")
                    except:
                        print(f"Text: {response.text[:200]}")
                else:
                    print(f"Content-Type: {content_type}")
                    print(f"Response: {response.text[:200]}")
            else:
                print(f"Error: {response.text[:100]}")

        except Exception as e:
            print(f"Error: {e}")


def analyze_fragment_website():
    """Analyze Fragment website structure."""
    print("\n" + "="*60)
    print("Analyzing Fragment Website")
    print("="*60)

    url = "https://fragment.com"

    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            html = response.text

            # Look for API endpoints or data in the HTML
            if 'api' in html.lower():
                print("\n✓ Found 'api' mentions in HTML")

                # Extract potential API URLs
                import re
                api_urls = re.findall(r'["\']https?://[^"\']*api[^"\']*["\']', html)
                if api_urls:
                    print("Potential API URLs found:")
                    for api_url in api_urls[:5]:
                        print(f"  - {api_url}")

            # Look for embedded data
            if '__NEXT_DATA__' in html or 'window.__' in html:
                print("\n✓ Found embedded data in page (Next.js or similar)")
                print("This means data might be loaded dynamically")

    except Exception as e:
        print(f"Error: {e}")


def check_ton_fragment_library():
    """Check if ton-fragment library works."""
    print("\n" + "="*60)
    print("Checking ton-fragment Library")
    print("="*60)

    try:
        import fragment
        print("✓ fragment library is installed")

        # Try to use it
        print("\nNote: This library might need authentication")
        print("Install: pip install ton-fragment")

    except ImportError:
        print("✗ fragment library not installed")
        print("\nThere's a Python library for Fragment:")
        print("  GitHub: https://github.com/iw4p/Ton-Fragment")
        print("  Install: pip install ton-fragment")
        print("\n  Example usage:")
        print("    from fragment import Gift")
        print("    gifts = Gift().get_available_gifts()")


def main():
    """Run all Fragment tests."""
    print("\n🔍 Testing Fragment (Official Telegram NFT Marketplace)\n")

    test_fragment_graphql()
    test_fragment_rest()
    analyze_fragment_website()
    check_ton_fragment_library()

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print("""
Fragment.com является официальным маркетплейсом Telegram для NFT подарков.

Проблемы:
1. GraphQL API требует правильную схему запроса
2. REST API endpoints неизвестны
3. Сайт может использовать динамическую загрузку данных

Возможные решения:
1. Использовать библиотеку ton-fragment (Python)
   - GitHub: https://github.com/iw4p/Ton-Fragment
   - Может иметь готовые методы для работы с API

2. Reverse engineering Fragment website
   - Открыть DevTools → Network
   - Посмотреть какие запросы делает сайт
   - Воспроизвести их в коде

3. Использовать веб-скрейпинг
   - Парсить HTML страницы Fragment
   - Менее надёжно, но работает без API

4. Вернуться к Portals + сделать авто-обновление токена
   - Использовать pyrogram для автоматического получения токена
   - Токен будет обновляться программно

Рекомендация: Попробовать библиотеку ton-fragment
    """)


if __name__ == "__main__":
    main()
