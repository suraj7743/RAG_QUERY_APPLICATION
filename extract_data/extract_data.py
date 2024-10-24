import requests
import json
from llama_index.readers.web import FireCrawlWebReader
from llama_index.core import VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from config import application_config
from llama_index.core.schema import Document
from termcolor import colored
import http.client
from firecrawl import FirecrawlApp

import json

# global
from llama_index.core import Settings
CRED = '\033[91m'
CEND = '\033[0m'

node_parser = SentenceSplitter(chunk_size=1444, chunk_overlap=20)


class SearchProvider:
    def __init__(self):
        self.serper_api_key = application_config["SERPER_API_KEY"]
        self.firecrawl_reader = FireCrawlWebReader(
            api_key=application_config["FIRECRAWL_API_KEY"],
            mode="scrape",
            params={"additional": "parameters"},
        )

    def search_google(self, search_word, num_results):
        try:
            """
            Perform a Google search using serper.dev API and return a list of URLs.
            """
            conn = http.client.HTTPSConnection("google.serper.dev")
            payload = json.dumps({"q": search_word, "num": num_results})
            headers = {
                'X-API-KEY': self.serper_api_key,
                'Content-Type': 'application/json'
                }
            conn.request("POST", "/search", payload, headers)
            res = conn.getresponse()
            data = res.read()
            response_json = json.loads(data.decode("utf-8"))
            links = []
            if 'organic' in response_json:
                for item in response_json['organic']:
                    if 'link' in item:
                        links.append(item['link'])
            return links
        except Exception as e:
            raise Exception(f"Error searching Google: {e}")

    def download_and_extract_content(self, urls, search_term):
        """
        Download content from given URLs and return as LlamaIndex Documents.
        """
        documents = []
        for url in urls:
            try:
                original_doc = self.firecrawl_reader.load_data(url=url)
                if original_doc:
                    markdown_content = original_doc[0].get_content()
                    original_doc = original_doc[0].to_dict()

                    doc = {
                        "text": markdown_content,
                        "metadata": {
                            "original_doc": original_doc["metadata"],
                            "search_term": search_term,
                            "url": url,
                        },
                    }
                    documents.append(doc)
                else:
                    print(f"Failed to download {url}: No content retrieved")
            except Exception as e:
                print(f"Error downloading {url}: {str(e)}")
        return documents
        # return documents

    def return_nodes(self, search_word, num_results):
        """
        Perform a Google search if product in not there, download contents, and return a Query Engine.
        """
        urls = self.search_google(search_word, num_results)
        documents = self.download_and_extract_content(urls, search_term=search_word)
        llama_documents = [
            Document(text=doc["text"], metadata=doc["metadata"]) for doc in documents
        ]
        # Initialize a node parser for chunking
        nodes = node_parser.get_nodes_from_documents(
            llama_documents, show_progress=True
        )
        print("parsed documents done ")
        return nodes