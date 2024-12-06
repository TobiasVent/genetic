import random
import time
from itertools import combinations
import numpy as np

import csv

#global variables
starttime = time.time()




def evaluate(solution, clauses):
    eval_result = 0
    for clause in clauses:
        # Evaluate the clause: a clause is satisfied if at least one literal is True
        for element in clause:
            if (element > 0 and solution[element - 1]) or (element < 0 and not solution[abs(element) - 1]):
                eval_result += 1
                break
    return eval_result


def process_cnf(cnf_content):
    clauses = []
    num_vars, num_clauses = 0, 0
    
    for line in cnf_content.splitlines():
        line = line.strip()
     
        if not line or line.startswith('c'):
            continue
        if line.startswith("%"):

            continue
        if line.startswith("0"):
            continue
      
        if line.startswith('p cnf'):
            parts = line.split()

            num_vars = int(parts[2])
            num_clauses = int(parts[3])
        else:
           
            clause = list(map(int, line.split()))
            
            if clause[-1] != 0:
                clause.append(0)
           
            clauses.append(clause[:-1])
    
    return num_vars, num_clauses, clauses

def create_random_solution(n):
    # Randomly generate a solution as a list of boolean values
    return [random.choice([True, False]) for _ in range(n)]

def create_flip_positions(n, max_dist):
    flip_positions = {}
    for dist in range(1, max_dist + 1):
        positions = list(combinations(range(n), dist))
        random.shuffle(positions)  # Shuffle once and reuse
        flip_positions[dist] = positions
    return flip_positions


def pertubate(distance,solution,num_vars):
    flip_positions = []
    # flip_position = list(range(distance))
    # flip_position = combinations(flip_position,2)
    # flip_position = list(flip_position)
    # random.shuffle(flip_position)
    flip_positions = np.random.choice(np.arange(0, num_vars), size=distance, replace=False)
    new_solution = solution[:]
    for pos in flip_positions:
        new_solution[pos] = not new_solution[pos]
    return new_solution

def write_results_to_csv(filename, results):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Evaluation", "Objective Count", "Runtime (seconds)"])  # Write header
        writer.writerows(results)

def next_ascent(num_vars,clauses,solution,result,eval_count):
    succes = False
    improvement = True
    while improvement:
        flip_positions = list(range(0, num_vars))

        # Shuffle the list to get a random order
        random.shuffle(flip_positions)
        improvement = False
        for position in flip_positions:
                # Flip positions in the current solution
                new_solution = solution[:]
                #for pos in positions:
                new_solution[position] = not new_solution[position]

                new_result = evaluate(new_solution, clauses)
                eval_count = eval_count +1 

                if new_result > result:
                    result = new_result
                    solution = new_solution
                    improvement = True
                    if result == len(clauses):
                        
                        succes = True
                        return result, solution, eval_count, succes
                    
                    break  # Exit once an improvement is found

    
    return result, solution, eval_count, succes

def integrated_local_search(num_vars, clauses, solution, result, max_evals=10000000):
    eval_count = 0
    result, solution, eval_count, succes = next_ascent(num_vars,clauses,solution,result,eval_count)
    while eval_count < max_evals:
        new_solution = pertubate(6,solution, num_vars)
        new_result = evaluate(solution, clauses)
        new_result, new_solution, eval_count, succes = next_ascent(num_vars,clauses,new_solution,new_result,eval_count)
        if succes:
            endtime = time.time()
            return new_result, new_solution, eval_count, endtime - starttime
        if new_result > result:
            result = new_result
            solution = new_solution
    endtime = time.time()
    return result, solution, eval_count, endtime - starttime



# with open("uf100-01.cnf", 'r') as file:
#     # Lese den Inhalt der Datei
#     content = file.read()
# # Process the CNF content
# num_vars, num_clauses, clauses = process_cnf(content)    
    
    
# solution = create_random_solution(num_vars)
# result = evaluate(solution, clauses)
# eval_result, solution, objective_count, runtime = integrated_local_search(num_vars,clauses,solution,result)


# print("result: " + str(result) + " after "+ str(objective_count)+ " evaluation")
    
    
with open("uf20-01.cnf", 'r') as file:
    uf20 = file.read()
with open("uf100-01.cnf", 'r') as file:
    uf100 = file.read()
with open("uf250-01.cnf", 'r') as file:
    uf250 = file.read()


all_results = []
for i in range(30):
    num_vars, num_clauses, clauses = process_cnf(uf20)
  
    solution = create_random_solution(num_vars)
    result = evaluate(solution, clauses)
    eval_result, solution, objective_count, runtime = integrated_local_search(num_vars, clauses, solution, result)
    all_results.append([eval_result, objective_count, runtime]) 
write_results_to_csv("integrated_local_search_results_uf20.csv", all_results)  

all_results = []
for i in range(30):
    num_vars, num_clauses, clauses = process_cnf(uf100)
    max_dist = 1
    solution = create_random_solution(num_vars)
    result = evaluate(solution, clauses)
    eval_result, solution, objective_count, runtime = integrated_local_search(num_vars, clauses, solution, result)
    all_results.append([eval_result, objective_count, runtime]) 
write_results_to_csv("integrated_local_search_results_uf100.csv", all_results) 

all_results = []
for i in range(30):
    num_vars, num_clauses, clauses = process_cnf(uf250)
    max_dist = 1
    solution = create_random_solution(num_vars)
    result = evaluate(solution, clauses)
    eval_result, solution, objective_count, runtime = integrated_local_search(num_vars, clauses, solution, result)
    all_results.append([eval_result, objective_count, runtime]) 
write_results_to_csv("integrated_local_search_results_uf250.csv", all_results)







  
    
    
    
    
