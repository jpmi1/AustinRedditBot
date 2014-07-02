import praw
import json
import requests
import tweepy
import time

accessToken = "2599011378-5H8sNl69mboprX9iyWHeYUB6mSJ8oQnRfLXIpJO"
accessTokenSecret = "I77ii4vo0nX747D4kZJkc1q92f7SeWyyh0LVQdRcPaZOK"
apiKey = "WO6KobmjOVUorzTBv2GoWaMCa"
apiSecret = "OXzfbCJpvBfrJO8HzDsl0UNQs2s43iVSvHe1ZBVuoADqXtZJ4B"
SUBREDDIT = "Austin"

# gets list of titles/links from reddit and turns them
# into 140-character or less tweets
def createTweets(subreddit_name):
	#connect to reddit and convert subreddit name(string) to subreddit object
	r = praw.Reddit("Tweeting posts from " + subreddit_name)
	subreddit = r.get_subreddit(subreddit_name)

	print "connected to reddit"

	#store post urls, titles, and ids; shorten text in post if needed 
	#(leaving room for goo.gl link and hashtags)
	posts = {}
	ids = []
	for post in subreddit.get_hot(limit=20):
		title = post.title if len(post.title) < 90 else post.title[:93]+"..."
		posts[title] = post.url
		ids.append(post.id)

	print "posts retrieved"
	
	#shorten urls with goo.gl
	for post in posts:
		link = posts[post]
		posts[post] = shorten(link)

	print "links shortened"

	return posts, ids

# checks if post is a duplicate; if so, it won't be posted
# (twitter doesn't support multiple posts with the same text)
def isDuplicate(id):
	with open('posts.txt', 'r') as file:
		for line in file:
			if id in line:
				return true #yes, duplicate

	return false #no, post away

# tweets all non-duplicate posts in list
def tweetPosts(posts, ids):
	auth = tweepy.OAuthHandler(apiKey, apiSecret)
	auth.set_access_token(accessToken, accessTokenSecret)
	api = tweepy.API(auth)
	for post, id in zip(posts, ids):
		if isDuplicate(id):
			api.update_status(post+" "+posts[post]+" #austin #reddit #bot")
			with open('posts.txt', 'a') as file:
				file.write(str(id) + "\n")
			time.sleep(30)
			print "[bot] Posted:" + post+" "posts[post]
		else:
			print "[bot] duplicate post"

def main():
	tweetPosts(createPosts(SUBREDDIT))

if __name__ == '__main__':
	main()

