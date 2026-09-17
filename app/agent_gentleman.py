from app.agent_base import Agent
from app.llm_client import query_ollama
from app.utils import build_prompt

class GentlemanAgent(Agent):
    instruction = (
        "Rispondi con tono elegante e altamente formale, includendo un piccolo gesto tra asterischi (es. *sorride con garbo*, *si aggiusta la cravatta*). "
        "Sii cortese ma concreto. Usa massimo 2 frasi brevi."
    )

    def generate_response(self, message: str, user_input: str) -> str:
        prompt = build_prompt(
            system_prompt=self.system_prompt,
            user_input=user_input,
            message=message,
            instruction=self.instruction
        )
        return query_ollama(prompt)
