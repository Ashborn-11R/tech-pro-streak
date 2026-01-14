import requests
import json
from datetime import datetime, timedelta

BASE_URL = 'http://127.0.0.1:8000/api'

# Register and login
print("=== Registering User ===")
register_data = {
    'username': f'streaktest_{datetime.now().timestamp()}',
    'email': 'streaktest@example.com',
    'password': 'SecurePass123!',
    'password2': 'SecurePass123!',
    'timezone': 'America/New_York'
}

response = requests.post(f'{BASE_URL}/auth/register/', json=register_data)
data = response.json()
access_token = data['tokens']['access']
headers = {'Authorization': f'Bearer {access_token}'}

print(f"✅ User created: {data['user']['username']}")

# Get dashboard
print("\n=== Getting Dashboard ===")
response = requests.get(f'{BASE_URL}/dashboard/', headers=headers)
dashboard = response.json()
print(f"Current Streak: {dashboard['user']['current_streak']}")
print(f"Level: {dashboard['user']['level']}")
print(f"Time until midnight: {dashboard['time_until_midnight']['formatted']}")

# Complete all 3 missions
print("\n=== Completing Missions ===")
for mission_num in [1, 2, 3]:
    mission_data = {
        'mission_number': mission_num,
        'notes': f'Completed mission {mission_num} - testing streak engine'
    }
    response = requests.post(f'{BASE_URL}/missions/complete/', json=mission_data, headers=headers)
    result = response.json()
    
    print(f"Mission {mission_num}: ✅")
    if result.get('streak_increased'):
        print(f"  🔥 STREAK INCREASED TO {result['user']['current_streak']}!")

# Get streak status
print("\n=== Checking Streak Status ===")
response = requests.get(f'{BASE_URL}/streak/status/', headers=headers)
streak_status = response.json()

print(f"Current Streak: {streak_status['current_streak']} days")
print(f"Level: {streak_status['level']}")
print(f"Reset Reason: {streak_status['reset_reason']}")
print(f"Level Info:")
print(f"  Current: {streak_status['level_info']['current_level']['name']} {streak_status['level_info']['current_level']['icon']}")
if streak_status['level_info']['next_level']:
    print(f"  Next: {streak_status['level_info']['next_level']['name']} ({streak_status['level_info']['days_to_next_level']} days away)")
print(f"  Progress: {streak_status['level_info']['progress_percentage']}%")