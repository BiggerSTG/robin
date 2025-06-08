import os
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain.vectorstores.chroma import Chroma
from app.rag.get_embedding_function import get_embedding_function
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

#Load all the documents(page-wise) into the all_documents list
def load_documents():
    pdfs = Path("../PDFs")
    all_documents = []

    for folder in pdfs.iterdir():
        if folder.is_dir():
            print("Processing folder:", folder)
            document_loader = PyPDFDirectoryLoader(folder)
            docs = document_loader.load()
            all_documents.extend(docs)

    return all_documents

documents = load_documents()
print(f"Loaded {len(documents)} documents.")

# Split the documents into chunks for the RAG system
def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1600,
        chunk_overlap = 120,
        length_function = len,
        is_separator_regex=False
    )
    return text_splitter.split_documents(documents)

chunks = split_documents(documents)
print(f"Split into {len(chunks)} Chunks.")
print(f"Random Context: {chunks[465]}")

# Function to split the list into smaller lists of size 5461
def split_into_sublists(lst, sublist_size):
    return [lst[i:i + sublist_size] for i in range(0, len(lst), sublist_size)]

# Split the chunks list into smaller lists of size 5461
chunk_sublists = split_into_sublists(chunks, 5000)
print(f"Split into {len(chunk_sublists)} sublists.")

def add_to_chroma(chunks: list[Document]):
    CHROMA_PATH = os.getenv("CHROMA_PATH")
    # Create a new Chroma database
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())
    for chunks in chunk_sublists:
        db.add_documents(chunks)
        print(f"Added {len(chunks)} chunks to the database.")
    db.persist()

add_to_chroma(chunks)
CHROMA_PATH = os.getenv("CHROMA_PATH")
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())
print("Database loaded successfully.")
# Example query to the database
results = db.similarity_search("What is Algebra?", k=5)
print("Results:", results)