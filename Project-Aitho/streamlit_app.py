import streamlit as st
import random
import time

from app.orchestrator import Orchestrator
from app.discussion_state import DiscussionState

# Emoji associate a ciascun agente
AGENT_EMOJIS = {
    "Utente": "🧑",
    "Visionario": "🌟",
    "Critico": "🧐",
    "Pragmatico": "🛠️",
    "Sperimentatore": "🧪",
    "Empatico": "💞",
    "Stratega": "🧠",
    "SummarizerAgent": "📚",
    "Gentleman": "🎩",
    "Pessimista": "☁️",
    "Minimalista": "🛏️",
    "Ecologista": "🍃",
    "Poeta": "🎭",
    "Avvocato": "⚖️",
}

THINK_TIME_SECONDS = 3

st.set_page_config(page_title="AI Brainstorming Collaborativo", layout="wide")

st.markdown(
    """
    <div style="text-align: left; font-size: 14px; color: gray;">
        <strong>Made by Daniele Conti · UNICT</strong>
    </div>
    """, unsafe_allow_html=True,
)
st.title("🤖 AI Brainstorming Collaborativo")  # Titolo del progetto

# Sidebar - pulsante Istruzioni d'uso
with st.sidebar.expander("ℹ️ Istruzioni d'uso", expanded=False):
    st.markdown("""
    - Inserisci uno **spunto iniziale** da cui far partire la conversazione.
    - Seleziona se vuoi **partecipare** alla conversazione.
    - Puoi selezionare quali agenti **escludere** dalla conversazione.
    - Imposta il **numero fisso di turni** manualmente.
    - Personalizza la **velocità dell'animazione** o disattivala.
    - Al termine, potrai leggere il **report finale**, che verrà automaticamente scaricato.
    - Una volta terminata la conversazione, verrà mostrato il tempo totale della sessione.
    - Una volta terminata la conversazione, premi **Inizia una nuova sessione** per ricominciare.
    - Puoi chiudere la sidebar premendo il pulsante < in alto, oppure regolarne la dimensione tenendo premeuta la linea di confine sidebar/chat e spostando il cursore.
                
    **ATTENZIONE**:
    - ⚠️ La conversazione non può iniziare con meno di 2 agenti
    - ⚠️ Si consiglia altamente di **non modificare** le impostazioni durante l'esecuzione del programma
    - ⚠️ **Non chiudere** il terminale durante l'esecuzione del programma

    Sperimenta con tutte le impostazioni e vedi i risultati che ottieni.
    Buon Divertimento 😊! 
    """)

st.sidebar.markdown("---")

# Lista completa degli agenti + le loro Emoji associate
ALL_AI_AGENTS = [
    "🌟 Visionario", "🧐 Critico", "🛠️ Pragmatico",
    "🧪 Sperimentatore", "💞 Empatico", "🧠 Stratega",
    "🎩 Gentleman", "☁️ Pessimista", "🍃 Ecologista",
    "⚖️ Avvocato", "🎭 Poeta", "🛏️ Minimalista"
]

# Sidebar - Impostazione di Esclusione Agenti dalla conversazione
excluded_agents = st.sidebar.multiselect(
    "🙈 Seleziona gli agenti da ESCLUDERE dalla discussione:",
    options=ALL_AI_AGENTS,
    default=[],
    help="Non puoi iniziare una conversazione con meno di 2 agenti"
)

st.sidebar.markdown("---")

# Sidebar - Impostazione di Frequenza intervento utente nella conversazione 
user_frequency = st.sidebar.slider(
    "👤 Frequenza intervento utente (ogni N turni)",
    min_value=2,
    max_value=10,
    value=5,
    step=1,
    help="Funziona solo se attivi l'opzione di pertecipare alla discussione"
)
st.session_state["user_frequency"] = user_frequency

st.sidebar.markdown("---")

# Sidebar - Impostazione di decisione Numero di turni della discussione
fixed_turns = st.sidebar.slider(
    "🔁 Numero di turni della discussione",
    min_value=5,
    max_value=50,
    value=15,
    step=1,
    help="Il turno iniziale dell'utente e finale della sintesi non fanno parte del conteggio"
)

st.sidebar.markdown("---")

# Sidebar - Impostazione di Attivazione/Disattivazione dell'animazione di scrittura
animation_enabled = st.sidebar.checkbox(
    "✍️ Attiva animazione della scrittura",
    value=True
)
# Selezione manuale della velocità di scrittura dei caratteri
st.session_state["animation"] = animation_enabled
if animation_enabled:
    animation_speed = st.sidebar.slider(
        "⏱️ Velocità animazione (secondi per carattere)",
        min_value=0.001,
        max_value=0.1,
        value=0.015,
        step=0.001,
        format="%.3f",
        help="0.001s = veloce | 0.100s = lento"
    )
else:
    animation_speed = 0.0

st.session_state["animation_speed"] = animation_speed

# Inizializzazione variabili all'apertura del programma
if "started" not in st.session_state:
    st.session_state.update({
        "started": False,
        "turn_number": 0,
        "max_turns": 0,
        "show_report": False,
        "report_path": "",
        "orchestrator": None,
        "current_message": "",
        "last_agent": None,
        "auto_continue": False,
        "human_input": "",
        "animation": True,
        "excluded_agents": excluded_agents,
        "start_time": None,
        "end_time": None,
    })

user_input_initial = st.text_input("🗣 Inserisci uno spunto iniziale per la discussione:")  # Box in cui l'utente inserisci il messaggio iniziale
include_human_flag = st.checkbox("👤 Vuoi partecipare attivamente alla discussione?", value=False)  # Box in cui l'utente seleziona se partecipare alla conversazione o no

