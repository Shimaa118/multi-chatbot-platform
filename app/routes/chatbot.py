from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.document_processing import process_document
from app.database import chroma_client
import os
from sentence_transformers import SentenceTransformer

# Initialize the embedder
embedder = SentenceTransformer('all-MiniLM-L6-v2')

chatbot_router = APIRouter()

# Directory to save the uploaded files
upload_dir = "uploads"
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)

@chatbot_router.post("/create")
def create_chatbot(name: str, description: str):
    # Create a collection for the chatbot
    chatbot_collection = chroma_client.get_or_create_collection(name=name)
    return {"message": f"Chatbot '{name}' created successfully"}

@chatbot_router.post("/upload_document")
async def upload_document(chatbot_name: str, file: UploadFile = File(...)):
    # Validate the file type
    if not (file.filename.endswith('.pdf') or file.filename.endswith('.txt')):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and TXT files are allowed.")

    # Save the file to the uploads directory
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Process the document (e.g., extract text, process into chunks, etc.)
    processed_chunks = process_document(file_path)

    # Add the processed chunks to the chatbot collection
    chatbot_collection = chroma_client.get_or_create_collection(name=chatbot_name)
    
    # Create unique ids for each chunk (you can customize this to your needs)
    document_ids = [f"{chatbot_name}_{i}" for i in range(len(processed_chunks))]
    
    for chunk, doc_id in zip(processed_chunks, document_ids):
        chatbot_collection.add(
            documents=[chunk], 
            metadatas={"source": "uploaded_doc"}, 
            ids=[doc_id]  # Provide the ids list here
        )

    return {"message": f"Document uploaded and processed for chatbot '{chatbot_name}'"}


@chatbot_router.post("/ask")
async def ask_chatbot(chatbot_name: str, query: str):
    try:
        # Check if the collection exists, otherwise create it
        try:
            chatbot_collection = chroma_client.get_collection(name=chatbot_name)
        except ValueError:
            chatbot_collection = chroma_client.create_collection(name=chatbot_name)

        # Generate embedding for the query and ensure it's a list of lists
        query_embedding = embedder.encode([query]).tolist()  # Convert ndarray to list of lists

        # Perform the search using the embedding
        results = chatbot_collection.query(
            query_embeddings=query_embedding, n_results=3
        )

        if not results['documents']:
            return {"message": "No relevant documents found for the query."}

        return {
            "query": query,
            "results": results
        }

    except Exception as e:
        return {"error": str(e)}
