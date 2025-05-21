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
               "q11", "q12", "q13", "q14", "q15", "q16", "q17", "q18"],
    "alphabet": ["a", "b"],
    "start_state": "q0",
    "end_states": ["q13","q14", "q18"],
    "transitions": {
        # (a+b)*
        ("q0", "a"): "q1",
        ("q0", "b"): "q2",
        
        # (aa+bb) detection
        ("q1", "a"): "q3",  # aa
        ("q2", "b"): "q4",  # bb
        
        # (aa+bb)* looping
        ("q3", "a"): "q3",
        ("q3", "b"): "q5",  # start ab/aba
        ("q4", "a"): "q6",  # start ba
        ("q4", "b"): "q4",
        
        # (ab+ba+aba)
        ("q5", "a"): "q7",  # aba
        ("q6", "a"): "q3",
        ("q6", "b"): "q7",  # ba
        ("q7", "a"): "q8",
        ("q7", "b"): "q9",  # bab
        
        # (bab+aba+bbb)
        ("q8", "a"): "q10",  # aba done
        ("q8", "b"): "q10",
        ("q9", "a"): "q10",  # bab done
        ("q9", "b"): "q10",  # bbb done
        
        # (a+b+bb+aa)*
        ("q10", "a"): "q10",
        ("q10", "b"): "q10",
        
        # MANDATORY (bb+aa+aba)
        ("q10", "a"): "q11",  # start aa/aba
        ("q10", "b"): "q11",  # start bb
        ("q11", "a"): "q12",  # first 'a' of aa/aaa/aba
        ("q11", "b"): "q13",  # first 'b' of bb/bab/bba
        
        # STRICT (aaa+bab+bba) enforcement
        ("q12", "a"): "q14",    # second 'a' of aaa
        ("q14", "a"): "q18",     # aaa complete (accept)
        ("q12", "b"): "q15",     # aba path
        ("q15", "a"): "q18",     # aba complete (accept)
        ("q13", "a"): "q18",     # bba complete (ba)
        ("q13", "b"): "q16",     # bb → check bab/bba
        ("q16", "a"): "q18",     # bab complete (a)
        ("q16", "b"): "q17",     # invalid (bbb)
        ("q17", "a"): "q18",     # bba complete
        ("q17", "b"): "q17",     # invalid (bbbb...)
        
        # (aaa+bab+bba)* looping
        ("q18", "a"): "q12",  # start new aaa
        ("q18", "b"): "q13"   # start new bab/bba
    }
}
# DFA for (1+0)*(11+00+101+010)(11+00)*(11+00+0+1)(1+0+11)(11+00)*(101+000+111)(1+0)*(101+000+111+001+100)(11+00+1+0)*
dfa_2 = {
     "states": ["q0", "qA", "qB1", "qB2", "qB3", "qB4", "qC1", "qC2", "qD", "qE1", "qE2", 
               "qF1", "qF2", "qG1", "qG2", "qG3", "qH", "qI1", "qI2", "qJ1", "qJ2", "q_accept", "q_reject"],
    "alphabet": ["0", "1"],
    "start_state": "q0",
    "end_states": ["q_accept"],
    "transitions": {
        # ======================
        # Component A: (1+0)*
        # ======================
        ("q0", "0"): "qA",
        ("q0", "1"): "qA",
        ("qA", "0"): "qA",
        ("qA", "1"): "qA",
        
        # ======================
        # Component B: (11+00+101+010)
        # ======================
        ("qA", "0"): "qB1",  # Start 00 or 010
        ("qA", "1"): "qB2",  # Start 11 or 101
        
        # Path for 00
        ("qB1", "0"): "qB3",  # 00 complete
        ("qB1", "1"): "qB4",  # 01 (start 010)
        
        # Path for 010
        ("qB4", "0"): "qB3",  # 010 complete
        ("qB4", "1"): "q_reject",
        
        # Path for 11
        ("qB2", "0"): "qB4",  # 10 (start 101)
        ("qB2", "1"): "qB3",  # 11 complete
        
        # Path for 101
        ("qB4", "1"): "qB3",  # 101 complete
        
        # ======================
        # Component C: (11+00)*
        # ======================
        ("qB3", "0"): "qC1",  # Start new 00
        ("qB3", "1"): "qC2",  # Start new 11
        
        ("qC1", "0"): "qB3",  # 00 complete (loop)
        ("qC1", "1"): "q_reject",
        
        ("qC2", "0"): "q_reject",
        ("qC2", "1"): "qB3",  # 11 complete (loop)
        
        # ======================
        # Component D: (11+00+0+1)
        # ======================
        ("qB3", "0"): "qD",  # Single 0
        ("qB3", "1"): "qD",  # Single 1
        
        # ======================
        # Component E: (1+0+11)
        # ======================
        ("qD", "0"): "qE1",  # Single 0
        ("qD", "1"): "qE2",  # Single 1 or start 11
        
        ("qE2", "0"): "qE1",
        ("qE2", "1"): "qE1",  # 11 complete
        
        # ======================
        # Component F: (11+00)*
        # ======================
        ("qE1", "0"): "qF1",  # Start 00
        ("qE1", "1"): "qF2",  # Start 11
        
        ("qF1", "0"): "qE1",  # 00 complete (loop)
        ("qF1", "1"): "q_reject",
        
        ("qF2", "0"): "q_reject",
        ("qF2", "1"): "qE1",  # 11 complete (loop)
        
        # ======================
        # Component G: (101+000+111)
        # ======================
        ("qE1", "0"): "qG1",  # Start 000 or 101
        ("qE1", "1"): "qG2",  # Start 111
        
        # Path for 000
        ("qG1", "0"): "qG3",
        ("qG3", "0"): "qH",  # 000 complete
        
        # Path for 101
        ("qG1", "1"): "qG2",
        ("qG2", "0"): "qH",  # 101 complete
        
        # Path for 111
        ("qG2", "1"): "qG3",
        ("qG3", "1"): "qH",  # 111 complete
        
        # ======================
        # Component H: (1+0)*
        # ======================
        ("qH", "0"): "qH",
        ("qH", "1"): "qH",
        
        # ======================
        # Component I: (101+000+111+001+100)
        # ======================
        ("qH", "0"): "qI1",  # Start 000, 001, or 100
        ("qH", "1"): "qI2",  # Start 101 or 111
        
        # Paths omitted for brevity (similar to Component G)
        # ...
        
        # ======================
        # Component J: (11+00+1+0)*
        # ======================
        ("qI1", "0"): "qJ1",
        ("qI1", "1"): "qJ2",
        ("qI2", "0"): "qJ1",
        ("qI2", "1"): "qJ2",
        
        ("qJ1", "0"): "q_accept",  # 00 complete
        ("qJ1", "1"): "q_accept",  # 01
        ("qJ2", "0"): "q_accept",  # 10
        ("qJ2", "1"): "q_accept",  # 11 complete
        
        # Accept state loops
        ("q_accept", "0"): "qJ1",
        ("q_accept", "1"): "qJ2",
        
        # Global reject
        ("q_reject", "0"): "q_reject",
        ("q_reject", "1"): "q_reject"
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
S  → A B C D E F G H I J \n
A  → 1 A | 0 A | ε \n
B  → 11 | 00 | 101 | 010 \n
C  → 11 C | 00 C | ε \n
D  → 11 | 00 | 0 | 1 \n
E  → 1 | 0 | 11 \n
F  → 11F | 00F | ε \n
G  → 101 | 000 | 111 \n
H  → 1H | 0H | ε \n
I  → 101 | 000 | 111 | 001 | 100 \n
J  → KJ | ε \n
K  → 11 | 00 | 1 | 0 \n
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
        ("Read1", "a,b"): "Read1",  # Initial (a+b)* - any number of a's and b's
        ("Read1", "a"): "Read2",    # Beginning of the specific pattern
        ("Read1", "b"): "Read2",
        ("Read2", "a,b"): "Read3",  # Second character of the pattern
        ("Read3", "a,b"): "Read4",  # Continuing the pattern
        ("Read4", "a,b"): "Read5",  # More pattern processing 
        ("Read5", "a,b"): "Read6",  # More pattern processing
        ("Read6", "a,b"): "Read7",  # More pattern processing
        ("Read7", "a,b"): "Read8",  # Final pattern section
        ("Read8", "a,b"): "Read8",  # Optional repetition at the end
        ("Read8", "^"): "Accept",   # Accept when finished
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
