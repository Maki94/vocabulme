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

    @staticmethod
    def parse_words(results) -> list:
        word_list = list()
        if results:
            for element in results.elements:
                word_name = element[0]['data']['name']
                word_definition = element[0]['data']['definition']
                word_label = WordModel().get_label(element[0]['metadata']['labels'])
                w = Word(word_name, word_label, word_definition)
                word_list.append(w)
        return word_list

    @staticmethod
    def get_number_labels(word_list):
        v = 0
        n = 0
        a = 0
        for word in word_list:
            if word.label == "Noun":
                n += 1
            elif word.label == "Verb":
                v += 1
            elif word.label == "Adjective":
                a += 1
        return [v, n, a]

    def get_next_word(self) -> list():
        try:
            n = 4
            query = """
                MATCH (n)
                WHERE rand() < 0.2
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
                match (n:Word{name:"%s", definition:"%s"}) return n limit 1
            """ % (word.name, word.definition)
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
