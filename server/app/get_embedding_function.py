from langchain_google_vertexai import VertexAIEmbeddings

def get_embedding_function():
    embeddings_model = VertexAIEmbeddings(model="text-embedding-large-exp-03-07")