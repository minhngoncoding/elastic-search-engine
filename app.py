from flask import Flask
from elasticsearch import Elasticsearch
from flask import render_template

app = Flask(__name__)

es = Elasticsearch(hosts=['https://127.0.0.1:9200'])

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/search")
def search_autocomplete():
    return ""


if __name__ == "__main__":
    app.run(debug=True)
