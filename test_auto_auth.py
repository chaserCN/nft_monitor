"""Test automatic authentication system."""
import os
from dotenv import load_dotenv
from portals_auth import PortalsAuthManager

load_dotenv()


def main():
    """Test authentication manager."""
    print("\n" + "="*60)
    print("TESTING AUTOMATIC AUTHENTICATION SYSTEM")
    print("="*60)

    # Create auth manager
    manager = PortalsAuthManager()

    # Print current status
    manager.print_status()

    # Try to get a token
    print("\n" + "="*60)
    print("ATTEMPTING TO GET TOKEN")
    print("="*60)

    try:
        import asyncio
        token = asyncio.run(manager.get_token())

        print("\n✓ SUCCESS! Got authentication token")
        print(f"Token length: {len(token)} characters")
        print(f"Token preview: {token[:50]}...")

        # Test with portalsmp
        print("\n" + "="*60)
        print("TESTING TOKEN WITH PORTALS API")
        print("="*60)

        try:
            import portalsmp

            print("\nFetching collections...")
            collections = portalsmp.collections(authData=token)

            print(f"\n✓ SUCCESS! Got {len(collections)} collections")

            # Show first few
            print("\nFirst 5 collections:")
            for i, coll in enumerate(collections[:5]):
                name = coll.get('name', 'Unknown')
                floor = coll.get('floor_price', 0)
                print(f"  {i+1}. {name}: {floor} TON")

            print("\n" + "="*60)
            print("🎉 AUTHENTICATION SYSTEM WORKS PERFECTLY!")
            print("="*60)
            print("\nYour bot is ready to monitor NFT gifts!")

        except ImportError:
            print("⚠️  portalsmp not installed")
            print("Install with: pip install portalsmp")

        except Exception as e:
            print(f"\n✗ API call failed: {e}")
            print("\nPossible issues:")
            print("- Token might be invalid")
            print("- API might be down")
            print("- Network connectivity issue")

    except ValueError as e:
        print(f"\n✗ Authentication not configured")
        print(f"\nError: {e}")

        print("\n" + "="*60)
        print("SETUP INSTRUCTIONS")
        print("="*60)
        print("""
You have two options to configure authentication:

OPTION 1: Automatic (Recommended)
  1. Go to https://my.telegram.org/auth
  2. Login with your phone number
  3. Go to "API development tools"
  4. Create an application (any name)
  5. Copy api_id and api_hash
  6. Add to .env file:
     TELEGRAM_API_ID=your_api_id
     TELEGRAM_API_HASH=your_api_hash
  7. Run this script again
  8. On first run, enter your phone and SMS code
  9. Done! Token will auto-refresh every 5 days

OPTION 2: Manual
  1. Follow instructions in GET_AUTH_TOKEN.md
  2. Add to .env file:
     PORTALS_AUTH_DATA=tma <your_token>
  3. Token expires in 1-7 days (need to repeat)

See AUTHENTICATION_EXPLAINED.md for more details.
        """)

    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
