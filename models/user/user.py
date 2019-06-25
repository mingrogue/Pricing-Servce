import uuid
from dataclasses import dataclass, field
from typing import Dict, List

from models.model import Model
import models.user.errors as UserErrors
from common.utils import Utils


@dataclass
class User(Model):
    collection: str = field(init=False, default='users')
    email: str
    password: str
    _id: str = field(default_factory=lambda:uuid.uuid4().hex)

    @classmethod
    def find_by_email(cls, email: str) -> "List[User]":
        try:
            user = cls.find_one_by('email', email)
            return user
        except TypeError:
            raise UserErrors.UserNotFoundError('A user with this email id is not found')

    @classmethod
    def register_user(cls, email: str, password: str):
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError('Email id is not valid')

        #try:
        user = cls.find_by_email(email)
            #for users in user:
        if len(user) > 0:
            raise UserErrors.UserAlreadyRegisteredError('User with this email {} is already registered'.format(email))
        else:
            User(email, Utils.hash_password(password)).save_to_mongo()

        return True


    @classmethod
    def is_login_valid(cls, email, password):
        user = cls.find_by_email(email)
        for users in user:
            if not Utils.check_hashed_password(password, users.password):
                raise UserErrors.IncorrectPasswordError('The email id or password is incorrect')
        return True

    def json(self) -> Dict:
        return {
            '_id': self._id,
            'email': self.email,
            'password': self.password
        }
