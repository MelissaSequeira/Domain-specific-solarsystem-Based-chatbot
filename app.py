from docx import Document
from flask import Flask, request, render_template
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

# ---------- 1. Load DOCX ----------
def load_docx(file_path):
    doc = Document(file_path)
    text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    return text

document_text = load_docx("Solar System.docx")

# ---------- 2. Split text ----------
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = text_splitter.split_text(document_text)

# ---------- 3. Embeddings ----------
embeddings = HuggingFaceBgeEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)
vectorstore = FAISS.from_texts(chunks, embeddings)

# ---------- 4. LLM ----------
llm = Ollama(model="tinyllama")  # Tiny, fast, human-like answers

# ---------- 5. Prompt ----------
template = """
You are a Solar System assistant.

You MUST answer ONLY using the context provided below.
If the answer is not clearly present in the context,
reply EXACTLY with:

"I don’t know based on the provided document."

Do NOT use any external knowledge.
Do NOT guess.
Do NOT explain beyond the document.

Context:
{context}

Question:
{question}

Answer:
"""

prompt = PromptTemplate(template=template, input_variables=["context", "question"])


# ---------- 6. QA Chain ----------
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)
,
    chain_type="stuff",  # simplest QA chain
    chain_type_kwargs={"prompt": prompt}
)

app=Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    answer=""
    if request.method=="POST":
        user_input=request.form["question"]
        answer=qa.run(user_input)
    return render_template("index.html", answer=answer)

if __name__=="__main__":
    app.run(debug=True)
