import os 
from dotenv import load_dotenv
from google import genai 
import chromadb
from src.config import CHROMA_DB_PATH, COLLECTION_NAME, EMBEDDING_MODEL_NAME
from src.rag_pipeline import load_documents, split_documents

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

def initialize_vector_store():
    if collection.count() > 0:
        return 
    
    documents = load_documents()
    chunks = split_documents(documents)

    add_chunks_to_vector_store(chunks)

def search_similar_chunks(query, top_k=3):
    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k 
    )

    return results 

def format_search_results(results):
    context_chunks = []

    if not results or not results['documents']:
        return context_chunks
    
    documents = results['documents'][0]
    metadatas = results['metadatas'][0]
    distances = results['distances'][0]

    for i in range(len(documents)):
        chunk_info = {
            'text': documents[i],
            'source': metadatas[i]['source'],
            'chunk_index': metadatas[i]['chunk_index'],
            'score': 1 - distances[i]
        }
        context_chunks.append(chunk_info)

    return context_chunks


if __name__ == "__main__":
    query = "I forgot my password."
    
    results = search_similar_chunks(query)

    print(f"Results for query: {results}")