clean_excluded = [name.split(" ", 1)[1] for name in excluded_agents]
active_agents_count = len(ALL_AI_AGENTS) - len(clean_excluded)

avvia_disabled = active_agents_count < 2
# Warning - Se l'utente lascia attivi meno di 2 agenti la discussione non può partire
if avvia_disabled:
    st.warning("⚠️ Devi mantenere **almeno 2 agenti attivi** per avviare la discussione.")

# Pulsante di avvio della discussione
if st.button("💬 Avvia discussione", disabled=avvia_disabled) and user_input_initial.strip() and not st.session_state.started:
    st.session_state["excluded_agents"] = clean_excluded
    st.session_state.orchestrator = Orchestrator(
        include_human=include_human_flag,
        excluded_agents=clean_excluded
    )
    discussion = st.session_state.orchestrator.discussion_state
    st.session_state.started = True
    st.session_state.start_time = time.time() # Inizio del timer di sessione
    st.session_state.turn_number = 1
    st.session_state.max_turns = fixed_turns
    st.session_state.current_message = user_input_initial.strip()
    st.session_state.last_agent = random.choice(
        [a for a in st.session_state.orchestrator.agents if a.name != "Utente"]
    )
    st.session_state.auto_continue = True
    discussion.add_responses({"Utente": user_input_initial.strip()})

def print_history(discussion: DiscussionState):
    for turn in discussion.history:
        for agent_name, message in turn.items():
            label = "📚 Sintesi Finale" if agent_name == "SummarizerAgent" else f"{AGENT_EMOJIS.get(agent_name, '🤖')} {agent_name}"
            st.markdown(f"**{label}**:\n> {message}")
            st.markdown("<hr style='border: none; border-top: 1px solid #eee; margin: 8px 0;'>", unsafe_allow_html=True)

def animate_message(agent_name: str, response: str):
    label = "📚 Sintesi Finale" if agent_name == "SummarizerAgent" else f"{AGENT_EMOJIS.get(agent_name, '🤖')} {agent_name}"
    if st.session_state.animation:
        placeholder = st.empty()
        text = ""
        for char in response:
            text += char
            placeholder.markdown(f"**{label}**:\n> {text}")
            time.sleep(st.session_state["animation_speed"])
    else:
        st.markdown(f"**{label}**:\n> {response}")

# Nel caso in cui l'utente ha selezionato di voler partecipare alla discussione
def ask_human_turn():
    user_msg = st.text_input(
        "È il tuo turno! Inserisci il tuo contributo:",
        value=st.session_state.human_input,
        key=f"human_turn_{st.session_state.turn_number}",
    )
    if user_msg.strip():
        st.session_state.human_input = ""
        return user_msg.strip()
    return None

if st.session_state.started and st.session_state.orchestrator:
    orchestrator = st.session_state.orchestrator
    discussion = orchestrator.discussion_state

    print_history(discussion)

    # Una volta raggiunto il numero di turni preimpostato...
    if st.session_state.turn_number > st.session_state.max_turns and not discussion.concluded:
        st.markdown("***📚 Sintesi finale...***")
        summary = orchestrator.summarizer_agent.summarize_and_ask(
            discussion.get_history_as_text_list(),
            user_input_initial
        )
        discussion.add_responses({"SummarizerAgent": summary})
        discussion.set_conclusion(summary)
        animate_message("SummarizerAgent", summary)
        st.session_state.end_time = time.time() # Fine del timer di sessione
        st.rerun()

    if discussion.concluded:
        if not st.session_state.show_report:
            path = discussion.export_detailed_report()
            st.session_state.show_report = True
            st.session_state.report_path = path

        with open(st.session_state.report_path, "r", encoding="utf-8") as f:
            content = f.read()

        st.text_area("📄 Report finale della sessione", value=content, height=400)

        # Viene mostrata la durata totale della sessione
        if st.session_state.start_time and st.session_state.end_time:
            duration = int(st.session_state.end_time - st.session_state.start_time)
            minutes = duration // 60
            seconds = duration % 60
            st.success(f"⏱️ Durata totale della sessione: {minutes} min {seconds} sec")

        # Pulsante di download del report nel caso in cui questo non fosse avvenuto automaticamente
        st.download_button(
            label="📥 Scarica il report se non è presente nella cartella",
            data=content,
            file_name=st.session_state.report_path.split("/")[-1],
            mime="text/plain",
        )

        # Pulsante che fa il refresh della pagina per ricominciare con una nuova discussione
        if st.button("🔄 Inizia una nuova sessione"):
            st.session_state.clear()
            st.rerun()
        st.stop()

    if orchestrator.include_human and st.session_state.turn_number % st.session_state["user_frequency"] == 0:
        human_msg = ask_human_turn()
        if human_msg:
            discussion.add_responses({"Utente": human_msg})
            st.session_state.current_message = human_msg
            st.session_state.last_agent = "Utente"
            st.session_state.turn_number += 1
            st.rerun()
        st.stop()

    available_agents = [
        a for a in orchestrator.agents
        if a != st.session_state.last_agent
        and a.name != "Utente"
        and a.name not in st.session_state.excluded_agents
    ]
    current_agent = random.choice(available_agents)

    # Simulazione del "pensiero" dell'AI usando la variabile globale impostata all'inizio
    with st.spinner(f"🤖 {current_agent.name} sta pensando..."):
        time.sleep(THINK_TIME_SECONDS)

    response = current_agent.generate_response(
        st.session_state.current_message, user_input_initial
    )
    discussion.add_responses({current_agent.name: response})
    animate_message(current_agent.name, response)

    st.session_state.current_message = response
    st.session_state.last_agent = current_agent
    st.session_state.turn_number += 1  # Incremento del contatore di turni

    if st.session_state.auto_continue:
        st.rerun()
