from crewai import Crew
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_openai import ChatOpenAI

#Initialize FastAPI app
app = FastAPI(
    title="Robin",
    description="Teaches you everything about Math and CS",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#Root Endpoint
@app.get('/')
def root():
    return {"message": "Fast API is running"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)