from deterministic_dfs import Variable, extract_cnf
import random
from collections import defaultdict
import time
import logging
import argparse



class RandomizedGraph:
    def __init__(self):
        # self.clauses is meant to be a list of nested tuple ((lit1, assign), (lit2, assign))
        self.clauses = []
        self.literals = {}

    def add_clause(self, lit_0: Variable, lit_1: Variable):
        # Set all literals assignments to None first
        self.literals[lit_0.boolean_var()] = None
        self.literals[lit_1.boolean_var()] = None
        self.clauses.append(((lit_0.boolean_var(), lit_0.is_negated()),
                             (lit_1.boolean_var(), lit_1.is_negated())))


# Random algorithm

# 1. Repeat y times
#     1. Pick an arbitrary truth assignment X
#     2. Repeat 2n^2 times
#         1. If X satisfies all clauses, return satisfiable
#         2. Otherwise, pick any clause that is not satisfied and choose one
#            of the variables uniformly at random from this clause and flip the
#            truth table assignment of that variable
# 2. Return unsatisfiable


def randomized_dfs(file_path : str ="./largeSat.cnf", y : int = 100):
    start_time = time.time()

    graph = get_randomized_graph(file_path)



    for _ in range(y):
        for literal in graph.literals.keys():
            graph.literals[literal] = random.choice([True, False])

        for _ in range(2 * (len(graph.literals) ** 2)):
            satisfiable = True
            value = []
            for clause in graph.clauses:
                if graph.literals[clause[0][0]] != clause[0][1] \
                        and graph.literals[clause[1][0]] != clause[1][1]:
                    satisfiable = False
                    value.append(clause)

            # If the algorithm terminates with a truth assignment, it clearly returns a correct answer
            if satisfiable:
                print("Random DFS found satisfiable assignment")
                logging.info("Random DFS found satisfiable assignment")

                return time.time() - start_time
            else:
                # random_clause here is a nested tuple ((lit1, assign), (lit2, assign))
                # Pick a random clause and flip the assignment of one of the literals
                random_clause = random.choice(value)
                if graph.literals[random_clause[0][0]] != random_clause[0][1] \
                        and graph.literals[random_clause[1][0]] != random_clause[1][1]:
                    random_literal = random.choice(
                        [random_clause[0][0], random_clause[1][0]])
                    assign = graph.literals[random_literal]
                    graph.literals[random_literal] = not assign
                elif graph.literals[random_clause[0][0]] != random_clause[0][1]:
                    graph.literals[random_clause[0]
                                  [0]] = random_clause[0][1]
                elif graph.literals[random_clause[1][0]] != random_clause[1][1]:
                    graph.literals[random_clause[1]
                                  [0]] = random_clause[1][1]

    print("Random DFS found unsatisfiable assignment")
    logging.info("Random DFS found unsatisfiable assignment")
    return time.time() - start_time


def get_randomized_graph(file_path):
    graph = RandomizedGraph()
    clauses = extract_cnf(file_path)

    for clause in clauses:
        if len(clause) == 2:
            lit_0 = Variable(clause[0])
            lit_1 = Variable(clause[1])
            graph.add_clause(lit_0, lit_1)

    return graph
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, help='Path to CNF file', default='largeSat.cnf')
    args = parser.parse_args()

    logging.basicConfig(handlers=[logging.FileHandler(filename="test.log",
                                                      encoding='utf-8', mode='w')],
                        format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                        datefmt="%F %A %T",
                        level=logging.DEBUG)


    randomized_dfs(args.path)

# Time complexity : O(N^2)
