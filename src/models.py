import re
import string
import urllib.request

import bs4 as bs

from classes import Word, User
from models.UserModel import UserModel
from models.WordModel import WordModel


def fill_db():
    url = "https://www.easypacelearning.com/english-books/the-big-list-of-a-to-z-of-words/473-word-list-a-with-brief-definitions"
    dom = "https://www.easypacelearning.com/"
    url_list = list()

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

    for fullWord in word_list:
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


if __name__ == "__main__":
    # fill_db()

    userModel = UserModel()
    _email = "marko@gmail.com"
    # userModel.create(User(email=_email, password="Hello"))

    user = userModel.get(User(email=_email))
    wordModel = WordModel()
    wordName = "Abduction"
    word = wordModel.get(Word(name=wordName, label="", definition=""))

    print(user.email, user.password, "\n")
    print(word.name, word.label, word.definition)

    new_user_model = UserModel()
    new_user_model.seen_word(user, word)
