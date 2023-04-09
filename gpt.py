from os import getenv
from requests import post
from json import dumps
from config import config

class Api():
    def __init__(self, url):
        self.url = url
    
    def make_post(self, data):
        return post(
            self.url, 
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {config['openai']['api_key']}"
            }, 
            data=dumps(data)
        ).json()

class Embeddings(Api):
    def __init__(self):
        Api.__init__(self, "https://api.openai.com/v1/embeddings")

    def create(self, inp):
        return self.make_post({
            "input": inp,
            "model": "text-embedding-ada-002"
        })
        
class Completions(Api):
    def __init__(self):
        Api.__init__(self, "https://api.openai.com/v1/completions")
        
    def create(self, question, context):
        return self.make_post({
            "prompt": f"Answer the question based on the context below, and if the question can't be answered based on the context, say \"I don't know\"\n\nContext: {' '.join(context)}\n\n---\n\nQuestion: {question}\nAnswer:",
            "model": "ada",
            "max_tokens": 500,
            "temperature": 0
        })