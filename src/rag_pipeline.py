from langchain_text_splitters import RecursiveCharacterTextSplitter 
from src.config import DATA_DIR, SUPPORTED_EXTENSIONS, CHUNK_SIZE, CHUNK_OVERLAP
from pypdf import PdfReader

def load_documents():
    documents = []
    print('DATA_DIR:', DATA_DIR.resolve())
    for file_path in DATA_DIR.iterdir():
        if file_path.suffix not in SUPPORTED_EXTENSIONS:
            continue

        if file_path.suffix == '.pdf':
            reader = PdfReader(file_path)
            content = ""

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    content += page_text + '\n'

            documents.append({'source': file_path.name, 'content': content})
        else:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read() 

                documents.append({'source': file_path.name, 'content': content})
        
    return documents

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = []

    for doc in documents:
        split_text = splitter.split_text(doc['content'])

        for i, chunk in enumerate(split_text):
            chunks.append({
                'id': f"{doc['source']}_chunk_{i}",
                'source': doc['source'],
                'chunk_index': i,
                'text': chunk
            })

    return chunks


if __name__ == "__main__":
    docs = load_documents()
    chunks = split_documents(docs)
    
    print(f"Loaded {len(docs)} documents.")
    print(f"Created {len(chunks)} chunks.")

    for chunk in chunks[:5]:
        print('========')
        print(f"Chunk ID: {chunk['id']}")
        print(f"Source: {chunk['source']}")
        print(f"Chunk Index: {chunk['chunk_index']}")
        print(f"Content: {chunk['text'][:100]}...")