from sys import argv
from time import sleep
from gpt import Embeddings, Completions
from database import Db
from scraper import RocksetDocs

db = Db()
embeddings = Embeddings()
completions = Completions()

def train():
    page = RocksetDocs()

    print("Adding embeddings to database...")
    i = 1
    sectionsNum = len(page.sections)
    for section in page.sections:
        sleep(1) # because of openai rate limiting
        embeddingData = embeddings.create(section)
        db.addEmbeddings(embeddingData, text=section)
        print(f"{i}/{sectionsNum}")
        i = i + 1

def ask(question):
    embedding = embeddings.create(question)["data"][0]["embedding"]
    context = db.getContext(embedding)
    return context
    #print("\n\n\n".join(context))
    #exit()
    #return completions.create(question, context)["choices"][0]["text"]

if argv[-1] == "--train":
    train()
else:
    #train()
    while True:
        print(ask(input("Question: ")))