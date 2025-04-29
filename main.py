from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from controller.endpoint import router

app = FastAPI()

# Include the sentiment API router
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
app.include_router(router)

if __name__ == "__main__":
     uvicorn.run(app, host="localhost", port=8000)