import ollama
from pathlib import Path

def load_prompt(file_path: str) -> str:
    return Path(file_path).read_text(encoding='utf-8')

def query_ollama(prompt: str, model: str = "gemma3:1b", system: str = "") -> str:
    """
    Usa la libreria ollama per interrogare un modello locale, con gestione degli errori.
    """
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        response = ollama.chat(model=model, messages=messages)
        return response['message']['content'].strip()
    except Exception as e:
        return f"[⚠️ Errore] Il modello non ha risposto correttamente: {str(e)}"