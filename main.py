from hyperon import MeTTa, SymbolAtom, ExpressionAtom, GroundedAtom
import os
import glob

metta = MeTTa()
metta.run(f"!(bind! &space (new-space))")

def load_dataset(path: str) -> None:
    if not os.path.exists(path):
        raise ValueError(f"Dataset path '{path}' does not exist.")
    paths = glob.glob(os.path.join(path, "**/*.metta"), recursive=True)
    if not paths:
        raise ValueError(f"No .metta files found in dataset path '{path}'.")
    for path in paths:
        print(f"Start loading dataset from '{path}'...")
        try:
            metta.run(f'''
                !(load-ascii &space {path})
                ''')
        except Exception as e:
            print(f"Error loading dataset from '{path}': {e}")
    print(f"Finished loading {len(paths)} datasets.")

# Example usage:
try:
    dataset = load_dataset("./Data")
   
except Exception as e:
    print(f"An error occurred: {e}")

# 2 Points   
def get_transcript(node):
    transcript = metta.run(f'''!(match &space (, (transcribed_to ({node[0]}) $transcript))(,(transcribed_to ({node[0]}) $transcript)))''')
    return transcript

#2 Points
def get_protein(node):
    transcript = metta.run(f'''!(match &space (, (transcribed_to ({node[0]}) $transcript)) $transcript)''')[0][0].get_children()
    protein = metta.run(f'''!(match &space (, (translates_to ({transcript[0]} {transcript[1]}) $protein))(,(translates_to ({transcript[0]} {transcript[1]}) $protein)))''')
    return protein

#6 Points
def metta_seralizer(metta_result):
    result = []

    for relation in metta_result[0]:
        children = relation.get_children()
        
        edge = children[1].get_children()[0]
        source_node = children[1].get_children()[1].get_children()
        source = f"{source_node[0].get_name()} {source_node[1].get_name()}"

        target_node = children[1].get_children()[2].get_children()
        target = f"{target_node[0].get_name()} {target_node[1].get_name()}"
               
        entry = {
            'edge': edge,
            'source': source,
            'target': target
        }
        result.append(entry)
    
    return result


#1
transcript_result= (get_transcript(['gene ENSG00000166913']))
print(transcript_result) 
"""
Expected Output Format::
# [[(, (transcribed_to (gene ENSG00000166913) (transcript ENST00000372839))), (, (transcribed_to (gene ENSG00000166913) (transcript ENST00000353703)))]]
""" 

#2
protein_result= (get_protein(['gene ENSG00000166913']))
print(protein_result) 
"""
Expected Output Format::
# [[(, (translates_to (transcript ENST00000353703) (protein P31946))), (, (translates_to (transcript ENST00000372839) (protein P31946)))]]
"""

#3
parsed_result = metta_seralizer(transcript_result)
print(parsed_result) 
"""
Expected Output Format:
[
    {'edge': 'transcribed_to', 'source': 'gene ENSG00000175793', 'target': 'transcript ENST00000339276'}
]
"""

