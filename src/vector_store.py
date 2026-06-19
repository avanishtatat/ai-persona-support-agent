import os 
from dotenv import load_dotenv
from google import genai 
import chromadb
from src.config import CHROMA_DB_PATH, COLLECTION_NAME, EMBEDDING_MODEL_NAME

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

client = genai.Client(api_key=api_key)

chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)

def get_embedding(text):
    response = client.models.embed_content(
        model=EMBEDDING_MODEL_NAME,
        contents=text
    )
    
    return response.embeddings[0].values

def add_chunks_to_vector_store(chunks):
    for chunk in chunks:
        embedding = get_embedding(chunk['text'])

        collection.add(
            ids=[chunk['id']],
            embeddings=[embedding],
            documents=[chunk['text']],
            metadatas=[{
                'source': chunk['source'],
                'chunk_index': chunk['chunk_index']
            }]
        )
    return len(chunks)

if __name__ == "__main__":
    from src.rag_pipeline import load_documents, split_documents

    docs = load_documents()
    chunks = split_documents(docs)

    num_added = add_chunks_to_vector_store(chunks)
    print(f"Added {num_added} chunks to the vector store.")



