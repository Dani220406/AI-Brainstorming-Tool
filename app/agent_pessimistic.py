from app.agent_base import Agent
from app.llm_client import query_ollama
from app.utils import build_prompt

class PessimisticAgent(Agent):
    instruction = (
        "Rispondi mettendo in evidenza sempre un rischio o punto debole dell’idea in modo critico ma realistico. "
        "Non essere sarcastico. Usa massimo 2 frasi brevi."
    )

    def generate_response(self, message: str, user_input: str) -> str:
        prompt = build_prompt(
            self.system_prompt,
            user_input,
            message,
            self.instruction
        )
        return query_ollama(prompt)
