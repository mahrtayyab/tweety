# tweety
Reverse Engineered Twitter Frontend API.

[![Downloads](https://static.pepy.tech/personalized-badge/tweety-ns?period=total&units=international_system&left_color=orange&right_color=blue&left_text=Downloads)](https://pepy.tech/project/tweety-ns)

## Installation: 
```bash
pip install tweety-ns
```

## Keep synced with latest fixes

##### **Pip might not be always updated , so to keep everything synced.**

```bash
pip install https://github.com/mahrtayyab/tweety/archive/main.zip --upgrade 
```

## A Quick Example:
```python
  from tweety import Twitter
  
  app = Twitter("session")
  
# assuming app is authenticated class instance
  
  all_tweets = app.get_tweets("elonmusk")
  for tweet in all_tweets:
      print(tweet)
```

> [!IMPORTANT] 
> Even Twitter Web Client has a lot of rate limits now, Abusing tweety can lead to `read_only` Twitter account.

Do check [FAQs](https://github.com/mahrtayyab/tweety/wiki/FAQs)

Full Documentation and Changelogs are [here](https://mahrtayyab.github.io/tweety_docs/)
