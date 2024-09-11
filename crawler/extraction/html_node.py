from typing import Self
from bs4 import BeautifulSoup
from .dynamic_attribute import DynamicAttribute
from .locator import Locator


class HtmlNode:

    child_types: list[type[Self]]|list[str] = []
    locator: Locator|None = None
    is_leaf = False
    scope: Locator|None = None
    dynamic_attrs: dict[str, DynamicAttribute]|None = None
    
    @classmethod
    def find_canidates(type: type[Self], parent: Self) -> list[BeautifulSoup]:
        if not type.locator:
            raise Exception(f"No locator or method 'find_canidates' was supplied to model class {type.__name__}")
        return type.locator.find_elements(parent.soup, type.scope)
    
    @classmethod
    def get_dynamic_attrs(cls, tag) -> dict[str,str]:
        result = {}
        if cls.dynamic_attrs is None:
             cls.dynamic_attrs = {attr_name: attr for attr_name, attr in cls.__dict__.items() 
                                  if isinstance(attr, DynamicAttribute)}
        for attr_name, attr in cls.dynamic_attrs.items():
            value = attr.get_value(tag)
            if not value:
                raise AttributeError()
            result[attr_name] = value
        return result

    def __init__(self, parent) -> None:
        self.parent: HtmlNode|None = parent
        self.soup: BeautifulSoup|None = None

    def set_soup(self, soup: BeautifulSoup):
        self.soup = soup

    def delete_soup(self):
        self.soup = None
