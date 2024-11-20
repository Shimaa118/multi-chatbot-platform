from chromadb.config import Settings
import chromadb

# Initialize Chroma Client
chroma_client = chromadb.Client(
    Settings(
        persist_directory="./chroma_data"  # Directory for persistence
    )
)
