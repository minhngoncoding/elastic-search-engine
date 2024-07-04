from flask import Flask
from elasticsearch import Elasticsearch
from flask import render_template, request
import time
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


@app.route("/synonym")
def search_synonym():

    query = request.args.get('q').lower()

    response = client.search(index="synonym-index", body={
        "query": {
            "fuzzy": {
                "title": {
                    "value": query,
                    "fuzziness": 2
                }
            }
        }
    })

    result = []
    print(response)
    for data in response["hits"]["hits"]:
        title = data["_source"]["title"]
        link = data["_source"]["additional_urls"][0]
        result.append({"title": title, "link": link})

    return result

def create_synonym_index():
    # Define the settings for the new index
    settings = {
        "settings": {
            "analysis": {
                "filter": {
                    "synonym_filter": {
                        "type": "synonym",
                        "synonyms": [
                            "quick,fast",
                            "python,py"
                            # Add more synonyms here
                        ]
                    }
                },
                "analyzer": {
                    "synonym_analyzer": {
                        "tokenizer": "standard",
                        "filter": ["lowercase", "synonym_filter"]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "title": {
                    "type": "text",
                    "analyzer": "synonym_analyzer"
                }
            }
        }
    }

    # Create a new index with these settings
    client.indices.create(index="new-search-document", body=settings)

    # Reindex the data from the old index to the new one
    client.reindex({
        "source": {
            "index": "search-document"
        },
        "dest": {
            "index": "new-search-document"
        }
    })

    # Optionally, delete the old index if it's no longer needed
    # client.indices.delete(index="search-document")

@app.route("/search")
def search_autocomplete():

    query = request.args.get('q').lower()

#     index_settings = {
#     "settings": {
#         "index": {
#             "analysis": {
#                 "analyzer": {
#                     "my_analyzer": {
#                         "tokenizer": "standard",
#                         "filter": ["lowercase", "my_synonyms"]  # Apply synonym filter
#                     }
#                 },
#                 "filter": {
#                     "my_synonyms": {
#                         "type": "synonym",
#                         "synonyms": [
#                             "quick, fast",
#                             "python, py",
#                             "elasticsearch, es",
#                             "cnn, convolutional neural network"
#                         ]
#                     }
#                 }
#             }
#         }
#     },
# }
#
#     client.indices.close(index='search-document')
#     client.indices.put_mapping(
#         index="search-document",
#         body={"properties": {"title": {"type": "text", "analyzer": "my_analyzer"}}}
#     )
#     client.indices.put_settings(index="search-document", body=index_settings)
    # Define the settings for the new index
    settings = {
        "settings": {
            "analysis": {
                "filter": {
                    "synonym_filter": {
                        "type": "synonym",
                        "synonyms": [
                            "quick,fast",
                            "python,py"
                            # Add more synonyms here
                        ]
                    }
                },
                "analyzer": {
                    "synonym_analyzer": {
                        "tokenizer": "standard",
                        "filter": ["lowercase", "synonym_filter"]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "title": {
                    "type": "text",
                    "analyzer": "synonym_analyzer"
                }
            }
        }
    }
    client.indices.delete(index="new-search-document")
    # Create a new index with these settings
    client.indices.create(index="new-search-document", body=settings)
    print("here")
    client.indices.open(index='search-document')
    # Reindex the data from the old index to the new one
    # response = client.reindex(
    #     body={
    #         "source": {"index": "search-document"},
    #         "dest": {"index": "new-search-document"}
    #     }
    # )
    # print("here1")
    # Optionally, delete the old index if it's no longer needed
    # client.indices.delete(index="search-document")
    start = time.time()
    response = client.search(index="search-document", body={
        "query": {
            "match": {
                "title": query,
            }
        }
    }, size=5)

    end_time = time.time()
    print(f"Query took {end_time-start} seconds")
    result = []
    print(response)
    for data in response["hits"]["hits"]:
        title = data["_source"]["title"]
        link = data["_source"]["additional_urls"][0]
        result.append({"title": title, "link": link})

    return result


if __name__ == "__main__":

    app.run(debug=True)
