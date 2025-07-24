from elasticsearch import Elasticsearch  
from dotenv import load_dotenv
import os

load_dotenv()

es_password = os.getenv("ES_PASSWORD")

new_connection = Elasticsearch(["http://localhost:9200"], basic_auth=("elastic", es_password), verify_certs=False)


class SearchInfrastructure:
    def __init__(self):
        self.connection = new_connection
        
    
    def search_record(self, search_term, index_id):
        index = f"index_hackathon_{index_id}"
        query = {
            "query": {
                "match": {
                    "recordName": {
                        "query": search_term,
                        "fuzziness": 1,
                        "operator": "and"
                    }
                }
            },
            "size": 15
        }

        response = self.connection.search(index=index, body=query)
        # Extract and return only the hits' source docs:
        hits = response.get("hits", {}).get("hits", [])
        return [hit["_source"] for hit in hits]
        
curr_inf = SearchInfrastructure()

# print(curr_inf.search_record("Jane", "726"))