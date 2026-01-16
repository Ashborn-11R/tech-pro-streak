import requests
import json
from datetime import datetime

BASE_URL = 'http://127.0.0.1:8000/api'

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.END}")

def print_section(msg):
    print(f"\n{Colors.YELLOW}{'='*60}{Colors.END}")
    print(f"{Colors.YELLOW}{msg}{Colors.END}")
    print(f"{Colors.YELLOW}{'='*60}{Colors.END}")

# Store tokens globally
access_token = None
refresh_token = None
headers = {}

def test_register():
    """Test user registration"""
    print_section("TEST 1: User Registration")
    
    global access_token, refresh_token, headers
    
    username = f'testuser_{int(datetime.now().timestamp())}'
    
    data = {
        'username': username,
        'email': f'{username}@test.com',
        'password': 'SecurePass123!',
        'password2': 'SecurePass123!',
        'timezone': 'America/New_York'
    }
    
    response = requests.post(f'{BASE_URL}/auth/register/', json=data)
    
    if response.status_code == 201:
        result = response.json()
        access_token = result['tokens']['access']
        refresh_token = result['tokens']['refresh']
        headers = {'Authorization': f'Bearer {access_token}'}
        
        print_success(f"User registered: {result['user']['username']}")
        print_success(f"Access token received (length: {len(access_token)})")
        print_success(f"Refresh token received (length: {len(refresh_token)})")
        return True
    else:
        print_error(f"Registration failed: {response.status_code}")
        print(response.json())
        return False

def test_login():
    """Test user login"""
    print_section("TEST 2: User Login")
    
    # First create a user
    username = f'logintest_{int(datetime.now().timestamp())}'
    
    # Register
    register_data = {
        'username': username,
        'email': f'{username}@test.com',
        'password': 'LoginPass123!',
        'password2': 'LoginPass123!',
        'timezone': 'UTC'
    }
    requests.post(f'{BASE_URL}/auth/register/', json=register_data)
    
    # Now login
    login_data = {
        'username': username,
        'password': 'LoginPass123!'
    }
    
    response = requests.post(f'{BASE_URL}/auth/login/', json=login_data)
    
    if response.status_code == 200:
        result = response.json()
        print_success("Login successful")
        print_success(f"Access token received: {result['access'][:50]}...")
        print_success(f"Refresh token received: {result['refresh'][:50]}...")
        return True
    else:
        print_error(f"Login failed: {response.status_code}")
        return False

def test_get_current_user():
    """Test getting current user info"""
    print_section("TEST 3: Get Current User")
    
    response = requests.get(f'{BASE_URL}/auth/me/', headers=headers)
    
    if response.status_code == 200:
        user = response.json()['user']
        print_success(f"User retrieved: {user['username']}")
        print_info(f"  Email: {user['email']}")
        print_info(f"  Current Streak: {user['current_streak']}")
        print_info(f"  Level: {user['level']}")
        print_info(f"  Timezone: {user['timezone']}")
        return True
    else:
        print_error(f"Failed: {response.status_code}")
        return False

