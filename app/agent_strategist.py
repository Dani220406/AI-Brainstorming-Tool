from app.agent_base import Agent
from app.llm_client import query_ollama
from app.utils import build_prompt

class StrategistAgent(Agent):
    instruction = (
        "Agisci da stratega. Trasforma quanto discusso in un piano d'azione concreto: evidenzia obiettivi, fasi operative o vincoli da considerare. "
        "Usa massimo 2 frasi brevi, con linguaggio tecnico e orientato all'esecuzione."
    )

    def generate_response(self, message: str, user_input: str) -> str:
        prompt = build_prompt(
            self.system_prompt,
            user_input,
            message,
            self.instruction
        )
        return query_ollama(prompt)
