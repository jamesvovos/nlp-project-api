from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# establish connection database using SQLAlchemy ORM
SQLALCHEMY_DATABASE_URL = ''

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# the database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class to create a database model/table
Base = declarative_base()
