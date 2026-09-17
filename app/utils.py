def build_prompt(system_prompt: str, user_input: str, message: str, instruction: str) -> str:
    return (
        f"{system_prompt.strip()}\n\n"
        f"Contesto dell'utente: {user_input.strip()}\n\n"
        f"Messaggio ricevuto: {message.strip()}\n\n"
        f"{instruction.strip()}"
    )