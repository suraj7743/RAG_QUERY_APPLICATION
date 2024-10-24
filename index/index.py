
from  extract_data.extract_data import SearchProvider
import os
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext,load_index_from_storage
from llama_index.core import PromptTemplate
from llama_index.core.query_engine import RetrieverQueryEngine



BASE_DIR = "index_store"

def create_and_save_index(field):
    try:
        search = SearchProvider()
        nodes = search.return_nodes(field, 20)
        
        if not nodes:  # Check if nodes are empty
            raise ValueError("No nodes found for the provided field.")
        
        persist_dir = os.path.join(BASE_DIR, field)

        # Create the directory if it does not exist
        os.makedirs(persist_dir, exist_ok=True)

        # Create the vector index
        index = VectorStoreIndex(nodes)

        # Save the index to disk
        index.storage_context.persist(persist_dir=persist_dir)
        retriever = index.as_retriever()
        return retriever
    except Exception as e:
        print(f"Error in create_and_save_index: {str(e)}")
        raise  # Re-raise to bubble up the exception


def check_index_return_true_if_exists(field):
    persist_dir = os.path.join(BASE_DIR, field)
    if not os.path.exists(persist_dir):
        return False
    else:
        return True


def load_index(field):
    # Create the directory path for the field
    persist_dir = os.path.join(BASE_DIR, field)
    storage_context = StorageContext.from_defaults(persist_dir=persist_dir)

    # Create a storage context and load the index
    index = load_index_from_storage(storage_context)
    
    print(f"Index for '{field}' loaded from {persist_dir}.")
    retriever = index.as_retriever()
    return retriever


def create_query_engine(field):
        if check_index_return_true_if_exists(field=field):
            retriever=load_index(field=field)
        else:
            retriever=create_and_save_index(field=field)
        
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


