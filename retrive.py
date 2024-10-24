from llama_index.core.schema import Document
from llama_index.core import VectorStoreIndex
from llama_index.core import PromptTemplate
from llama_index.core.query_engine import RetrieverQueryEngine
from vectorstore.vectorstre import storage_context
class Retrieval:
    def __init__(self, search_words):
        self.storage_context = storage_context
        self.search_words=search_words

    def create_query_engine(self, retriever):
        """
        Create a query engine using the provided retriever.
        """
        template = (
            "Context information is below.\n"
            "---------------------\n"
            "{context_str}\n"
            "---------------------\n"
            "Given the context information "
            "Provide a thorough and explanatory overview for the answer to the query including relevant information and insights that would help someone understand this topic better.\n"
            "Query: {query_str}\n"
            "Answer: "
        )
        
        new_summary_tmpl = PromptTemplate(template)

        # Create a query engine with retriever
        query_engine = RetrieverQueryEngine.from_args(retriever, response_mode="tree_summarize")
        query_engine.update_prompts({"response_synthesizer:summary_template": new_summary_tmpl})

        return query_engine
    def query_and_run_engine(self, retriever, question):
        results = retriever.retrieve("dummy")  # Retrieve documents based on query string
        if results:
            print("Documents Retrieved")
            query_engine= self.create_query_engine(retriever=retriever)
            response = query_engine.query(question)
            return response
        else:
            return None




