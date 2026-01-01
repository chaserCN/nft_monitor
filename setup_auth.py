"""Interactive setup for Telegram authentication."""
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()


async def setup_authentication():
    """Setup Telegram authentication interactively."""
    print("="*60)
    print("SETTING UP AUTOMATIC AUTHENTICATION")
    print("="*60)

    api_id = os.getenv("TELEGRAM_API_ID")
    api_hash = os.getenv("TELEGRAM_API_HASH")

    if not api_id or not api_hash:
        print("\n✗ TELEGRAM_API_ID and TELEGRAM_API_HASH not found in .env")
        print("\nPlease add them to .env file:")
        print("TELEGRAM_API_ID=your_api_id")
        print("TELEGRAM_API_HASH=your_api_hash")
        return False

    print(f"\n✓ Found credentials in .env")
    print(f"  API_ID: {api_id}")
    print(f"  API_HASH: {api_hash[:10]}...")

    print("\n" + "="*60)
    print("FIRST TIME SETUP")
    print("="*60)
    print("\nYou'll be asked for:")
    print("1. Your phone number (with country code, e.g., +1234567890)")
    print("2. Verification code from Telegram")
    print("3. (Optional) 2FA password if enabled")
    print("\nThis data will be saved in 'account.session' file.")
    print("Future runs won't need this - token will auto-refresh!")
    print("\n" + "="*60)

    try:
        from portalsmp import update_auth

        print("\nGenerating authentication token...")
        print("(You'll be prompted for phone and code)\n")

        token = await update_auth(
            api_id=int(api_id),
            api_hash=api_hash
        )

        print("\n" + "="*60)
        print("✓ AUTHENTICATION SUCCESSFUL!")
        print("="*60)
        print(f"\nToken length: {len(token)} characters")
        print(f"Token preview: {token[:50]}...")

        # Save to .env for future use
        print("\nSaving token to .env for manual fallback...")

        # Read existing .env
        env_path = "/Users/yarohort/Projects/nft_monitor/.env"
        with open(env_path, 'r') as f:
            lines = f.readlines()

        # Update or add PORTALS_AUTH_DATA
        found = False
        for i, line in enumerate(lines):
            if line.startswith('PORTALS_AUTH_DATA='):
                lines[i] = f'PORTALS_AUTH_DATA={token}\n'
                found = True
                break

        if not found:
            lines.append(f'\nPORTALS_AUTH_DATA={token}\n')

        # Write back
        with open(env_path, 'w') as f:
            f.writelines(lines)

        print("✓ Token saved to .env")

        print("\n" + "="*60)
        print("SETUP COMPLETE!")
        print("="*60)
        print("\nYou can now:")
        print("1. Run: python3 search_ionic_dryer_auto.py")
        print("2. Run: python3 main.py (to start monitoring)")
        print("\nToken will auto-refresh every 5 days. No more manual work!")

        return True

    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nPossible issues:")
        print("- Wrong phone number format (use +countrycode + number)")
        print("- Wrong verification code")
        print("- Network issues")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function."""
    asyncio.run(setup_authentication())


if __name__ == "__main__":
    main()
