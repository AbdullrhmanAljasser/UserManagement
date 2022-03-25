from datetime import datetime, timedelta
from uuid import uuid4
import jwt

from database.session import db_client

_secret = "1F74F4AD9EF93F235514849CB2F42"
_algorithm = "HS256"

def jwt_encode(info):
    return jwt.encode(
        info,
        _secret,
        algorithm=_algorithm
    )
    
def jwt_decode(info):
    try:
        return jwt.decode(
            info,
            _secret,
            algorithms=_algorithm
        )
    except:
        return None
    
def generate_token_with_user_uuid(uuid):
    expiry = datetime.utcnow() + timedelta(weeks=2)
    return jwt_encode({
        "user": {
            "uuid": uuid,
            "token_expire_at": expiry.strftime("%m/%d/%Y, %H:%M:%S")
        }
    })
    
def generate_new_jwt_secret():
    db_client.get_database().get_collection("user_management_secert").insert_one({"secret": str(uuid4()), "verified_until": datetime.utcnow() + timedelta(weeks=1)})
    
# def get_latest