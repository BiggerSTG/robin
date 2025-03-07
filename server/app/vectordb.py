import os
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from pathlib import Path

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

