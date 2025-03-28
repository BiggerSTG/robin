import asyncio
from openai import OpenAI
from dotenv import load_dotenv
from langchain.vectorstores.chroma import Chroma
from server.core.get_embedding_function import get_embedding_function
import os
from collections import OrderedDict

load_dotenv()

PROMPT_TEMPLATE = """
You are an expert teacher and educator. You are given a chapter topic and some context.
Your task is to generate a comprehensive course content that is somewhat ppt friendly and 
about a few slides long for the given chapter topic using the provided context.
The course content should be detailed and cover all the important aspects of the topic.
Use the following context to generate the course content:

{context}

---

Generate the course content for the following topic based on the above context: {topic}
"""

async def process_query(query):
    topics = fetch_topics(query)
    topics_list = topics.split(";")

    # Run rag_retrieval in parallel
    retrieval_tasks = [async_rag_retrieval(topic) for topic in topics_list]
    retrieved_topics = await asyncio.gather(*retrieval_tasks)

    # Run query_llm in parallel
    content_tasks = [async_query_llm(topic) for topic in retrieved_topics]
    contents = await asyncio.gather(*content_tasks)

    # Maintain order using OrderedDict
    topics_dict = OrderedDict(zip(topics_list, contents))
    return topics_dict

async def async_rag_retrieval(topic):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, rag_retrieval, topic)

async def async_query_llm(prompt):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, query_llm, prompt)

def fetch_topics(query):
    PROMPT_TEMPLATE = """
    You are a curriculum design assistant with expertise in education and educational content.
    A user has provided a chapter topic, and your task is to break it down into its core subtopics.
    For example, if the chapter topic is 'Mensuration' list the main subtopics such as 'Cylinders'; 'Cones'; 'Spheres' etc. Provide a clear, semi-colon separated list of the subtopics that cover the chapter comprehensively.
    Chapter Topic: {query}
    """
    final_prompt = PROMPT_TEMPLATE.format(query=query)
    return query_llm(final_prompt)

def rag_retrieval(topic):
    CHROMA_PATH = os.getenv("CHROMA_PATH")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())
    results = db.similarity_search(topic, k=5)
    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
    return PROMPT_TEMPLATE.format(context=context_text, topic=topic)

def query_llm(prompt):
    client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )
    return response.choices[0].message.content

# Example usage
if __name__ == "__main__":
    query = "Your main topic here"
    result = asyncio.run(process_query(query))
    print(result)