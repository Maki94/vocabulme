import tweepy
from settings import TWITTER_API
from classes import TwitterExample, Word


class TwitterAPI:
    consumer_key = TWITTER_API['consumer_key']
    consumer_secret = TWITTER_API['consumer_secret']

    access_token = TWITTER_API['access_token']
    access_token_secret = TWITTER_API['access_token_secret']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    def get_tweets(self, word: Word, count: int) -> TwitterExample:
        searched_tweets = self.api.search(q=word.name, count=count)

        tweets = [status.text for status in searched_tweets]

        return TwitterExample(word, tweets)
        # for status in searched_tweets:
        #     print(status.text)
