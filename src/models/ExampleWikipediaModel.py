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
