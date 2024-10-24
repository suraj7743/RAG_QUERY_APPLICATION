from llama_index.core import StorageContext,load_index_from_storage
import SimpleDocumentStore


storage_context = StorageContext.from_defaults(persist_dir="docStore")
new_index = load_index_from_storage(storage_context)
