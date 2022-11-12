# tweety
Twitter's API is annoying to work with, and has lots of limitations — luckily their frontend (JavaScript) has it's own API, which I reverse–engineered. No API rate limits. No restrictions. Extremely fast.

[![Downloads](https://static.pepy.tech/personalized-badge/tweety-ns?period=total&units=international_system&left_color=orange&right_color=blue&left_text=Downloads)](https://pepy.tech/project/tweety-ns)
## Prerequisites

Before you begin, ensure you have met the following requirements:

* Internet Connection
* Python 3.6+
* BeautifulSoup (Python Module)
* Requests (Python Module)
* openpyxl (Python Module)
* wget (Python Module) [Optional , you need to install it manually]

## Installation:
```bash
pip install tweety-ns
```

## A Quick Example:
```python
  from tweety.bot import Twitter
  
  app = Twitter("elonmusk")
  
  all_tweets = app.get_tweets()
  for tweet in all_tweets:
      print(tweet)
```

Full Documentation and Changelogs are [here](https://mahrtayyab.github.io/tweety_docs/)
