
# 2-Minute ADK: Speed Up Your Agent with Parallel Tools

[![Bo Yang](https://miro.medium.com/v2/resize:fill:32:32/1*WKkE_qokDfeRqH_x6G6Kkw.jpeg)](https://medium.com/@bo-yang-svl?source=---byline--56450c3edb64---------------------------------------)

[Bo Yang](https://medium.com/@bo-yang-svl?source=---byline--56450c3edb64---------------------------------------)

Follow

2 min read

·

Sep 17, 2025

206

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D56450c3edb64&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fgoogle-cloud%2F2-minute-adk-speed-up-your-agent-with-parallel-tools-56450c3edb64&source=---header_actions--56450c3edb64---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*Mq-ePojofm3PmRN4B729Qw.png)

In the Agent Development Kit (ADK), you can make your agent run faster by calling tools in parallel. This is especially useful when your agent needs to perform multiple tasks that don’t depend on each other.

To demonstrate this feature, let’s build an agent that helps you with investment questions. It will query real-time stock prices and perform simple calculations for you.

## Before: Run Tools Sequentially

First, we’ll build a tool that queries live stock prices by sending request to the Yahoo Finance API.

```
def get_stock_price(symbol: str) -> float:
  """Fetches the current stock price for a given ticker symbol."""
  url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
  headers = {'User-Agent': 'ADK Agent'}

  response = requests.get(url, headers=headers)
  response.raise_for_status()
  price = response.json()['chart']['result'][0]['meta']['regularMarketPrice']
  return price
```

Now, let’s define our agent and give it the `get_stock_price` tool:

```
root_agent = Agent(
    model='gemini-2.0-flash',
    name='stock_agent',
    instruction="""You help people with questions about stocks.""",
    tools=[get_stock_price],
)
```

Time to test! We’ll ask “ **I have $1000, how many shares of GOOG, NVDA, MSFT, CSCO, AAPL can I buy?”**

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*HXi0CoR--TnypKFTZ8KjzQ.png)

As you can see, the agent called `get_stock_price` five times, one for each stock symbol, and did so one after another. Since the Yahoo Finance API is fast, the total latency is 475ms, which isn’t bad. However, if you were calling an API that takes 5 seconds per request, the total latency would be 25 seconds.

## Get Bo Yang’s stories in your inbox

Join Medium for free to get updates from this writer.

Subscribe

Subscribe

Remember me for faster sign in

How can we do better?

## After: Run Tools in Parallel

For ADK to run your tools in parallel, you’ll need to declare your function as an **async function**, and use async versions of I/O libraries. In our case, we’ll use `aiohttp`. Let’s install it first:

```
pip install aiohttp
```

Next, we’ll rewrite our `get_stock_price` to be async:

```
async def get_stock_price(symbol: str) -> float:
  url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
  headers = {'User-Agent': 'ADK Agent'}
  async with aiohttp.ClientSession(headers=headers) as session:
    async with session.get(url) as response:
      response.raise_for_status()
      data = await response.json()
      price = data['chart']['result'][0]['meta']['regularMarketPrice']
      return price
```

Let’s try again with the same prompt.

Press enter or click to view image in full size

![](https://miro.medium.com/v2/resize:fit:700/1*dgGRE3iIn8YXl8vAdUZW5A.png)

This time, all five tool calls finished in about 165ms, a significant improvement over the 475ms we had earlier. This difference will become even more pronounced if you have more tools or slower APIs.

## More…

For more recommendations and details, you can consult the official documentation: [Increase tool performance with parallel execution](https://google.github.io/adk-docs/tools/performance/)

[2minuteadk](https://medium.com/tag/2minuteadk?source=---footer_tags--56450c3edb64---------------------------------------)

[Adk](https://medium.com/tag/adk?source=---footer_tags--56450c3edb64---------------------------------------)

[Genai](https://medium.com/tag/genai?source=---footer_tags--56450c3edb64---------------------------------------)

[AI Agent](https://medium.com/tag/ai-agent?source=---footer_tags--56450c3edb64---------------------------------------)

[Agent Development Kit](https://medium.com/tag/agent-development-kit?source=---footer_tags--56450c3edb64---------------------------------------)

[![Google Cloud - Community](https://miro.medium.com/v2/resize:fill:48:48/1*FUjLiCANvATKeaJEeg20Rw.png)](https://medium.com/google-cloud?source=---post_publication_info--56450c3edb64---------------------------------------)

[![Google Cloud - Community](https://miro.medium.com/v2/resize:fill:64:64/1*FUjLiCANvATKeaJEeg20Rw.png)](https://medium.com/google-cloud?source=---post_publication_info--56450c3edb64---------------------------------------)

Follow

[**Published in Google Cloud - Community**](https://medium.com/google-cloud?source=---post_publication_info--56450c3edb64---------------------------------------)

[76K followers](https://medium.com/google-cloud/followers?source=---post_publication_info--56450c3edb64---------------------------------------)

· [Last published 1 day ago](https://medium.com/google-cloud/exposing-geap-endpoints-privately-188002843481?source=---post_publication_info--56450c3edb64---------------------------------------)

A collection of technical articles and blogs published or curated by Google Cloud Developer Advocates. The views expressed are those of the authors and don't necessarily reflect those of Google.

Follow

[![Bo Yang](https://miro.medium.com/v2/resize:fill:48:48/1*WKkE_qokDfeRqH_x6G6Kkw.jpeg)](https://medium.com/@bo-yang-svl?source=---post_author_info--56450c3edb64---------------------------------------)

[![Bo Yang](https://miro.medium.com/v2/resize:fill:64:64/1*WKkE_qokDfeRqH_x6G6Kkw.jpeg)](https://medium.com/@bo-yang-svl?source=---post_author_info--56450c3edb64---------------------------------------)

Follow

[**Written by Bo Yang**](https://medium.com/@bo-yang-svl?source=---post_author_info--56450c3edb64---------------------------------------)

[437 followers](https://medium.com/@bo-yang-svl/followers?source=---post_author_info--56450c3edb64---------------------------------------)

· [1 following](https://medium.com/@bo-yang-svl/following?source=---post_author_info--56450c3edb64---------------------------------------)

Tech Lead - Agent Development Kit - Google

Follow

[Help](https://help.medium.com/hc/en-us?source=-----56450c3edb64---------------------------------------)

[Status](https://status.medium.com/?source=-----56450c3edb64---------------------------------------)

[About](https://medium.com/about?autoplay=1&source=-----56450c3edb64---------------------------------------)

[Careers](https://medium.com/jobs-at-medium/work-at-medium-959d1a85284e?source=-----56450c3edb64---------------------------------------)

[Press](mailto:pressinquiries@medium.com)

[Blog](https://blog.medium.com/?source=-----56450c3edb64---------------------------------------)

[Store](https://medium.com/store)

[Privacy](https://policy.medium.com/medium-privacy-policy-f03bf92035c9?source=-----56450c3edb64---------------------------------------)

[Rules](https://policy.medium.com/medium-rules-30e5502c4eb4?source=-----56450c3edb64---------------------------------------)

[Terms](https://policy.medium.com/medium-terms-of-service-9db0094a1e0f?source=-----56450c3edb64---------------------------------------)

[Text to speech](https://speechify.com/medium?source=-----56450c3edb64---------------------------------------)
