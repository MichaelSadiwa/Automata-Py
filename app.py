import streamlit as st
import utils
import time

# Set Streamlit config (must be first)
st.set_page_config(
    page_title="Automata Project",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styles
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
    .btn-toggle {
        background-color: rgba(72, 255, 174, 0.08) !important;
        color: #80ffd3 !important;
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
        margin-top: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #333;
    }
    .sidebar-title {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 0.5rem;
        border-left: 4px solid #48ffaa;
        font-size: 13px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .recent-box {
        font-size: 13px;
        margin-bottom: 10px;
        padding: 0.5rem;
        border-radius: 5px;
    }
    .invalid-box {
        background-color: rgba(255, 0, 0, 0.08);
        color: #ff7f7f;
    }
    .valid-box {
        background-color: rgba(0, 255, 0, 0.08);
        color: #80ff80;
    }
    header[data-testid="stHeader"] {
        z-index: 999;
    }
    </style>
""", unsafe_allow_html=True)

# --- Initialize session state ---
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.disabled = True
    st.session_state.placeholder_text = ""
    st.session_state.regex_input = utils.regex_options[0]
    st.session_state.selected_pattern = ""
    st.session_state.trigger_validation = False
    st.session_state.valid_inputs = []
    st.session_state.invalid_inputs = []
    st.session_state.show_cfg = False
    st.session_state.show_pda = False

# --- Sidebar ---
st.sidebar.markdown('<div class="sidebar-title">REGEX → DFA, CFG, PDA COMPILER</div>', unsafe_allow_html=True)

# CFG/PDA buttons
col_sb1, col_sb2 = st.sidebar.columns(2)
with col_sb1:
    if st.button("📄 View CFG"):
        st.session_state.show_cfg = not st.session_state.show_cfg
        st.session_state.show_pda = False
with col_sb2:
    if st.button("📊 View PDA"):
        st.session_state.show_pda = not st.session_state.show_pda
        st.session_state.show_cfg = False

# Regex selector
regex_input = st.sidebar.selectbox(
    "Choose Regular Expression",
    utils.regex_options,
    index=utils.regex_options.index(st.session_state.regex_input),
)

# Activate expression
if regex_input != utils.regex_options[0]:
    st.session_state.disabled = False
    st.session_state.regex_input = regex_input

    if regex_input == utils.regex_options[1]:
        st.session_state.placeholder_text = "aaababbaaa"
        st.session_state.selected_pattern = "(a+b)*(aa+bb)(aa+bb)*(ab+ba+aba)(bab+aba+bbb)(a+b+bb+aa)*(bb+aa+aba)(aaa+bab+bba)(aaa+bab+bba)*"
        current_dfa = utils.dfa_1
        current_pda = utils.pda_1
        current_cfg = utils.cfg_1
    else:
        st.session_state.placeholder_text = "101101000111"
        st.session_state.selected_pattern = "(1+0)* (11+00+101+010)(11+00)*(11+00+0+1)(1+0+11)(11+00)*(101+000+111)(1+0)*(101+000+111+001+100)(11+00+1+0)*"
        current_dfa = utils.dfa_2
        current_pda = utils.pda_2
        current_cfg = utils.cfg_2

    # --- Sidebar logs ---
    st.sidebar.markdown('<div class="recent-box invalid-box">❌ Latest 5 Invalid Strings<br>' + "<br>".join(st.session_state.invalid_inputs[-5:][::-1]) + '</div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="recent-box valid-box">✅ Latest 5 Valid Strings<br>' + "<br>".join(st.session_state.valid_inputs[-5:][::-1]) + '</div>', unsafe_allow_html=True)

    # --- Main UI ---
    st.title("Regular Expression to Deterministic Finite Automaton, Context-Free Grammar, and Pushdown Automaton Compiler")
    st.markdown(f"<div class='regex-box'><strong>Selected Expression:</strong><br>{st.session_state.selected_pattern}</div>", unsafe_allow_html=True)

    string_input = st.text_input(
        "Test String",
        key="string_input",
        disabled=st.session_state.disabled,
        placeholder=st.session_state.placeholder_text
    )

    # --- Buttons ---
    st.markdown('<div class="stButton btn-validate">', unsafe_allow_html=True)
    if st.button("Validate", key="validate_button", disabled=st.session_state.disabled):
        st.session_state.trigger_validation = True
    st.markdown('</div>', unsafe_allow_html=True)

    # --- DFA Graph ---
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">🧮 Deterministic Finite Automaton</div>', unsafe_allow_html=True)

    if not string_input.strip():
        st.graphviz_chart(utils.generate_dfa_visualization(current_dfa))

    # --- DFA Validation ---
    if st.session_state.trigger_validation and string_input.strip():
        st.session_state.trigger_validation = False  # reset trigger after use
        string_input = string_input.strip()
        if not all(char in current_dfa["alphabet"] for char in string_input):
            st.session_state.invalid_inputs.append(string_input)
            st.error(f"Invalid characters! Allowed: {current_dfa['alphabet']}")
        else:
            st.write(f"Analyzing: `{string_input}`")
            with st.spinner("🔄 The program is tracing..."):
                is_valid, checks, steps = utils.validate_dfa(current_dfa, string_input)
                utils.animate_dfa_validation(current_dfa, checks, steps)
            if is_valid:
                st.session_state.valid_inputs.append(string_input)
                st.success("✅ String accepted by DFA.")
            else:
                st.session_state.invalid_inputs.append(string_input)
                st.error("❌ String rejected by DFA.")

    # --- CFG Section ---
    if st.session_state.show_cfg:
        st.markdown('<div class="section-title">📄 Context-Free Grammar</div>', unsafe_allow_html=True)
        st.markdown(f"<div class='graph-container'>{current_cfg}</div>", unsafe_allow_html=True)

    # --- PDA Section ---
    if st.session_state.show_pda:
        st.markdown('<div class="section-title">📊 Pushdown Automaton</div>', unsafe_allow_html=True)
        st.graphviz_chart(utils.generate_pda_visualization(current_pda), use_container_width=False)
