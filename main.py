from sys import argv
from gpt import Embeddings
from database import Db
from server import Server
from config import config
from os import getenv
from scraper import scrape

if __name__ != "__main__": # deployment
    config["openai"]["api_key"] = getenv("OPENAI_API_KEY")
    config["rockset"]["api_key"] = getenv("ROCKSET_API_KEY")
    config["rockset"]["collection"] = getenv("ROCKSET_COLLECTION")
    config["rockset"]["workspace"] = getenv("ROCKSET_WORKSPACE")
        
embeddings = Embeddings()
db = Db()

def train():
    print("Crawling website...")
    scrape(embeddings, db)
    print(f"Embeddings generated from {config['allowed_domains']} added to {db.workspace}.{db.collection}")

if argv[-1] == "--train":
    train()
else:
    app = Server(db, embeddings)
    if __name__ == "__main__":
        app.run()