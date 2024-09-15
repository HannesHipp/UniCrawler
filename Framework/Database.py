import json
import os
import keyring
from abc import ABC, abstractmethod

class Database(ABC):
    FILENAME = "database.json"

    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def save(self, value):
        pass

    @abstractmethod
    def get(self):
        pass


class ReadableDatabase(Database):

    def __init__(self, name):
        super().__init__(name)
        if not os.path.exists(self.FILENAME):
            with open(self.FILENAME, 'w') as file:
                json.dump({}, file)

    def save(self, value):
        with open(self.FILENAME, 'r+') as file:
            file_data = json.load(file)
            file_data[self.name] = value
            file.seek(0)
            json.dump(file_data, file, indent=4)
            file.truncate()

    def get(self):
        with open(self.FILENAME, 'r') as file:
            file_data = json.load(file)
        return file_data.get(self.name, None)


class SecureDatabase(Database):
    
    def save(self, value):
        if not isinstance(value, str):
            raise TypeError("Only strings can be stored in the secure database.")
        keyring.set_password("UniCrawler", self.name, value)

    def get(self):
        return keyring.get_password("UniCrawler", self.name)

