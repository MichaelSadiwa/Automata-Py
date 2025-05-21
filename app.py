import streamlit as st
import utils
import time

# Set page config first
st.set_page_config(
    page_title="Regular Expression to DFA, CFG, PDA Compiler",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown(f"""
    <style>
    body {{
        background-color: #f9f9f5;
        color: #1d3c34;
    }}
    .block-container {{
        font-size: 15px;
    }}
    .stButton > button {{
        background-color: rgba(29, 60, 52, 0.85) !important;
        color: white !important;
        font-size: 0.85rem;
        padding: 0.35em 1em;
        border-radius: 6px;
        margin: 2px;
    }}
    .stButton > button:hover {{
        background-color: rgba(29, 60, 52, 1.0) !important;
    }}
    .regex-box {{
        background-color: #e8f0ec;
        padding: 0.8rem;
        border-left: 5px solid #1d3c34;
        border-radius: 6px;
        font-size: 14px;
        white-space: pre-wrap;
    }}
    </style>
""", unsafe_allow_html=True)

# Init session state
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
st.sidebar.title("Controls")

regex_input = st.sidebar.selectbox(
    "Choose a Regular Expression",
    utils.regex_options,
    index=utils.regex_options.index(st.session_state.regex_input),
    key="regex_input"
)

# Handle regex logic
if st.session_state.regex_input != utils.regex_options[0]:
    st.session_state.disabled = False

    if st.session_state.regex_input == utils.regex_options[1]:
        st.session_state.placeholder_text = "aaababbaaa"
        st.session_state.selected_pattern = "(a+b)*(aa+bb)(aa+bb)*(ab+ba+aba)(bab+aba+bbb)(a+b+bb+aa)*(bb+aa+aba)(aaa+bab+bba)(aaa+bab+bba)*"
    elif st.session_state.regex_input == utils.regex_options[2]:
        st.session_state.placeholder_text = "101101000111"
        st.session_state.selected_pattern = "(1+0)* (11+00+101+010) (11+00)* (11+00+0+1) (1+0+11) (11+00)* (101+000+111) (1+0)* (101+000+111+001+100) (11+00+1+0)*"

    # Sidebar buttons
    if st.sidebar.button("Show PDA"):
        st.session_state.show_pda = not st.session_state.show_pda
        st.session_state.show_cfg = False

    if st.sidebar.button("Show CFG"):
        st.session_state.show_cfg = not st.session_state.show_cfg
        st.session_state.show_pda = False

# Title
st.title("Regular Expression to Deterministic Finite Automaton, Context-Free Grammar, and Pushdown Automaton Compiler")

# Show regex description
if st.session_state.regex_input != utils.regex_options[0]:
    st.markdown(f"<div class='regex-box'><strong>Selected Regular Expression:</strong><br>{st.session_state.selected_pattern}</div>", unsafe_allow_html=True)

    string_input = st.text_input(
        "Enter a string to test:",
        key="string_input",
        disabled=st.session_state.disabled,
        placeholder=st.session_state.placeholder_text
    )

    # Button row
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Validate", key="validate_button", disabled=st.session_state.disabled):
            st.session_state.trigger_validation = True
        else:
            st.session_state.trigger_validation = False
    with col2:
        if st.button("Clear"):
            st.session_state.string_input = ""
            st.session_state.clear_trigger = True

    # CFG/PDA rendering
    if st.session_state.show_pda:
        st.markdown("### 📊 Pushdown Automaton")
        pda = utils.generate_pda_visualization(
            utils.pda_1 if st.session_state.regex_input == utils.regex_options[1] else utils.pda_2
        )
        st.graphviz_chart(pda)

    if st.session_state.show_cfg:
        st.markdown("### 📄 Context-Free Grammar")
        st.markdown(utils.cfg_1 if st.session_state.regex_input == utils.regex_options[1] else utils.cfg_2)

    # Determine DFA
    current_dfa = utils.dfa_1 if st.session_state.regex_input == utils.regex_options[1] else utils.dfa_2

    if not string_input:
        st.subheader("Deterministic Finite Automaton")
        dfa = utils.generate_dfa_visualization(current_dfa)
        st.graphviz_chart(dfa)

    # Validation
    if st.session_state.get("trigger_validation", False) and string_input.strip():
        cleaned = string_input.strip()
        if not all(char in current_dfa["alphabet"] for char in cleaned):
            st.error(f"❌ Invalid characters used. Allowed: {current_dfa['alphabet']}")
        else:
            st.write(f"Analyzing: `{cleaned}`")
            with st.spinner("🔄 The program is tracing..."):
                is_valid, state_checks, transitions_used = utils.validate_dfa(current_dfa, cleaned)
                utils.animate_dfa_validation(current_dfa, state_checks, transitions_used)
            if is_valid:
                st.success("✅ The string is accepted by the DFA!")
            else:
                st.error("❌ The string is NOT accepted by the DFA.")

if st.session_state.clear_trigger:
    st.session_state.clear_trigger = False
