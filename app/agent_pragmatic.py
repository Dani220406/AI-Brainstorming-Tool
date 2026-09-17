from app.agent_base import Agent
from app.llm_client import query_ollama
from app.utils import build_prompt

class PragmaticAgent(Agent):
    instruction = (
        "Rispondi in modo pratico e realistico, proponendo una soluzione o un'azione concreta e attuabile. "
        "Non essere astratto. Usa massimo 2 frasi brevi."
    )

    def generate_response(self, message: str, user_input: str) -> str:
        prompt = build_prompt(
            self.system_prompt,
            user_input,
            message,
            self.instruction
        )
        return query_ollama(prompt)
