from sys import argv
from time import sleep
from gpt import Embeddings, Completions
from database import Db
from scraper import RocksetDocs

db = Db()
embeddings = Embeddings()
completions = Completions()

def train():
    print("Crawling website...")
    page = RocksetDocs()

    print("Adding embeddings to database...")
    i = 1
    sectionsNum = len(page.sections)
    for section in page.sections:
        sleep(0.5) # because of openai rate limiting
        embeddingData = embeddings.create(section)
        if "data" not in embeddingData.keys():
            raise Exception(embeddingData["error"]["message"])
        db.addEmbeddings(embeddingData, text=section)
        print(f"Embeddings added: {i}/{sectionsNum}", end="\r")
        i = i + 1
        
    print(f"\nAll {sectionsNum} embeddings generated from {page} added to {db.workspace}.{db.collection}")

def ask(question):
    if question:
        embedding = embeddings.create(question)["data"][0]["embedding"]
        context = db.getContext(embedding)
        print(completions.create(question, context)["choices"][0]["text"])
        #completions.create(question, context)["choices"][0]["text"]

if argv[-1] == "--train":
    train()
else:
    while True:
        ask(input("Question: "))