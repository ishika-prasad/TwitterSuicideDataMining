import tweepy

CONSUMER_KEY = "37l57S03dtkVC3bIWJBg5A2RO"
CONSUMER_SECRET = "BDkcIJv6nJHGjOwvdZShsDSzFMFGVgO2TsBbmaGrbpOMI4brAd"
ACCESS_TOKEN = "224555687-91w92eyoMcqONCQYvlkb6yNqY4AD14WAGr0UT42i"
ACCESS_SECRET = "tMvxg2e5Z4Kd1uy22RS5IeICfzHEsT8h4CI5jHfxyhl7Z"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True)

search_words = "depression"

tweets = tweepy.Cursor(api.search, q=search_words, lang="en").items(3)

for tweet in tweets:
    print(tweet.text)