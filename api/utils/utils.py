from config import JWT_ALGORITHM, JWT_KEY
from jwt import decode
import datetime
 
def check_account(jwt_token):
    """
    Check info about account (JWT)
    """

    pass

def get_user_by_jwt(jwt_token : str) -> dict:
    user_info = decode(jwt_token, JWT_KEY, algorithms=[JWT_ALGORITHM])

    return user_info

def parse_date(date):
    DATE_FORMAT = '%d/%m/%Y'
    return datetime.datetime.strptime(date, DATE_FORMAT)