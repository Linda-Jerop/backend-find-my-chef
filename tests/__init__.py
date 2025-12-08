"""
Tests Package

This package contains all backend tests organized by feature.

Structure matches frontend structure:
- tests/auth/ → Tests for authentication (login, register)
- tests/profile/ → Tests for chef and client profiles
- tests/search/ → Tests for chef search and filtering
- tests/bookings/ → Tests for booking management
- tests/models/ → Tests for database models

To run tests:
    pytest                          # Run all tests
    pytest tests/auth/              # Run auth tests only
    pytest tests/bookings/ -v       # Run booking tests with verbose output
    pytest --cov=app tests/         # Run with coverage report
"""
