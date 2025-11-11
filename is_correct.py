import json
import sys
import os

output_dir = sys.argv[1]

# Define your filtering criteria in a function
def dominates(other_solution, solution):
    score1 = other_solution['score']['Int']
    score2 = solution['score']['Int']
    
    if score1 < score2:
        return True 
    m1 = []
    m2 = []
    m3 = []
    m4 = []

    for row in other_solution['rel1_RelationAsMatrix']['AbstractLiteral']['Matrix']:
        for cell in row:
            if isinstance(cell, dict):
                for el in cell['AbstractLiteral']['Matrix']:
                    if isinstance(el, list) and len(el)>0:
                        for k in el:
                            m1.append(k['Int'])

    for row in solution['rel1_RelationAsMatrix']['AbstractLiteral']['Matrix']:
        for cell in row:
            if isinstance(cell, dict):
                for el in cell['AbstractLiteral']['Matrix']:
                    if isinstance(el, list) and len(el)>0:
                        for k in el:
                            m2.append(k['Int'])

    for row in other_solution['rel2_RelationAsMatrix']['AbstractLiteral']['Matrix']:
        for cell in row:
            if isinstance(cell, dict):
                for el in cell['AbstractLiteral']['Matrix']:
                    if isinstance(el, list) and len(el)>0:
                        for k in el:
                            m3.append(k['Int'])

    for row in solution['rel2_RelationAsMatrix']['AbstractLiteral']['Matrix']:
        for cell in row:
            if isinstance(cell, dict):
                for el in cell['AbstractLiteral']['Matrix']:
                    if isinstance(el, list) and len(el)>0:
                        for k in el:
                            m4.append(k['Int'])



    for i in range(0,len(m1)):
        if m2[i]>m1[i]:
            return False
    
    for i in range(0,len(m3)):
        if m4[i]>m3[i]:
            return False

    return True


def filter_json(input_file):
   
    with open(input_file, 'r') as infile:
   
        data = json.load(infile)
        filtered_solutions = []
        for i in range(len(data)):
            for j in range(i):  # j ranges from 0 to i-1
                if dominates(data[j], data[i]):
                    print(data[j], "dominates\n\n\n\n", data[i])
                    filtered_solutions.append(data[i])  # 

input_file = os.path.join(output_dir, 'sols.json')


# Run the filter function
filter_json(input_file)
