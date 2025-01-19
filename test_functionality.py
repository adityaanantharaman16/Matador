import requests
import json
from datetime import datetime

def test_app():
    BASE_URL = "http://127.0.0.1:8000"

    def print_test(name, response):
        print(f"\n=== Testing {name} ===")
        print(f"Status: {response.status_code}")
        try:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Raw response: {response.text}")
        print("=" * 50)

    # 1. Test health endpoint
    print("\nTesting connection...")
    health = requests.get(f"{BASE_URL}/health")
    print_test("Health Check", health)

    # 2. Test user creation
    print("\nCreating test user...")
    user_response = requests.post(f"{BASE_URL}/test/user")
    print_test("User Creation", user_response)

    # 3. Test user retrieval
    print("\nGetting all users...")
    users_response = requests.get(f"{BASE_URL}/test/users")
    print_test("User Retrieval", users_response)

if __name__ == "__main__":
    try:
        test_app()
        print("\nTests completed!")
    except Exception as e:
        print(f"\nError during testing: {str(e)}")