from crewai import Agent, Task
from langchain_openai import ChatOpenAI
#from sympy import false

from server.agents.tools import MediaTool
import os
from dotenv import load_dotenv


load_dotenv()


# Use Ollama with CrewAI
llm = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    model_name="deepseek-reasoner", 
    base_url="https://api.deepseek.com"
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
    role="Educational Media Expert",
    goal="Fetch important educational media content based on the provided query.",
    backstory="Provides accurate and relevant educational media content for enhancing presentations and learning materials.",
    llm=llm,
    tools=[media_tool],
    allow_delegation=False
)

media_task = Task(
    description="Retrieve educational media content for the following topic: {topic}.",
    expected_output="A list of educational media content including titles and download URLs for the specified topic.",
    agent=media_agent
)

#-------------------------------#
## Generator Agent
#-------------------------------#

gen_agent = Agent(
    role="Itinerary Generator Expert",
    goal="""
    Generate a comprehensive travel itinerary by merging data from weather, maps, hotels, and contextual tips.
            """,
    backstory="""
    Synthesizes live data and retrieved insights to produce a tailored last-minute trip plan.
    """,
    llm=llm,
    allow_delegation=False
)

gen_task = Task(
    description=("Combine the following data into a final itinerary: weather: {weather}, map info: {map}."),
    expected_output="A final itinerary that integrates all the components into a coherent travel plan.",
    agent=gen_agent
)