from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str

class LearningPreferenceRequest(BaseModel):
    topic: str
    goal: str

class QuizRequest(BaseModel):
    topic: str
