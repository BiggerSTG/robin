import asyncio
from openai import OpenAI
import ast
from dotenv import load_dotenv
from langchain.vectorstores.chroma import Chroma
from server.services.query_llm import query_llm
from server.core.get_embedding_function import get_embedding_function
from server.animation.templates.animate_text import construct_slideshow
from manim import *
import os
from collections import OrderedDict
from crewai import Crew
from server.agents.agents import media_agent, media_task
from server.agents.tools import MediaTool
from server.agents.test_kickoff import select_best_image
import re


load_dotenv()

num_slides = 5  # Default number of slides

PROMPT_TEMPLATE = """
You are an expert educational content creator specializing in Khan Academy-style video lessons. Your task is to create detailed, beginner-friendly 
PowerPoint content that can be directly converted into instructional videos. The main content is already provided and 
you have to build your course structure around it. The audience has ZERO prior knowledge of the topic.

### Pedagogical Requirements
1. **Lesson Structure**  
   - Include 1-2 real-world applications per major concept
   - Add frequent analogies ("This works like...")

2. **Content Guidelines**
   - Explain concepts based on the level mentioned in query (e.g., high-school, graduate). If not specified, choose the most appropriate based on context.
   - Use second-person language ("You'll notice...", "Your first step...")
   - Anticipate and address common misunderstandings

3. **Visual Flow**  
   - Structure each slide as a JSON object with the following keys:
     - `"title"`: Slide heading
     - `"content"`: Plain English explanation. If emphasis is needed, use Markdown-like formatting (e.g., `**important**`) that can be parsed later.
     - `"math"`: Valid LaTeX string (double-escaped) for formulas. Leave empty if no math.
     - `"image"`: Set to the image description if an image should be shown; else leave as empty string `""`
   - **You must generate exactly {num_slides} slides**, dividing the material logically and evenly across them.
   - Do **NOT** embed "(IMAGE)" or "(VISUAL)" inside `"content"` — use the dedicated `"image"` key instead.
   - Indicate animations inline in the `"content"` using the word `"ANIMATE"` as a callout where appropriate.
   - Keep all mathematical expressions in the `"math"` field only.
   - Do not include `\textbf`, `\frac`, or any LaTeX syntax in `"content"`.

Use the context provided to the best of your capabilities. The context is the actual knowledge base and educational content.
Your role is to provide the required format. So, strictly adhere to the instructions.

### Task
Using this context: {context}

Create a video-ready lesson about: {topic}

### Output Format (Strict)
{tech_specs}
"""

tech_specs = """
Return only a valid Python list of slide dictionaries:
{
    "title": "Slide Title",
    "content": "Explanation of the slide content. Use plain English and Markdown-like formatting for emphasis strictly using one of **bold**, *italic*, __underline__, and/or `teletype` (for code or other similar stuff).",
    "math": "Any LaTeX formula like \\\\frac{{a}}{{b}}. Use \\\\begin{{aligned}} for multi-line.",
    "image": "A description of the image"  # Only if an image should be shown; else use ""
}
"""


async def process_query(query):
    topics = fetch_topics(query)
    topics_list = topics.split(";")

    # Run rag_retrieval in parallel
    retrieval_tasks = [async_rag_retrieval(topic) for topic in topics_list]
    retrieved_topics = await asyncio.gather(*retrieval_tasks)

    # Run slide_generator in parallel
    content_tasks = [async_slide_generator(topic) for topic in retrieved_topics]
    contents = await asyncio.gather(*content_tasks)

    # Maintain order using OrderedDict
    topics_dict = OrderedDict(zip(topics_list, contents))
    return topics_dict

async def async_rag_retrieval(topic):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, rag_retrieval, topic)

async def async_slide_generator(prompt):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, slide_generator, prompt)

def fetch_topics(query):
    PROMPT_TEMPLATE = """
    You are a curriculum design assistant with expertise in education and educational content.
    A user has provided a chapter topic, and your task is to break it down into its core subtopics.
    For example, if the chapter topic is 'Mensuration' list the two main subtopics such as 'Cylinders'; 
    'Cones' etc. Provide a clear, semi-colon separated list of two (strictly) subtopics that 
    cover the chapter comprehensively. DO NOT over specify using brackets. Only include the sub topics in a semicolon separated list.
    Chapter Topic: {query}
    """
    final_prompt = PROMPT_TEMPLATE.format(query=query)
    print(f"Prompt for topic extraction: {final_prompt}")
    return query_llm(final_prompt)

def rag_retrieval(topic):
    CHROMA_PATH = os.getenv("CHROMA_PATH")
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())
    results = db.similarity_search(topic, k=5)
    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
    print(f"Context for topic '{topic}': {context_text}")
    return PROMPT_TEMPLATE.format(tech_specs=tech_specs, context=context_text, topic=topic, num_slides=num_slides)

def set_num_slides(new_num_slides):
    num_slides = new_num_slides

def slide_generator(prompt):
    raw_output = query_llm(prompt)

    try:
        parsed_output = ast.literal_eval(raw_output)
    except Exception as e:
        print("Error parsing LLM output:", e)
        parsed_output = [{"title": "Error", "content": raw_output}]
    return parsed_output

def markdown_to_markuptext(text):
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\*(.*?)\*", r"<i>\1</i>", text)
    text = re.sub(r"__(.*?)__", r"<u>\1</u>", text)
    text = re.sub(r"`(.*?)`", r"<tt>\1</tt>", text)
    text = re.sub(r"&", r"&amp;", text)
    return text


# Example usage
if __name__ == "__main__":
    
    query = "Frequency Distribution"
    
    result = asyncio.run(process_query(query))

    # For a combined slideshow, flatten all slides into one list
    combined_slides = []
    
    print("Generated Slides per Subtopic:")
    
    for topic, slides in result.items():
        print(f"Subtopic: {topic}")
        for slide in slides:
            print(f"  - {slide['title']}")
            combined_slides.append(slide)
    
    # Preprocess the slides for animation
    for slide in combined_slides:
        # print(slide)
        content = slide.get('content', '')

        # Convert Markdown-like formatting to Markup
        content = markdown_to_markuptext(content)
        slide['content'] = content

        # Get the best image URL
        content = slide.get('content')
        image = slide.get('image')
        if image:
            image_url = select_best_image(image)

            # Replace placeholders with the selected image URL
            slide['image'] = image_url

    print("Combined Slides", combined_slides)

    construct_slideshow(combined_slides)