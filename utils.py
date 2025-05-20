from graphviz import Digraph
import streamlit as st
import time

# List of regular expressions assigned to our group
regex_options = [
    "--- Select ---",
    "(a+b)*(aa+bb)(aa+bb)*(ab+ba+aba)(bab+aba+bbb)(a+b+bb+aa)*(bb+aa+aba)(aaa+bab+bba)(aaa+bab+bba)*",
    "(1+0)*(11+00+101+010)(11+00)*(11+00+0+1)(1+0+11)(11+00)*(101+000+111)(1+0)*(101+000+111+001+100)(11+00+1+0)*"
]

# DFA for (a+b)*(aa+bb)(aa+bb)*(ab+ba+aba)(bab+aba+bbb)(a+b+bb+aa)*(bb+aa+aba)(aaa+bab+bba)(aaa+bab+bba)*
dfa_1 = {
    "states": ["q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10", 
               "q11", "q12", "q13", "q14", "q15", "q16", "q17", "q18", "q19", "q20", "qd"],
    "alphabet": ["a", "b"],
    "start_state": "q0",
    "end_states": ["q20"],
    "transitions": {
        # Initial prefix of (a+b)* followed by (aa+bb)
        ("q0", "a"): "q1",   # Start processing 'a'
        ("q0", "b"): "q2",   # Start processing 'b'
        ("q1", "a"): "q3",   # 'aa' detected
        ("q1", "b"): "q2",   # Back to 'b'
        ("q2", "a"): "q1",   # Back to 'a'
        ("q2", "b"): "q4",   # 'bb' detected
        
        # (aa+bb)* part
        ("q3", "a"): "q3",   # Another 'aa'
        ("q3", "b"): "q5",   # Move to next part
        ("q4", "a"): "q5",   # Move to next part
        ("q4", "b"): "q4",   # Another 'bb'
        
        # (ab+ba+aba) part
        ("q5", "a"): "q6",   # Start 'ab' or 'aba'
        ("q5", "b"): "q7",   # Start 'ba'
        ("q6", "b"): "q8",   # 'ab' complete
        ("q6", "a"): "qd",   # Dead state - invalid
        ("q7", "a"): "q8",   # 'ba' complete
        ("q7", "b"): "qd",   # Dead state - invalid
        ("q8", "a"): "q9",   # 'aba' option
        ("q8", "b"): "q10",  # Continue to next part
        ("q9", "b"): "q10",  # Continue after 'aba'
        ("q9", "a"): "qd",   # Dead state - invalid
        
        # (bab+aba+bbb) part
        ("q10", "a"): "q11", # Start 'aba'
        ("q10", "b"): "q12", # Start 'bab' or 'bbb'
        ("q11", "b"): "q13", # 'ab' part of 'aba'
        ("q11", "a"): "qd",  # Dead state - invalid
        ("q12", "a"): "q13", # 'ba' part of 'bab'
        ("q12", "b"): "q13", # 'bb' part of 'bbb'
        ("q13", "a"): "q14", # Complete 'aba'
        ("q13", "b"): "q14", # Complete 'bab' or 'bbb'
        
        # (a+b+bb+aa)* part - optional
        ("q14", "a"): "q15", # Continue to next part or start 'aa'
        ("q14", "b"): "q16", # Continue to next part or start 'bb'
        
        # (bb+aa+aba) part
        ("q15", "a"): "q17", # Complete 'aa'
        ("q15", "b"): "q18", # 'ab' part of 'aba'
        ("q16", "b"): "q17", # Complete 'bb'
        ("q16", "a"): "q14", # Back to optional section (part of a+b+bb+aa)*
        ("q17", "a"): "q19", # Move to next part - start 'aaa'
        ("q17", "b"): "q19", # Move to next part - start 'bab' or 'bba'
        ("q18", "a"): "q17", # Complete 'aba'
        ("q18", "b"): "qd",  # Dead state - invalid
        
        # (aaa+bab+bba) part
        ("q19", "a"): "q20", # Complete pattern with 'aaa' or 'bba'
        ("q19", "b"): "q20", # Complete pattern with 'bab'
        
        # (aaa+bab+bba)* - optional repeats
        ("q20", "a"): "q19", # Start another pattern
        ("q20", "b"): "q19", # Start another pattern
        
        # Dead state transitions
        ("qd", "a"): "qd",   # Stay in dead state
        ("qd", "b"): "qd"    # Stay in dead state
    }
}
# DFA for (1+0)*(11+00+101+010)(11+00)*(11+00+0+1)(1+0+11)(11+00)*(101+000+111)(1+0)*(101+000+111+001+100)(11+00+1+0)*
dfa_2 = {
    "states": ["q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10"],
    "alphabet": ["1", "0"],
    "start_state": "q0",
    "end_states": ["q10"],
    "transitions": {
        ("q0", "0"): "q1",
        ("q0", "1"): "q1",
        ("q1", "0"): "q2",
        ("q1", "1"): "q2",
        ("q2", "0"): "q3",
        ("q2", "1"): "q3",
        ("q3", "0"): "q4",
        ("q3", "1"): "q4",
        ("q4", "0"): "q5",
        ("q4", "1"): "q5",
        ("q5", "0"): "q6",
        ("q5", "1"): "q6",
        ("q6", "0"): "q7",
        ("q6", "1"): "q7",
        ("q7", "0"): "q8",
        ("q7", "1"): "q8",
        ("q8", "0"): "q9",
        ("q8", "1"): "q9",
        ("q9", "0"): "q10",
        ("q9", "1"): "q10",
        ("q10", "0,1"): "q10",
    }
}

