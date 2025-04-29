from fastapi import APIRouter
from services.sentiment_services import analyze_sentiment, fetch_suggestions

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "Welcome to the Sentiment Analysis API!"}

@router.get("/get_suggestions")
async def get_suggestions(query: str):
    suggestions = await fetch_suggestions(query)
    return suggestions

@router.get("/get_sentiment")
async def get_sentiment(package_id: str):
    sentiment = await analyze_sentiment(package_id)
    return sentiment
