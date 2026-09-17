import os
from typing import List, Dict
from datetime import datetime

# Classe usata per tenere traccia della history del discorso e per generare il file di report.txt finale
class DiscussionState:
    def __init__(self, agent_names: List[str]):
        self.agent_names = agent_names
        self.turn = 0
        self.history: List[Dict[str, str]] = []
        self.latest_responses: Dict[str, str] = {name: "" for name in agent_names + ["Utente", "Sintesi Finale"]}
        self.concluded = False
        self.final_conclusion = None

    def add_responses(self, responses: dict, from_agent: str = None):
        if from_agent:
            formatted = {f"[{from_agent} -> {k}]": v for k, v in responses.items()}
            self.history.append(formatted)
        else:
            self.history.append(responses)
        self.latest_responses.update(responses)

    def set_conclusion(self, conclusion: str):
        self.concluded = True
        self.final_conclusion = conclusion

    def get_latest_responses(self) -> Dict[str, str]:
        return self.latest_responses

    def get_history(self) -> List[Dict[str, str]]:
        return self.history

    def get_history_as_text_list(self) -> list[str]:
        messages = []
        for turn in self.history:
            for agent, response in turn.items():
                messages.append(f"{agent}: {response}")
        return messages

    def export_detailed_report(self, filepath: str = None) -> str:
        lines = []
        for i, turn_responses in enumerate(self.history, start=1):
            lines.append(f"Turno {i}:\n")
            for agent, response in turn_responses.items():
                lines.append(f"  {agent}:\n    {response}\n")
            lines.append("\n")

        if self.concluded and self.final_conclusion:
            lines.append("=== Sintesi finale ===\n")
            lines.append(self.final_conclusion)
            lines.append("\n")

        report = "\n".join(lines)

        # Viene creato il file di report nel formato: brainstorm_report_(data)_(ora).txt
        if filepath is None:
            timestamp = datetime.now().strftime("%d%m%Y_%H%M")
            dir_path = "brainstorm_reports"  # cartella brainstorm_reports
            os.makedirs(dir_path, exist_ok=True)
            filepath = os.path.join(dir_path, f"brainstorm_report_{timestamp}.txt")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(report)

        return filepath

    @staticmethod
    def show_report(filepath: str = "brainstorm_report.txt"):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            print(f"Il file '{filepath}' non è stato trovato.")
        except Exception as e:
            print(f"Errore durante la lettura del file: {e}")
