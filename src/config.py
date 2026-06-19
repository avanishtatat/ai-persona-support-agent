from pathlib import Path

DATA_DIR = Path('data')

SUPPORTED_EXTENSIONS = ['.txt', '.md', '.pdf']

MODEL_NAME = 'gemini-2.5-flash-lite'

CHUNK_SIZE = 400 

CHUNK_OVERLAP = 40  

CHROMA_DB_PATH = './chroma_db'

COLLECTION_NAME = 'support_documents'

EMBEDDING_MODEL_NAME = 'gemini-embedding-001'