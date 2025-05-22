from graphviz import Digraph
import streamlit as st
import time

# List of regular expressions assigned to our group
regex_options = [
    "",
    "Alphabet Pattern",
    "Binary Pattern"
]

# DFA for (a+b)*(aa+bb)(aa+bb)*(ab+ba+aba)(bab+aba+bbb)(a+b+bb+aa)*(bb+aa+aba)(aaa+bab+bba)(aaa+bab+bba)*
dfa_1 = {
     "states": [f"q{i}" for i in range(46)], # 46 states
    "alphabet": ["a", "b"],
    "start_state": "q0",
    "end_states": ["q7", "q1", "q3", "q11","q5"],
    "transitions": {
        ("q0", "b"): "q45",
        ("q0", "a"): "q44",
        ("q45", "a"): "q44",
        ("q45", "b"): "q41",
        ("q44", "a"): "q39",
        ("q44", "b"): "q45",
        ("q39", "a"): "q43",
        ("q39", "b"): "q35",
        ("q35", "a"): "q31",
        ("q35", "b"): "q41",
        ("q31", "b"): "q25",
        ("q31", "a"): "q30",
        ("q25", "a"): "q23",
        ("q25", "b"): "q42",
        ("q42", "b"): "q22",
        ("q42", "a"): "q38",
        ("q38", "b"): "q33",
        ("q38", "a"): "q39",
        ("q33", "a"): "q29",
        ("q33", "b"): "q40",
        ("q29", "a"): "q30",
        ("q29", "b"): "q26",
        ("q43", "b"): "q33",
        ("q43", "a"): "q43",
        ("q30", "a"): "q43",
        ("q30", "b"): "q24",
        ("q26", "a"): "q22",
        ("q26", "b"): "q42",
        ("q24", "a"): "q22",
        ("q24", "b"): "q41",
        ("q40", "a"): "q23",
        ("q40", "b"): "q37",
        ("q41", "a"): "q38",
        ("q41", "b"): "q36",
        ("q36", "a"): "q32",
        ("q36", "b"): "q36",
        ("q37", "a"): "q32",
        ("q37", "b"): "q22",
        ("q32", "a"): "q30",
        ("q32", "b"): "q28",
        ("q28", "a"): "q27",
        ("q28", "b"): "q34",
        ("q27", "a"): "q23",
        ("q27", "b"): "q22",
        ("q23", "a"): "q39",
        ("q23", "b"): "q22",
        ("q34", "a"): "q30",
        ("q34", "b"): "q22",
        ("q22", "a"): "q18",
        ("q22", "b"): "q20",
        ("q20", "a"): "q18",
        ("q20", "b"): "q16",
        ("q18", "a"): "q13",
        ("q18", "b"): "q21",
        ("q21", "a"): "q13",
        ("q21", "b"): "q16",
        ("q13", "a"): "q12",
        ("q13", "b"): "q6",
        ("q16", "a"): "q9",
        ("q16", "b"): "q15",
        ("q9", "a"): "q17",
        ("q9", "b"): "q21",
        ("q17", "a"): "q11",
        ("q17", "b"): "q6",
        ("q6", "a"): "q2",
        ("q6", "b"): "q19",
        ("q19", "a"): "q11",
        ("q19", "b"): "q15",
        ("q15", "a"): "q10",
        ("q15", "b"): "q8",
        ("q10", "a"): "q17",
        ("q10", "b"): "q1",
        ("q2", "a"): "q12",
        ("q2", "b"): "q7",
        ("q7", "a"): "q14",
        ("q7", "b"): "q8",
        ("q1", "a"): "q12",
        ("q1", "b"): "q15",
        ("q14", "a"): "q4",
        ("q14", "b"): "q7",
        ("q8", "a"): "q3",
        ("q8", "b"): "q8",
        ("q12", "a"): "q4",
        ("q12", "b"): "q6",
        ("q3", "a"): "q4",
        ("q3", "b"): "q7",
        ("q11", "a"): "q4",
        ("q11", "b"): "q6",
        ("q4", "a"): "q5",
        ("q4", "b"): "q6",
        ("q5", "a"): "q5",
        ("q5", "b"): "q6",
    }
}

