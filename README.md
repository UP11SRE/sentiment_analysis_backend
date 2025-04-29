# Sentiment Analysis API with FastAPI and LangChain

This project provides an API for analyzing app reviews using LangChain and the Gemini 2.0-Flash model. The app get the app packageid in input and fetches latest 100 reviews from the Google Play Store, processes them using the model, and returns an average sentiment score for the given app.

## Project Setup

### Prerequisites

- Python 3.7 or above
- `uv`

### Steps to Run

1. **Clone the repository**:
   ```
   git clone https://github.com/yourusername/sentiment-analysis-api.git
   cd SENTIMENT_ANALYSIS
   cd app
   ```

2- **Install Dependencies**

```
uv pip install -r pyproject.toml
```

3- **Set Up Environment Variables**:

```
Copy the env.example file to a new .env file
```

4- **Run App**

```
uv run main.py
```

server will run on localhost:8000

## How the App Works

### Fetches app reviews:

The API takes an app's package ID (from the Google Play Store) and fetches the latest reviews for the app.

### Sentiment analysis:

The reviews are then processed by a language model (Gemini 2.0-Flash) that assigns a sentiment score for each review. The overall sentiment score for the app is then calculated and returned as an average.

### API response:

The response will include the average sentiment score, ranging from -1 (negative) to 1 (positive).

## Project Structure:

```
sentiment-analysis/
│
├── app/
│   ├── controller/
│   │   └── endpoint.py
│   ├── services/
│   │   └── sentiment_services.py
│   ├── main.py
│
├── env.example
├── .gitignore
├── python-version
├── pyproject.toml
├── uv.lock
└── README.md
```

## API's

This app expects two APIs from the backend:

### GET /get_suggestions

Description: Returns a list of app suggestions based on a query.

Example:

```
http://localhost:8000/get_suggestions?query=your_query
```

Response:

```
[
  {
    "name": "Facebook",
    "packageId": "com.facebook.katana"
  },
  {
    "name": "Facebook Lite",
    "packageId": "com.facebook.lite"
  }
]
```

### GET /get_sentiment

Description: Returns sentiment score and total number of reviews for a selected app.

Example:

```
http://localhost:8000/get_sentiment?package_id=your_package_id
```

Response:

```
{
  "score": 4.2,
  "totalReviews": 15324
}
```

### Sentiment Score Explanation:

| Score Range   | Interpretation             |
| ------------- | -------------------------- |
| `1`           | Very positive              |
| `0`           | Neutral                    |
| `-1`          | Very negative              |
| `0.2`, `-0.2` | Slightly positive/negative |

🔹 Model Used
This project uses the free-tier Gemini model, specifically Gemini 2.0 Flash, for performing sentiment analysis via LangChain.

🔹 App Review Source
To fetch app reviews from the Google Play Store, this project uses the google-play-scraper Python library.
