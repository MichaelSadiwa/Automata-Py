import streamlit as st
import utils

# Streamlit interface
def main():
    # Set page title and icon
    st.set_page_config(
        page_title="Automata Project",
    )

    # Initialize Streamlit session state values
    if len(st.session_state) == 0:
        st.session_state.disabled = True
        st.session_state.placeholder_text = ""
        st.session_state.show_cfg = False
        st.session_state.show_pda = False

    # Handle query params for styled button logic (new API)
    query_params = st.query_params
    if "clear" in query_params:
        st.session_state.regex_input = "--- Select ---"
        st.session_state.string_input = ""
        st.session_state.disabled = True
        st.session_state.placeholder_text = ""
        st.session_state.show_cfg = False
        st.session_state.show_pda = False
        st.query_params.clear()

    if "cfg" in query_params:
        st.session_state.show_cfg = not st.session_state.show_cfg
        st.session_state.show_pda = False
        st.query_params.clear()

    if "pda" in query_params:
        st.session_state.show_pda = not st.session_state.show_pda
        st.session_state.show_cfg = False
        st.query_params.clear()

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

    # Interface containers
    regex_to_dfa_con = st.container()

    with regex_to_dfa_con:
        st.subheader("Regex to DFA, CFG, & PDA")

        # Select box for regex
        regex_input = st.selectbox(
            label="Select a Regular Expression",
            options=utils.regex_options,
            key="regex_input",
            on_change=regex_input_callbk
        )

        # Styled button row
        st.markdown(
            """
            <style>
            .button-row {
                display: flex;
                justify-content: space-between;
                margin-bottom: 1rem;
            }
            .custom-btn {
                background-color: #1f77b4;
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                border-radius: 8px;
                transition-duration: 0.3s;
                cursor: pointer;
                margin-right: 10px;
            }
            .custom-btn:hover {
                background-color: #0e4a75;
            }
            </style>

            <div class="button-row">
                <form action="?clear=true" method="post">
                    <button class="custom-btn" type="submit">🔄 Clear</button>
                </form>
                <form action="?cfg=true" method="post">
                    <button class="custom-btn" type="submit">📄 Show CFG</button>
                </form>
                <form action="?pda=true" method="post">
                    <button class="custom-btn" type="submit">📊 Show PDA</button>
                </form>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Input string field
        string_input = st.text_input(
            label="Enter a string to check its validity for displayed DFA",
            key="string_input",
            disabled=st.session_state.disabled,
            placeholder=st.session_state.placeholder_text
        )

        # Validate button
        validate_button = st.button(
            label="Validate",
            disabled=st.session_state.disabled
        )

        # Show DFA + CFG/PDA based on selection
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
