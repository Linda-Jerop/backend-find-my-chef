from app import Base, engine
from app.models import User, Chef, Client, Booking


def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)  # This creates all tables from models.
    print("✅ Database tables created successfully!")
    print("Tables: users, chefs, clients, bookings")


if __name__ == "__main__":
    init_db()
