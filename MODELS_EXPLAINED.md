# 📚 Database Models Explained - Find My Chef

## 🎯 Overview

We created **4 database tables** that work together to run the Find My Chef platform. Think of them as Excel spreadsheets that are connected to each other.

---

## 1️⃣ USERS Table - The Authentication Hub

**Purpose**: Store login information for everyone (both chefs and clients)

**Think of it as**: Your login credentials for the app

### Fields Explained:

```python
id = 1                          # Unique number for each user
email = "chef@example.com"      # Used to log in
password_hash = "hashed_pwd"    # Encrypted password (not plain text!)
name = "Chef Mario"             # Full name
role = "chef"                   # Either "chef" or "client"
firebase_uid = "abc123"         # For Google/Facebook login (optional)
created_at = "2025-12-06"       # When they joined
```

### Why This Design?
- **Security**: Passwords are hashed (encrypted) before storing
- **Flexibility**: Same table handles both chef and client logins
- **Social Auth**: firebase_uid stores Google/Facebook login info

### Real-World Example:
```
When "Chef Mario" registers:
1. Email & password saved in users table
2. role = "chef" (so system knows they're a chef)
3. Separate chef profile created in chefs table
```

---

## 2️⃣ CHEFS Table - Professional Profiles

**Purpose**: Store chef business information (portfolio, pricing, etc.)

**Think of it as**: A chef's business card with all their details

### Fields Explained:

```python
id = 1                              # Chef's unique ID
user_id = 1                         # Links to users table (same person)
bio = "Italian cuisine expert"      # About me section
cuisines = "Italian,French,Greek"   # What they cook (comma-separated)
hourly_rate = 50.00                 # Price in KSH per hour
location = "Nairobi"                # Where they work
phone = "+254712345678"             # Contact number
photo_url = "https://..."           # Profile picture URL
rating = 4.8                        # Average rating (0-5 stars)
years_of_experience = 10            # How long they've cooked professionally
is_available = 1                    # 1=taking bookings, 0=not available
```

### Why This Design?
- **One-to-One**: Each user can have only ONE chef profile
- **Searchable**: Cuisines and location used for filtering
- **Pricing**: hourly_rate stored here (chef sets their own price)
- **Portfolio**: Bio and photo make profile attractive to clients

### Real-World Example:
```
Frontend search: "Find Italian chefs in Nairobi under KSH 60/hour"
Backend queries:
- WHERE cuisines LIKE '%Italian%'
- AND location = 'Nairobi'  
- AND hourly_rate <= 60
```

---

## 3️⃣ CLIENTS Table - Customer Profiles

**Purpose**: Store client information and preferences

**Think of it as**: Customer account details

### Fields Explained:

```python
id = 1                                  # Client's unique ID
user_id = 2                             # Links to users table
phone = "+254798765432"                 # Contact number
address = "123 Main St, Nairobi"        # Where they live/want service
preferred_cuisines = "Italian,Chinese"  # What they like to eat
total_bookings = 5                      # How many times they've booked
```

### Why This Design?
- **One-to-One**: Each user can have only ONE client profile
- **Contact**: Phone & address help chefs reach them
- **Tracking**: total_bookings tracks customer activity

### Real-World Example:
```
When client books a chef:
1. System looks up client.address (where to send chef)
2. Uses client.phone (for chef to confirm)
3. Increments total_bookings counter
```

---

## 4️⃣ BOOKINGS Table - The Heart of the Business

**Purpose**: Connects clients with chefs (appointments/orders)

**Think of it as**: A reservation system (like booking a restaurant table)

### Fields Explained:

```python
id = 1                          # Booking ID
client_id = 2                   # Which client made the booking
chef_id = 1                     # Which chef they booked
booking_date = "2025-12-15"     # What day
booking_time = "18:00"          # What time (6 PM)
duration_hours = 3.0            # How long (3 hours)
location = "Client's home"      # Where the service happens
hourly_rate = 50.00             # Chef's rate (locked in)
total_price = 150.00            # 3 hours × 50 = 150 KSH
status = "pending"              # pending/accepted/declined/completed
special_requests = "Vegan food" # Client's notes
notes = "Will bring supplies"   # Chef's notes
```

