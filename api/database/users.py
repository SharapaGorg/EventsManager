"""
Interaction with users table
"""

from models import User
from controller import Session, engine
from sqlalchemy import select
from cryptocode import encrypt, decrypt
from config import ENCRYPT_CODE

def add_user(
    login : str,
    password : str
) -> User:
    """ Register new user """
    
    session = Session()
    if get_user(login) is not None:
        return False

    user = User(
        login = login,
        password = encrypt(password, ENCRYPT_CODE)
    )

    session.add(user)
    session.commit()

    return user

def get_init_user(login: str) -> User:
    return select(User).where(User.login == login)

def get_user(login : str) -> dict:
    session = Session()
    user = get_init_user(login)

    users_ = list(session.scalars(user))

    if not users_:
        return None

    e = users_[0]

    return {
        'id': e.id,
        'login' : e.login,
        'password' : e.password
    }

def login_user(login : str, password : str):
    user = get_user(login)

    decrypted = decrypt(user['password'], ENCRYPT_CODE)
    if user is None or password != decrypted:
        return False

    return True


def drop_users_table():
    User.__table__.drop(engine)

def delete_user(user : User) -> None:
    _session = Session()
    _session.delete(user)
    _session.commit()