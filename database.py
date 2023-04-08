from rockset import Client, Q, F
from config import config
from pathlib import Path
from os import path
from requests import post

class Queries():
    def __init__(self, rs):
        self.rs = rs
        self.dir = path.join(Path(__file__).parent, "queries")
        
    def get(self, query_name):
        return open(path.join(self.dir, f"{query_name}.sql"), "r").read()
    
    def build(self, query_text, params):
        for name in params:
            value = params[name]
            query_text = query_text.replace(f":{name}", value.__str__())
        return query_text
        
    def execute(self, query_name, params):
        # cannot use api wrapper because query params of type lists
        # not implemented 
        return self.rs.sql(Q(self.build(self.get(query_name), params)))

class Db():
    def __init__(self):
        self.rs = Client(api_key=config["rockset"]["api_key"])
        self.workspace = config["rockset"]["workspace"]
        self.collection = config["rockset"]["collection"]
        self.queries = Queries(self.rs)
    
    def addEmbeddings(self, embeddings, text):
        try:
            self.rs.Collection.add_docs(
                self.collection, 
                [{**i, **{"text": text}} for i in embeddings["data"]],
                workspace=self.workspace
            )
        except KeyError as e:
            print(embeddings)
            raise e
    
    def getClosestResponseText(self, question_embedding):
        return self.queries.execute("getAnswer", {
            "location": f"{self.workspace}.{self.collection}",
            "question_embedding": question_embedding
        })[0]["text"]