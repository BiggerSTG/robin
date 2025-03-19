from openai import OpenAI
from dotenv import load_dotenv
from langchain.vectorstores.chroma import Chroma
from get_embedding_function import get_embedding_function
import os

load_dotenv()

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def process_query(query):
    final_prompt = rag_retrieval(query)
    response = query_llm(final_prompt)
    return response

def fetch_topics(query):
    #This function is used to fetch the subtopics from the query.



def rag_retrieval(query):
    # Load the vector-database
    CHROMA_PATH = os.getenv("CHROMA_PATH")

    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())
    print("Database loaded successfully.")

    # query to the database
    results = db.similarity_search(query, k=5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
    final_prompt = PROMPT_TEMPLATE.format(context=context_text, question=query)
    
    return final_prompt


def query_llm(final_prompt):
    client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=[
            {"role": "user", "content": final_prompt},
        ],
        stream=False
    )

    return response.choices[0].message.content