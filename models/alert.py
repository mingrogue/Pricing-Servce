import uuid
from typing import Dict
from libs.mailgun import Mailgun
from models.item import Item
from models.model import Model
from dataclasses import dataclass, field


@dataclass(eq=False)
class Alert(Model):
    collection: str = field(init=False, default='alerts')
    name: str
    item_id: str
    user_email: str
    Price_limit: float
    item_url: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def __post_init__(self):
        self.item = Item.get_by_id(self.item_id)
        self.price: float = None


    def json(self)-> Dict:
        return{
            "item_id": self.item_id,
            "name": self.name,
            "Price_limit": self.Price_limit,
            "user_email": self.user_email,
            "item_url": self.item_url,
            "_id": self._id
        }

    def load_item_price(self) -> float:
        item = Item.get_by_id(self.item_id)
        for it in item:
            self.price = it.load_price()
            print(self.price)
        return self.price

    def get_item_url(self):
        item = Item.get_by_id(self.item_id)
        for it in item:
            self.item_url = it.url
        return self.item_url

    def notify_if_price_reached(self):
        if self.price < float(self.Price_limit):
            print(f"item {self.name} has reached a price lower than the price limit {self.Price_limit}, its price is {self.price}")
            Mailgun.send_mail(
                [self.user_email],
                'notification for {}'.format(self.name),
                'the price limit has been reached desired price.'
            )
