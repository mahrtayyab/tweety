from src.tweety.bot import Twitter
import json
from env import cookies


app = Twitter(cookies=cookies)
total_users = 0
for retweet in app.tweet_retweeters("1674101384390782976"):

	total_users += 1
	print(f"Usernames [{total_users}] => ", retweet["legacy"]["screen_name"])

