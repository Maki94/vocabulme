import codecs

from API.WikipediaAPI import WikipediaAPI
from classes import Word
from config import RedisDatabase


class ExampleWikipediaModel(RedisDatabase):
    api = WikipediaAPI()
    label = '_wikipedia'

    def get_examples(self, word: Word, start=0, end=5) -> list:
        key = word.name + self.label
        contents = self._db.lrange(name=key, start=start, end=end)
        if not contents:
            wikis = self.api.get_content(word, end - start)
            if not wikis:
                return []
            contents = wikis.get_contents()
            self._db.lpush(key, *contents)
            return contents
        c = list()
        for content in contents:
            if isinstance(content, bytes):
                c.append(codecs.decode(content, "utf-8"))
            else:
                c.append(content)
        return c

    @staticmethod
    def trigger_database(word_list: list, start=0, end=5):
        try:
            w = ExampleWikipediaModel()
            for word in word_list:
                ex = w.get_examples(word, start, end)
                print(ex)
        except Exception as e:
            print(e)
