from elasticsearch import Elasticsearch
from flask import Flask

es = Elasticsearch(hosts=['https://localhost:9200'])

ELASTIC_PASSWORD = "V9FIXaAZs79O7MuwjuPB0AyO"

CLOUD_ID = "elasticsearch-big-data-project:146514a5e1c942b99e9347b7af461f9d"

client = Elasticsearch(
    cloud_id=CLOUD_ID,
    basic_auth=("elastic", ELASTIC_PASSWORD)
)
client.info()