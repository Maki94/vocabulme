from API.WikipediaAPI import WikipediaAPI
from models.ExampleTwitterModel import ExampleTwitterModel
from models.WordModel import WordModel

if __name__ == '__main__':
    word_model = WordModel()
    words = word_model.get_words(12)

    # for word in words:
    #     exampleTwitterModel = ExampleTwitterModel()
    #     tweets = exampleTwitterModel.get_examples(word.name)
    #     for tweet in tweets:
    #         print(tweet)
    for word in words:
        contents = WikipediaAPI.get_content(word.name, 2)
        print("\n\nWORD:\t", word, "\n")
        if contents:
            for content in contents:
                print("\n")
                print("title:\t", content[0], "\n")
                print("categories:\t", content[1], "\n")
                print("content:\t", content[2], "\n")
