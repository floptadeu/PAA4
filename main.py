from queue import PriorityQueue
import random
import time
import matplotlib.pyplot as plt

def generate_test_data(n, max_deadline, max_penalty):
    return [Job(random.randint(1, max_deadline), random.randint(1, max_penalty)) for _ in range(n)]


def measure_execution_time(function, *args):
    start_time = time.time()
    result = function(*args)
    end_time = time.time()
    return end_time - start_time, result

class Job:
    def __init__(self, deadline, profit):
        self.deadline = deadline
        self.profit = profit


def job_sequencing_with_deadlines(jobs):
    # Ordena os trabalhos com base no lucro (profit)
    jobs.sort(key=lambda job: job.profit, reverse=True)

    # Encontra o prazo máximo (deadline) entre todos os trabalhos
    max_deadline = max(job.deadline for job in jobs)

    # Inicializa a programação dos trabalhos com 0 (nenhum trabalho alocado)
    schedule = [0] * max_deadline
    total_profit = 0

    # Atribui os trabalhos à última posição possível antes do prazo
    for job in jobs:
        deadline = job.deadline - 1
        while deadline >= 0:
            if schedule[deadline] == 0:
                schedule[deadline] = 1
                total_profit += job.profit
                break
            deadline -= 1

    return total_profit

class Node:
    def __init__(self, level, penalty, assigned_jobs):
        self.level = level
        self.penalty = penalty
        self.assigned_jobs = assigned_jobs

    def __lt__(self, other):
        return self.penalty < other.penalty
    



def calculateLowerBound(jobs, assigned_jobs, current_penalty, level):
    estimated_penalty = current_penalty
    for i in range(level, len(jobs)):
        if i not in assigned_jobs:
            estimated_penalty += jobs[i].profit  # Accessing the profit attribute
    return estimated_penalty

def jobSequencingBranchAndBound(jobs):
    jobs.sort(reverse=True, key=lambda job: job.profit)  # Sort by penalty, descending
    pq = PriorityQueue()
    pq.put((0, Node(0, 0, set())))  # cost, level, penalty, assigned jobs

    max_deadline = max(jobs, key=lambda job: job.deadline).deadline
    best_penalty = float('inf')
    best_schedule = set()

    while not pq.empty():
        _, node = pq.get()

        if node.level == len(jobs):  # Reached the end
            if node.penalty < best_penalty:
                best_penalty = node.penalty
                best_schedule = node.assigned_jobs
            continue

        for i in range(max_deadline):
            if i not in node.assigned_jobs:  # If time slot is available
                new_assigned_jobs = node.assigned_jobs.copy()
                new_assigned_jobs.add(i)
                new_penalty = node.penalty
                if i >= jobs[node.level].deadline:  # If job is overdue
                    new_penalty += jobs[node.level].profit
                new_node = Node(node.level + 1, new_penalty, new_assigned_jobs)
                lb = calculateLowerBound(jobs, new_assigned_jobs, new_penalty, node.level + 1)
                if lb < best_penalty:
                    pq.put((lb, new_node))

    return best_penalty, best_schedule


# Generate three test datasets
g1 = generate_test_data(1000, 1000, 1000)  # Small dataset
g2 = generate_test_data(5000, 5000, 5000)  # Medium dataset
g3 = generate_test_data(10000, 10000, 10000)  # Large dataset

# Measure execution time for each dataset
tg1, _ = measure_execution_time(job_sequencing_with_deadlines, g1)
tg2, _ = measure_execution_time(job_sequencing_with_deadlines, g2)
tg3, _ = measure_execution_time(job_sequencing_with_deadlines, g3)


# Data for plotting
dataset_sizes = ['1000 jobs', '5000 jobs', '10000 jobs']
execution_times = [tg1, tg2, tg3]

# Plotting
plt.figure(figsize=(10, 6))
plt.bar(dataset_sizes, execution_times, color='blue')
plt.xlabel('Dataset Size')
plt.ylabel('Execution Time')
plt.title('Execution Time of Greedy Job Sequencing With Deadlines for Different Dataset Sizes')
plt.show()



# Generate three test datasets
b1 = generate_test_data(10, 10, 10)  # Small dataset
b2 = generate_test_data(10, 20, 50)  # Medium dataset
b3 = generate_test_data(30, 40, 100)  # Large dataset


# Measure execution time for each dataset
tb1, _ = measure_execution_time(jobSequencingBranchAndBound, b1)
tb2, _ = measure_execution_time(jobSequencingBranchAndBound, b2)
tb3, _ = measure_execution_time(jobSequencingBranchAndBound, b3)


# Data for plotting
bb_sizes = ['10 jobs', '50 jobs', '100 jobs']
bb_times = [tb1, tb2, tb3]

# Plotting
plt.figure(figsize=(10, 6))
plt.bar(bb_sizes, bb_times, color='green')
plt.xlabel('Dataset Size')
plt.ylabel('Execution Time')
plt.title('Execution Time of Brach and Bound Job Sequencing With Deadlines for Different Dataset Sizes')
plt.show()

