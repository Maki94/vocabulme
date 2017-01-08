from classes import User
from config import Graph
from models.WordModel import WordModel


class UserModel(Graph):
    _seen = "Seen"
    _label = "User"
    _user = None

    def create(self, user):
        user_node = self._db.nodes.create(email=user.email, password=user.password)
        user_node.labels.add(self._label)

    def update(self, user):
        person = self._db.labels.get(self._label).get(email=user.email)
        if person[0]:
            person[0].set('email', user.email)
            person[0].set('password', user.password)

    def get(self, user):
        try:
            person = self._db.labels.get(self._label).get(email=user.email)
            if person and person[0]:
                return User(person[0].properties['email'], person[0].properties['password'])
        except Exception as e:
            print(e)
        else:
            return None

    def get_node(self, user):
        try:
            person = self._db.labels.get(self._label).get(email=user.email)
            if person[0]:
                return person[0]
        except Exception as e:
            print(e)
        else:
            return None

    def is_valid(self, user):
        try:
            person = self._db.labels.get(self._label).get(email=user.email)
            if person[0]:
                return True
        except Exception as e:
            print(e)
        else:
            return False

    def seen_word(self, user, word):
        try:
            user_node = self.get_node(user)
            word_node = WordModel().get_node(word)
            user_node.relationships.create(self._seen, word_node)
        except Exception as e:
            print(e)

    def get_all(self):
        try:
            user_list = list()
            users = self._db.labels.get(self._label).all()
            for user in users:
                user_list.append(User(user.properties['email'], user.properties['password']))
            return user_list
        except Exception as e:
            print(e)
            return None
