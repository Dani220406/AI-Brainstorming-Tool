from app.agent_base import Agent
from app.llm_client import query_ollama
from app.utils import build_prompt

class VisionaryAgent(Agent):
    instruction = (
        "Espandi l'idea con uno slancio creativo, immaginativo e ispirato. "
        "Offri una visione audace o futura, anche utopica o poco realistica, ma sempre con ottimismo e originalità. "
        "Usa massimo 2 frasi brevi."
    )

    def generate_response(self, message: str, user_input: str) -> str:
        prompt = build_prompt(
            self.system_prompt,
            user_input,
            message,
            self.instruction
        )
        return query_ollama(prompt)
