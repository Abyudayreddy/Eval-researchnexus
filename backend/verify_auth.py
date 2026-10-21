import requests
import sys

BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api"

def print_result(name, passed):
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{name.ljust(30)}: {status}")

def run_tests():
    print("Running Backend Verification Tests...\n")
    
    # 1. /health
    try:
        r = requests.get(f"{BASE_URL}/health")
        print_result("/health", r.status_code == 200 and r.json().get("status") == "ok")
    except:
        print_result("/health", False)
        print("Backend server is not running on localhost:8000. Start it first!")
        return

    # 2. Registration
    import random
    test_email = f"testuser_{random.randint(1000, 9999)}@example.com"
    payload = {
        "email": test_email,
        "password": "SecurePassword123!",
        "name": "Test User"
    }
    
    r_reg = requests.post(f"{API_URL}/auth/register", json=payload)
    reg_success = r_reg.status_code == 200 and "access_token" in r_reg.json()
    print_result("Registration", reg_success)
    
    if reg_success:
        # Check no password in response
        no_pwd = "password" not in r_reg.json() and "hashed_password" not in r_reg.json()
        print_result("No password in response", no_pwd)
        
    # 3. Duplicate email handling
    r_dup = requests.post(f"{API_URL}/auth/register", json=payload)
    print_result("Duplicate email handling", r_dup.status_code == 400)
    
    # 4. Login
    login_payload = {
        "username": test_email,
        "password": "SecurePassword123!"
    }
    r_login = requests.post(f"{API_URL}/auth/login", data=login_payload)
    login_success = r_login.status_code == 200 and "access_token" in r_login.json()
    print_result("Login & JWT generation", login_success)
    
    # 5. /api/auth/me (Protected Route)
    if login_success:
        token = r_login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        r_me = requests.get(f"{API_URL}/auth/me", headers=headers)
        me_success = r_me.status_code == 200 and r_me.json().get("email") == test_email
        print_result("/api/auth/me (JWT validation)", me_success)
    else:
        print_result("/api/auth/me (JWT validation)", False)
        
    # 6. Unauthorized request rejection
    r_unauth = requests.get(f"{API_URL}/auth/me")
    print_result("Unauthorized request rejection", r_unauth.status_code == 401)
    
    print("\nNext: Open the React frontend to test CORS, Frontend Registration, Login, and Logout.")

if __name__ == "__main__":
    run_tests()
