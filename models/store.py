import re
import uuid
from typing import Dict
from models.model import Model
from dataclasses import dataclass, field


@dataclass(eq=False)
class Store(Model):
    collection: str = field(init=False, default='stores')
    name: str
    url_prefix: str
    tag_name: str
    query: Dict
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def json(self):
        return {
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "_id": self._id,
            "query": self.query
        }

    @classmethod
    def get_by_name(cls, store_name: str):
        return cls.find_one_by("name", store_name)

    @classmethod
    def get_by_url_prefix(cls, url_prefix: str):
        url_regex = {"$regex": "^{}".format(url_prefix)}
        return cls.find_one_by("url_prefix", url_regex)

    @classmethod
    def get_by_url_self_made(cls, url: str) -> "Store":
        a = 0
        l = len(url)
        url1 = []
        for b in range(0, l):
            if a < 3:
                if url[b] == "/":
                    a = a + 1
                url1.append(url[b])
            else:
                break
        url2 = ''.join(url1)
        data = cls.find_one_by("url_prefix", url2)
        print(data)
        return data

    @classmethod
    def convert_url(cls, url: str) -> str:
        a = 0
        l = len(url)
        url1 = []
        for b in range(0, l):
            if a < 3:
                if url[b] == "/":
                    a = a + 1
                url1.append(url[b])
            else:
                break
        url2 = ''.join(url1)
        return url2


    @classmethod
    def get_by_url(cls, url: str) -> "Store":
        pattern = re.compile(r"(https?//.*?/)")
        match = pattern.search(url)
        url_prefix = match.group(1)
        return cls.get_by_url_prefix(url_prefix)

