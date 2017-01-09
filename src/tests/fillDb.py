from models import Graph
import bs4 as bs
import urllib.request


class CreateWord(Graph):
    _label = "Word"
    _word = None

    def __init__(self, word_name, word_type, word_definition):
        if self._word is None:
            self._word = self._db.labels.create(self._label)

        word_node = self._db.nodes.create(name=word_name, type=word_type, definition=word_definition)
        self._word.add(word_node)


class FillDb:
    url = "https://www.easypacelearning.com/english-books/the-big-list-of-a-to-z-of-words/473-word-list-a-with-brief-definitions"
    dom = "https://www.easypacelearning.com/"
    urlList = list()

    def __init__(self):
        sauce = urllib.request.urlopen(url=self.url).read()
        soup = bs.BeautifulSoup(sauce, 'lxml')
        for h2 in soup.find_all('h2'):
            if h2.a:
                for a in h2.find_all('a'):
                    self.urlList.append(self.dom + a.get('href'))

    def run(self):
        word_list = list()

        for url in self.urlList:
            sauce = urllib.request.urlopen(url).read()
            soup = bs.BeautifulSoup(sauce, 'lxml')
            paragraphs = soup.find_all('p')
            for paragraph in paragraphs:
                if paragraph.strong:
                    word_list.append(paragraph.text.split(' ', 2))

        for word in word_list:
            CreateWord(word_name=word[0], word_type=word[1], word_definition=word[2])


if __name__ == "__main__":
    Graph()
    # print("All words saved")