# CFG for (a+b)*(aa+bb)(aa+bb)*(ab+ba+aba)(bab+aba+bbb)(a+b+bb+aa)*(bb+aa+aba)(aaa+bab+bba)(aaa+bab+bba)*
cfg_1 = """
S -> aS | bS | aaA | bbA \n
A -> aaA | bbA | abB | baB | abaB \n
B -> babC | abaC | bbbC \n
C -> aC | bC | aaC | bbC | D | ^ \n
D -> bbE | aaE | abaE \n
E -> aaaF | babF | bbaF \n
F -> aaaF | babF | bbaF | ^
"""

# CFG for (1+0)*(11+00+101+010)(11+00)*(11+00+0+1)(1+0+11)(11+00)*(101+000+111)(1+0)*(101+000+111+001+100)(11+00+1+0)*
cfg_2 = '''
        S -> WXYZ \n
        W -> 1W | 0W | 11 | 00 | 101 | 010 \n
        X -> 11X | 00X | 11 | 00 | 0 | 1 \n
        Y -> 1Y | 0Y | 11Y | 101 | 000 | 111 \n
        Z -> 1Z | 0Z | 11Z | 00Z | 101 | 000 | 111 | 001 | 100 | ^
        '''

# PDA for (a+b)*(aa+bb)(aa+bb)*(ab+ba+aba)(bab+aba+bbb)(a+b+bb+aa)*(bb+aa+aba)(aaa+bab+bba)(aaa+bab+bba)*
pda_1 = {
    "states": ["Start", "Read1", "Read2", "Read3", "Read4", "Read5", "Read6", "Read7", "Read8", "Accept"],
    "alphabet": ["a", "b"],
    "start_state": "Start",
    "push_states": [None],
    "pop_states": [None],
    "accept_states": ["Accept"],
    "transitions": {
        ("Start", ""): "Read1",
        ("Read1", "a,b"): "Read1",
        ("Read1", "a"): "Read2",
        ("Read1", "b"): "Read2",
        ("Read2", "a,b"): "Read3",
        ("Read3", "a,b"): "Read4",
        ("Read4", "a,b"): "Read5", 
        ("Read5", "a,b"): "Read6",
        ("Read6", "a,b"): "Read7",
        ("Read7", "a,b"): "Read8",
        ("Read8", "a,b"): "Read8",
        ("Read8", "^"): "Accept",
    }
}

