import tweepy
import wikipedia
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import StreamListener

consumer_key = "AZj9yZQEt9sUqBFG5yjUHXJNd"
consumer_secret = "IQkVWKw1SvXq6C252BJhBKzrV6wlKvNqjaWfIsDMf3w63MywTl"

access_token = "4865456854-gCGNWnlI1DtK0LysTN77XFepdOywhLTRpe2Jtoy"
access_token_secret = "I29yUTUSzSHBr8ygaB29G0Upa50x1BCgrIi01fYJrAsp2"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

print(api.me().name)


class StdOutListener(StreamListener):
    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    query = 'python'
    max_tweets = 10
    # searched_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]
    # searched_tweets = search_results = api.search(q="Abbot", count=10)

    # for status in searched_tweets:
    #     print(status.text)

    # print(wikipedia.summary("Wikipedia"), "\n")
    items = wikipedia.search("Abbot")
    page = wikipedia.page(items[0])
    print(page.content)
    # for item in items:
    #     page = wikipedia.page(item)
    #     print(page.title, page.content, page.categories, page.url)
    # print(item)
