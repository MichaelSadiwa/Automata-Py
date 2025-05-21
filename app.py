import streamlit as st
import utils
import time

# Set full-page config
st.set_page_config(
    page_title="Automata Visualizer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme overrides (off-white and dark green)
st.markdown("""
    <style>
    body {
        background-color: #f9f9f5;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3, h4 {
        color: #1d3c34;
    }
    .stButton > button {
        background-color: rgba(29, 60, 52, 0.85) !important;
        color: white !important;
        font-size: 0.85rem;
        padding: 0.4em 1em;
        border-radius: 8px;
        margin: 4px;
    }
    .stButton > button:hover {
        background-color: rgba(29, 60, 52, 1.0) !important;
    }
    .regex-box {
        background-color: #e8f0ec;
        padding: 1rem;
        border-left: 4px solid #1d3c34;
        border-radius: 8px;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "disabled" not in st.session_state:
    st.session_state.disabled = True
    st.session_state.placeholder_text = ""
    st.session_state.show_cfg = False
    st.session_state.show_pda = False
    st.session_state.clear_trigger = False
    st.session_state.regex_input = utils.regex_options[0]
    st.session_state.string_input = ""
    st.session_state.selected_pattern = ""

# Sidebar
st.sidebar.title("💬 Automata Controls")
regex_input = st.sidebar.selectbox(
    label="Select Regular Expression",
    options=utils.regex_options,
    index=utils.regex_options.index(st.session_state.regex_input),
    key="regex_input"
)

if st.session_state.regex_input != utils.regex_options[0]:
    st.session_state.disabled = False
    if st.session_state.regex_input == utils.regex_options[1]:
        st.session_state.placeholder_text = "aaababbaaa"
        st.session_state.selected_pattern = "(a+b)*(aa+bb)..."
    elif st.session_state.regex_input == utils.regex_options[2]:
        st.session_state.placeholder_text = "101101000111"
        st.session_state.selected_pattern = "(1+0)*(11+00+...)"

    col1, col2, col3 = st.sidebar.columns(3)
    with col1:
        if st.button("🔄 Clear"):
            st.session_state.string_input = ""
            st.session_state.clear_trigger = True
    with col2:
        if st.button("📄 CFG"):
            st.session_state.show_cfg = not st.session_state.show_cfg
            st.session_state.show_pda = False
    with col3:
        if st.button("📊 PDA"):
            st.session_state.show_pda = not st.session_state.show_pda
            st.session_state.show_cfg = False

# Input + DFA tracing panel
col_main, = st.columns([1])
with col_main:
    st.title("🧠 Automata Compiler & Visualizer")

    if st.session_state.regex_input != utils.regex_options[0]:
        st.markdown(f"<div class='regex-box'>Selected Pattern: <code>{st.session_state.selected_pattern}</code></div>", unsafe_allow_html=True)
        st.write("")
        string_input = st.text_input(
            label="Test a string on the DFA:",
            key="string_input",
            disabled=st.session_state.disabled,
            placeholder=st.session_state.placeholder_text
        )

        validate_button = st.button("Validate", key="validate_button", disabled=st.session_state.disabled)

        if st.session_state.regex_input == utils.regex_options[1]:
            current_dfa = utils.dfa_1
            current_pda = utils.pda_1
            current_cfg = utils.cfg_1
        elif st.session_state.regex_input == utils.regex_options[2]:
            current_dfa = utils.dfa_2
            current_pda = utils.pda_2
            current_cfg = utils.cfg_2

        # DFA graph (initial)
        if not string_input:
            st.subheader("🧭 Deterministic Finite Automaton")
            dfa_graph = utils.generate_dfa_visualization(current_dfa)
            st.graphviz_chart(dfa_graph)

        # Validation logic
        if validate_button and string_input.strip() and not st.session_state.clear_trigger:
            cleaned = string_input.strip()
            if not all(char in current_dfa["alphabet"] for char in cleaned):
                st.error(f"String '{cleaned}' contains invalid characters. Only use: {current_dfa['alphabet']}")
            else:
                st.write(f"✅ Validating string: `{cleaned}`")
                with st.spinner("🔄 The program is tracing..."):
                    is_valid, state_checks, transitions_used = utils.validate_dfa(current_dfa, cleaned)
                    utils.animate_dfa_validation(current_dfa, state_checks, transitions_used)

                if is_valid:
                    st.success("✅ The string is accepted by the DFA!")
                else:
                    st.error("❌ The string is NOT accepted by the DFA.")

        # CFG / PDA panels
        if st.session_state.show_cfg:
            st.subheader("📄 Context-Free Grammar")
            st.markdown(current_cfg)

        if st.session_state.show_pda:
            st.subheader("📊 Pushdown Automaton")
            pda_graph = utils.generate_pda_visualization(current_pda)
            st.graphviz_chart(pda_graph)

# Reset clear flag
if st.session_state.clear_trigger:
    st.session_state.clear_trigger = False
