from sys import argv
from time import sleep
from gpt import Embeddings
from database import Db
from scraper import RocksetDocs
from server import Server
from config import config
from os import getenv

if __name__ != "__main__": # deployment
    config["openai"]["api_key"] = getenv("OPENAI_API_KEY")
    config["rockset"]["api_key"] = getenv("ROCKSET_API_KEY")
    config["rockset"]["collection"] = getenv("ROCKSET_COLLECTION")
    config["rockset"]["workspace"] = getenv("ROCKSET_WORKSPACE")
        
db = Db()
embeddings = Embeddings()

def train():
    print("Crawling website...")
    page = RocksetDocs()

    print("Adding embeddings to database...")
    i = 1
    sections_num = len(page.sections)
    for section in page.sections:
        sleep(0.5) # because of openai rate limiting
        embedding_data = embeddings.create(section)
        if "data" not in embedding_data.keys():
            raise Exception(embedding_data["error"]["message"])
        db.add_embeddings(embedding_data, text=section)
        print(f"Embeddings added: {i}/{sections_num}", end="\r")
        i = i + 1
        
    print(f"\nAll {sections_num} embeddings generated from {page} added to {db.workspace}.{db.collection}")

if argv[-1] == "--train":
    train()
else:
    app = Server(db, embeddings)
    if __name__ == "__main__":
        app.run()