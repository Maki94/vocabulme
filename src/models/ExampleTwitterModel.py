from API.DetectLanguageAPI import DetectLanguageAPI
from API.TwitterAPI import TwitterAPI
from classes import Word, TwitterExample
from config import RedisDatabase


class ExampleTwitterModel(RedisDatabase):
    api = TwitterAPI()
    label = '_twitter'

    def get_examples(self, word: Word, start=0, end=5) -> TwitterExample:
        key = word.name + self.label
        tweets = self._db.lrange(name=key, start=start, end=end)

        if not tweets:
            tweets = self.api.get_tweets(word, int((end - start) * 1.5))
            tweets.statuses = self.remove_non_en_tweets(tweets.statuses)
            self._db.lpush(key, *tweets.statuses)
        else:
            tweets = TwitterExample(word, tweets)
        return tweets

    @staticmethod
    def remove_non_en_tweets(statuses) -> list():
        new_tweets = list()
        for status in statuses:
            if DetectLanguageAPI.is_english(status):
                new_tweets.append(status)
        return new_tweets
