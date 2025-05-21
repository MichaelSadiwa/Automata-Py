import streamlit as st
import utils
import time

# Set page config first
st.set_page_config(
    page_title="Regular Expression to DFA, CFG, PDA Compiler",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global styles
st.markdown("""
    <style>
    html, body, [class*="css"] {
        background-color: #0e1117;
        color: #e0e0e0;
        font-family: "Segoe UI", sans-serif;
        font-size: 15px;
    }
    .stButton > button {
        font-size: 14px;
        padding: 0.35rem 0.9rem;
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
        padding: 0.6rem;
        border-left: 4px solid #48ffaa;
        border-radius: 4px;
        font-size: 14px;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    .graph-container {
        background-color: #1e222a;
        padding: 0.6rem;
        border-radius: 6px;
        border: 1px solid #333;
        margin-bottom: 1rem;
    }
    .section-title {
        margin-top: 1.2rem;
        font-size: 17px;
        color: #80ffd3;
    }
    hr {
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
        border: 1px solid #333;
    }
    .sidebar-title {
        font-size: 14px;
        font-weight: bold;
        color: #80ffd3;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Init session state safely
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.disabled = True
    st.session_state.placeholder_text = ""
    st.session_state.show_cfg = False
    st.session_state.show_pda = False
    st.session_state.trigger_validation = False
    st.session_state.regex_input = utils.regex_options[0]
    st.session_state.selected_pattern = ""
    st.session_state.string_input = ""

# Callback to clear input safely
def clear_input_callback():
    st.session_state.string_input = ""
    st.session_state.trigger_validation = False

# Sidebar
st.sidebar.markdown('<div class="sidebar-title">📘 Regex → DFA/CFG/PDA Compiler</div>', unsafe_allow_html=True)
st.sidebar.title("Navigation")

col_sb1, col_sb2 = st.sidebar.columns(2)
with col_sb1:
    if st.button("📊 PDA"):
        st.session_state.show_pda = not st.session_state.show_pda
        st.session_state.show_cfg = False
with col_sb2:
    if st.button("📄 CFG"):
        st.session_state.show_cfg = not st.session_state.show_cfg
        st.session_state.show_pda = False

# Dropdown
regex_input = st.sidebar.selectbox(
    "Choose Regular Expression",
    utils.regex_options,
    index=utils.regex_options.index(st.session_state.regex_input)
)

# Determine states
if regex_input != utils.regex_options[0]:
    st.session_state.regex_input = regex_input
    st.session_state.disabled = False

    if regex_input == utils.regex_options[1]:
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

    # Title
    st.title("Regular Expression to Deterministic Finite Automaton, Context-Free Grammar, and Pushdown Automaton Compiler")

    # Show selected regex
    st.markdown(f"<div class='regex-box'><strong>Selected Expression:</strong><br>{st.session_state.selected_pattern}</div>", unsafe_allow_html=True)

    # Input box
    string_input = st.text_input(
        "Test String",
        value=st.session_state.string_input,
        key="string_input",
        disabled=st.session_state.disabled,
        placeholder=st.session_state.placeholder_text
    )

    # Validate and Clear Buttons
    colv, colc = st.columns([1, 1])
    with colv:
        st.markdown('<div class="stButton btn-validate">', unsafe_allow_html=True)
        if st.button("Validate", key="validate_button", disabled=st.session_state.disabled):
            st.session_state.trigger_validation = True
        st.markdown('</div>', unsafe_allow_html=True)

    with colc:
        if st.session_state.string_input.strip():
            st.markdown('<div class="stButton btn-clear">', unsafe_allow_html=True)
            st.button("Clear Input", on_click=clear_input_callback)
            st.markdown('</div>', unsafe_allow_html=True)

    # DFA Graph
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">🧮 Deterministic Finite Automaton</div>', unsafe_allow_html=True)
    if not string_input.strip():
        st.graphviz_chart(utils.generate_dfa_visualization(current_dfa))

    # CFG View
    if st.session_state.show_cfg:
        st.markdown('<div class="section-title">📄 Context-Free Grammar</div>', unsafe_allow_html=True)
        st.markdown(f"<div class='graph-container'>{current_cfg}</div>", unsafe_allow_html=True)

    # PDA View
    if st.session_state.show_pda:
        st.markdown('<div class="section-title">📊 Pushdown Automaton</div>', unsafe_allow_html=True)
        with st.container():
            st.graphviz_chart(utils.generate_pda_visualization(current_pda), use_container_width=False)

    # DFA validation animation
    if st.session_state.trigger_validation and string_input.strip():
        cleaned = string_input.strip()
        if not all(char in current_dfa["alphabet"] for char in cleaned):
            st.error(f"Invalid characters! Allowed: {current_dfa['alphabet']}")
        else:
            st.write(f"Analyzing: `{cleaned}`")
            with st.spinner("🔄 The program is tracing..."):
                is_valid, checks, steps = utils.validate_dfa(current_dfa, cleaned)
                utils.animate_dfa_validation(current_dfa, checks, steps)
            if is_valid:
                st.success("✅ String accepted by DFA.")
            else:
                st.error("❌ String rejected by DFA.")
