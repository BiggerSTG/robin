from openai import OpenAI
from dotenv import load_dotenv
from langchain.vectorstores.chroma import Chroma
from get_embedding_function import get_embedding_function
import os

load_dotenv()

CHROMA_PATH = r"X:\robin\server\app\chroma_db"
db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())
print("Database loaded successfully.")
# Example query to the database
results = db.similarity_search("Explain standardized sums in detail with examples with refernce to bernoulli trials?", k=5)
#print("Results:", results)

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""
context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
final_prompt = PROMPT_TEMPLATE.format(context=context_text, question="Explain standardized sums in detail with examples with refernce to bernoulli trials?")

client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=[
        {"role": "user", "content": final_prompt},
    ],
    stream=False
)

print(response.choices[0].message.content)