# DFA for (1+0)*(11+00+101+010)(11+00)*(11+00+0+1)(1+0+11)(11+00)*(101+000+111)(1+0)*(101+000+111+001+100)(11+00+1+0)*
dfa_2 = {
    "states": ["q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10", "q11", "q12", "q13", "q14", "q15", "q16", "q17", "q18", "q19", "q20", "q21", "q22", "q23", "q24", "q25", "q26", "q27", "q28", "q29", "q30", "q31", "q32"],
    "alphabet": ["1", "0"],
    "start_state": "q0",
    "end_states": ["q32"],
    "transitions": {
        ("q0", "1"): "q1",
        ("q0", "0"): "q2",
        ("q1", "1"): "q7",
        ("q1", "0"): "q4",
        ("q2", "1"): "q3",
        ("q2", "0"): "q5",
        ("q3", "1"): "q7",
        ("q3", "0"): "q9",
        ("q4", "1"): "q6",
        ("q4", "0"): "q5",
        ("q5", "1"): "q8",
        ("q5", "0"): "q12",
        ("q6", "1"): "q11",
        ("q6", "0"): "q11",
        ("q7", "0"): "q10",
        ("q7", "1"): "q11",
        ("q8", "1"): "q17",
        ("q8", "0"): "q13",
        ("q9", "1"): "q11",
        ("q9", "0"): "q12",
        ("q10", "0"): "q17",
        ("q10", "1"): "q15",
        ("q11", "0"): "q17",
        ("q11", "1"): "q17",
        ("q12", "1"): "q14",
        ("q12", "0"): "q17",
        ("q13", "0"): "q18",
        ("q13", "1"): "q21",
        ("q14", "1"): "q20",
        ("q14", "0"): "q24",
        ("q15", "1"): "q20",
        ("q15", "0"): "q16",
        ("q16", "0"): "q26",
        ("q16", "1"): "q17",
        ("q17", "1"): "q20",
        ("q17", "0"): "q25",
        ("q18", "0"): "q26",
        ("q18", "1"): "q14",
        ("q19", "0"): "q22",
        ("q19", "1"): "q28",
        ("q20", "0"): "q22",
        ("q20", "1"): "q19",
        ("q21", "0"): "q23",
        ("q21", "1"): "q23",
        ("q22", "0"): "q26",
        ("q22", "1"): "q28",
        ("q23", "0"): "q25",
        ("q23", "1"): "q28",
        ("q24", "0"): "q26",
        ("q24", "1"): "q21",
        ("q25", "0"): "q26",
        ("q25", "1"): "q20",
        ("q26", "0"): "q28",
        ("q26", "1"): "q20",
        ("q27", "0"): "q31",
        ("q27", "1"): "q29",
        ("q28", "0"): "q27",
        ("q28", "1"): "q29",
        ("q29", "0"): "q31",
        ("q29", "1"): "q30",
        ("q30", "0"): "q31",
        ("q30", "1"): "q32",
        ("q31", "0"): "q32",
        ("q31", "1"): "q32",
        ("q32", "0"): "q32",
        ("q32", "1"): "q32",
        
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
    "states": [
    "Start", "Read2", "Read4", "Read6", "Read8", "Read9", "Read10", "Read12", "Read13", "Read14",
    "Read15", "Read16", "Read17", "Read18", "Read19", "Read20", "Read21", "Read22", "Read23", "Read24",
    "Read25", "Read26", "Read27", "Read28", "Read29", "Read30", "Read31", "Read32", "Read33", "Read34",
    "Read35", "Read36", "Read37", "Read38", "Read39", "Read40", "Read41", "Read42", "Read43", "Read44",
    "Read45"
],  # 46 states
    "alphabet": ["a", "b"],
    "start_state": "Start",
    "push_states": [None],  # Not using stack operations
    "pop_states": [None],   # Not using stack operations
    "accept_states": ["Accept7", "Accept1", "Accept3", "Accept11", "Accept5"],  # Same as end_states in DFA
    "transitions": {
        ("Start", ""): "Read44",
        ("Read45", "a"): "Read44",
        ("Read45", "b"): "Read41",
        ("Read44", "a"): "Read39",
        ("Read44", "b"): "Read45",
        ("Read39", "a"): "Read43",
        ("Read39", "b"): "Read35",
        ("Read35", "a"): "Read31",
        ("Read35", "b"): "Read41",
        ("Read31", "b"): "Read25",
        ("Read31", "a"): "Read30",
        ("Read25", "a"): "Read23",
        ("Read25", "b"): "Read42",
        ("Read42", "b"): "Read22",
        ("Read42", "a"): "Read38",
        ("Read38", "b"): "Read33",
        ("Read38", "a"): "Read39",
        ("Read33", "a"): "Read29",
        ("Read33", "b"): "Read40",
        ("Read29", "a"): "Read30",
        ("Read29", "b"): "Read26",
        ("Read43", "b"): "Read33",
        ("Read43", "a"): "Read43",
        ("Read30", "a"): "Read43",
        ("Read30", "b"): "Read24",
        ("Read26", "a"): "Read22",
        ("Read26", "b"): "Read42",
        ("Read24", "a"): "Read22",
        ("Read24", "b"): "Read41",
        ("Read40", "a"): "Read23",
        ("Read40", "b"): "Read37",
        ("Read41", "a"): "Read38",
        ("Read41", "b"): "Read36",
        ("Read36", "a"): "Read32",
        ("Read36", "b"): "Read36",
        ("Read37", "a"): "Read32",
        ("Read37", "b"): "Read22",
        ("Read32", "a"): "Read30",
        ("Read32", "b"): "Read28",
        ("Read28", "a"): "Read27",
        ("Read28", "b"): "Read34",
        ("Read27", "a"): "Read23",
        ("Read27", "b"): "Read22",
        ("Read23", "a"): "Read39",
        ("Read23", "b"): "Read22",
        ("Read34", "a"): "Read30",
        ("Read34", "b"): "Read22",
        ("Read22", "a"): "Read18",
        ("Read22", "b"): "Read20",
        ("Read20", "a"): "Read18",
        ("Read20", "b"): "Read16",
        ("Read18", "a"): "Read13",
        ("Read18", "b"): "Read21",
        ("Read21", "a"): "Read13",
        ("Read21", "b"): "Read16",
        ("Read13", "a"): "Read12",
        ("Read13", "b"): "Read6",
        ("Read16", "a"): "Read9",
        ("Read16", "b"): "Read15",
        ("Read9", "a"): "Read17",
        ("Read9", "b"): "Read21",
        ("Read17", "a"): "Accept11",
        ("Read17", "b"): "Read6",
        ("Read6", "a"): "Read2",
        ("Read6", "b"): "Read19",
        ("Read19", "a"): "Accept11",
        ("Read19", "b"): "Read15",
        ("Read15", "a"): "Read10",
        ("Read15", "b"): "Read8",
        ("Read10", "a"): "Read17",
        ("Read10", "b"): "Accept1",
        ("Read2", "a"): "Read12",
        ("Read2", "b"): "Accept7",
        ("Accept7", "a"): "Read14",
        ("Accept7", "b"): "Read8",
        ("Accept1", "a"): "Read12",
        ("Accept1", "b"): "Read15",
        ("Read14", "a"): "Read4",
        ("Read14", "b"): "Accept7",
        ("Read8", "a"): "Accept3",
        ("Read8", "b"): "Read8",
        ("Read12", "a"): "Read4",
        ("Read12", "b"): "Read6",
        ("Accept3", "a"): "Read4",
        ("Accept3", "b"): "Accept7",
        ("Accept11", "a"): "Read4",
        ("Accept11", "b"): "Read6",
        ("Read4", "a"): "Accept5",
        ("Read4", "b"): "Read6",
        ("Accept5", "a"): "Accept5",
        ("Accept5", "b"): "Read6",
    }
}
# PDA for (1+0)*(11+00+101+010)(11+00)*(11+00+0+1)(1+0+11)(11+00)*(101+000+111)(1+0)*(101+000+111+001+100)(11+00+1+0)*
pda_2 = {
    "states": [f"Read{i}" for i in range(33)] + ["Accept"],  # 33 states (Read0-Read32) plus Accept
    "alphabet": ["1", "0"],
    "start_state": "Start",
    "push_states": [None],
    "pop_states": [None],
    "accept_states": ["Accept"],
    "transitions": {
        ("Start", ""): "Read0",
        ("Read0", "1"): "Read1",
        ("Read0", "0"): "Read2",
        ("Read1", "1"): "Read7",
        ("Read1", "0"): "Read4",
        ("Read2", "1"): "Read3",
        ("Read2", "0"): "Read5",
        ("Read3", "1"): "Read7",
        ("Read3", "0"): "Read9",
        ("Read4", "1"): "Read6",
        ("Read4", "0"): "Read5",
        ("Read5", "1"): "Read8",
        ("Read5", "0"): "Read12",
        ("Read6", "1"): "Read11",
        ("Read6", "0"): "Read11",
        ("Read7", "0"): "Read10",
        ("Read7", "1"): "Read11",
        ("Read8", "1"): "Read17",
        ("Read8", "0"): "Read13",
        ("Read9", "1"): "Read11",
        ("Read9", "0"): "Read12",
        ("Read10", "0"): "Read17",
        ("Read10", "1"): "Read15",
        ("Read11", "0"): "Read17",
        ("Read11", "1"): "Read17",
        ("Read12", "1"): "Read14",
        ("Read12", "0"): "Read17",
        ("Read13", "0"): "Read18",
        ("Read13", "1"): "Read21",
        ("Read14", "1"): "Read20",
        ("Read14", "0"): "Read24",
        ("Read15", "1"): "Read20",
        ("Read15", "0"): "Read16",
        ("Read16", "0"): "Read26",
        ("Read16", "1"): "Read17",
        ("Read17", "1"): "Read20",
        ("Read17", "0"): "Read25",
        ("Read18", "0"): "Read26",
        ("Read18", "1"): "Read14",
        ("Read19", "0"): "Read22",
        ("Read19", "1"): "Read28",
        ("Read20", "0"): "Read22",
        ("Read20", "1"): "Read19",
        ("Read21", "0"): "Read23",
        ("Read21", "1"): "Read23",
        ("Read22", "0"): "Read26",
        ("Read22", "1"): "Read28",
        ("Read23", "0"): "Read25",
        ("Read23", "1"): "Read28",
        ("Read24", "0"): "Read26",
        ("Read24", "1"): "Read21",
        ("Read25", "0"): "Read26",
        ("Read25", "1"): "Read20",
        ("Read26", "0"): "Read28",
        ("Read26", "1"): "Read20",
        ("Read27", "0"): "Read31",
        ("Read27", "1"): "Read29",
        ("Read28", "0"): "Read27",
        ("Read28", "1"): "Read29",
        ("Read29", "0"): "Read31",
        ("Read29", "1"): "Read30",
        ("Read30", "0"): "Read31",
        ("Read30", "1"): "Read32",
        ("Read31", "0"): "Read32",
        ("Read31", "1"): "Read32",
        ("Read32", "0"): "Read32",
        ("Read32", "1"): "Read32",
        # Adding epsilon transition from accepting state to Accept
        ("Read32", "^"): "Accept"
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
    transitions_used = []
    current_state = dfa["start_state"]

    # Iterate through each character in string
    for i, char in enumerate(string):
        # Check if transition has "0,1", if so replace char with "0,1"
        if (current_state,"0,1") in dfa["transitions"].keys():
            char = "0,1"
        
        # Check if transition has "a,b", if so replace char with "a,b"
        if (current_state,"a,b") in dfa["transitions"].keys():
            char = "a,b"
        
        transition = (current_state, char)
        transition_exists = transition in dfa["transitions"].keys()
        
        # Store the state, validity, and the character that was processed
        state_checks.append((current_state, transition_exists, char))

        # Check if current char is in transitions
        if transition_exists:
            next_state = dfa["transitions"][transition]
            # Store the transition that was used
            transitions_used.append((current_state, next_state, char))
            current_state = next_state
        # Return False if current character in the string is not in the dfa transitions
        else:
            return False, state_checks, transitions_used
    
    # Add state check for last transition
    if current_state in dfa["end_states"]:
        state_checks.append((current_state, True, None))
    else:
        state_checks.append((current_state, False, None))

    result = current_state in dfa["end_states"] # Checks if last current_state is in dfa end_states

    # Return the validation result, state_checks array, and transitions_used
    return (result, state_checks, transitions_used)

# Generate validation animation
def animate_dfa_validation(dfa, state_checks, transitions_used):
    graph_placeholder = st.empty()
    completed_transitions = []

    # Generate all transitions only once
    all_edges = list(dfa["transitions"].items())

    for i, state_check in enumerate(state_checks):
        state, is_valid, char = state_check if len(state_check) == 3 else (*state_check, None)

        dot = Digraph(engine="dot", graph_attr={'rankdir': 'LR'})

        # Add states (highlight current state)
        for s in dfa["states"]:
            if s == state:
                color = "green" if s in dfa["end_states"] and is_valid else "red" if not is_valid else "yellow"
                dot.node(s, style="filled", fillcolor=color, shape="doublecircle" if s in dfa["end_states"] else "circle")
            else:
                dot.node(s, shape="doublecircle" if s in dfa["end_states"] else "circle")

        # Add all transitions, using blue for completed, red for current
        for (src, sym), dest in all_edges:
            edge_color = "black"
            penwidth = "1.0"

            if (src, dest, sym) in completed_transitions:
                edge_color = "blue"
                penwidth = "2.0"
            elif i < len(transitions_used) and transitions_used[i] == (src, dest, sym):
                edge_color = "red"
                penwidth = "3.0"

            dot.edge(src, dest, label=sym, color=edge_color, penwidth=penwidth)

        if i < len(transitions_used):
            completed_transitions.append(transitions_used[i])

        graph_placeholder.graphviz_chart(dot.source, use_container_width=True)
        time.sleep(0.5)
