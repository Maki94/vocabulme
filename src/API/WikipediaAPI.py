import wikipedia
from classes import Word, WikipediaExample, Wiki


class WikipediaAPI:
    @staticmethod
    def get_content(word: Word, count: int) -> WikipediaExample:
        wikis = []
        try:
            items = wikipedia.search(word.name)[:count]
            for item in items:
                page = wikipedia.page(item)
                wikis.append(Wiki(page.title, page.content.split('\n', 1)[0], page.categories))
        except Exception as e:
            print(e)
        else:
            return WikipediaExample(word, wikis)
