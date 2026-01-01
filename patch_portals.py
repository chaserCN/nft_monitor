"""Patch portalsmp to use correct domain."""
import sys
import os

def patch_portalsmp():
    """Replace portals-market.com with portals.tg in portalsmp."""
    try:
        import portalsmp
        import inspect

        # Find portalsmp installation directory
        portalsmp_file = inspect.getsourcefile(portalsmp)
        portalsmp_dir = os.path.dirname(portalsmp_file)
        portalsapi_file = os.path.join(portalsmp_dir, 'portalsapi.py')

        if not os.path.exists(portalsapi_file):
            print(f"❌ File not found: {portalsapi_file}")
            return False

        # Read file
        with open(portalsapi_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check if already patched
        if 'portals-market.com' not in content:
            print("✓ portalsmp already patched or using correct domain")
            return True

        # Replace domain
        new_content = content.replace('portals-market.com', 'portals.tg')

        # Write back
        with open(portalsapi_file, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"✓ Successfully patched {portalsapi_file}")
        print("  portals-market.com → portals.tg")
        return True

    except ImportError:
        print("❌ portalsmp not installed")
        return False
    except Exception as e:
        print(f"❌ Error patching portalsmp: {e}")
        return False

if __name__ == "__main__":
    success = patch_portalsmp()
    sys.exit(0 if success else 1)