# PDA for (1+0)*(11+00+101+010)(11+00)*(11+00+0+1)(1+0+11)(11+00)*(101+000+111)(1+0)*(101+000+111+001+100)(11+00+1+0)*
pda_2 = {
    "states": ["Start", "Read1", "Read2", "Read3", "Read4", "Read5", "Read6", "Read7", "Read8", "Read9", "Accept"],
    "alphabet": ["1", "0"],
    "start_state": "Start",
    "push_states": [None],
    "pop_states": [None],
    "accept_states": ["Accept"],
    "transitions": {
        ("Start", ""): "Read1",
        ("Read1", "0,1"): "Read1",
        ("Read1", "0,1"): "Read2",
        ("Read2", "0,1"): "Read3",
        ("Read3", "0,1"): "Read4",
        ("Read4", "0,1"): "Read5",
        ("Read5", "0,1"): "Read6",
        ("Read6", "0,1"): "Read7",
        ("Read7", "0,1"): "Read8",
        ("Read8", "0,1"): "Read9",
        ("Read9", "0,1"): "Read9",
        ("Read9", "^"): "Accept",
    }
}



# Generate DFA visualization using Graphviz
def generate_dfa_visualization(dfa):
    dot = Digraph(engine="dot", graph_attr={'rankdir': 'LR'}, renderer="gd")

    # Add graph nodes for the states
    for state in dfa["states"]:
        if state in dfa["end_states"]:
            dot.node(state, shape="doublecircle")
        else:
            dot.node(state, shape="circle")

    # Add edges/transitions
    for transition, target_state in dfa["transitions"].items():
        source_state, symbol = transition
        dot.edge(source_state, target_state, label=symbol)

    # Return the Graphviz graph for the DFA visualization
    return dot


# Generate PDA visualization using Graphviz
def generate_pda_visualization(pda):
    dot = Digraph(engine="dot", renderer="gd")

    # Add graph nodes for the states
    for state in pda["states"]:
        if state in pda["start_state"] or state in pda["accept_states"]:
            dot.node(state, shape="ellipse")
        elif state in pda["push_states"]:
            dot.node(state, shape="rectangle")
        else:
            dot.node(state, shape="diamond")

    # Add edges/transitions
    for transition, target_state in pda["transitions"].items():
        source_state, symbol = transition
        dot.edge(source_state, target_state, label=symbol)

    # Return the Graphviz graph for the DFA visualization
    return dot


# Validate given string for DFA 
def validate_dfa(dfa, string):
    state_checks = []
    current_state = dfa["start_state"]

    # Iterate through each character in string
    for char in string:
        # Check if transition has "0,1", if so replace char with "0,1"
        if (current_state,"0,1") in dfa["transitions"].keys():
            char = "0,1"
        
        # Check if transition has "a,b", if so replace char with "a,b"
        if (current_state,"a,b") in dfa["transitions"].keys():
            char = "a,b"
        
        transition = (current_state, char)
        transition_exists = transition in dfa["transitions"].keys()
        state_checks.append((current_state, transition_exists))

        # Check if current char is in transitions
        if transition_exists:
            current_state = dfa["transitions"][transition]
        # Return False if current character in the string is not in the dfa transitions
        else:
            return False, state_checks
    
    # Add state check for last transition
    if current_state in dfa["end_states"]:
        state_checks.append((current_state, True))
    else:
        state_checks.append((current_state, False))

    result = current_state in dfa["end_states"] # Checks if last current_state is in dfa end_states

    # Return the validation result and state_checks array
    return (result, state_checks)


# Generate validation animation
def animate_dfa_validation(dfa, state_checks):
    dot = generate_dfa_visualization(dfa)  # Generate the DFA visualization
    graph = st.graphviz_chart(dot.source, use_container_width=True) # Create a Streamlit Graphviz component

    # Iterate through each state in state_checks
    for state_check in state_checks:
        state, is_valid = state_check

        time.sleep(1)  # Add a delay for visualization purposes

        if is_valid and state in dfa["end_states"]:
            dot.node(state, style="filled", fillcolor="green")  # Set end state to green
            graph.graphviz_chart(dot.source, use_container_width=True) # Render the updated visualization

        elif not is_valid:
            dot.node(state, style="filled", fillcolor="red")  # Set invalid state to red
            graph.graphviz_chart(dot.source, use_container_width=True) # Render the updated visualization

        else:
            dot.node(state, style="filled", fillcolor="yellow") # Set state to yellow if True                
            graph.graphviz_chart(dot.source, use_container_width=True) # Render the updated visualization

            time.sleep(0.5)  # Add a delay for blink effect
            dot.node(state, style="filled", fillcolor="white") # Set previous state back to white            
            graph.graphviz_chart(dot.source, use_container_width=True) # Render the updated visualization
