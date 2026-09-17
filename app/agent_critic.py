from app.agent_base import Agent
from app.llm_client import query_ollama
from app.utils import build_prompt

class CriticAgent(Agent):
    instruction = "Rispondi in modo critico e conciso, evidenzia contraddizioni, debolezze o rischi. Usa massimo 2 frasi brevi"

    def generate_response(self, message: str, user_input: str) -> str:
        prompt = build_prompt(
            system_prompt=self.system_prompt,
            user_input=user_input,
            message=message,
            instruction=self.instruction
        )
        return query_ollama(prompt)
