import os
from dotenv import load_dotenv

load_dotenv()

application_config = {
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
    "SERPER_API_KEY": os.getenv("SERPER_API_KEY"),
    "FIRECRAWL_API_KEY": os.getenv("FIRECRAWL_API_KEY"),
    "MONGO_URI": os.getenv("MONGO_URI"),
    "QDRANT_URL": os.getenv("QDRANT_URL"),
    "QDRANT_API_KEY": os.getenv("QDRANT_API_KEY"),
    "QDRANT_COLLECTION_NAME": os.getenv("QDRANT_COLLECTION_NAME"),
}
