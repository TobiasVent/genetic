
import random
import time
from itertools import combinations
import csv
def evaluate(solution, clauses):
    eval_result = 0
    for clause in clauses:
        # Evaluate the clause: a clause is satisfied if at least one literal is True
        for element in clause:
            if (element > 0 and solution[element - 1]) or (element < 0 and not solution[abs(element) - 1]):
                eval_result += 1
                break
    return eval_result

def write_results_to_csv(filename, results):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Evaluation", "Objective Count", "Runtime (seconds)"])  # Write header
        writer.writerows(results)

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


def one_point_crossover(num_vars,population):
    positions = list(combinations(range(len(population)), 2))
    
    population.extend(population)
    
    random.shuffle(population)
    new_population = []
    for i in range(0,len(population),2):
        point1, point2 = sorted(random.sample(range(1, num_vars), 2))
        child1 = (population[i][:point1] + population[i+1][point1:point2] + population[i][point2:])
        child2 = (population[i+1][:point1] + population[i][point1:point2] + population[i+1][point2:])
        new_population.append(child1)
        new_population.append(child2)
    # new_population = []
    # for position in positions:
    # #    print("population[position[0]]: " + str(population[position[0]]))
    # #    print("population[position[1]]: " +  str(population[position[1]]))
    #     point1, point2 = sorted(random.sample(range(1, num_vars), 2))
    #     child1 = (population[position[0]][:point1] + population[position[1]][point1:point2] + population[position[0]][point2:])
    #     child2 = (population[position[1]][:point1] + population[position[0]][point1:point2] + population[position[1]][point2:])
    # #    child1 = population[position[0]][:crossover_point] + population[position[1]][crossover_point:]
    # #    child2 = population[position[1]][:crossover_point] + population[position[0]][crossover_point:]
    #     new_population.append(child1)
    #     new_population.append(child2)
    # #    print("child1: " + str(offspring1))
    # #    print("child2: " + str(offspring2))

    # random.shuffle(new_population)

    return new_population




def truncation_selection(population,clauses,selection_rate,objective_count):
    
    fitnesses = []
    for individual in population:
        fitness = evaluate(individual,clauses)
        objective_count += 1
        if fitness == len(clauses):
            
            return len(clauses), objective_count, True
        fitnesses.append(fitness)
    
    paired = list(zip(population, fitnesses))
    
    # Sort based on fitness (higher fitness first)
    sorted_population = sorted(paired, key=lambda x: x[1], reverse=True)
    
    # Calculate the number of individuals to select
    num_to_select = int(len(population) * selection_rate)
    # Select the top individuals
    selected = [individual for individual, _ in sorted_population[:num_to_select]]
    
    return selected, objective_count, False

def mutate(individual, mutation_rate):
    """
    Mutates an individual by flipping bits with a given mutation rate.
    """
    return [
        not gene if random.random() < mutation_rate else gene
        for gene in individual
    ]

def apply_mutation(population, mutation_rate):
    """
    Applies mutation to the entire population.
    """
    return [mutate(individual, mutation_rate) for individual in population]

def genetic(population,objective_count,max_evals):
    succes = False
    while objective_count < max_evals:
        if all(x == population[0] for x in population):
            result = evaluate(population[0],clauses)
            return objective_count,result
        selected, objective_count, succes = truncation_selection(population,clauses,selection_rate,objective_count)
        if succes:
                
            return objective_count, selected
        population = one_point_crossover(num_vars,selected)
    fitnesses = []
    
    for individual in population:
            fitness = evaluate(individual,clauses)
            if fitness == len(clauses):
                return objective_count, fitness
            
            fitnesses.append(fitness)
    paired = list(zip(population, fitnesses))
        
        # Sort based on fitness (higher fitness first)
    sorted_population = sorted(paired, key=lambda x: x[1], reverse=True)  
    

    return objective_count, sorted_population[0][1]

population_size = 500
population = []
selection_rate = 0.5
objective_count = 0
# with open("uf20-01.cnf", 'r') as file:
#     hoos = file.read()
# num_vars, num_clauses, clauses = process_cnf(hoos)
# for i in range(population_size):
#     population.append(create_random_solution(num_vars))

# objective_count = 0

# objective_count, result = genetic(population, objective_count,10000)
# print(result)

with open("uf20-01.cnf", 'r') as file:
    uf20 = file.read()
with open("uf100-01.cnf", 'r') as file:
    uf100 = file.read()
with open("uf250-01.cnf", 'r') as file:
    uf250 = file.read()

population = []
all_results = []

for i in range(30):
    num_vars, num_clauses, clauses = process_cnf(uf20)
    objective_count = 0
    for i in range(population_size):
        population.append(create_random_solution(num_vars))
    start = time.time()
    objective_count, eval_result = genetic(population, objective_count,10000000)
    end = time.time()
    runtime = end - start
    all_results.append([eval_result, objective_count, runtime]) 
write_results_to_csv("genetic_search_results_uf20.csv", all_results)  
population = []
all_results = []

for i in range(30):
    num_vars, num_clauses, clauses = process_cnf(uf100)
    objective_count = 0
    for i in range(population_size):
        population.append(create_random_solution(num_vars))
    start = time.time()
    objective_count, eval_result = genetic(population, objective_count,10000000)
    end = time.time()
    runtime = end - start
    all_results.append([eval_result, objective_count, runtime]) 
write_results_to_csv("genetic_search_results_uf100.csv", all_results) 
population = []
all_results = []

for i in range(30):
    objective_count = 0
    num_vars, num_clauses, clauses = process_cnf(uf250)
    for i in range(population_size):
        population.append(create_random_solution(num_vars))
    
    start = time.time()
    objective_count, eval_result = genetic(population, objective_count,10000000)
    end = time.time()
    runtime = end - start
    all_results.append([eval_result, objective_count, runtime]) 
write_results_to_csv("genetic_search_results_uf250.csv", all_results)


# finished = False
# while finished is not True:

#     selected, finished = truncation_selection(population,clauses,selection_rate)
#     population = one_point_crossover(num_vars,selected)
#    # population = apply_mutation(population,0.01)

# finished = False
# objective_count = 0
# for i in range(10):


#     selected, objective_count, finished = truncation_selection(population,clauses,selection_rate,objective_count)
#     if finished:
#         print(selected)
#     population = one_point_crossover(num_vars,selected)
#    # population = apply_mutation(population,0.01)
# fitnesses = []
# for individual in population:
#         fitness = evaluate(individual,clauses)
#         if fitness == len(clauses):
#             print("success!")
             
#         fitnesses.append(fitness)


# paired = list(zip(population, fitnesses))
    
#     # Sort based on fitness (higher fitness first)
# sorted_population = sorted(paired, key=lambda x: x[1], reverse=True)

# print(sorted_population[0])



