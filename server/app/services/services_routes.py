from fastapi import APIRouter
from app.services.parallel_query import process_query


router = APIRouter()


@router.post("/query")
async def query(request: str):
    """
    Endpoint to process a query and return a response.
    """
    response = await process_query(request)
    return {"response": response}