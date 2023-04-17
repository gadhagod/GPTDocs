# GPTDocs
An AI that crawls a website and allows you to ask questions regarding its content.

## Setup
### Dependencies
Dependencies can be installed with `pip`.

    python3 -m pip install -r requirements.txt

### Database Configuration
[Create a Rockset collection](https://rockset.com/docs/collections/) with its input source set to the [Write API](https://rockset.com/docs/write-api).

Place the name of your Rockset API key, collection, and its workspace, in `config.json`:

```json
{
    "rockset": {
        "workspace": "<workspace name>",
        "collection": "<collection name>",
        "api_key": "<api key>"
    }
}
```

### OpenAI Configuration
Create an OpenAI [API key](https://platform.openai.com/account/api-keys) and place it in `config.json`.

```json
{
    "openai": {
        "api_key": "<api key>"
    }
}
```

Now, you are ready to test the project. Skip to [#training] if you want to test the project on GitHub documentation. 

However, if you want to crawl a different site, you must configure the crawler.

### Crawler Configuration
By default, the crawler is set to crawl `docs.github.com`, but you can set the links to crawl in `config.json`. The `start_urls` key should be a list of links to start crawling from. The `allowed_domains` consists of the domains that are allowed to be crawled. Here is an example configuration to crawl GitHub docs:

```
{
    "start_urls": ["https://docs.github.com/en"],
    "allowed_domains": ["docs.github.com"]
}
```

Starting from links in `start_urls`, the crawler will scrape the page and all the links it refers to, so long as it has a domain listed in `allowed_domains`. 

In `config.py`, you can set more specific filters to accept and reject links. The `is_allowed` variable defined `config.py` refers to a function that takes in a link that must evaluate to `True` if the link should be crawled.

To accept all links, set the following variables in `config.py`

```python
is_allowed = lambda url : True   # all urls are allowed
```

However, often times we want to set restrictions on what should be crawled. With the example of crawling GitHub docs, we only want to crawl the english version of the docs. So, we set `is_allowed` as follows:

```python
# The URL must start with https://docs.github.com/en
is_allowed = lambda url : url.startswith("https://docs.github.com/en")
```

But we also want to skip `https://docs.github.com/enterprise` links, because they are not documentation but still start with `https://docs.github.com/en`. We can tighten the crawler restrictions like so:

```python
is_allowed = lambda url : url.startswith("https://docs.github.com/en") and not url.startswith("https://docs.github.com/enterprise")
```

### Training
Train the model by running `main.py` with the `--train` flag. This will crawl the site at config.json and load the embeddings into your collection.

```bash
python3 main.py --train
```

## Execution
`main.py` will repeatedly ask you to input your question to check the documentation for. To ask a question, run the program without the `--train` flag.

```bash
python3 main.py
```