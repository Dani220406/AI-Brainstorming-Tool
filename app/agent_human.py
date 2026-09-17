from app.agent_base import Agent

class HumanAgent(Agent):
    def generate_response(self, message: str, user_input: str) -> str:
        print("\n[UTENTE] Inserisci il tuo contributo per la discussione:")
        user_message = input("> ")
        return user_message.strip()
