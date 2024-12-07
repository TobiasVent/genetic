import random
import time
import csv
from itertools import combinations


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


def variable_neighbourhood_ascent(num_vars, clauses, solution, result, max_dist, multistart=False, max_evals=10000000):
    flip_positions = create_flip_positions(num_vars, max_dist)
    improvement = True
    eval_count = 0
    starttime = time.time()
    best_result = 0
    while improvement and eval_count < max_evals:
        improvement = False
        for dist in range(1, max_dist + 1):
            for positions in flip_positions[dist]:
                # Flip positions in the current solution
                new_solution = solution[:]
                for pos in positions:
                    new_solution[pos] = not new_solution[pos]

                new_result = evaluate(new_solution, clauses)
                eval_count += 1

                if new_result > result:
                    result = new_result
                    solution = new_solution
                    improvement = True
                    if result == len(clauses):
                        endtime = time.time()
                        return result, eval_count, endtime - starttime
                    
                    break  # Exit once an improvement is found
            
            if improvement:
                break  # Go back to distance 1 when improvement is found
    if multistart:
            if result > best_result:
                best_result = result
            improvement = True
            solution = create_random_solution(num_vars)
            result = evaluate(solution, clauses)
            eval_count += 1
    else:
            best_result = result

    endtime = time.time()
    return best_result, eval_count, endtime - starttime


# Write results to a CSV file
def write_results_to_csv(filename, results):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Evaluation", "Objective Count", "Runtime (seconds)"])  # Write header
        writer.writerows(results)


# Read CNF file
# with open("uf20-01.cnf", 'r') as file:
#     content = file.read()

# num_vars, num_clauses, clauses = process_cnf(content)
# max_dist = 3

# # Collect all results
# all_results = []

# for i in range(30):
#     solution = create_random_solution(num_vars)
#     result = evaluate(solution, clauses)
#     eval_result, objective_count, runtime = variable_neighbourhood_ascent(num_vars, clauses, solution, result, max_dist, False)
#     all_results.append([eval_result, objective_count, runtime])  # Store results

# # Save results to CSV
# write_results_to_csv("hill_climbing_results.csv", all_results)



    
with open("uf20-01.cnf", 'r') as file:
    uf20 = file.read()
with open("uf100-01.cnf", 'r') as file:
    uf100 = file.read()
with open("uf250-01.cnf", 'r') as file:
    uf250 = file.read()


# all_results = []
# for i in range(30):
#     num_vars, num_clauses, clauses = process_cnf(uf20)
#     max_dist = 1
#     solution = create_random_solution(num_vars)
#     result = evaluate(solution, clauses)
#     eval_result, objective_count, runtime = variable_neighbourhood_ascent(num_vars, clauses, solution, result, max_dist, False)
#     all_results.append([eval_result, objective_count, runtime]) 
# write_results_to_csv("hill_climbing_results_uf20.csv", all_results)  

# all_results = []
# for i in range(30):
#     num_vars, num_clauses, clauses = process_cnf(uf100)
#     max_dist = 1
#     solution = create_random_solution(num_vars)
#     result = evaluate(solution, clauses)
#     eval_result, objective_count, runtime = variable_neighbourhood_ascent(num_vars, clauses, solution, result, max_dist, False)
#     all_results.append([eval_result, objective_count, runtime]) 
# write_results_to_csv("hill_climbing_results_uf100.csv", all_results) 

# all_results = []
# for i in range(30):
#     num_vars, num_clauses, clauses = process_cnf(uf250)
#     max_dist = 1
#     solution = create_random_solution(num_vars)
#     result = evaluate(solution, clauses)
#     eval_result, objective_count, runtime = variable_neighbourhood_ascent(num_vars, clauses, solution, result, max_dist, False)
#     all_results.append([eval_result, objective_count, runtime]) 
# write_results_to_csv("hill_climbing_results_uf250.csv", all_results)



# all_results = []
# for i in range(30):
#     num_vars, num_clauses, clauses = process_cnf(uf20)
#     max_dist = 1
#     solution = create_random_solution(num_vars)
#     result = evaluate(solution, clauses)
#     eval_result, objective_count, runtime = variable_neighbourhood_ascent(num_vars, clauses, solution, result, max_dist, True)
#     all_results.append([eval_result, objective_count, runtime]) 
# write_results_to_csv("multistart_hill_climbing_results_uf20.csv", all_results) 

