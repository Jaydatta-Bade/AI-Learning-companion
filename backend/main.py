import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from fastapi import FastAPI
from models.request_models import QueryRequest, LearningPreferenceRequest, QuizRequest
from services.ai_service import ask_gpt, get_personalized_recommendation, generate_quiz

app = FastAPI()

@app.post("/ask")
async def ask_gpt_api(request: QueryRequest):
    """API endpoint for AI-based responses"""
    return ask_gpt(request.question)

@app.post("/recommend")
async def recommend_learning_path(request: LearningPreferenceRequest):
    """API endpoint to get personalized learning recommendations"""
    return get_personalized_recommendation(request.topic, request.goal)

@app.post("/quiz")
async def generate_quiz_api(request: QuizRequest):
    """Generates a quiz based on the given topic."""
    return generate_quiz(request.topic)
