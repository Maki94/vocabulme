import codecs


class User:
    def __init__(self, email, password=""):
        self.email = email
        self.password = password

    def __str__(self):
        return str(self.get_dictionary())

    def get_dictionary(self):
        return {'email': self.email, 'password': self.password}


class Word:
    def __init__(self, name, label, definition):
        self.name = name
        self.label = label
        self.definition = definition

    def __str__(self):
        return str(self.get_dictionary())

    def get_dictionary(self):
        return {'name': self.name, 'label': self.label, 'definition': self.definition}


class WordView:
    def __init__(self, word: Word, definitions: list):
        self.word = word
        self.definitions = definitions

    def __str__(self):
        return str(self.get_dictionary())

    def get_dictionary(self):
        return {'word': self.word.get_dictionary(), 'definitions': self.definitions}


class WordListView:
    def __init__(self, seen_word_list, learnt_word_list, forgotten_word_list):
        self.seen_word_list = seen_word_list
        self.learnt_word_list = learnt_word_list
        self.forgotten_word_list = forgotten_word_list


class Wiki:
    def __init__(self, title: str, content: str, categories: list):
        self.title = title
        self.content = content
        self.categories = categories

    def __str__(self):
        return str(self.get_dictionary())

    def get_dictionary(self):
        return {'title': self.title, 'content': self.content, 'categories': self.categories}


class WikipediaExample:
    def __init__(self, word: Word, wikis: list):
        self.word = word
        self.wikis = wikis

    def __str__(self):
        return str(self.get_dictionary())

    def get_contents(self):
        return [wiki.content for wiki in self.wikis]

    def get_dictionary(self):
        return {'word': self.word.get_dictionary(), 'wikis': self.wikis}


class TwitterExample:
    def __init__(self, word: Word, statuses: list):
        self.word = word
        self.statuses = []
        for status in statuses:
            if isinstance(status, bytes):
                self.statuses.append(codecs.decode(status, "utf-8"))
            else:
                self.statuses.append(status)

    def __str__(self):
        return str(self.get_dictionary())

    def get_dictionary(self):
        return {'word': self.word.get_dictionary(), 'statuses': self.statuses}
