"""Encode session file to base64 for Railway deployment."""
import base64
import sys

def encode_session(session_path='account.session'):
    """Encode session file to base64."""
    try:
        with open(session_path, 'rb') as f:
            session_data = f.read()

        base64_encoded = base64.b64encode(session_data).decode('utf-8')

        print("Session file encoded successfully!")
        print("\nAdd this to Railway environment variables:")
        print(f"TELEGRAM_SESSION_BASE64={base64_encoded}")

        return base64_encoded
    except FileNotFoundError:
        print(f"❌ File not found: {session_path}")
        print("Please run the bot locally first to create account.session")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    encode_session()
