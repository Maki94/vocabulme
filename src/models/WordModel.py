from config import Graph
from classes import Word


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
            words = list(self._db.labels.get(self._label_adjective).all())[:n-1]
            word_list = list()
            for word in words:
                word_list.append(self.node_to_class(word))
            return word_list
        except Exception as e:
            print
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