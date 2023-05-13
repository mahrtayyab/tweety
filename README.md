# tweety
Twitter's API is annoying to work with, and has lots of limitations — luckily their frontend (JavaScript) has it's own API, which I reverse–engineered. No API rate limits. No restrictions. Extremely fast.

[![Downloads](https://static.pepy.tech/personalized-badge/tweety-ns?period=total&units=international_system&left_color=orange&right_color=blue&left_text=Downloads)](https://pepy.tech/project/tweety-ns)
## Prerequisites

Before you begin, ensure you have met the following requirements:

* Internet Connection
* Python 3.6+
* httpx 
* openpyxl
* tqdm

## Installation: 
```bash
pip install tweety-ns
```

## Keep synced with latest fixes

##### **Pip might not be always updated , so to keep everything synced.**

```bash
pip install git+https://github.com/mahrtayyab/tweety.git --upgrade --force-reinstall
```

## A Quick Example:
```python
  from tweety.bot import Twitter
  
  app = Twitter()
  
  all_tweets = app.get_tweets("elonmusk")
  for tweet in all_tweets:
      print(tweet)
```

Full Documentation and Changelogs are [here](https://mahrtayyab.github.io/tweety_docs/)
