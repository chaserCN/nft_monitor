"""Test ton-fragment library."""
import sys


def test_fragment_gifts():
    """Test getting gifts from Fragment using ton-fragment library."""
    print("="*60)
    print("Testing ton-fragment Library")
    print("="*60)

    try:
        from fragment import Gift
        print("✓ ton-fragment library imported successfully\n")

        # Try to get available gifts
        print("Fetching available gifts from Fragment...")
        print("-" * 60)

        gift_client = Gift()

        # Get gifts
        try:
            gifts = gift_client.get_available_gifts()

            if gifts:
                print(f"✓ Found {len(gifts)} gifts!\n")

                # Show first few gifts
                for i, gift in enumerate(gifts[:10]):
                    print(f"{i+1}. Gift:")

                    # Different libraries might have different attribute names
                    # Try to get all available info
                    if hasattr(gift, '__dict__'):
                        for key, value in gift.__dict__.items():
                            if value and key not in ['_', '__']:
                                print(f"   {key}: {value}")
                    else:
                        print(f"   {gift}")

                    print()

                print("\n🎉 SUCCESS! Fragment API works!")
                return True

            else:
                print("No gifts found")
                return False

        except AttributeError as e:
            print(f"✗ Method error: {e}")
            print("\nAvailable methods:")
            for method in dir(gift_client):
                if not method.startswith('_'):
                    print(f"  - {method}")

        except Exception as e:
            print(f"✗ Error getting gifts: {e}")
            print(f"Error type: {type(e).__name__}")

            # Try alternative methods
            print("\nTrying alternative methods...")

            alt_methods = [
                'get_gifts',
                'gifts',
                'list_gifts',
                'search_gifts',
            ]

            for method_name in alt_methods:
                if hasattr(gift_client, method_name):
                    print(f"\nTrying: {method_name}()")
                    try:
                        method = getattr(gift_client, method_name)
                        result = method()
                        print(f"✓ {method_name}() works!")
                        print(f"Result: {result}")
                        return True
                    except Exception as e2:
                        print(f"  Error: {e2}")

    except ImportError as e:
        print(f"✗ Failed to import fragment library: {e}")
        return False

    return False


def test_fragment_stars():
    """Test getting Stars data from Fragment."""
    print("\n" + "="*60)
    print("Testing Fragment Stars")
    print("="*60)

    try:
        from fragment import Star

        print("✓ Star class imported\n")

        star_client = Star()

        # Try to get Stars data
        methods_to_try = [
            'get_available_stars',
            'get_stars',
            'list',
        ]

        for method_name in methods_to_try:
            if hasattr(star_client, method_name):
                print(f"Trying: {method_name}()")
                try:
                    method = getattr(star_client, method_name)
                    result = method()
                    print(f"✓ Success!")
                    print(f"Result: {result}")
                    break
                except Exception as e:
                    print(f"  Error: {e}")

    except ImportError:
        print("Star class not available in this version")
    except Exception as e:
        print(f"Error: {e}")


def test_fragment_nft_search():
    """Test searching for specific NFTs."""
    print("\n" + "="*60)
    print("Testing NFT Search")
    print("="*60)

    try:
        from fragment import Gift

        gift_client = Gift()

        search_terms = ["delicious", "cake", "star"]

        for term in search_terms:
            print(f"\nSearching for: '{term}'")

            # Try different search methods
            if hasattr(gift_client, 'search'):
                try:
                    results = gift_client.search(term)
                    print(f"✓ Found {len(results) if results else 0} results")
                    if results:
                        print(f"First result: {results[0]}")
                except Exception as e:
                    print(f"  Error: {e}")

    except Exception as e:
        print(f"Error: {e}")


def main():
    """Run all tests."""
    print("\n🎁 Testing Fragment Library for Telegram Gifts\n")

    success = test_fragment_gifts()

    if not success:
        print("\n" + "="*60)
        print("ALTERNATIVE APPROACH NEEDED")
        print("="*60)
        print("""
Fragment library может не работать или иметь другой API.

Альтернативы:
1. Reverse engineer Fragment website
   - Открыть https://fragment.com/gifts
   - DevTools → Network
   - Посмотреть реальные API запросы
   - Воспроизвести их

2. Использовать Portals с auto-refresh токена
   - Библиотека portalsmp поддерживает programmatic auth
   - Нужны api_id и api_hash от Telegram
   - Получить на https://my.telegram.org/auth

3. Веб-скрейпинг Fragment/GetGems
   - Использовать Selenium/Playwright
   - Парсить страницы маркетплейсов
   - Медленнее, но работает всегда
        """)
    else:
        test_fragment_stars()
        test_fragment_nft_search()

        print("\n" + "="*60)
        print("✓ TESTS COMPLETED")
        print("="*60)


if __name__ == "__main__":
    main()
