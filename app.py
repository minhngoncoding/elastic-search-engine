from flask import Flask
from elasticsearch import Elasticsearch
from flask import render_template, request

app = Flask(__name__)


ELASTIC_PASSWORD = "V9FIXaAZs79O7MuwjuPB0AyO"

CLOUD_ID = "elasticsearch:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyRlMTVmNjdlNGEyNjg0NDY1ODdkYzZkMTI4MjBhZTkwYSRhNTllYmU0YTMxOTA0OTY0YjU1OTljNzdiY2JjNTU0NA=="

client = Elasticsearch(
    cloud_id=CLOUD_ID,
    basic_auth=("elastic", ELASTIC_PASSWORD)
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search")
def search_autocomplete():
    query = request.args.get('q').lower()

    response = client.search(index="search-document", body={
        "query": {
            "match": {
                "title": query
            }
        }
    }, size=5)

    result = []
    for data in response["hits"]["hits"]:
        title = data["_source"]["title"]
        link = data["_source"]["additional_urls"][0]
        result.append({"title": title, "link": link})

    return result


if __name__ == "__main__":
    app.run(debug=True)
