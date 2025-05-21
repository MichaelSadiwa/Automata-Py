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
  "states": ["q0", "q1", "q2", "q3", "q4", "q6", "q7", "q8", "q9", "q10", 
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
        ("q3", "b"): "q7",  # start ab/aba
        ("q4", "a"): "q6",  # start ba
        ("q4", "b"): "q4",
        
        # (ab+ba+aba)
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
  "states": [
        'q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9',
        'q10', 'q11', 'q12', 'q13', 'q14', 'q15', 'q16', 'q17', 'q18', 'q19',
        'q20', 'q21', 'q22', 'q23', 'q24', 'q25', 'q26', 'q27', 'q28', 'q29']
    
  "alphabet": ["0", "1"],
  "start_state": "q0",
  "end_states": ["q25", "q26", "q27", "q28"],
  "transitions": {
        # ======================
        # Component A: (1+0)*
        # ======================
        ('q0', '0'): 'q0',
        ('q0', '1'): 'q0',
        
        # Transition to Component B
        ('q0', '0'): 'q1',  # Start 00 or 010
        ('q0', '1'): 'q2',  # Start 11 or 101
        
        # ======================
        # Component B: (11+00+101+010)
        # ======================
        # Path for 00
        ('q1', '0'): 'q3',
        # Path for 010
        ('q1', '1'): 'q4',
        ('q4', '0'): 'q3',
        
        # Path for 11
        ('q2', '1'): 'q3',
        # Path for 101
        ('q2', '0'): 'q4',
        ('q4', '1'): 'q3',
        
        # ======================
        # Component C: (11+00)*
        # ======================
        ('q3', '0'): 'q5',
        ('q3', '1'): 'q6',
        ('q5', '0'): 'q3',  # 00 loop
        ('q6', '1'): 'q3',  # 11 loop
        
        # Transition to Component D
        ('q3', '0'): 'q7',
        ('q3', '1'): 'q8',
        
        # ======================
        # Component D: (11+00+0+1)
        # ======================
        ('q7', '0'): 'q9',  # 00
        ('q7', '1'): 'q10', # 01
        ('q8', '0'): 'q11', # 10
        ('q8', '1'): 'q12', # 11
        
        # Single symbol paths
        ('q7', '0'): 'q13', # Single 0
        ('q7', '1'): 'q13', # Single 1
        ('q8', '0'): 'q13',
        ('q8', '1'): 'q13',
        
        # ======================
        # Component E: (1+0+11)
        # ======================
        ('q13', '0'): 'q14',
        ('q13', '1'): 'q15',
        ('q15', '1'): 'q14',  # 11 path
        
        # ======================
        # Component F: (11+00)*
        # ======================
        ('q14', '0'): 'q16',
        ('q14', '1'): 'q17',
        ('q16', '0'): 'q14',  # 00 loop
        ('q17', '1'): 'q14',  # 11 loop
        
        # ======================
        # Component G: (101+000+111)
        # ======================
        ('q14', '0'): 'q18',  # Start 000 or 101
        ('q14', '1'): 'q19',  # Start 111
        
        # Path for 000
        ('q18', '0'): 'q20',
        ('q20', '0'): 'q21',
        # Path for 101
        ('q18', '1'): 'q19',
        ('q19', '0'): 'q21',
        # Path for 111
        ('q19', '1'): 'q20',
        ('q20', '1'): 'q21',
        
        # ======================
        # Component H: (1+0)*
        # ======================
        ('q21', '0'): 'q21',
        ('q21', '1'): 'q21',
        
        # ======================
        # Component I: (101+000+111+001+100)
        # ======================
        ('q21', '0'): 'q22',  # Start 000, 001, or 100
        ('q21', '1'): 'q23',  # Start 101 or 111
        
        # Paths for 000, 001, 100
        ('q22', '0'): 'q24',
        ('q22', '1'): 'q24',
        ('q24', '0'): 'q25',
        ('q24', '1'): 'q25',
        
        # Paths for 101, 111
        ('q23', '0'): 'q25',
        ('q23', '1'): 'q24',
        ('q24', '1'): 'q25',
        
        # ======================
        # Component J: (11+00+1+0)*
        # ======================
        ('q25', '0'): 'q26',
        ('q25', '1'): 'q27',
        ('q26', '0'): 'q25',  # 00 loop
        ('q27', '1'): 'q25',  # 11 loop
        ('q26', '1'): 'q28',  # Single symbols
        ('q27', '0'): 'q28',
        ('q28', '0'): 'q28',
        ('q28', '1'): 'q28'
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
