from flask import Flask, render_template, request
from gpt import Completions

class Server(Flask):
    def __init__(self, db, embeddings):
        Flask.__init__(self, __name__)
        self.db = db
        self.embeddings = embeddings
        self.completions = Completions()
        self.add_url_rule("/", view_func=lambda : render_template("index.jinja"))
        self.add_url_rule("/", view_func=self.get_answer, methods=["POST"])

    def get_answer(self):
        if "question" not in request.form.keys():
            return {"response": "", "message": "Please specify question"}, 400
        
        question = request.form["question"]
        embedding = self.embeddings.create(question)["data"][0]["embedding"]
        context = self.db.get_context(embedding)
        return {"response": self.completions.create(question, context)["choices"][0]["text"]}