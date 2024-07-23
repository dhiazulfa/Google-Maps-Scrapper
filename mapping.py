from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

mapping = {
    "mappings": {
        "properties": {
            "Name": {"type": "text"},
            "Address": {"type": "text"},
            "Website": {"type": "text"},
            "Phone Number": {"type": "text"},
            "Review Count": {"type": "integer"},
            "Average Review Count": {"type": "float"},
            "Store Shopping": {"type": "text"},
            "In Store Pickup": {"type": "text"},
            "Store Delivery": {"type": "text"},
            "Place Type": {"type": "text"},
            "Opens At": {"type": "text"},
            "Introduction": {"type": "text"}
        }
    }
}

index_name = "scraped_data"
es.indices.create(index=index_name, body=mapping, ignore=400)  # Ignore error jika indeks sudah ada
