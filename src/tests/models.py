import random

from config import Graph
from classes import Word
from neo4jrestclient import client


class WordModel(Graph):
    _label_adjective = "Adjective"
    _label_noun = "Noun"
    _label_verb = "Verb"
    _label = "Word"

    def create(self, word):
        word_node = self._db.nodes.create(name=word.name, definition=word.definition)
        word_node.labels.add([self._label, word.label])

    def get(self, word):
        try:
            word = self._db.labels.get(self._label).get(name=word.name)
            if word[0]:
                return self.node_to_class(word[0])
        except Exception as e:
            print(e)
        else:
            return None

    def get_node(self, word):
        try:
            word = self._db.labels.get(self._label).get(name=word.name)
            if word[0]:
                return word[0]
        except Exception as e:
            print(e)
        else:
            return None

    def get_words(self, n=12):
        try:
            query = """
                MATCH (n:Word)
                WHERE rand() < 0.01
                return n limit """ + str(n) + """
            """
            results = list(self._db.query(query, returns=client.Node))
            w_list = [self.node_to_class(word[0]) for word in results]
            return w_list
        except Exception as e:
            print(e)
            return None

    def get_next_word(self):
        try:
            n = 4
            query = """
                MATCH (n)
                WHERE rand() < 0.01
                return n limit """ + str(n) + """
            """
            results = list(self._db.query(query, returns=client.Node))
            word_list = [self.node_to_class(word[0]) for word in results]
            random_list1 = random.sample(range(0, n), n)
            random_list2 = random.sample(range(0, n), n)

            for i in range(n):
                temp = word_list[random_list1[i]].definition
                word_list[random_list1[i]].definition = word_list[random_list2[i]].definition
                word_list[random_list2[i]].definition = temp
                if i != 0:
                    word_list[i].name = ""
            return word_list
        except Exception as e:
            print(e)
            return None

    def node_to_class(self, word_node):
        lab = self._label
        name = word_node.properties['name']
        definition = word_node.properties['definition']

        if word_node:
            for label in word_node.labels:
                if self._label != label._label:
                    lab = label._label
        return Word(name, lab, definition)

    def is_matched(self, word):
        try:
            query = """
                match (n:Word{name:'""" + word.name + """', definition:'""" + word.definition + """'}) return n limit 1
            """
            results = list(self._db.query(query, returns=client.Node))
            if results:
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def get_label(labels) -> str:
        for label in labels:
            if WordModel._label != label:
                return label

import random
import re
import string
import urllib.request

import bs4 as bs

from classes import Word, User


def fill_db():
    url = "https://www.easypacelearning.com/english-books/the-big-list-of-a-to-z-of-words/473-word-list-a-with-brief-definitions"
    dom = "https://www.easypacelearning.com/"
    url_list = list()
    number_of_words = 100

    sauce = urllib.request.urlopen(url=url).read()
    soup = bs.BeautifulSoup(sauce, 'lxml')

    for h2 in soup.find_all('h2'):
        if h2.a:
            for a in h2.find_all('a'):
                url_list.append(dom + a.get('href'))

    word_list = list()
    for url in url_list:
        sauce = urllib.request.urlopen(url).read()
        soup = bs.BeautifulSoup(sauce, 'lxml')
        paragraphs = soup.find_all('p')
        for paragraph in paragraphs:
            if paragraph.strong:
                word_list.append(paragraph.text.split(' ', 2))

    word_model = WordModel()
    random_list = random.sample(range(0, len(word_list)), len(word_list))[:number_of_words]
    new_word_list = list()
    for i in random_list:
        new_word_list.append(word_list[i])
    print(new_word_list)

    for fullWord in new_word_list:
        lab = re.sub(r'[.]', '', fullWord[1])
        if lab == "adj":
            lab = "Adjective"
        elif lab == "n":
            lab = "Noun"
        elif lab == "v":
            lab = "Verb"
        else:
            continue
        word_class = Word(name=string.capwords(fullWord[0]), label=lab, definition=fullWord[2])
        word_model.create(word_class)

#
# if __name__ == "__main__":
#     fill_db()

    # userModel = UserModel()
    # _email = "marko@gmail.com"
    # # userModel.create(User(email=_email, password="Hello"))
    #
    # user = userModel.get(User(email=_email))
    # wordModel = WordModel()
    # wordName = "Abduction"
    # word = wordModel.get(Word(name=wordName, label="", definition=""))
    #
    # print(user.email, user.password, "\n")
    # print(word.name, word.label, word.definition)
    #
    # new_user_model = UserModel()
    # new_user_model.seen_word(user, word, False)
