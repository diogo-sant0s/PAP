from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker, declarative_base
import uuid

db = create_engine('sqlite:///database.db', echo=False)
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

class Login(Base):
    __tablename__ = "Login"

    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)


Base.metadata.create_all(bind=db)

# Create default admin user if it does not exist
DEFAULT_ADMIN_EMAIL = "admin"
DEFAULT_ADMIN_PASSWORD = "1234"

existing_admin = session.query(Login).filter_by(email=DEFAULT_ADMIN_EMAIL).first()
if not existing_admin:
    admin_user = Login(
        id=str(uuid.uuid4()),
        email=DEFAULT_ADMIN_EMAIL,
        password=DEFAULT_ADMIN_PASSWORD,
    )
    session.add(admin_user)
    session.commit()
    print("Default admin user created with user admin and password 1234.")
else:
    print("Default admin user already exists.")

print("Database created successfully!")