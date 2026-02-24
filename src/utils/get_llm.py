from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

class LLMConfig:
    def __init__(
        self, 
        model_name: str = "llama-3.3-70b-versatile", 
        temperature: float = 0.7
    ):
        self.model_name = model_name
        self.temperature = temperature

    def get_llm(self):
        return ChatGroq(model_name=self.model_name, temperature=self.temperature)