from app.agent_base import Agent
from app.llm_client import query_ollama
from app.utils import build_prompt

class SummarizerAgent(Agent):
    def summarize_and_ask(self, discussion_history: list[str], user_input: str) -> str:
        instruction = (
            "Fornisci una sintesi chiara e lineare della discussione finora, concentrandoti sui punti chiave emersi. "
            "Non aggiungere elenchi puntati o tabelle, ma un testo coeso e discorsivo in massimo 3 frasi."
        )
        prompt = build_prompt(
            system_prompt=self.system_prompt,
            user_input=user_input,
            message="\n".join(discussion_history),
            instruction=instruction
        )
        return query_ollama(prompt)