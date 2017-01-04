import json


class User:
    def __init__(self, email, password=""):
        self.email = email
        self.password = password

    def get_dictionary(self):
        return {'email': self.email, 'password': self.password}


class Word:
    def __init__(self, name, label, definition):
        self.name = name
        self.label = label
        self.definition = definition

    def get_dictionary(self):
        return {'name': self.name, 'label': self.label, 'definition': self.definition}
