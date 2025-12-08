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
