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
               "q11", "q12", "q13", "q14", "q15", "q16", "q17",],
    "alphabet": ["a", "b"],
    "start_state": "q0",
    "end_states": ["q13","q14","q17"],
    "transitions": {
        # (a+b)*
        ("q0", "a"): "q1",
        ("q0", "b"): "q2",
        
        # (aa+bb) detection
        ("q1", "a"): "q3",  # aa
        ("q1", "b"): "q2",
        ("q2", "a"): "q1",
        ("q2", "b"): "q4",  # bb
        
        # (aa+bb)* looping
        ("q3", "a"): "q3",
        ("q3", "b"): "q5",  # start ab/aba
        ("q4", "a"): "q6",  # start ba
        ("q4", "b"): "q4",
        
        # (ab+ba+aba)
        ("q5", "a"): "q7",  # aba
        ("q5", "b"): "q4",  # invalid
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
        
        
        # (aaa+bab+bba)* looping
        ("q17", "a"): "q17",  # start new aaa
        ("q17", "b"): "q13"   # start new bab/bba
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
