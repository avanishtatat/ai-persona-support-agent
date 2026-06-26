# ResolveAI – AI Customer Support Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Gemini](https://img.shields.io/badge/Google-Gemini-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![ChromaDB](https://img.shields.io/badge/Vector%20DB-ChromaDB-5A67D8)](https://www.trychroma.com/)

ResolveAI is a Retrieval-Augmented Generation (RAG) customer support assistant that answers user queries using a custom knowledge base, identifies the user's persona, adapts response tone, and escalates low-confidence queries to human support.

It is built with Google Gemini, ChromaDB, LangChain text splitting, and Streamlit. The project demonstrates practical AI engineering concepts such as document ingestion, semantic search, embeddings, persona classification, grounded response generation, and escalation handling.

## Key Highlights 🚀

- Built a RAG pipeline to retrieve relevant answers from PDF and Markdown knowledge base documents
- Used ChromaDB for vector storage and semantic search
- Implemented persona classification for Technical Expert, Frustrated User, and Business Executive users
- Generated context-aware responses using Google Gemini
- Added confidence-based escalation when retrieved context is insufficient
- Created a Streamlit interface for testing support queries interactively
- Implemented reusable retry handling with exponential backoff for improved resilience against temporary AI service failures

## Features ✨

- Retrieval-Augmented Generation (RAG)
- Customer persona classification:
	- Technical Expert
	- Frustrated User
	- Business Executive
- Adaptive response generation by persona
- Human escalation for low-confidence retrieval
- Semantic search with embeddings
- Gemini Embedding Model integration
- ChromaDB vector database
- Automatic document loading and vector DB initialization
- Supports `.md`, `.txt`, and `.pdf` knowledge documents
- Automatic chunking with LangChain text splitters
- Streamlit web interface
- Automatic retry with exponential backoff for temporary AI service failures

## Tech Stack 🧰

| Category | Tools |
|---|---|
| Language | Python |
| LLM | Google Gemini API |
| Embeddings | Gemini Embedding Model |
| Vector Store | ChromaDB |
| Framework/UI | Streamlit |
| Document Processing | LangChain, PyPDF |
| Configuration | python-dotenv |

## Architecture 🏗️

The pipeline follows a complete RAG workflow with persona-aware generation:

```mermaid
flowchart TD
		A[Knowledge Base Documents] --> B[Document Loader]
		B --> C[Text Chunking]
		C --> D[Embedding Generation]
		D --> E[ChromaDB Vector Store]

		F[User Query] --> G[Persona Classification]
		G --> H[Semantic Retrieval]
		E --> H
		H --> I[Adaptive Response Generation]
		I --> J{Low Confidence?}
		J -- No --> K[Final Response]
		J -- Yes --> L[Human Escalation]
```

### RAG Pipeline Summary

1. Knowledge documents are loaded from the local data source.
2. Documents are split into optimized chunks for retrieval quality.
3. Chunks are embedded using Gemini embeddings and stored in ChromaDB.
4. A user query is classified into a persona.
5. Top relevant chunks are retrieved semantically from ChromaDB.
6. Gemini generates a persona-adaptive answer grounded in retrieved context.
7. If retrieval confidence is low, the assistant triggers human escalation.

## Project Structure 📁

```text
customer-support-agent/
|
|-- app.py
|-- requirements.txt
|-- README.md
|-- .env.example
|-- data/
|-- screenshots/
|-- src/
|   |-- ai_utils.py
|   |-- config.py
|   |-- rag_pipeline.py
|   |-- vector_store.py
|   |-- classifier.py
|   \-- generator.py
```

<details>
<summary><strong>File Responsibilities</strong></summary>

| File | Responsibility |
|---|---|
| `app.py` | Streamlit entry point; handles user interaction and app flow |
| `requirements.txt` | Python dependencies for local/dev/deployment setup |
| `README.md` | Project documentation |
| `.env.example` | Template for environment variable configuration |
| `data/` | Knowledge base source files (`.md`, `.txt`, `.pdf`) used for retrieval |
| `screenshots/` | UI and result screenshots for documentation |
| `src/ai_utils.py` | Shared utilities for AI retry handling, exponential backoff, and temporary error detection |
| `src/config.py` | Centralized configuration (paths, model names, constants) |
| `src/rag_pipeline.py` | End-to-end orchestration of the RAG workflow |
| `src/vector_store.py` | ChromaDB initialization, indexing, and retrieval operations |
| `src/classifier.py` | Persona classification logic for incoming user queries |
| `src/generator.py` | Persona-aware response generation and escalation handling |

</details>

## Installation ⚙️

1. Clone the repository

```bash
git clone https://github.com/avanishtatat/ai-persona-support-agent.git
cd ai-persona-support-agent
```

2. Create a virtual environment

```bash
python -m venv .venv
```

3. Activate the environment

```bash
# macOS/Linux
source .venv/bin/activate

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

4. Install dependencies

```bash
pip install -r requirements.txt
```

5. Configure environment variables

```bash
cp .env.example .env
```

6. Run the Streamlit app

```bash
streamlit run app.py
```

> **Note**
>
> ResolveAI builds a local ChromaDB vector store from the knowledge-base documents during startup when no existing collection is found. The generated `chroma_db/` directory is ignored from Git because ChromaDB persistence files may not be portable across deployment environments.

## Environment Variables 🔐

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | Yes | API key for accessing Google Gemini LLM and embedding services |

## Deployment 🌐

This application is deployed on **Streamlit Community Cloud** and uses a persistent ChromaDB vector store for fast document retrieval.

- Live App: `https://ai-persona-support-agent-ja2ydakgcx4sla3gpzyczh.streamlit.app/`

## Demo Video 🎥

- YouTube Demo: [https://youtu.be/ZkDUmtsF4rA](https://youtu.be/ZkDUmtsF4rA)

## Screenshots 🖼️

![Deployed Home](screenshots/deployed-home.png)
![Successful Response](screenshots/successful-response.png)
![Escalation Handoff](screenshots/escalation-handoff.png)
![Technical Expert Response](screenshots/technical-expert-response.png)

## Example Queries 💬

| Persona | Sample Query |
|---|---|
| Technical Expert | Why am I getting a 401 Unauthorized error when calling the API? |
| Frustrated User | I forgot my password and I am not receiving the OTP. |
| Business Executive | Our client delivery is delayed because users cannot log in. |

## Future Improvements 🔭

- Better confidence scoring for retrieval quality
- Conversation memory for multi-turn context
- User authentication and role-based access
- Admin dashboard for support insights
- Feedback collection loop for continuous improvement
- Multi-language support
- Larger, domain-specific knowledge base
- Persistent conversation history and analytics

## Author 👤

- GitHub: `https://github.com/avanishtatat`
- LinkedIn: `https://linkedin.com/in/avanishtiwari18`
- Portfolio: `https://avanishtiwari.vercel.app`


