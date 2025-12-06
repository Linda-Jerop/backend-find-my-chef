# Find My Chef Backend

Backend API for the Find My Chef platform - connecting clients with professional chefs.

## 🏗️ Project Structure

```
backend-find-my-chef/
│
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── models/               # Database models
│   │   ├── __init__.py
│   │   ├── user.py          # Base User model
│   │   ├── chef.py          # Chef profile model
│   │   ├── client.py        # Client profile model
│   │   └── booking.py       # Booking model
│   │
│   ├── routes/              # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication routes
│   │   ├── chef.py          # Chef routes
│   │   ├── client.py        # Client routes
│   │   └── booking.py       # Booking routes
│   │
│   ├── controllers/         # Business logic
│   │   └── __init__.py
│   │
│   ├── middleware/          # Custom middleware
│   │   └── __init__.py
│   │
│   └── utils/               # Utility functions
│       └── __init__.py
│
├── config/
│   ├── __init__.py
│   └── settings.py          # Configuration settings
│
├── migrations/              # Database migrations
│
├── tests/                   # Test files
│
├── .env.example             # Environment variables template
├── .gitignore
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
└── README.md

```

## 🛠️ Technologies

- **Flask** - Web framework
- **SQLAlchemy** - ORM
- **Flask-Migrate** - Database migrations
- **Flask-JWT-Extended** - JWT authentication
- **Flask-CORS** - CORS handling
- **PostgreSQL/SQLite** - Database
- **Bcrypt** - Password hashing

## 📋 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user (client/chef)
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `POST /api/auth/refresh` - Refresh JWT token

### Chefs
- `GET /api/chefs` - Get all chefs (with filters)
- `GET /api/chefs/:id` - Get single chef profile
- `PATCH /api/chefs/:id` - Update chef profile (owner only)
- `DELETE /api/chefs/:id` - Delete chef profile (owner only)

### Clients
- `GET /api/clients/:id` - Get client profile
- `PATCH /api/clients/:id` - Update client profile (owner only)
- `DELETE /api/clients/:id` - Delete client profile (owner only)

### Bookings
- `POST /api/bookings` - Create new booking
- `GET /api/bookings` - Get user's bookings (client or chef)
- `GET /api/bookings/:id` - Get single booking
- `PATCH /api/bookings/:id` - Update booking status
- `DELETE /api/bookings/:id` - Cancel booking

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)

### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/Linda-Jerop/backend-find-my-chef.git
cd backend-find-my-chef
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize database**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

6. **Run the application**
```bash
python run.py
# Or using Flask CLI
flask run --port=8000
```

The API will be available at `http://localhost:8000`

## 🧪 Testing

Run tests with:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app tests/
```

## 🔧 Development

### Running in development mode
```bash
export FLASK_ENV=development
python run.py
```

### Database migrations
```bash
# Create migration
flask db migrate -m "Description of changes"

# Apply migration
flask db upgrade

# Rollback migration
flask db downgrade
```

## 📝 Environment Variables

See `.env.example` for required environment variables.

Key variables:
- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - Flask secret key
- `JWT_SECRET_KEY` - JWT signing key
- `CORS_ORIGINS` - Allowed CORS origins

## 🤝 Contributing

This is a Phase 3 group project:
- **Scrum Master**: Linda Jerop (@LogicLegends)
- **Contributors**: Ian Nasoore, David Kamau, Sasha Lisa, Banai Marysah

## 📄 License

This project is part of a software engineering preparation program.

## 🔗 Related Repositories

- Frontend: [frontend-find-my-chef](https://github.com/Linda-Jerop/frontend-find-my-chef)
