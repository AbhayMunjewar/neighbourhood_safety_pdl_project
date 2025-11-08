"""
Quick test script to verify Flask backend is working
Run: python test_backend.py
"""
import requests
import sys

def test_backend():
    """Test if backend is running and responding"""
    base_url = "http://localhost:3000"
    
    print("Testing Flask backend...")
    print("=" * 50)
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"✓ Root endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"  Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to backend!")
        print("  Make sure Flask is running: python app.py")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/api/health")
        print(f"✓ Health endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ Health endpoint error: {e}")
        return False
    
    print("=" * 50)
    print("✓ Backend is running correctly!")
    return True

if __name__ == "__main__":
    if not test_backend():
        sys.exit(1)