def test_get_dashboard():
    """Test getting dashboard data"""
    print_section("TEST 4: Get Dashboard")
    
    response = requests.get(f'{BASE_URL}/dashboard/', headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print_success("Dashboard retrieved")
        print_info(f"  Missions for: {data['mission']['mission_date']}")
        print_info(f"  Mission 1 completed: {data['mission']['mission_1_completed']}")
        print_info(f"  Mission 2 completed: {data['mission']['mission_2_completed']}")
        print_info(f"  Mission 3 completed: {data['mission']['mission_3_completed']}")
        print_info(f"  Current streak: {data['user']['current_streak']}")
        print_info(f"  Time until midnight: {data['time_until_midnight']['formatted']}")
        
        if data['quote']:
            print_info(f"  Quote: \"{data['quote']['quote'][:50]}...\"")
        
        return True
    else:
        print_error(f"Failed: {response.status_code}")
        return False

def test_get_todays_missions():
    """Test getting today's missions"""
    print_section("TEST 5: Get Today's Missions")
    
    response = requests.get(f'{BASE_URL}/missions/today/', headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print_success("Today's missions retrieved")
        print_info(f"  Date: {data['mission']['mission_date']}")
        print_info(f"  Templates loaded: {len(data['templates'])}")
        
        for template in data['templates']:
            print_info(f"    Mission {template['mission_number']}: {template['title']}")
        
        return True
    else:
        print_error(f"Failed: {response.status_code}")
        return False

def test_complete_missions():
    """Test completing all 3 missions"""
    print_section("TEST 6: Complete Missions")
    
    missions_data = [
        {'mission_number': 1, 'notes': 'Explained REST APIs to a friend'},
        {'mission_number': 2, 'notes': 'Built Django models and views'},
        {'mission_number': 3, 'notes': 'Reflected on today\'s learning'}
    ]
    
    for mission_data in missions_data:
        response = requests.post(
            f'{BASE_URL}/missions/complete/',
            json=mission_data,
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            mission_num = mission_data['mission_number']
            
            if result['streak_increased']:
                print_success(f"Mission {mission_num} completed! 🔥 STREAK INCREASED to {result['user']['current_streak']}!")
            else:
                print_success(f"Mission {mission_num} completed")
        else:
            print_error(f"Mission {mission_data['mission_number']} failed: {response.status_code}")
            return False
    
    return True

def test_get_streak_status():
    """Test getting streak status"""
    print_section("TEST 7: Get Streak Status")
    
    response = requests.get(f'{BASE_URL}/streak/status/', headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print_success("Streak status retrieved")
        print_info(f"  Current Streak: {data['current_streak']} days")
        print_info(f"  Longest Streak: {data['longest_streak']} days")
        print_info(f"  Total Days: {data['total_days_completed']}")
        print_info(f"  Level: {data['level']}")
        
        level_info = data['level_info']
        if level_info['current_level']:
            print_info(f"  Current Level: {level_info['current_level']['name']} {level_info['current_level']['icon']}")
        if level_info['next_level']:
            print_info(f"  Next Level: {level_info['next_level']['name']} ({level_info['days_to_next_level']} days away)")
        print_info(f"  Progress: {level_info['progress_percentage']}%")
        
        return True
    else:
        print_error(f"Failed: {response.status_code}")
        return False

def test_get_mission_history():
    """Test getting mission history"""
    print_section("TEST 8: Get Mission History")
    
    response = requests.get(f'{BASE_URL}/missions/history/', headers=headers)
    
    if response.status_code == 200:
        missions = response.json()
        print_success(f"Mission history retrieved: {len(missions)} missions")
        
        if missions:
            latest = missions[0]
            print_info(f"  Latest mission: {latest['mission_date']}")
            print_info(f"    All completed: {latest['all_completed']}")
        
        return True
    else:
        print_error(f"Failed: {response.status_code}")
        return False

def test_token_refresh():
    """Test refreshing access token"""
    print_section("TEST 9: Token Refresh")
    
    global access_token, headers
    
    data = {'refresh': refresh_token}
    response = requests.post(f'{BASE_URL}/auth/refresh/', json=data)
    
    if response.status_code == 200:
        result = response.json()
        access_token = result['access']
        headers = {'Authorization': f'Bearer {access_token}'}
        
        print_success("Token refreshed successfully")
        print_info(f"  New access token: {access_token[:50]}...")
        return True
    else:
        print_error(f"Failed: {response.status_code}")
        return False

def test_update_profile():
    """Test updating user profile"""
    print_section("TEST 10: Update Profile")
    
    data = {'timezone': 'Europe/London'}
    response = requests.put(f'{BASE_URL}/auth/profile/', json=data, headers=headers)
    
    if response.status_code == 200:
        user = response.json()
        print_success("Profile updated")
        print_info(f"  New timezone: {user['timezone']}")
        return True
    else:
        print_error(f"Failed: {response.status_code}")
        return False

def run_all_tests():
    """Run all API tests"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}🚀 TECH PRO STREAK - API TEST SUITE{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}")
    
    tests = [
        test_register,
        test_login,
        test_get_current_user,
        test_get_dashboard,
        test_get_todays_missions,
        test_complete_missions,
        test_get_streak_status,
        test_get_mission_history,
        test_token_refresh,
        test_update_profile,
    ]
    
    results = []
    
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print_error(f"Test crashed: {str(e)}")
            results.append(False)
    
    # Summary
    print_section("TEST SUMMARY")
    passed = sum(results)
    total = len(results)
    
    print(f"\n{Colors.BLUE}Results: {passed}/{total} tests passed{Colors.END}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{'='*60}{Colors.END}")
        print(f"{Colors.GREEN}🎉 ALL TESTS PASSED! API IS READY FOR FRONTEND!{Colors.END}")
        print(f"{Colors.GREEN}{'='*60}{Colors.END}\n")
    else:
        print(f"\n{Colors.RED}❌ Some tests failed. Check the output above.{Colors.END}\n")

if __name__ == '__main__':
    run_all_tests()