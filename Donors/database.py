from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from Donors.models import BloodGroup  

# Use the correct database URL for SQLAlchemy
DATABASE_URL = "postgresql://password:12345@localhost/db_name"  

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the base class for models
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to check if the database is connected
def check_db_connection():
    db = SessionLocal()
    try:
        # Attempt a simple query to check the connection (adjust table/model accordingly)
        db.query(BloodGroup).first()
        print("OK")  # Will print to terminal if the DB connection is successful
    except SQLAlchemyError as e:
        print(f"Database connection error: {str(e)}")
    finally:
        db.close()

# Call the check_db_connection function to verify connection on startup
check_db_connection()  # Check the connection when the app starts
