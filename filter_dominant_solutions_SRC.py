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


def filter_json(input_file, output_file):
   
    with open(input_file, 'r') as infile:
   
        data = json.load(infile)
        filtered_solutions = []

        for solution in data:
            keep_solution = True
            for other_solution in data:
                if solution==other_solution:
                    continue
                if dominates(other_solution, solution):
                    keep_solution = False
                    break

            if keep_solution:
                filtered_solutions.append(solution)
        

    # Write the filtered solutions to the output file
    with open(output_file, 'w') as outfile:
        json.dump(filtered_solutions, outfile, indent=4)

    print(f"Filtered solutions have been saved to {output_file}.")

input_file = os.path.join(output_dir, 'sols.json')
output_file = os.path.join(output_dir, 'non-dominated.json')


# Run the filter function
filter_json(input_file, output_file)
