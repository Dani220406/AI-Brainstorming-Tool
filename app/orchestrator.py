import random
import re

from app.prompts_loader import load_prompt
from app.discussion_state import DiscussionState

# Import di tutte le classi agente
from app.agent_summarizer import SummarizerAgent
from app.agent_visionary import VisionaryAgent
from app.agent_critic import CriticAgent
from app.agent_pragmatic import PragmaticAgent
from app.agent_empathic import EmpathicAgent
from app.agent_strategist import StrategistAgent
from app.agent_experimenter import ExperimenterAgent
from app.agent_gentleman import GentlemanAgent
from app.agent_pessimistic import PessimisticAgent
from app.agent_poet import PoetAgent
from app.agent_lawyer import LawyerAgent
from app.agent_ecologist import EcologistAgent
from app.agent_minimalist import MinimalistAgent

def truncate_to_sentences(text: str, max_sentences: int = 3) -> str:
    sentences = re.split(r'(\.|\!|\?)\s+', text)
    grouped = [sentences[i] + (sentences[i + 1] if i + 1 < len(sentences) else '') for i in range(0, len(sentences), 2)]
    return ' '.join(grouped[:max_sentences]).strip()

# Classe Orchestrator (modificare con cautela 🙏)
class Orchestrator:
    def __init__(self, include_human: bool = False, excluded_agents: list[str] = None):
        self.include_human = include_human # Necessario per streamlit_app.py
        excluded_agents = excluded_agents or []

        # Registro di tutti gli agenti
        AGENT_REGISTRY = {
            "Visionario": VisionaryAgent,
            "Critico": CriticAgent,
            "Pragmatico": PragmaticAgent,
            "Empatico": EmpathicAgent,
            "Stratega": StrategistAgent,
            "Sperimentatore": ExperimenterAgent,
            "Gentleman": GentlemanAgent,
            "Pessimista": PessimisticAgent,
            "Poeta": PoetAgent,
            "Avvocato": LawyerAgent,
            "Ecologista": EcologistAgent,
            "Minimalista": MinimalistAgent,
        }

        self.agents = [
            agent_class(name, load_prompt(name.lower()))
            for name, agent_class in AGENT_REGISTRY.items()
            if name not in excluded_agents
        ]

        # SummarizeAgent aggiunto a parte perchè non partecipa (ovviamente) alla conversazione
        self.summarizer_agent = SummarizerAgent("Summarizer", load_prompt("summarizer"))
        self.turn_number = 0  # Contatore di turni (inizializzato a 0)
        self.latest_responses = {}
        self.history = []
        self.max_turns = 10  # Numero di turni (Modificabile manualmente)
        self.discussion_state = DiscussionState([agent.name for agent in self.agents])

    def run(self, user_input: str):
        print("\n###################\n\nInizio della sessione di brainstorming...\n")
        last_agent = random.choice([a for a in self.agents if a.name != "Utente"])
        current_message = user_input

        print(f"[Utente]: {user_input}\n")
        self.discussion_state.add_responses({"Utente": user_input})

        while True:
            self.turn_number += 1  # Incremento del contatore di turni ad ogni "ciclo"

            current_agent = self._select_next_agent(last_agent)
            response = self._generate_response(current_agent, current_message, user_input)
            response = truncate_to_sentences(response, 3)

            # Stampa la relazione tra gli agenti
            print(f"[{current_agent.name} -> {last_agent.name}]:\n{response}\n")

            self.discussion_state.add_responses({last_agent.name: response}, from_agent=current_agent.name)
            self.latest_responses = self.discussion_state.get_latest_responses()

            current_message = response
            last_agent = current_agent

            # Una volta raggiunto il numero di turni impostato...
            if self.turn_number >= self.max_turns:
                print("\n***Sintesi finale della discussione...***\n")
                summary = self.summarizer_agent.summarize_and_ask(
                    self.discussion_state.get_history_as_text_list(), user_input
                )
                print(f"[Sintesi Finale]:\n{summary}\n")
                self.discussion_state.add_responses({"Sintesi Finale": summary})
                self._finalize_discussion()
                break

    # L'agente che "risponde" viene scelto a caso ma risponde comunque a quello precedente
    def _select_next_agent(self, last_agent):
        return random.choice([
            a for a in self.agents
            if a != last_agent and (not self.include_human or a.name != "Utente")
        ])

    def _generate_response(self, agent, message, user_input):
        return agent.generate_response(message, user_input)

    # Messaggio alla fine del programma
    def _finalize_discussion(self):
        print("\n__Fine della discussione.__\n")
        report_path = self.discussion_state.export_detailed_report()
        print(f"Report finale salvato in: {report_path}\n") # La cartella brainstorm_report si dovrebbe generare automaticamente nella cartella del progetto