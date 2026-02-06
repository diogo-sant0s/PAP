from sqlalchemy import create_engine, Column, String, inspect, DateTime, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import UniqueConstraint
import datetime
import uuid

db = create_engine('sqlite:///database.db', echo=False)
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

class Users(Base):
    __tablename__ = "Users"
    __table_args__= (UniqueConstraint("email", name="uq_email"),)

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)


Base.metadata.create_all(bind=db)

# Inspect columns
inspector = inspect(db)
columns = [col['name'] for col in inspector.get_columns('Users')]
print(columns)
