"""
Interaction with users table
"""

from models import User
from controller import Session, engine
from sqlalchemy import select
import hashlib
import os
from config import ENCRYPT_CODE, JWT_KEY, JWT_ALGORITHM

def encrypt_password(password: str) -> str:
    """Simple password hashing using SHA256 with salt"""
    salt = ENCRYPT_CODE.encode('utf-8')
    return hashlib.sha256(salt + password.encode('utf-8')).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    return encrypt_password(password) == hashed
from jwt import encode, decode


def add_user(
    login: str,
    password: str
) -> User:
    """ Register new user """

    session = Session()
    if get_user(login) is not None:
        return False

    user = User(
        login=login,
        password=encrypt_password(password)
    )

    session.add(user)
    session.commit()

    return encode(
        {'id' : user.id, 'login': user.login, 'password': user.password},
        JWT_KEY,
        algorithm=JWT_ALGORITHM
    )


def get_init_user(login: str) -> User:
    return select(User).where(User.login == login)


def get_user(login: str) -> dict:
    session = Session()
    user = get_init_user(login)

    users_ = list(session.scalars(user))

    if not users_:
        return None

    e = users_[0]

    return {
        'id': e.id,
        'login': e.login,
        'password': e.password
    }
    
def login_user(login: str, password: str):
    user = get_user(login)

    if user is None:
        return False

    if not verify_password(password, user['password']):
        return False

    return encode(user, JWT_KEY, algorithm=JWT_ALGORITHM)


def drop_users_table():
    User.__table__.drop(engine)


def delete_user(user: User) -> None:
    _session = Session()
    _session.delete(user)
    _session.commit()