class Agent:
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt

    def generate_response(self, message: str, user_input: str) -> str:
        raise NotImplementedError("Ogni agente deve implementare generate_response.")