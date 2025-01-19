# test_connection.py
import requests
import json

def test_database_connection():
    # Base URL of your FastAPI application
    base_url = "http://localhost:8000"

    # Test creating a user
    print("Creating test user...")
    create_response = requests.post(f"{base_url}/test/user")
    print(f"Create user response: {create_response.json()}\n")

    # Test getting all users
    print("Getting all users...")
    get_response = requests.get(f"{base_url}/test/users")
    print(f"Get users response: {json.dumps(get_response.json(), indent=2)}")

if __name__ == "__main__":
    test_database_connection()