import os
from openai import AzureOpenAI
from config import ENDPOINT_URL, DEPLOYMENT_NAME, AZURE_OPENAI_API_KEY

# Initialize Azure OpenAI Service client
client = AzureOpenAI(
    azure_endpoint=ENDPOINT_URL,
    api_key=AZURE_OPENAI_API_KEY,
    api_version="2024-05-01-preview",
)

def ask_gpt(question: str):
    """Handles queries to Azure OpenAI GPT"""
    try:
        messages = [{"role": "user", "content": question}]
        completion = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=messages,
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return {"response": completion.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}


def get_personalized_recommendation(topic: str, goal: str):
    """Generates a personalized learning plan using Azure OpenAI."""
    try:
        messages = [
            {"role": "system", "content": "You are an AI tutor that helps users learn effectively."},
            {"role": "user", "content": f"I want to learn {topic} and my goal is {goal}. Can you provide a personalized study plan?"}
        ]

        completion = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=messages,
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
        )
        return {"recommendation": completion.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

def generate_quiz(topic: str):
    """Generates a multiple-choice quiz based on the given topic."""
    try:
        prompt = f"Generate a multiple-choice quiz on {topic} with 3 questions. Each question should have 4 options (A, B, C, D) and the correct answer labeled."
        # Call Azure OpenAI or other AI service to generate the quiz
        messages = [{"role": "user", "content": prompt}]
        completion = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=messages,
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return {"quiz": completion.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}
