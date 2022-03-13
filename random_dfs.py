from deterministic_dfs import Variable,get_graph
import random
from collections import defaultdict

# Random algorithm

# 1. Repeat y times
#     1. Pick an arbitrary truth assignment X
#     2. Repeat 2n^2 times
#         1. If X satisfies all clauses, return satisfiable
#         2. Otherwise, pick any clause that is not satisfied and choose one
#            of the variables uniformly at random from this clause and flip the
#            truth table assignment of that variable
# 2. Return unsatisfiable

# def random_dfs(y : int):
#     for _ in range(y):
#         for literal in 


def implication_graph(cnf : str, y : int):
    graph = defaultdict(list)
    for clause in cnf:
        if len(clause) == 2:
            lit_0 = Variable(clause[0])
            lit_1 = Variable(clause[1])
            graph[lit_1.get_negated()].append(lit_0)
            graph[lit_0.get_negated()].append(lit_1)
    return graph

def randomized_dfs(file_path : str ="./largeSat.cnf", y : int = 100):
    graph = get_graph(file_path)
