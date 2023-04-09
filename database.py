from rockset import Client, Q, F
from config import config
from pathlib import Path
from os import path
from requests import post

class Query():
    def __init__(self, rs, query_name):
        self.rs = rs
        self.dir = path.join(Path(__file__).parent, "queries")
        self.query_name = query_name
        
    @staticmethod
    def build(query_text, params):
        for name in params:
            value = params[name]
            query_text = query_text.replace(f":{name}", value.__str__())
        return query_text
    
    def get(self):
        return open(path.join(self.dir, f"{self.query_name}.sql"), "r").read()
        
    def execute(self, params):
        # cannot use api wrapper because query params of type lists
        # not implemented 
        return self.rs.sql(Q(Query.build(self.get(), params)))

class Db():
    def __init__(self):
        self.rs = Client(api_key=config["rockset"]["api_key"])
        self.workspace = config["rockset"]["workspace"]
        self.collection = config["rockset"]["collection"]
    
    def add_embeddings(self, embeddings, text):
        try:
            self.rs.Collection.add_docs(
                self.collection, 
                [{**i, **{
                    "text": text, 
                    "_id": str(hash(text))
                }} for i in embeddings["data"]],
                workspace=self.workspace
            )
        except KeyError as e:
            raise e
    
    def get_context(self, question_embedding):
        print(Query(self.rs, "getAnswer").execute({
            "location": f"{self.workspace}.{self.collection}",
            "question_embedding": question_embedding
        }))
        return [i["text"] for i in Query(self.rs, "getAnswer").execute({
            "location": f"{self.workspace}.{self.collection}",
            "question_embedding": question_embedding
        })]