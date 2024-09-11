import os
import inspect
from importlib.machinery import SourceFileLoader
import importlib.util
from .html_node import HtmlNode


class Extractor:

    def __init__(self, model_path: str) -> None:
        types = get_type_instances(model_path)
        if 'Root' not in types:
            raise Exception('Model needs to contain Root class.')
        self.root_type:type = types['Root']

    def crawl_node(self, node: HtmlNode):
        leafs = []
        for child_type in type(node).child_types:
            child_nodes = self.extract_from_node(child_type, node)
            if child_type.is_leaf:
                leafs.extend(child_nodes)
            else:
                for child_node in child_nodes:
                    leafs.extend(self.crawl_node(child_node))
                    child_node.delete_soup()
        return leafs
    
    def extract_from_node(self, type:type[HtmlNode], node:HtmlNode) -> list[HtmlNode]:
        result = []
        canidates = type.find_canidates(node)
        for canidate in canidates:
            try:
                attrs = type.get_dynamic_attrs(canidate)
                element = type(node)
                element.set_soup(canidate.extract())
                result.append(element)
                for attr, value in attrs.items():
                    setattr(element, attr, value)
            except AttributeError:
                continue
        return result


def get_type_instances(folder_path):
    types = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".py") and not filename.startswith("__"):
            file_path = os.path.join(folder_path, filename)
            module = import_from_file(file_path)
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, HtmlNode):
                    types[name] = obj

    for _, obj in types.items():
        child_types = getattr(obj, "child_types", [])
        obj.child_types = [types[class_name] for class_name in child_types if class_name in types]

    return types

def import_from_file(file_path):
    name = ".".join(file_path.split("\\")[:-1] or [""])
    loader = SourceFileLoader(name, file_path)
    spec = importlib.util.spec_from_loader(name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod