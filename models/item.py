import uuid
from typing import Dict
from bs4 import BeautifulSoup
import requests
from models.model import Model
from dataclasses import dataclass, field
from re import sub
from decimal import Decimal


@dataclass(eq=False)
class Item(Model):
    collection: str = field(init=False, default='items')
    url: str
    tag_name: str
    query: Dict
    Price: float = field(default=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    # def __post_init__(self):
    #     self.price = None

    def __repr__(self):
        return f"<item {self.url}>"

    def load_price(self) -> float:
        response = requests.get(self.url)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)
        element1 = element.text.strip()
        element1 = element1[1:]
        print(element1)
        element1 = self.convert_yo_float(element1)
        element2 = Decimal(sub(r'[^\d.]', '', element1))
        #element2 = float(element1)
        #pattern = re.compile(r'{\d+\.\d\d}')
        self.price = element2
        return element2

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "url": self.url,
            "tag_name": self.tag_name,
            "Price": self.Price,
            "query": self.query
        }

    def convert_yo_float(self, element: str) -> str:
        n = len(element)
        b = []
        for a in range(0,n):
            if element[a] == ',':
                a = a + 1
            elif element[a] == '-':
                break
            else:
                b.append(element[a])
                a= a + 1
        b1 = ''.join(b)
        return b1
