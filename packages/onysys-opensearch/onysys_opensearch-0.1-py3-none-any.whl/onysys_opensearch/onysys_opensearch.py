from typing import Tuple

from opensearchpy import OpenSearch

class OnysysOpensearch():

    def __init__(self):
        self.client = OpenSearch(
            hosts = [{"host": "localhost", "port": 9200}],
            http_auth = ("admin", "admin"),
            use_ssl = True,
            verify_certs = False,
            ssl_assert_hostname = False,
            ssl_show_warn = False,
        )

    def info(self):
        response = self.client.info()
        print(str(response))
        return response

    def create_index(self, index, mapping):    
        response = self.client.indices.create(index=index, body=mapping)
        print(str(response))
        return response

    def create(self, index, id, document):
        response = self.client.index(index=index, id=id, body=document, refresh=True)
        return response

    def search(self, index: str, query: str):
        result = self.client.search(index=index, body=query)
        return result

    def count(self, index):
        self.client.indices.refresh(index=index)
        response = self.client.cat.count(index=index, format="json")
        print(str(response))
        return response

    def delete_index(self, index):
        response = self.client.indices.delete(index=index)
        print(str(response))
        return response
