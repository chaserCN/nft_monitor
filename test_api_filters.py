"""Test if API filters work or if we need client-side filtering."""
import asyncio
from dotenv import load_dotenv
from portals_auth import PortalsAuthManager

load_dotenv()


async def test_filters():
    """Test API filter parameters."""

    manager = PortalsAuthManager()
    token = await manager.get_token()

    import portalsmp

    print("="*60)
    print("TESTING API FILTER PARAMETERS")
    print("="*60)

    # Test 1: No filters
    print("\n[TEST 1] No filters (limit=5)")
    print("-"*60)
    results1 = portalsmp.search(authData=token, limit=5)
    print(f"Results: {len(results1)}")
    for r in results1:
        print(f"  - {r.get('name')}")

    # Test 2: With gift_name filter
    print("\n[TEST 2] With gift_name='Ionic dryer' (limit=5)")
    print("-"*60)
    results2 = portalsmp.search(authData=token, gift_name="Ionic dryer", limit=5)
    print(f"Results: {len(results2)}")
    for r in results2:
        print(f"  - {r.get('name')}")

    # Test 3: With model filter
    print("\n[TEST 3] With model='Love Burst' (limit=5)")
    print("-"*60)
    results3 = portalsmp.search(authData=token, model="Love Burst", limit=5)
    print(f"Results: {len(results3)}")
    for r in results3:
        print(f"  - {r.get('name')}")

    # Compare results
    print("\n" + "="*60)
    print("COMPARISON")
    print("="*60)

    ids1 = [r.get('id') for r in results1]
    ids2 = [r.get('id') for r in results2]
    ids3 = [r.get('id') for r in results3]

    print(f"\nTest 1 (no filter) IDs: {ids1}")
    print(f"Test 2 (gift_name) IDs: {ids2}")
    print(f"Test 3 (model) IDs:     {ids3}")

    if ids1 == ids2 == ids3:
        print("\n⚠️  ALL RESULTS ARE IDENTICAL!")
        print("API filters DON'T WORK - need client-side filtering")
    else:
        print("\n✓ Results differ - API filters work!")
        print("Can use API filtering")

    print("\n" + "="*60)
    print("CONCLUSION")
    print("="*60)
    print("""
If results are identical, it means:
- API ignores gift_name, model parameters
- We MUST filter on client side
- Use search(limit=100) and filter by name/attributes

If results differ, it means:
- API filters work
- We can use gift_name and model parameters
    """)


if __name__ == "__main__":
    asyncio.run(test_filters())
