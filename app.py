import streamlit as st
import utils
import time

# Set page config first
st.set_page_config(
    page_title="Regular Expression to DFA, CFG, PDA Compiler",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Global Styles ----------
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
        padding: 0.4rem 1rem;
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
        margin-top: 1.5rem;
        font-size: 17px;
        color: #80ffd3;
    }
    hr {
        margin-top: 0.5rem;
        margin-bottom: 0.8rem;
        border: 1px solid #333;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Initialize Session State ----------
if "regex_input" not in st.session_state:
    st.session_state.regex_input = utils.regex_options[0]
    st.session_state.placeholder_text = ""
    st.session_state.show_cfg = False
    st.session_state.show_pda = False
    st.session_state.selected_pattern = ""
    st.session_state.trigger_validation = False
    st.session_state.string_input = ""
    st.session_state.valid_strings = []
    st.session_state.invalid_strings = []

# ---------- Sidebar ----------
st.sidebar.markdown("<div class='regex-box'><strong>Automata Compiler</strong><br>Regex ➤ DFA, CFG, PDA</div>", unsafe_allow_html=True)

# PDA / CFG toggles
col_sb1, col_sb2 = st.sidebar.columns(2)
with col_sb1:
    if st.button("📊 PDA"):
        st.session_state.show_pda = not st.session_state.show_pda
        st.session_state.show_cfg = False
with col_sb2:
    if st.button("📄 CFG"):
        st.session_state.show_cfg = not st.session_state.show_cfg
        st.session_state.show_pda = False

# Regex selection dropdown
regex_input = st.sidebar.selectbox(
    "Choose Regular Expression",
    utils.regex_options,
    index=utils.regex_options.index(st.session_state.regex_input),
    key="regex_selectbox"
)

# Update DFA/PDA/CFG config if selected
if regex_input != utils.regex_options[0]:
    st.session_state.regex_input = regex_input

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

    # Display pattern
    st.title("Regular Expression to Deterministic Finite Automaton, Context-Free Grammar, and Pushdown Automaton Compiler")
    st.markdown(f"<div class='regex-box'><strong>Selected Expression:</strong><br>{st.session_state.selected_pattern}</div>", unsafe_allow_html=True)

    # Input field
    string_input = st.text_input(
        "Test String",
        key="string_input",
        placeholder=st.session_state.placeholder_text
    )

    # Buttons below input
    colv, colc = st.columns([1, 1])
    with colv:
        st.markdown('<div class="stButton btn-validate">', unsafe_allow_html=True)
        if st.button("Validate", key="validate_button"):
            st.session_state.trigger_validation = True
        st.markdown('</div>', unsafe_allow_html=True)

    with colc:
        if string_input.strip():
            st.markdown('<div class="stButton btn-clear">', unsafe_allow_html=True)
            if st.button("Clear Input"):
                st.session_state.trigger_validation = False
                st.session_state.update(string_input="")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # DFA Graph
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">🧮 Deterministic Finite Automaton</div>', unsafe_allow_html=True)
    if not string_input.strip():
        st.graphviz_chart(utils.generate_dfa_visualization(current_dfa))

    # CFG Display
    if st.session_state.show_cfg:
        st.markdown('<div class="section-title">📄 Context-Free Grammar</div>', unsafe_allow_html=True)
        st.markdown(f"<div class='graph-container'>{current_cfg}</div>", unsafe_allow_html=True)

    # PDA Display
    if st.session_state.show_pda:
        st.markdown('<div class="section-title">📊 Pushdown Automaton</div>', unsafe_allow_html=True)
        st.graphviz_chart(utils.generate_pda_visualization(current_pda), use_container_width=False)

    # DFA Validation
    if st.session_state.trigger_validation and string_input.strip():
        st.markdown("<hr>", unsafe_allow_html=True)
        if not all(char in current_dfa["alphabet"] for char in string_input):
            st.session_state.invalid_strings = [string_input] + st.session_state.invalid_strings[:4]
            st.error(f"Invalid characters! Use only: {current_dfa['alphabet']}")
        else:
            st.write(f"Analyzing: `{string_input}`")
            with st.spinner("🔄 The program is tracing..."):
                is_valid, checks, steps = utils.validate_dfa(current_dfa, string_input)
                utils.animate_dfa_validation(current_dfa, checks, steps)
            if is_valid:
                st.success("✅ String accepted by DFA.")
                st.session_state.valid_strings = [string_input] + st.session_state.valid_strings[:4]
            else:
                st.error("❌ String rejected by DFA.")
                st.session_state.invalid_strings = [string_input] + st.session_state.invalid_strings[:4]

# Show latest test results (even if no validation yet)
if st.session_state.regex_input != utils.regex_options[0]:
    st.sidebar.markdown("### 📌 Recent Results", unsafe_allow_html=True)
    st.sidebar.markdown(
        f"""
        <div style="background-color: rgba(255, 72, 72, 0.1); padding: 8px; border-radius: 6px; margin-bottom: 12px;">
            <strong>❌ Latest 5 Invalid Strings</strong><br>
            <ul style='margin: 0; padding-left: 1em;'>
                {''.join([f"<li>{s}</li>" for s in st.session_state.invalid_strings])}
            </ul>
        </div>
        <div style="background-color: rgba(72, 255, 174, 0.1); padding: 8px; border-radius: 6px;">
            <strong>✅ Latest 5 Valid Strings</strong><br>
            <ul style='margin: 0; padding-left: 1em;'>
                {''.join([f"<li>{s}</li>" for s in st.session_state.valid_strings])}
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
