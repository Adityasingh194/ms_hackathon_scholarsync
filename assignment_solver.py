import os
import re
import requests
from io import BytesIO
from pypdf import PdfReader
from dotenv import dotenv_values

# ---------------- ENV ----------------

env = dotenv_values(".env")
GROQ_KEY = env.get("GROQ_API_KEY")

CACHE_DIR = "cache"
PDF_DIR = "generated_pdfs"

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)


# ---------------- GOOGLE DRIVE LINK FIX ----------------

def convert_drive_link(url):

    match = re.search(r'/d/([a-zA-Z0-9_-]+)', url)

    if match:
        return f"https://drive.google.com/uc?export=download&id={match.group(1)}"

    match = re.search(r'id=([a-zA-Z0-9_-]+)', url)

    if match:
        return f"https://drive.google.com/uc?export=download&id={match.group(1)}"

    return url


# ---------------- DOWNLOAD PDF ----------------

def download_pdf(url):

    url = convert_drive_link(url)

    # extract real Google Drive id
    match = re.search(r'id=([a-zA-Z0-9_-]+)', url)

    if match:
        file_id = match.group(1)
    else:
        file_id = str(abs(hash(url)))

    path = f"{CACHE_DIR}/{file_id}.pdf"

    if os.path.exists(path):
        return path

    r = requests.get(url)

    with open(path, "wb") as f:
        f.write(r.content)

    return path

# ---------------- READ PDF ----------------

def load_pdf_text(path):

    reader = PdfReader(path)

    text = ""

    for page in reader.pages:
        t = page.extract_text()
        if t:
            text += t + "\n"

    return text


# ---------------- QUESTION ANSWERING ----------------

def solve_assignment(question, assignment_url, material_urls):

    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_groq import ChatGroq
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_classic.chains import create_retrieval_chain
    from langchain_classic.chains.combine_documents import create_stuff_documents_chain

    texts = []

    # assignment text
    if assignment_url:
        path = download_pdf(assignment_url)
        texts.append(load_pdf_text(path))

    # material texts
    for url in material_urls:
        try:
            path = download_pdf(url)
            texts.append(load_pdf_text(path))
        except:
            continue

    full_text = "\n".join(texts)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    docs = splitter.create_documents([full_text])

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.from_documents(docs, embeddings)

    retriever = db.as_retriever(search_kwargs={"k":4})

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        groq_api_key=GROQ_KEY,
        temperature=0
    )

    system_prompt = """
You are an expert academic assistant.

Use the provided study materials and assignment context to answer the question.

Rules:
- Give clear structured answers
- Show steps if solving problems
- Use headings if needed
- If answer not found say "Not found in materials"

Context:
{context}
"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])

    qa_chain = create_stuff_documents_chain(llm, prompt)

    rag_chain = create_retrieval_chain(retriever, qa_chain)

    result = rag_chain.invoke({"input": question})

    return result["answer"]


# ---------------- FULL ASSIGNMENT SOLVER ----------------

def solve_entire_assignment(assignment_url, material_urls):

    from langchain_groq import ChatGroq

    assignment_path = download_pdf(assignment_url)

    assignment_text = load_pdf_text(assignment_path)

    # LIMIT assignment size (important)
    assignment_text = assignment_text[:8000]

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        groq_api_key=GROQ_KEY,
        temperature=0
    )

    prompt = f"""
You are a university academic assistant.

Solve the following assignment completely.

Rules:
- Solve each question clearly
- Show steps if needed
- Provide explanations
- Structure answers properly
- Only solve the assignment below

ASSIGNMENT:

{assignment_text}
"""

    response = llm.invoke(prompt)

    return response.content


# ---------------- GENERATE SOLUTION PDF ----------------

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


def generate_solution_pdf(solution_text, assignment_id):

    file_name = f"solution_{assignment_id}.pdf"

    path = f"{PDF_DIR}/{file_name}"

    styles = getSampleStyleSheet()

    story = []

    for line in solution_text.split("\n"):
        story.append(Paragraph(line, styles["Normal"]))
        story.append(Spacer(1, 8))

    pdf = SimpleDocTemplate(path, pagesize=A4)

    pdf.build(story)

    return path