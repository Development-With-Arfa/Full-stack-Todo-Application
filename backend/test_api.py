"""
Basic API tests for authentication and task isolation
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_test(name, passed, details=""):
    status = f"{Colors.GREEN}[PASS]{Colors.END}" if passed else f"{Colors.RED}[FAIL]{Colors.END}"
    print(f"{status} - {name}")
    if details:
        print(f"  {details}")

def test_backend_health():
    """Test 1: Backend server is running"""
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        passed = response.status_code == 200
        print_test("Backend Health Check", passed, f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test("Backend Health Check", False, f"Error: {str(e)}")
        return False

def test_frontend_health():
    """Test 2: Frontend server is running"""
    try:
        response = requests.get(FRONTEND_URL, timeout=5)
        passed = response.status_code == 200
        print_test("Frontend Health Check", passed, f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test("Frontend Health Check", False, f"Error: {str(e)}")
        return False

def test_jwks_endpoint():
    """Test 3: JWKS endpoint is accessible"""
    try:
        response = requests.get(f"{FRONTEND_URL}/api/auth/jwks", timeout=5)
        passed = response.status_code == 200
        if passed:
            data = response.json()
            passed = "keys" in data
        print_test("JWKS Endpoint", passed, f"Status: {response.status_code}")
        return passed
    except Exception as e:
        print_test("JWKS Endpoint", False, f"Error: {str(e)}")
        return False

def test_tasks_without_auth():
    """Test 4: Tasks endpoint requires authentication"""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/tasks", timeout=5)
        passed = response.status_code == 401
        print_test("Tasks Require Auth", passed, f"Status: {response.status_code} (expected 401)")
        return passed
    except Exception as e:
        print_test("Tasks Require Auth", False, f"Error: {str(e)}")
        return False

def test_user_registration():
    """Test 5: User registration works"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        email = f"testuser{timestamp}@example.com"
        
        response = requests.post(
            f"{FRONTEND_URL}/api/auth/sign-up/email",
            json={
                "email": email,
                "password": "TestPass123",
                "name": "Test User"
            },
            timeout=5
        )
        
        passed = response.status_code in [200, 201]
        details = f"Status: {response.status_code}, Email: {email}"
        if not passed and response.status_code != 200:
            details += f", Response: {response.text[:100]}"
        
        print_test("User Registration", passed, details)
        return passed, email if passed else None
    except Exception as e:
        print_test("User Registration", False, f"Error: {str(e)}")
        return False, None

def test_duplicate_registration(email):
    """Test 6: Duplicate email registration fails"""
    try:
        response = requests.post(
            f"{FRONTEND_URL}/api/auth/sign-up/email",
            json={
                "email": email,
                "password": "TestPass123",
                "name": "Test User"
            },
            timeout=5
        )
        
        passed = response.status_code in [400, 409, 422]
        print_test("Duplicate Email Rejected", passed, f"Status: {response.status_code} (expected 4xx)")
        return passed
    except Exception as e:
        print_test("Duplicate Email Rejected", False, f"Error: {str(e)}")
        return False

def test_weak_password():
    """Test 7: Weak password validation"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        response = requests.post(
            f"{FRONTEND_URL}/api/auth/sign-up/email",
            json={
                "email": f"weak{timestamp}@example.com",
                "password": "weak",
                "name": "Test User"
            },
            timeout=5
        )
        
        passed = response.status_code in [400, 422]
        print_test("Weak Password Rejected", passed, f"Status: {response.status_code} (expected 4xx)")
        return passed
    except Exception as e:
        print_test("Weak Password Rejected", False, f"Error: {str(e)}")
        return False

def run_tests():
    """Run all tests"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}Running API Tests for Todo App Authentication{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    results = []
    
    # Test 1-4: Basic connectivity
    print(f"{Colors.YELLOW}Phase 1: Server Health Checks{Colors.END}")
    results.append(test_backend_health())
    results.append(test_frontend_health())
    results.append(test_jwks_endpoint())
    results.append(test_tasks_without_auth())
    
    # Test 5-7: Authentication
    print(f"\n{Colors.YELLOW}Phase 2: Authentication Tests{Colors.END}")
    reg_passed, test_email = test_user_registration()
    results.append(reg_passed)
    
    if test_email:
        results.append(test_duplicate_registration(test_email))
    else:
        print_test("Duplicate Email Rejected", False, "Skipped - registration failed")
        results.append(False)
    
    results.append(test_weak_password())
    
    # Summary
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    passed = sum(results)
    total = len(results)
    percentage = (passed / total * 100) if total > 0 else 0
    
    if percentage == 100:
        color = Colors.GREEN
    elif percentage >= 70:
        color = Colors.YELLOW
    else:
        color = Colors.RED
    
    print(f"{color}Test Results: {passed}/{total} passed ({percentage:.1f}%){Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")
    
    return passed == total

if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
