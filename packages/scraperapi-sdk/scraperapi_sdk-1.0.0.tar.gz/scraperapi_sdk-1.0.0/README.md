# ScraperAPI Python SDK
## Install 

```
pip install scraperapi-sdk
```


## Usage
```
from scraperapi_sdk import ScraperAPIClient

client = ScraperAPIClient("<API-KEY>")

# regular get request
content = client.get('https://amazon.com/')
# get request with premium
content = client.get('https://amazon.com/', params={'premium': True})

# post request
content = client.post('https://webhook.site/403e44ce-5835-4ce9-a648-188a51d9395d', headers={'Content-Type': 'application/x-www-form-urlencoded'}, data={'field1': 'data1'})

# put request
content = client.put('https://webhook.site/403e44ce-5835-4ce9-a648-188a51d9395d', headers={'Content-Type': 'application/json'}, data={'field1': 'data1'})

```

The `content` variable will contain the scraped page.

If you want to get the `Response` object instead of the content you can use `make_request`.

```

response = client.make_request(url=https://webhook.site/403e44ce-5835-4ce9-a648-188a51d9395d', headers={'Content-Type': 'application/json'}, data={'field1': 'data1'})
# response will be <Response [200]>
```

## Exception

```

from scraperapi_sdk import ScraperAPIClient
from scraperapi_sdk.exceptions import ScraperAPIException

client = ScraperAPIClient(
    api_key=api_key,
)
try:
    result = client.post('https://webhook.site/403e44ce-5835-4ce9-a648-188a51d9395d', headers={'Content-Type': 'application/x-www-form-urlencoded'}, data={'field1': 'data1'})
    _ = result
except ScraperAPIException as e:
    print(e.original_exception)  # you can access the original exception via `.original_exception` property.
```
