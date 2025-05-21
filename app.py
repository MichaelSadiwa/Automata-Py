import streamlit as st
import utils

# Streamlit interface
def main():
    st.set_page_config(page_title="Automata Project")

    # Init session state
    if len(st.session_state) == 0:
        st.session_state.disabled = True
        st.session_state.placeholder_text = ""
        st.session_state.show_cfg = False
        st.session_state.show_pda = False

    # Callback for regex selector
    def regex_input_callbk():
        if st.session_state.regex_input == "--- Select ---":
            st.session_state.disabled = True
        else:
            st.session_state.disabled = False

        if st.session_state.regex_input == utils.regex_options[1]:
            st.session_state.placeholder_text = "aaababbaaa"
        elif st.session_state.regex_input == utils.regex_options[2]:
            st.session_state.placeholder_text = "101101000111"
        else:
            st.session_state.placeholder_text = ""

        st.session_state.string_input = ""

    regex_to_dfa_con = st.container()

    with regex_to_dfa_con:
        st.subheader("Regex to DFA, CFG, & PDA")

        regex_input = st.selectbox(
            label="Select a Regular Expression",
            options=utils.regex_options,
            key="regex_input",
            on_change=regex_input_callbk
        )

        # Styled button section
        if st.session_state.regex_input != "--- Select ---":
            st.markdown("""
                <style>
                div.stButton > button {
                    background-color: #4CAF50;
                    color: white;
                    padding: 0.6em 1.2em;
                    font-size: 16px;
                    border: none;
                    border-radius: 8px;
                    margin-right: 10px;
                    transition: background-color 0.3s;
                }
                div.stButton > button:hover {
                    background-color: #3e8e41;
                }
                .no-green .stButton > button {
                    background-color: #999 !important;
                    color: white !important;
                }
                </style>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("🔄 Clear"):
                    for key in ["regex_input", "string_input", "disabled", "placeholder_text", "show_cfg", "show_pda"]:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.experimental_rerun()

            with col2:
                if st.button("📄 Show CFG"):
                    st.session_state.show_cfg = not st.session_state.show_cfg
                    st.session_state.show_pda = False

            with col3:
                if st.button("📊 Show PDA"):
                    st.session_state.show_pda = not st.session_state.show_pda
                    st.session_state.show_cfg = False

        # Input string
        string_input = st.text_input(
            label="Enter a string to check its validity for displayed DFA",
            key="string_input",
            disabled=st.session_state.disabled,
            placeholder=st.session_state.placeholder_text
        )

        # Validate button (no green)
        with st.container():
            st.markdown('<div class="no-green">', unsafe_allow_html=True)
            validate_button = st.button("Validate", key="validate_button", disabled=st.session_state.disabled)
            st.markdown('</div>', unsafe_allow_html=True)

        # Show DFA/CFG/PDA
        if regex_input == utils.regex_options[1]:
            current_dfa = utils.dfa_1
            st.write("**Deterministic Finite Automaton**")
            if not string_input:
                dfa = utils.generate_dfa_visualization(current_dfa)
                st.graphviz_chart(dfa)

            if st.session_state.show_cfg:
                st.write("**📄 Context-Free Grammar**")
                st.markdown(utils.cfg_1)

            if st.session_state.show_pda:
                st.write("**📊 Pushdown Automaton**")
                current_pda = utils.pda_1
                pda = utils.generate_pda_visualization(current_pda)
                st.graphviz_chart(pda)

        elif regex_input == utils.regex_options[2]:
            current_dfa = utils.dfa_2
            st.write("**Deterministic Finite Automaton**")
            if not string_input:
                dfa = utils.generate_dfa_visualization(current_dfa)
                st.graphviz_chart(dfa)

            if st.session_state.show_cfg:
                st.write("**📄 Context-Free Grammar**")
                st.markdown(utils.cfg_2)

            if st.session_state.show_pda:
                st.write("**📊 Pushdown Automaton**")
                current_pda = utils.pda_2
                pda = utils.generate_pda_visualization(current_pda)
                st.graphviz_chart(pda)

        # DFA string validation
        if validate_button or string_input:
            string_input = string_input.replace(" ", "")
            if len(string_input) == 0:
                st.error("Empty/Invalid Input", icon="❌")
            elif not all(char in current_dfa["alphabet"] for char in string_input):
                st.error(
                    f"String '{string_input}' contains invalid characters. Use only: {current_dfa['alphabet']}",
                    icon="❌"
                )
            else:
                st.write(f"Entered String: `{string_input}`")
                is_valid, state_checks, transitions_used = utils.validate_dfa(current_dfa, string_input)
                utils.animate_dfa_validation(current_dfa, state_checks, transitions_used)
                if is_valid:
                    st.success(f"The string '{string_input}' is valid for the DFA.", icon="✔️")
                else:
                    st.error(f"The string '{string_input}' is not valid for the DFA.", icon="❌")


if __name__ == "__main__":
    main()
