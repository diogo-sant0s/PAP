from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker, declarative_base
from werkzeug.security import generate_password_hash
import uuid

db = create_engine('sqlite:///database.db', echo=False)
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

class Login(Base):
    __tablename__ = "Login"

    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)


Base.metadata.create_all(bind=db)

DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "1234"
DEFAULT_USER_USERNAME = "user"
DEFAULT_USER_PASSWORD = "qualquercoisa"  

existing_user = session.query(Login).filter_by(username=DEFAULT_USER_USERNAME).first()
if not existing_user:
    user=Login(
        id=2,
        username=DEFAULT_USER_USERNAME,
        password=generate_password_hash(DEFAULT_USER_PASSWORD),
    )
    session.add(user)
    session.commit()

existing_admin = session.query(Login).filter_by(username=DEFAULT_ADMIN_USERNAME).first()
if not existing_admin:
    admin_user = Login(
        id=1,
        username=DEFAULT_ADMIN_USERNAME,
        password=generate_password_hash(DEFAULT_ADMIN_PASSWORD),
    )
    session.add(admin_user)
    session.commit()
    print("Default admin user created with user admin and password 1234.")
else:
    print("Default admin user already exists.")

print("Database created successfully!")