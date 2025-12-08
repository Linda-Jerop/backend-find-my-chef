# Find My Chef - Database Schema

## Database's Diagram

You should create this diagram on [dbdiagram.io](https://dbdiagram.io) as per project requirements.

### Tables Overview:

```
┌─────────────┐
│   USERS     │ ← Base authentication table
├─────────────┤
│ id (PK)     │
│ email       │
│ password    │
│ name        │
│ role        │ → enum: 'chef' or 'client'
│ firebase_uid│
│ created_at  │
└─────────────┘
      │
      ├────────────────────┐
      │                    │
      ▼                    ▼
┌─────────────┐      ┌─────────────┐
│   CHEFS     │      │  CLIENTS    │
├─────────────┤      ├─────────────┤
│ id (PK)     │      │ id (PK)     │
│ user_id(FK) │      │ user_id(FK) │
│ bio         │      │ phone       │
│ cuisines    │      │ address     │
│ hourly_rate │      │ preferences │
│ location    │      │ total_bookings
│ phone       │      └─────────────┘
│ photo_url   │            │
│ rating      │            │
│ is_available│            │
└─────────────┘            │
      │                    │
      └────────┬───────────┘
               │
               ▼
        ┌─────────────┐
        │  BOOKINGS   │ ← Connects clients & chefs
        ├─────────────┤
        │ id (PK)     │
        │ client_id(FK)│
        │ chef_id(FK) │
        │ booking_date│
        │ booking_time│
        │ duration    │
        │ location    │
        │ hourly_rate │
        │ total_price │
        │ status      │ → enum: pending/accepted/declined
        │ created_at  │
        └─────────────┘
```

## Relationships

### 1. User → Chef (One-to-One)
- **Relationship**: `users.id` ← `chefs.user_id`
- **Constraint**: One user can have only ONE chef profile
- **Purpose**: Separates authentication from business data
- **Example**: User logs in → System shows their chef profile

### 2. User → Client (One-to-One)
- **Relationship**: `users.id` ← `clients.user_id`
- **Constraint**: One user can have only ONE client profile
- **Purpose**: Separates authentication from customer data
- **Example**: User logs in → System shows their booking history

### 3. Client → Bookings (One-to-Many)
- **Relationship**: `clients.id` ← `bookings.client_id`
- **Constraint**: One client can have MANY bookings
- **Purpose**: Track all appointments made by a client
- **Example**: Client sees list of all their bookings (past & future)

### 4. Chef → Bookings (One-to-Many)
- **Relationship**: `chefs.id` ← `bookings.chef_id`
- **Constraint**: One chef can have MANY bookings
- **Purpose**: Track all appointments for a chef
- **Example**: Chef dashboard shows all booking requests

## dbdiagram.io Code

Paste this into [dbdiagram.io](https://dbdiagram.io) to generate the diagram to show the database diagram and display the relationships clearly,
so that you see the thought process:

```
Table users {
  id integer [primary key]
  email varchar(255) [unique, not null]
  password_hash varchar(255) [not null]
  name varchar(255) [not null]
  role varchar(10) [not null, note: 'chef or client']
  firebase_uid varchar(255) [unique]
  created_at timestamp
  updated_at timestamp
}

Table chefs {
  id integer [primary key]
  user_id integer [unique, not null, ref: > users.id]
  bio text
  cuisines varchar(500)
  specialties text
  hourly_rate float [not null]
  location varchar(255)
  phone varchar(20)
  photo_url varchar(500)
  years_of_experience integer
  rating float
  total_bookings integer
  is_available boolean
}

Table clients {
  id integer [primary key]
  user_id integer [unique, not null, ref: > users.id]
  phone varchar(20)
  address varchar(500)
  preferred_cuisines varchar(500)
  total_bookings integer
}

Table bookings {
  id integer [primary key]
  client_id integer [not null, ref: > clients.id]
  chef_id integer [not null, ref: > chefs.id]
  booking_date date [not null]
  booking_time time [not null]
  duration_hours float [not null]
  location varchar(500) [not null]
  hourly_rate float [not null]
  total_price float [not null]
  status varchar(20) [not null, note: 'pending/accepted/declined/completed/cancelled']
  special_requests text
  notes text
  created_at timestamp
  updated_at timestamp
}
```

## Our main/key Design Decisions

### Why Two Tables for Users?
- **Separation of Concerns**: Authentication (users) vs Business Logic (chefs/clients)
- **Flexibility**: Chef-specific fields don't clutter the client table
- **Security**: Password hashes stored separately from profile data

### Why Store hourly_rate in Bookings?
- **Price Lock**: Prevents price changes after booking is made
- **Historical Data**: Can see what rate was charged at time of booking
- **Integrity**: Client's total price won't change if chef updates rates

### Why Enums for role and status?
- **Data Integrity**: Only valid values can be stored
- **Type Safety**: Backend validates values automatically
- **Consistency**: Frontend and backend use same status values

## Sample Data Flow

### User Registration (as Chef):
1. Create record in `users` table (email, password, role='chef')
2. Create record in `chefs` table (linked to user_id)
3. Return both to frontend

### Creating a Booking:
1. Client selects chef from search
2. Frontend sends: chef_id, date, time, duration, location
3. Backend:
   - Looks up chef's current hourly_rate
   - Calculates total_price = duration * hourly_rate
   - Creates booking with status='pending'
4. Chef sees booking request in their dashboard

### Chef Accepts Booking:
1. Chef clicks "Accept" button
2. Frontend sends: PATCH /api/bookings/:id {status: 'accepted'}
3. Backend updates booking.status = 'accepted'
4. Client sees updated status in their bookings list
