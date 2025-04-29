from google_play_scraper import reviews, search, Sort
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableSequence
from dotenv import load_dotenv
import asyncio
import re

load_dotenv()

# Updated Prompt: Ask for a sentiment score between -1 and 1
prompt = PromptTemplate(
    input_variables=["reviews"],
    template=(
        "For the following app reviews, analyze each review individually and assign a sentiment score:\n"
        "- 1 for positive,\n"
        "- 0 for neutral/mixed,\n"
        "- -1 for negative.\n"
        "Then return ONLY the average sentiment score (as a float) across all reviews.\n"
        "Reviews:\n{reviews}\n"
        "Respond with only the number (example: 0.6 or -0.2), no explanation."
    )
)

# Fetch app suggestions based on a query
async def fetch_suggestions(query: str):
    result = search(
        query,
        lang="en",
        country="us",
        n_hits=5
    )
    if not result:
        return []
    return [{"packageId": app['appId'], "name": app['title']} for app in result]

# Fetch reviews for an app
async def fetch_reviews(package_id: str):
    review_list, _ = reviews(package_id, lang='en', country='us', sort=Sort.NEWEST, count=100)
    return [review['content'] for review in review_list]

# Analyze a batch of reviews
async def analyze_reviews_batch(llm, reviews_batch: list):
    reviews_text = " ".join(reviews_batch)
    chain: RunnableSequence = prompt | llm
    result = await chain.ainvoke({"reviews": reviews_text})
    
    # Make sure you get the actual string from the response
    if isinstance(result, dict):
        response_text = result.get("text", "") or result.get("content", "")
    else:
        response_text = str(result)

    # Try to extract float from response
    try:
        score = float(re.findall(r'-?\d+\.\d+', response_text)[0])
    except Exception:
        score = 0.0  # default if parsing fails
    return score

# Main function to fetch and analyze sentiment
async def analyze_sentiment(package_id: str):
    reviews_list = await fetch_reviews(package_id)

    if not reviews_list:
        return {"message": "No reviews found", "count": 0}

    # Initialize Gemini LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0
    )

    chunk_size = 50
    review_chunks = [reviews_list[i:i+chunk_size] for i in range(0, len(reviews_list), chunk_size)]

    tasks = [analyze_reviews_batch(llm, chunk) for chunk in review_chunks]

    scores = await asyncio.gather(*tasks)

    average_score = sum(scores) / len(scores) if scores else 0.0

    return {
        "score": round(average_score, 3),
        "totalReviews": len(reviews_list)
    }
