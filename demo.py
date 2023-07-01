from src.tweety.bot import Twitter
import json
from env import cookies

app = Twitter(cookies=cookies)
tweet_id = "1674458209577496577"
limit = 3000

print("Scraping retweets ...")

total_users = 0
for retweet in app.tweet_retweeters(tweet_id):
	total_users += 1
	print(f"Usernames [{total_users}] => ", retweet["legacy"]["screen_name"])
	if total_users >= limit:
		break

print("Scraping likes ...")

total_users = 0
for like in app.tweet_likes(tweet_id):
	total_users += 1
	print(f"Usernames [{total_users}] => ", like["legacy"]["screen_name"])
	if total_users >= limit:
		break
