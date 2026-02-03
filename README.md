# 🌞 Solar.Ai – Document Based Question Answering System

## 📌 Overview
**Solar.Ai** is a Flask-based chatbot that answers user questions **strictly from a given document** (`Solar System.docx`).  
It uses a **Retrieval-Augmented Generation (RAG)** approach to ensure accurate, document-grounded responses.

---

## 🧠 How It Works
1. User enters a question in the chat UI  
2. Question is sent to the Flask backend  
3. Relevant document chunks are retrieved using FAISS  
4. The LLM generates an answer **only from retrieved context**  
5. The answer is displayed in a chat-style UI  

---

## 🛠️ Tech Stack
- **Frontend**: HTML, CSS  
- **Backend**: Flask (Python)  
- **LLM**: TinyLLaMA (via Ollama)  
- **Embeddings**: `BAAI/bge-small-en-v1.5`  
- **Vector Store**: FAISS  
- **Framework**: LangChain  
- **Document Type**: `.docx`

---
