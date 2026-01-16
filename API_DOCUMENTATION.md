# Tech Pro Streak - API Documentation

Base URL: `http://127.0.0.1:8000/api` (development)

All endpoints except `/auth/register/` and `/auth/login/` require JWT authentication.

## Authentication

### Register User
**POST** `/auth/register/`

Request:
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "password2": "SecurePass123!",
  "timezone": "America/New_York"
}
```

Response (201):
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "current_streak": 0,
    "level": "Beginner"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

### Login
**POST** `/auth/login/`

Request:
```json
{
  "username": "johndoe",
  "password": "SecurePass123!"
}
```

Response (200):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Refresh Token
**POST** `/auth/refresh/`

Request:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

Response (200):
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Get Current User
**GET** `/auth/me/`  
**Headers:** `Authorization: Bearer <access_token>`

Response (200):
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "timezone": "America/New_York",
    "current_streak": 5,
    "longest_streak": 12,
    "total_days_completed": 25,
    "last_completion_date": "2026-01-14",
    "level": "Builder"
  }
}
```

## Dashboard

### Get Dashboard
**GET** `/dashboard/`  
**Headers:** `Authorization: Bearer <access_token>`

Response (200):
```json
{
  "user": { /* user object */ },
  "mission": {
    "mission_date": "2026-01-14",
    "mission_1_completed": true,
    "mission_2_completed": false,
    "mission_3_completed": false,
    "all_completed": false
  },
  "templates": [
    {
      "mission_number": 1,
      "title": "Communicate & Learn",
      "description": "Explain a tech concept..."
    }
  ],
  "quote": {
    "quote": "First, solve the problem. Then, write the code.",
    "author": "John Johnson"
  },
  "streak_stats": {
    "current_streak": 5,
    "time_until_midnight": {
      "hours": 8,
      "minutes": 30,
      "formatted": "8h 30m"
    }
  },
  "level_info": {
    "current_level": { "name": "Builder", "icon": "🔨" },
    "next_level": { "name": "Pro", "icon": "⚡" },
    "progress_percentage": 60
  }
}
```

## Missions

### Get Today's Missions
**GET** `/missions/today/`  
**Headers:** `Authorization: Bearer <access_token>`

### Complete Mission
**POST** `/missions/complete/`  
**Headers:** `Authorization: Bearer <access_token>`

Request:
```json
{
  "mission_number": 1,
  "notes": "Explained REST APIs to a friend"
}
```

Response (200):
```json
{
  "mission": { /* updated mission */ },
  "user": { /* updated user with new streak */ },
  "streak_increased": true,
  "message": "Mission 1 completed! 🔥 Streak: 6!"
}
```

### Get Mission History
**GET** `/missions/history/?limit=30`  
**Headers:** `Authorization: Bearer <access_token>`

## Streak

### Get Streak Status
**GET** `/streak/status/`  
**Headers:** `Authorization: Bearer <access_token>`

Response (200):
```json
{
  "current_streak": 6,
  "longest_streak": 12,
  "total_days_completed": 26,
  "level": "Builder",
  "level_info": {
    "current_level": { "name": "Builder", "min": 8, "max": 14, "icon": "🔨" },
    "next_level": { "name": "Pro", "min": 15, "max": 21, "icon": "⚡" },
    "progress_percentage": 66,
    "days_to_next_level": 9
  }
}
```