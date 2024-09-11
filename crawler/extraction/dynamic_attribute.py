from .locator import Locator, get_attr


class DynamicAttribute:

    def __init__(self, attr_name, locator=None) -> None:
        self.attr_name = attr_name
        self.locator:Locator|None = locator

    def get_value(self, tag):
        if self.locator:
            tags = self.locator.find_elements(tag)
            if not tags:
                return None
            else:
                tag = tags[0]
        return get_attr(tag, self.attr_name)
    
