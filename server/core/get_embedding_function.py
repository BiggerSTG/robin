import vertexai
from langchain_google_vertexai import VertexAIEmbeddings
from dotenv import load_dotenv
import os
import google.auth

load_dotenv()

# Load the environment variables from .env file
project_id = os.getenv("GOOGLE_PROJECT_ID")
location = os.getenv("GOOGLE_PROJECT_LOCATION")
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_VERTEXAI")

# Load the credentials from the file
credentials, project = google.auth.load_credentials_from_file(credentials_path)

# Initialize the Vertex AI client
vertexai.init(project=project_id, location=location, credentials=credentials)

# Initialize the Vertex AI embeddings model
def get_embedding_function():
    embeddings_model = VertexAIEmbeddings(model="text-embedding-004")
    return embeddings_model

# Example usage
if __name__ == "__main__":
    embedding_function = get_embedding_function()
    print("Embedding function initialized.")