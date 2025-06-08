from crewai import Agent, Task
from langchain_openai import ChatOpenAI
from app.agents.tools import MediaTool
import os
from dotenv import load_dotenv

load_dotenv()

# Use deepseek with CrewAI
llm = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    model_name="deepseek/deepseek-chat", 
)
#-------------------------------#
#-------------------------------#
##          Agents
#-------------------------------#
#-------------------------------#

#-------------------------------#
## Media Agent
#-------------------------------#

# Initialize the Media tool
media_tool = MediaTool()


media_agent = Agent(
    role="Educational Image Query Generator",
    goal="Generate 3 extremely concise search queries (each max 4 words) based on the given slide content for educational images.",
    backstory="Specializes in creating effective, ultra-short image search queries for academic presentations.",
    llm=llm,
    tools=[media_tool],
    allow_delegation=False,
    verbose=True,
    max_iter=3
)

    
media_task = Task(
    description="""Analyze this slide content and generate 3 concise image search queries.
    Each query should be at most 4 words and on a separate line. Try keeping the queries as short as possible, preferably 2 words
    but increase or decrease between min 1 to max 4 words as and when necessary. Never cross the word limit.
    Consider:
    1. Key visual elements
    2. Abstract concept representation
    3. Educational context

    Example: If the slide is Cell division takes place for multiplication of cells and creation of new cells IMAGE
    Output: 
    mitosis process
    cell division
    cell cycle

    Slide Content: {topic}""",

    expected_output="""Three separate lines; each line is a search query (max 4 words).
    mitosis process
    cell division
    cell cycle
    """,
    agent=media_agent
)
