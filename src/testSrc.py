from classes import User
from models.WordModel import WordModel
from models.UserModel import UserModel

if __name__ == '__main__':
    print("hello")
    user_model = UserModel()
    word_model = WordModel()
    Marko = User("markomihajlovicfm@gmail.com")
    wl = user_model.get_word_list_view(Marko)
