import os
from functools import lru_cache

@lru_cache(maxsize=None)
def load_prompt(agent_name: str) -> str:
    """
    Carica e memorizza in cache il prompt specifico per l'agente da un file .md nella cartella 'prompts'.
    Il nome del file deve corrispondere a <agent_name>.md (es. visionary.md).
    """
    base_path = os.path.dirname(__file__)
    prompts_dir = os.path.join(base_path, "..", "prompts")
    file_path = os.path.join(prompts_dir, f"{agent_name}.md")

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Prompt file non trovato: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().strip()
