from elasticsearch import Elasticsearch
from flask import Flask


ELASTIC_PASSWORD = "V9FIXaAZs79O7MuwjuPB0AyO"

CLOUD_ID = "elasticsearch:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvOjQ0MyRlMTVmNjdlNGEyNjg0NDY1ODdkYzZkMTI4MjBhZTkwYSRhNTllYmU0YTMxOTA0OTY0YjU1OTljNzdiY2JjNTU0NA=="

client = Elasticsearch(
    cloud_id=CLOUD_ID,
    basic_auth=("elastic", ELASTIC_PASSWORD)
)

response = client.search(index="search-document", body={
    "query": {
        "match": {
            "title": {}
        }
    }
}, size=5)

print(response)
for data in response["hits"]["hits"]:
    print(data["_source"]["title"] + " " + data["_source"]["additional_urls"][0])