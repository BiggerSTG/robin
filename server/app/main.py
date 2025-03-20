from crewai import Crew
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_openai import ChatOpenAI
import os
import asyncio
from dotenv import load_dotenv
from query import process_query

load_dotenv()

#Initialize FastAPI app
app = FastAPI(
    title="Robin",
    description="Teaches you everything about Math and CS",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CLIENT_URL")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/query")
def query(request: str):
    response = asyncio.run(process_query(request))
    return {"response": response}

#Root Endpoint
@app.get('/')
def root():
    return {"message": "Fast API is running"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)