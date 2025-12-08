# Backend Authentication API Guide for Frontend

## Base URL
```
http://localhost:8000/api
```

## Endpoints

### 1. Register New User
**POST** `/auth/register`

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securePassword123",
  "role": "chef"
}
```

**Valid Roles:** `"chef"` or `"client"`

**Response (201 Created):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "john@example.com",
    "name": "John Doe",
    "role": "chef"
  }
}
```

**Error Responses:**
- `400`: Email already registered
- `422`: Invalid input (wrong role value, short password, invalid email)

---

### 2. Login User
**POST** `/auth/login`

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "securePassword123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "john@example.com",
    "name": "John Doe",
    "role": "chef"
  }
}
```

**Error Responses:**
- `401`: Invalid credentials (wrong email or password)

---

### 3. Get Current User
**GET** `/auth/me`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "john@example.com",
  "name": "John Doe",
  "role": "chef"
}
```

**Error Responses:**
- `401`: Missing or invalid token
- `401`: Token expired
- `404`: User not found

---

### 4. Google Login (Coming Soon)
**POST** `/auth/google`

**Request Body:**
```json
{
  "firebase_id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjEyMyJ9..."
}
```

**Note:** Requires Firebase setup (credentials not yet configured)

---

## How to Use Tokens

### Store Token
After registration or login, save the `access_token` to:
- **localStorage** (for web)
- **AsyncStorage** (for React Native)
- **Keychain** (for native iOS)
- **Keystore** (for native Android)

```javascript
localStorage.setItem('access_token', response.access_token);
```

### Send Token with Requests
Include token in Authorization header for protected endpoints:

```javascript
const response = await fetch('http://localhost:8000/api/auth/me', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});
```

### Check Token Expiry
Tokens expire after **24 hours**. When expired:
1. Show login screen to user
2. Clear stored token
3. Redirect to login page

---

## Frontend Implementation Example

```javascript
// Registration
async function register(name, email, password, role) {
  const response = await fetch('http://localhost:8000/api/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, email, password, role })
  });
  
  if (response.ok) {
    const data = await response.json();
    localStorage.setItem('access_token', data.access_token);
    return data.user;
  } else {
    throw new Error(await response.text());
  }
}

// Login
async function login(email, password) {
  const response = await fetch('http://localhost:8000/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  
  if (response.ok) {
    const data = await response.json();
    localStorage.setItem('access_token', data.access_token);
    return data.user;
  } else {
    throw new Error('Invalid credentials');
  }
}

// Get Current User
async function getCurrentUser() {
  const token = localStorage.getItem('access_token');
  const response = await fetch('http://localhost:8000/api/auth/me', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  
  if (response.ok) {
    return await response.json();
  } else if (response.status === 401) {
    // Token expired, clear and redirect to login
    localStorage.removeItem('access_token');
    window.location.href = '/login';
  }
}

// Logout
function logout() {
  localStorage.removeItem('access_token');
  window.location.href = '/login';
}
```

---

## Password Requirements

- **Minimum length**: 8 characters
- **Recommended**: Mix of uppercase, lowercase, numbers, and special characters
- Example strong password: `MyChef2024!`

---

## Role Selection

When registering, users must choose their role:

- **`chef`**: Provider of cooking services
- **`client`**: Consumer of cooking services

This role is used to filter what features are available in the app.

---

## Error Handling

All errors follow this format:

```json
{
  "detail": "Error message explaining what went wrong"
}
```

Common HTTP status codes:
- `200`: Success
- `201`: Resource created successfully
- `400`: Bad request (validation error)
- `401`: Unauthorized (invalid credentials or expired token)
- `404`: Not found
- `422`: Invalid input format
- `500`: Server error

---

## Testing

### Test Register
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name":"Test User",
    "email":"test@example.com",
    "password":"testPassword123",
    "role":"chef"
  }'
```

### Test Login
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email":"test@example.com",
    "password":"testPassword123"
  }'
```

### Test Protected Endpoint
```bash
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

---

## API Documentation

Interactive API docs available at:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

All endpoints are documented with examples and can be tested directly in the browser.

