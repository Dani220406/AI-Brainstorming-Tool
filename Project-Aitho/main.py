from app.orchestrator import Orchestrator

# Inizio del programma (su terminale)
def main():
    print("\n __Benvenuto nell'AI Tool per il Brainstorming Collaborativo!__\n")
    user_input = input(" A cosa stai pensando oggi?\n> ")

    # Invocazione dell'Orchestrator
    orchestrator = Orchestrator()
    orchestrator.run(user_input)

if __name__ == "__main__":
    main()
