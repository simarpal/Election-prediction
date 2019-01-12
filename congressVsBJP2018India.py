import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import matplotlib.pyplot as plt
import numpy as np

class TwitterClient(object):

    def __init__(self):
        consumer_key = "6xBBCEPMnPspyu326TpmkzCGN"
        consumer_secret = "MxvbtzHp5Q8eELG4bbluq4IbHjk3kcqmVJUuu7dzilJA6TyfRt"
        access_token = "1054043104972603393-EE9nKAkNSUTc5LOZ1GTgKW4gZ22TZL"
        access_token_secret = "GTPoduOWt2si6PcsDJgsuA6CyEyevt5ZwayFul4mcjvTM"

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\ / \ / \S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):

        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count):
        '''
        function to fetch tweets and parse them.
        '''
        # empty array to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

                    # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


def main():
    # creating object of TwitterClient Class
    api = TwitterClient()

    # getting congress and bjp tweets from twitter
    congress_tweets = api.get_tweets(query='congress', count=3200)
    bjp_tweets = api.get_tweets(query='bjp', count=3200)

    # picking positive tweets from tweets
    congress_ptweets = [tweet for tweet in congress_tweets if tweet['sentiment'] == 'positive']
    bjp_ptweets = [tweet for tweet in bjp_tweets if tweet['sentiment'] == 'positive']

    # picking negative tweets from tweets
    congress_ntweets = [tweet for tweet in congress_tweets if tweet['sentiment'] == 'negative']
    bjp_ntweets = [tweet for tweet in bjp_tweets if tweet['sentiment'] == 'negative']

    # ploting graph
    n_groups = 3
    means_men = (len(congress_ptweets), len(congress_ntweets),
                 (len(congress_tweets) - len(congress_ntweets) - len(congress_ptweets)))
    std_men = (2, 3, 4)
    means_women = (len(bjp_ptweets), len(bjp_ntweets), (
            len(bjp_tweets) - len(bjp_ntweets) - len(bjp_ptweets)))
    std_women = (3, 5, 2)
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.4
    error_config = {'ecolor': '0.3'}
    rects1 = ax.bar(index, means_men, bar_width,
                    alpha=opacity, color='b',
                    yerr=std_men, error_kw=error_config,
                    label='Congress')
    rects2 = ax.bar(index + bar_width, means_women, bar_width,
                    alpha=opacity, color='r',
                    yerr=std_women, error_kw=error_config,
                    label='BJP')
    ax.set_ylabel('Tweets')
    ax.set_title('2018 India , Congress vs BJP')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(('positive tweets', 'Negative tweets', 'Neural tweets'))
    ax.legend()
    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()