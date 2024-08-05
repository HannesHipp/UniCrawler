from abc import ABC
from bs4 import BeautifulSoup


class Filter(ABC):

    def filter_soup(self, soup:BeautifulSoup) -> list:
        pass

    def filter_list(self, list:list) -> list:
        pass


class ExactFilter(Filter):

    def __init__(self, attrs_dict:dict[str,str]) -> None:
        self.name = None
        if 'name' in attrs_dict:
            self.name = attrs_dict.pop('name')
        self.attrs_dict = attrs_dict

    def filter_soup(self, soup: BeautifulSoup):
        if not self.attrs_dict:
            return soup.find_all(self.name)
        result = soup.find_all(attrs=self.attrs_dict)
        if self.name:
            return [tag for tag in result if tag.name == self.name]
        return result
    
    def filter_list(self, soup: BeautifulSoup):
        raise Exception("ExactFilters need to be the first active filter for performance reasons.")
    

class ContainsFilter:

    def __init__(self, contains_dict) -> None:
        self.contains_dict:dict[str,str] = contains_dict

    def filter_soup(self, soup: BeautifulSoup):
        list = soup.find_all(attrs={key: True for key in self.contains_dict})
        return self.filter_list(list)

    def filter_list(self, list: list):
        return [tag for tag in list if self.tag_matches(tag)]
    
    def tag_matches(self, tag):
        for attr_name, value in self.contains_dict.items():
            tag_value = get_attr(tag, attr_name)
            if not tag_value:
                return False
            if value not in tag_value:
                return False
        return True


class Locator:

    def __init__(self, *filter, subitem_locator=None) -> None:
        self.filter:list[Filter] = filter
        self.sub_item_locator = subitem_locator

    def find_elements(self, parent_soup, scope_locator):
        if scope_locator:
            if scope_soup := scope_locator.find_elements(parent_soup, None):
                parent_soup = scope_soup[0]
        matches = self.filter[0].filter_soup(parent_soup)
        for filter in self.filter[1:]:
            matches = filter.filter_list(matches)
        if matches and self.sub_item_locator:
            matches = self.sub_item_locator.find_elements(matches[0], None)
        return matches



def get_attr(tag, attr_name):
    result = tag.get(attr_name)
    if not result and hasattr(tag, attr_name):
        result = getattr(tag, attr_name)
    if isinstance(result, list):
        result = result[0]
    return result