import random
import string

from datetime import datetime, timedelta
from dataclasses import dataclass
from uuid import uuid4

from database.session import db_client

EXPIRY_OF_OTP = timedelta(weeks=1)
EXPIRY_OF_VERIFY_OTP = timedelta(minutes=5)

def rand_pass(size):
    generate_pass = ''.join([random.choice( string.ascii_uppercase +
                                            string.ascii_lowercase +
                                            string.digits)
                                            for n in range(size)])
                            
    return generate_pass

@dataclass
class Base:
    uuid: str = str(uuid4())
    
    registerd_at: datetime = datetime.utcnow()
    
    def _vars():
        return ["uuid", "registerd_at"]
    
@dataclass
class OTPBase(Base):
    verified_at: datetime = None
    
    latest_otp: str = None
    latest_otp_generated_at: datetime = None
    
    def _vars():
        return Base._vars() + ["verified_at", "latest_otp", "latest_otp_generated_at"]
    
    def is_expired_or_verified(self):
        # Check it hasn't passed the allowed limit
        return (
            (
                False
                if self.verified_at + timedelta < datetime.utcnow() else
                True
            ) if self.verified_at else False
        )
        
    def _submit_otp(self, otp, type):
        print(
            self.latest_otp_generated_at + EXPIRY_OF_VERIFY_OTP 
            > 
            datetime.utcnow()
        )
        if (
            self.latest_otp_generated_at + EXPIRY_OF_VERIFY_OTP 
            > 
            datetime.utcnow()
        ):
            if self.latest_otp == otp:
                db_client.get_database().get_collection("user_info").update_one({type: getattr(self, type)}, {"$set":{"verified_at": datetime.utcnow()}})
                return True
            else:
                return False
        else:
            return False
    def _create_new_otp(self, type):
        db_client.get_database().get_collection("user_info").update_one({type: getattr(self, type)}, {"$set": {"latest_otp": rand_pass(8), "latest_otp_generated_at": datetime.utcnow()}})
            

@dataclass
class UserInfoPhone(OTPBase):
    phone: str = ""
    
    def vars():
        return OTPBase._vars() + ["phone"]
    
    def submit_otp(self, otp):
        return self._submit_otp(otp, "phone")
    
    def create_new_otp(self):
        self._create_new_otp("phone")
    
    def get_user_by_phone(phone):
        return _serialize(db_client.get_database().get_collection("user_info").find_one({"phone": phone}), UserInfoPhone)

@dataclass
class UserInfoEmail(OTPBase):
    email: str = ""

@dataclass
class UserInfoUsername(Base):
    username: str = ""
    password: str = ""

def _serialize(user, Model):
    if user is None:
        return None
    return Model(
        **{
            attr: user.get(attr, None) for attr in Model.vars()
        }
    )

def create_user_by_phone(phone: str) -> UserInfoPhone:
    db_client.get_database().get_collection("user_info").insert_one(UserInfoPhone(phone=phone, uuid=str(uuid4()), latest_otp=rand_pass(8), latest_otp_generated_at=datetime.utcnow()).__dict__)
