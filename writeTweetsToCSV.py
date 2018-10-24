"""This file is used to get tweets of accounts that you give the usernames to it. The tweets are gathered in JSON format.
So, there is a method which translate these JSONs to CSV file."""

import tweepy
import json
import csv


# Twitter API credentials
consumer_key = "ae9tTzTaK9iXBAWlqTShhf5OK"
consumer_secret = "ZPdCF92ksjidJL0tGDRQmkqxT5YTAel3v6z8wQsRCpi77wd9Da"
access_key = "837614624442822656-K2ABJVcux9TzVvEKAsQP9daxyh5tpbK"
access_secret = "AcT7X18k4lsF5cji3ZXbwZXculOT7uCpCNb7ECWGyWDsH"

# This method was gotten from the internet.
def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # Authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # Initialize a list to hold all the tweepy Tweets
    alltweets = []

    # Make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    # Save most recent tweets
    alltweets.extend(new_tweets)

    # Save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # Keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        # All subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        # Save most recent tweets
        alltweets.extend(new_tweets)

        # Update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print
        "...%s tweets downloaded so far" % (len(alltweets))


    # Write tweet objects to JSON
    fileName = 'tweets.json'
    file = open(fileName, 'w')
    file.write("[\n")
    print
    "Writing tweet objects to JSON please wait..."
    for status in alltweets:
        json.dump(status._json, file, indent=4)
        if(status != alltweets[-1]):
            file.write(", ")
    file.write("\n]")

    # Close the file
    print
    "Done"
    file.close()

# This method is Converting JSON format of tweets to the CSV file.
def json_to_csv(fileName):
    with open(fileName, 'r') as f:
        datastore = json.load(f)
        dmp = json.dumps(datastore)
        x = json.loads(dmp.replace(";", ""))
        fileName = "tweets.csv"
        f = csv.writer(open(fileName, "w+"))

        # Write CSV Header, if you don't need that, remove this line.
        # These are the features I think can be important. You can add or remove these if you want.
        f.writerow(["hashtags", "retweeted", "text", "location", "name", "screen_name"])

        #
        for tw in x:
            # These line are for hathering hashtags in one column of the CSV file.
            hashtags = tw["entities"]["hashtags"]
            hashtagsText = ""
            for h in hashtags:
                hashtagsText = hashtagsText + h["text"] + ","
            # Write the information on "tweets.csv" file.
            f.writerow([hashtagsText,
                        tw["retweeted"],
                        tw["text"],
                        tw["user"]["name"],
                        tw["user"]["location"],
                        tw["user"]["screen_name"]])


if __name__ == '__main__':
    # Pass in the username of the account you want to download
    accounts = ["@ProFinda", "@cashflows_news", "@BitNautic", "@The_IMI", "@iwoca", "@LendInvest"]
    for acc in accounts:
        get_all_tweets(acc)
    json_to_csv("tweets.json")
