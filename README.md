# tweety
Reverse Engineered Twitter Frontend API. (Still Maintained)

### 💖 Recommended Proxy Provider

<table>
  <tr>
    <td align="center">
      <a href="https://proxy-seller.com/?utm_source=github&utm_medium=referral&utm_campaign=partner_promo&utm_term=github&partner=4YW20Q5AXMV3EV" target="_blank">
        <img src="https://mahrtayyab.github.io/proxy_seller.png" alt="CoreClaw" width="100%" />
      </a>
    </td>
  </tr>
  <tr>
    <td>
      <h3><a href="https://proxy-seller.com/?utm_source=github&utm_medium=referral&utm_campaign=partner_promo&utm_term=github&partner=4YW20Q5AXMV3EV">ProxySeller</a> — Buy Private Socks5, HTTPs & Residential Proxies (Use code TWEETY for 15% off)</h3>
      <p>
        <a href="https://proxy-seller.com/?utm_source=github&utm_medium=referral&utm_campaign=partner_promo&utm_term=github&partner=4YW20Q5AXMV3EV">
          👉 <b>Get 15% OFF</b>
        </a>
      </p>
    </td>
  </tr>
</table>

[![Downloads](https://static.pepy.tech/personalized-badge/tweety-ns?period=total&units=international_system&left_color=orange&right_color=blue&left_text=Downloads)](https://pepy.tech/project/tweety-ns) [![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/mahrtayyab/tweety)

## Installation: 
```bash
pip install tweety-ns
```

## Keep synced with latest fixes

##### **Pip might not be always updated , so to keep everything synced.**

```bash
pip install https://github.com/mahrtayyab/tweety/archive/main.zip --upgrade 
```

---


## A Quick Example:
```python
    from tweety import TwitterAsync
    import asyncio
    
    async def main():
    
        app = TwitterAsync("session")  
        all_tweets = await app.get_tweets("elonmusk")
        for tweet in all_tweets:
            print(tweet)

    asyncio.run(main())
```

> [!IMPORTANT] 
> Even Twitter Web Client has a lot of rate limits now, Abusing tweety can lead to `read_only` Twitter account.

Do check [FAQs](https://github.com/mahrtayyab/tweety/wiki/FAQs)

Full Documentation and Changelogs are [here](https://mahrtayyab.github.io/tweety_docs/)
