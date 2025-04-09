from crewai import Crew
from server.agents.agents import media_agent, media_task
from server.agents.tools import MediaTool
from openai import OpenAI
import os
from server.services.query_llm import query_llm


crew = Crew(
    agents=[media_agent],
    tasks=[media_task],
    process="sequential",
    verbose=True
)


def generate_image_urls(slides):
    """
    Given the context and number of placeholders found,
    call the media agent to generate 'count' queries and fetch their image URLs.
    """
    result = crew.kickoff(inputs={"topic": slides})
    result = result.raw

    queries = [line.strip() for line in result.strip().splitlines() if line.strip() != "```"]

    print(queries)

    media_tool = MediaTool()
    image_urls = []

    for query in queries:
        url = media_tool._run(query)
        image_urls.append(url)

    print(image_urls)
    return image_urls
    
def select_best_image(context):
    url_list = generate_image_urls(context)
    
    prompt = f"""
    I have the following image URLs:

    1. {url_list}

    The context is: {context}

    Based on the context
    which image URL best represents this concept? 
    Please return only the URL index from the list of url between 0 to 2.
    Example 
    input: ["url0", "url1", "url2"]
    output: 0

    You need to strictly return only the index (between 0 to 2)
    """
    
    raw_output = query_llm(prompt)
    print(raw_output)
    # print(url_list[int(raw_output)])
    return url_list[int(raw_output)]

# select_best_image("Cell division takes place for multiplication of cells and creation of new cells IMAGE")