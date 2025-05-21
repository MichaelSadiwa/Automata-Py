import streamlit as st
import utils
import time

# Set page config FIRST
st.set_page_config(
    page_title="Regular Expression to DFA, CFG, PDA Compiler",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark sleek styling
st.markdown("""
    <style>
    html, body, [class*="css"] {
        background-color: #0e1117;
        color: #e0e0e0;
        font-family: "Segoe UI", sans-serif;
        font-size: 15px;
    }
    .stButton > button {
        font-size: 0.875rem;
        padding: 0.4rem 1.2rem;
        border-radius: 6px;
        border: none;
    }
    .btn-validate {
        background-color: rgba(72, 255, 174, 0.2) !important;
        color: #48ffaa !important;
    }
    .btn-clear {
        background-color: rgba(255, 72, 72, 0.2) !important;
        color: #ff9999 !important;
    }
    .regex-box {
        background-color: #1c1f26;
        padding: 0.8rem;
        border-left: 4px solid #48ffaa;
        border-radius: 6px;
        font-size: 14px;
        white-space: pre-wrap;
        color: #ffffff;
        margin-bottom: 1rem;
    }
    .graph-container {
        background-color: #1e222a;
        padding: 1rem;
        border-radius: 6px;
        margin-top: 0.5rem;
        border: 1px solid #333;
    }
    .section-title {
        margin-top: 2rem;
        font-size: 20px;
        color: #80ffd3;
    }
    .sidebar-row {
        display: flex;
        justify-content: space-between;
        gap: 10px;
    }
    hr {
        margin-top: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #333;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize state
if "disabled" not in st.session_state:
    st.session_state.disabled = True
    st.session_state.placeholder_text = ""
    st.session_state.show_cfg = False
    st.session_state.show_pda = False
    st.session_state.clear_trigger = False
    st.session_state.regex_input = utils.regex_options[0]
    st.session_state.string_input = ""
    st.session_state.selected_pattern = ""

# Sidebar controls
st.sidebar.title("Controls")
st.sidebar.selectbox(
    "Choose a Regular Expression",
    utils.regex_options,
    index=utils.regex_options.index(st.session_state.regex_input),
    key="regex_input"
)

# CFG & PDA toggle buttons (side-by-side)
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("Show PDA"):
        st.session_state.show_pda = not st.session_state.show_pda
        st.session_state.show_cfg = False
with col2:
    if st.button("Show CFG"):
        st.session_state.show_cfg = not st.session_state.show_cfg
        st.session_state.show_pda = False

# Set regex and visual DFA
if st.session_state.regex_input != utils.regex_options[0]:
    st.session_state.disabled = False

    if st.session_state.regex_input == utils.regex_options[1]:
        st.session_state.placeholder_text = "aaababbaaa"
        st.session_state.selected_pattern = "(a+b)*(aa+bb)(aa+bb)*(ab+ba+aba)(bab+aba+bbb)(a+b+bb+aa)*(bb+aa+aba)(aaa+bab+bba)(aaa+bab+bba)*"
        current_dfa = utils.dfa_1
        current_pda = utils.pda_1
        current_cfg = utils.cfg_1
    else:
        st.session_state.placeholder_text = "101101000111"
        st.session_state.selected_pattern = "(1+0)* (11+00+101+010) (11+00)* (11+00+0+1) (1+0+11) (11+00)* (101+000+111) (1+0)* (101+000+111+001+100) (11+00+1+0)*"
        current_dfa = utils.dfa_2
        current_pda = utils.pda_2
        current_cfg = utils.cfg_2

    # Page title
    st.title("Regular Expression to Deterministic Finite Automaton, Context-Free Grammar, and Pushdown Automaton Compiler")

    # Show selected regex
    st.markdown(f"<div class='regex-box'><strong>Selected Regular Expression:</strong><br>{st.session_state.selected_pattern}</div>", unsafe_allow_html=True)

    # Input field
    string_input = st.text_input(
        "Enter a string to test:",
        key="string_input",
        disabled=st.session_state.disabled,
        placeholder=st.session_state.placeholder_text
    )

    # Button row
    colv, colc = st.columns(2)
    with colv:
        st.markdown('<div class="stButton btn-validate">', unsafe_allow_html=True)
        validate = st.button("Validate", key="validate_button", disabled=st.session_state.disabled)
        st.markdown('</div>', unsafe_allow_html=True)
        st.session_state.trigger_validation = validate

    with colc:
        if string_input.strip():
            st.markdown('<div class="stButton btn-clear">', unsafe_allow_html=True)
            if st.button("Clear"):
                st.session_state.string_input = ""
                st.session_state.clear_trigger = True
            st.markdown('</div>', unsafe_allow_html=True)

    # DFA output (with reduced spacing)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">🧮 Deterministic Finite Automaton</div>', unsafe_allow_html=True)
    if not string_input:
        with st.container():
            dfa = utils.generate_dfa_visualization(current_dfa)
            st.graphviz_chart(dfa)

    # CFG
    if st.session_state.show_cfg:
        st.markdown('<div class="section-title">📄 Context-Free Grammar</div>', unsafe_allow_html=True)
        with st.container():
            st.markdown(f"<div class='graph-container'>{current_cfg}</div>", unsafe_allow_html=True)

    # PDA
    if st.session_state.show_pda:
        st.markdown('<div class="section-title">📊 Pushdown Automaton</div>', unsafe_allow_html=True)
        with st.container():
            pda = utils.generate_pda_visualization(current_pda)
            st.graphviz_chart(pda, use_container_width=False)

    # DFA Validation
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

# Reset after clearing
if st.session_state.clear_trigger:
    st.session_state.clear_trigger = False
