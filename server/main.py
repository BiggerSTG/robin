from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.app.services import services_routes
from server.app.auth import auth_routes
import os
from dotenv import load_dotenv
from app.services.parallel_query import process_query

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


#Root Endpoint
@app.get('/')
def root():
    return {"message": "Fast API is running"}


#API routes
app.include_router(services_routes.router, prefix="/api/content", tags=["API"])
app.include_router(auth_routes.router, prefix="api/auth", tags=["Auth"])


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)