# all_results = []
# for i in range(30):
#     num_vars, num_clauses, clauses = process_cnf(uf100)
#     max_dist = 1
#     solution = create_random_solution(num_vars)
#     result = evaluate(solution, clauses)
#     eval_result, objective_count, runtime = variable_neighbourhood_ascent(num_vars, clauses, solution, result, max_dist, True)
#     all_results.append([eval_result, objective_count, runtime]) 
# write_results_to_csv("multistart_hill_climbing_results_uf100.csv", all_results) 

# all_results = []
# for i in range(30):
#     num_vars, num_clauses, clauses = process_cnf(uf250)
#     max_dist = 1
#     solution = create_random_solution(num_vars)
#     result = evaluate(solution, clauses)
#     eval_result, objective_count, runtime = variable_neighbourhood_ascent(num_vars, clauses, solution, result, max_dist, True)
#     all_results.append([eval_result, objective_count, runtime]) 
# write_results_to_csv("multistart_hill_climbing_results_uf250.csv", all_results) 



all_results = []
for i in range(30):
    num_vars, num_clauses, clauses = process_cnf(uf20)
    max_dist = 3
    solution = create_random_solution(num_vars)
    result = evaluate(solution, clauses)
    eval_result, objective_count, runtime = variable_neighbourhood_ascent(num_vars, clauses, solution, result, max_dist, False)
    all_results.append([eval_result, objective_count, runtime]) 
write_results_to_csv("variable_neighbourhood_ascent_uf20.csv", all_results) 



all_results = []
for i in range(30):
    num_vars, num_clauses, clauses = process_cnf(uf100)
    max_dist = 3
    solution = create_random_solution(num_vars)
    result = evaluate(solution, clauses)
    eval_result, objective_count, runtime = variable_neighbourhood_ascent(num_vars, clauses, solution, result, max_dist, False)
    all_results.append([eval_result, objective_count, runtime]) 
write_results_to_csv("variable_neighbourhood_ascent_uf100.csv", all_results) 


all_results = []
for i in range(30):
    num_vars, num_clauses, clauses = process_cnf(uf250)
    max_dist = 3
    solution = create_random_solution(num_vars)
    result = evaluate(solution, clauses)
    eval_result, objective_count, runtime = variable_neighbourhood_ascent(num_vars, clauses, solution, result, max_dist, False)
    all_results.append([eval_result, objective_count, runtime]) 
write_results_to_csv("variable_neighbourhood_ascent_uf250.csv", all_results) 




# all_results = []
# for i in range(30):
#     num_vars, num_clauses, clauses = process_cnf(uf20)
#     max_dist = 3
#     solution = create_random_solution(num_vars)
#     result = evaluate(solution, clauses)
#     eval_result, objective_count, runtime = variable_neighbourhood_ascent(num_vars, clauses, solution, result, max_dist, True)
#     all_results.append([eval_result, objective_count, runtime]) 
# write_results_to_csv("multistart_variable_neighbourhood_ascent_uf20.csv", all_results) 


# all_results = []
# for i in range(30):
#     num_vars, num_clauses, clauses = process_cnf(uf100)
#     max_dist = 3
#     solution = create_random_solution(num_vars)
#     result = evaluate(solution, clauses)
#     eval_result, objective_count, runtime = variable_neighbourhood_ascent(num_vars, clauses, solution, result, max_dist, True)
#     all_results.append([eval_result, objective_count, runtime]) 
# write_results_to_csv("multistart_variable_neighbourhood_ascent_uf100.csv", all_results) 


# all_results = []
# for i in range(30):
#     num_vars, num_clauses, clauses = process_cnf(uf250)
#     max_dist = 3
#     solution = create_random_solution(num_vars)
#     result = evaluate(solution, clauses)
#     eval_result, objective_count, runtime = variable_neighbourhood_ascent(num_vars, clauses, solution, result, max_dist, True)
#     all_results.append([eval_result, objective_count, runtime]) 
# write_results_to_csv("multistart_variable_neighbourhood_ascent_uf250.csv", all_results) 