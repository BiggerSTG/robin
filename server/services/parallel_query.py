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


load_dotenv()

PROMPT_TEMPLATE = """
You are an expert educational content creator specializing in Khan Academy-style video lessons. Your task is to create detailed, beginner-friendly 
PowerPoint content that can be directly converted into instructional videos. The main content is already provided and 
you have to built your course structure around it The audience has ZERO prior knowledge of the topic.

### Pedagogical Requirements
1. **Lesson Structure**  
   - Include 1-2 real-world applications per major concept
   - Add frequent analogies ("This works like...") 

2. **Content Guidelines**
   - Explain concepts based on the level mentioned in query example High-School level, graduate level, etc
   - If no level is mentioned go with the best suitable approach as of the context passed for your use
   - Use second-person language ("You'll notice...", "Your first step...")
   - Anticipate and address common misunderstandings

3. **Visual Flow**  
   - Structure content for screen recording with:
     - Left side: Visuals/diagrams (describe in parentheses)
     - Right side: Text explanations
   - Include callouts for animations/transitions where needed
     (e.g., "ANIMATE: Reveal equation parts step-by-step")
   - Where ever you would find suitable to have an image included just mention in plane english all caps IMAGE follow this convention extremely strictly
   - You strictly must not use any reference such as (IMAGE) or VISUALS or VISUALS: description of visual etc, only include the placeholder IMAGE that is it and nothing else or nothing surrounding it
Use the context provided to the best of your capabilities. The context is the actual knowledge base and educationals content, 
your role is to provide the required format. So strictly adhere to the instructions. Where ever you find it suitabel to include animage just mention 
in plane english all caps IMAGE, strictly.
{tech_specs}

### Task
Using this context: {context}

Create a video-ready lesson about: {topic}

Output ONLY the Python list of slides - no commentary.
"""

tech_specs = """
### Technical Specifications
- **Slides**: Generate as many slides as needed for complete topic coverage
- **Math Formatting**:
  - All equations in LaTeX with double-escaped backslashes
  - Complex equations split across multiple lines
  - Align equations using `\\begin{{aligned}}...\\end{{aligned}}`  <!-- Double curly braces escape for literal {}
- **Content Formatting**:
  - Use \\textbf{{}} for key terms  <!-- Proper escaping for both LaTeX and Python
  - Create lists with `\\begin{{itemize}}/\\end{{itemize}}`
  - Highlight steps with `\\texttt{{\\rightarrow}}` arrows  <!-- Nested escaping

### Example Output
[
    {
        "title": "Understanding Fractions",
        "content": "Imagine you have (IMAGE) a whole pizza. \\\\textbf{Fractions} represent parts of this whole.\\\\par\\\\smallskip Let's break it down: \\\\begin{itemize} \\\\item Numerator: How many slices you have \\\\item Denominator: Total slices in the pizza \\\\end{itemize} ANIMATE: Highlight numerator/denominator sequentially",
        "math": ""
    },
    {
        "title": "Adding Fractions",
        "content": "(VISUAL: Side-by-side fraction bars) To add fractions with \\\\textbf{same denominators}: \\\\begin{enumerate} \\\\item Keep denominator unchanged \\\\item Add numerators \\\\end{enumerate} COMMON MISTAKE: Students often add denominators too - remind them this changes the whole!",
        "math": "\\\\frac{1}{4} + \\\\frac{2}{4} = \\\\frac{1+2}{4} = \\\\frac{3}{4}"
    }
]
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
    For example, if the chapter topic is 'Mensuration' list the three main subtopics such as 'Cylinders'; 
    'Cones'; 'Spheres' etc. Provide a clear, semi-colon separated list of three (strictly) subtopics that 
    cover the chapter comprehensively. Chapter Topic: {query}
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
    return PROMPT_TEMPLATE.format(tech_specs=tech_specs, context=context_text, topic=topic)


def slide_generator(prompt):
    client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=[{"role": "user", "content": prompt}],
        stream=False
    )
    raw_output = response.choices[0].message.content
    try:
        parsed_output = ast.literal_eval(raw_output)
    except Exception as e:
        print("Error parsing LLM output:", e)
        parsed_output = [{"title": "Error", "content": raw_output}]
    return parsed_output


# Example usage
if __name__ == "__main__":
    query = "Frequency Distribution"
    result = asyncio.run(process_query(query))
    print("Generated Slides per Subtopic:")
    for topic, slides in result.items():
        print(f"Subtopic: {topic}")
        for slide in slides:
            print(f"  - {slide['title']}")
    # For a combined slideshow, flatten all slides into one list
    combined_slides = []
    # for slides in result.values():
    """ operation to pass slides to an agent that would generate the most relevant 
    max 3 worded query to fetch image url from mediatool, and then move on to
    the next step """
    
    # Get the image urls for the slide
    for slide in slides:
        # print(slide)
        content = slide.get('content', '')

        print(content)

        # Get the best image URL
        content = slide.get('content')
        if content and ("IMAGE" in content or "VISUAL" in content):
            image_url = select_best_image(slide)
            print(image_url)

            # Download image from URL if the 

            

            # Replace placeholders with the selected image URL
            slide['content'] = content.replace("IMAGE", image_url).replace("(IMAGE)", image_url).replace("VISUAL", image_url)
            print(slide)

        combined_slides.extend(slides)

    construct_slideshow(combined_slides)

    # slide = slides[0]

    # Debugging: Print slide content
    # print(slide)
    # content = slide.get('content', '')

    # print(content)

    # # Get the best image URL
    # image_url = select_best_image(slide)
    # print(image_url)

    # # Replace placeholders with the selected image URL
    # if content:
    #     slide['content'] = content.replace("IMAGE", image_url).replace("(IMAGE)", image_url).replace("VISUAL", image_url)
    #     print(slide)

    # combined_slides.append(slide)
    # print("Combined Slides", combined_slides)
    # construct_slideshow(combined_slides)
    # print(result)


# # Create a Crew to execute the task
# crew = Crew(
#     agents=[media_agent],
#     tasks=[media_task],
#     process="sequential",
#     verbose=True
# )