### Status Lifecycle:
```
pending → Chef hasn't responded yet
   ↓
accepted → Chef said yes! Booking confirmed
   ↓
completed → Service was delivered
   ↓
(or declined → Chef said no, client must book another chef)
(or cancelled → Someone cancelled it)
```

### Why This Design?
- **Price Lock**: hourly_rate stored here so price doesn't change if chef updates rates later
- **Calculation**: total_price = duration_hours × hourly_rate
- **Tracking**: created_at and updated_at track when things happened
- **Communication**: special_requests and notes allow messaging

### Real-World Example:
```
Client wants to book Chef Mario for 3 hours:

Step 1: Client fills form
- Select chef: "Chef Mario"
- Date: "2025-12-15"
- Time: "18:00"
- Duration: 3 hours
- Location: "My apartment"

Step 2: Backend creates booking
- Looks up Chef Mario's current rate (50 KSH/hour)
- Calculates total: 3 × 50 = 150 KSH
- Status starts as "pending"

Step 3: Chef sees notification
- Chef Mario logs in
- Sees booking request with all details
- Clicks "Accept" or "Decline"

Step 4: Status updated
- If accepted: status = "accepted"
- Client gets notification
- Booking is confirmed!
```

---

## 🔗 How They Connect (Relationships)

### Visual Flow:

```
USER registers as CHEF
    ↓
Creates profile in CHEFS table
    ↓
CLIENT searches and finds CHEF
    ↓
CLIENT creates BOOKING
    ↓
Links: client_id → CLIENTS table
       chef_id → CHEFS table
    ↓
CHEF accepts/declines BOOKING
    ↓
Status updates
```

### Database Relationships:

1. **User ↔ Chef** (One-to-One)
   - `users.id` = `chefs.user_id`
   - One user account = One chef profile

2. **User ↔ Client** (One-to-One)
   - `users.id` = `clients.user_id`
   - One user account = One client profile

3. **Chef → Bookings** (One-to-Many)
   - `chefs.id` = `bookings.chef_id`
   - One chef = Many bookings

4. **Client → Bookings** (One-to-Many)
   - `clients.id` = `bookings.client_id`
   - One client = Many bookings

---

## 💡 Common Questions

### Q: Why not just one "User" table with all fields?
**A**: Separation of concerns. Chefs need different fields than clients. This keeps tables clean and organized.

### Q: Why store hourly_rate in bookings if it's already in chefs?
**A**: Price protection! If chef raises rate from 50 to 70 KSH, old bookings should still show 50 KSH (what was agreed upon).

### Q: Can one person be both chef and client?
**A**: No! The role field forces you to choose. In real-world apps, you might allow both, but that's more complex.

### Q: What happens if a chef is deleted?
**A**: All their bookings are also deleted (cascade delete). In production, you might want to keep bookings for records.

---

## 🎓 Learning Points

### 1. **Foreign Keys** = Connections
- `user_id` in chefs table points to `id` in users table
- This creates a relationship between tables

### 2. **Enums** = Controlled Values
- `role` can only be "chef" or "client" (not "admin" or "manager")
- `status` can only be "pending", "accepted", "declined", etc.

### 3. **Timestamps** = Audit Trail
- `created_at` = When record was created
- `updated_at` = When it was last modified
- Helpful for tracking and debugging

### 4. **Indexes** = Speed
- `index=True` on email makes login queries fast
- Database can find users quickly by email

---

## 📊 Data Example (Putting it all together)

```python
# User registers as chef
users_table:
  id=1, email="mario@chef.com", role="chef", name="Chef Mario"

chefs_table:
  id=1, user_id=1, hourly_rate=50, location="Nairobi", cuisines="Italian"

# Another user registers as client  
users_table:
  id=2, email="john@client.com", role="client", name="John Doe"

clients_table:
  id=1, user_id=2, phone="+254700000000", address="Downtown Nairobi"

# Client books chef
bookings_table:
  id=1, client_id=1, chef_id=1, date="2025-12-15", time="18:00",
  duration=3, hourly_rate=50, total_price=150, status="pending"

# Chef accepts
bookings_table (updated):
  id=1, ..., status="accepted", updated_at="2025-12-06 10:30:00"
```

---

This is the foundation of your entire backend! 🎉
Next: We'll create Pydantic schemas (validation rules) and API routes (endpoints) to interact with this data.
