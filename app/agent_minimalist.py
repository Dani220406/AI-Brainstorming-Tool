from app.agent_base import Agent
from app.llm_client import query_ollama
from app.utils import build_prompt

class MinimalistAgent(Agent):
    instruction = "Rispondi con una proposta o valutazione essenziale, puntando alla semplicità e al minimalismo. Usa massimo 2 frasi brevi."

    def generate_response(self, message: str, user_input: str) -> str:
        prompt = build_prompt(
            system_prompt=self.system_prompt,
            user_input=user_input,
            message=message,
            instruction=self.instruction
        )
        return query_ollama(prompt)
