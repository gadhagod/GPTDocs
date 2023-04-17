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

Do not share the contents of `config.json` with anyone!

### Training
Train the model by running `main.py` with the `--train` flag. This will crawl [https://docs.rockset.com](https://docs.rockset.com) and load the embeddings into your collection.

```bash
python3 main.py --train
```

## Execution
`main.py` will repeatedly ask you to input your question to check the documentation for. To ask a question, run the program without the `--train` flag.

```bash
python3 main.py
```