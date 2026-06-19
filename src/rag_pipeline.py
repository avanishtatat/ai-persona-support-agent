from src.config import DATA_DIR, SUPPORTED_EXTENSIONS 

def load_documents():
    documents = []

    for file_path in DATA_DIR.iterdir():
        if file_path.suffix not in SUPPORTED_EXTENSIONS:
            continue

        if file_path.suffix in ['.txt', '.md']:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read() 

                documents.append({'source': file_path.name, 'content': content})
        
    return documents

if __name__ == "__main__":
    docs = load_documents()
    print(f"Loaded {len(docs)} documents.")

    for doc in docs:
        print('========')
        print(f"Source: {doc['source']}")
        print(f"Content: {doc['content'][:100]}...")