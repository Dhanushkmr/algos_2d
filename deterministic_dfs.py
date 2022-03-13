from collections import defaultdict
import logging
import argparse
import time

class Variable:
    __cache = {}

    def __init__(self, literal):
        self.lit = literal
        self.index = None
        self.lowlink = None

    def __new__(cls, x):
        if x in Variable.__cache:
            return Variable.__cache[x]
        else:
            o = object.__new__(cls)
            o.x = x
            Variable.__cache[x] = o
            return o

    def __str__(self):
        return self.lit

    def __repr__(self):
        return self.lit

    def __hash__(self):
        return hash(self.lit)
    
    def is_negated(self):
        if self.lit[0] == "-":
            return True
        return False

    def boolean_var(self):
        if self.is_negated():
            return self.lit[1:]
        return self.lit
    
    def get_negated(self):
        if self.is_negated():
            return Variable(self.boolean_var())
        return Variable("-"+self.boolean_var())


def deterministic_dfs(file_path):
    start_time = time.time()

    graph = get_graph(file_path)
    logging.debug(graph)
    sccs = strongly_connected_components(graph)

    bool_assn = {}
    for scc in sccs:
        check_negation = set([i.lit for i in scc])
        for node in scc:
            # Fails if there exists positive and negative literal in the within the same strongly connected component
            if node.get_negated().lit in check_negation:
                print("UNSATISFIABLE", check_negation)
                logging.info("UNSATISFIABLE")
                return time.time() - start_time
            if node.is_negated():
                bool_assn[node.boolean_var()] = False
            else:
                bool_assn[node.boolean_var()] = True

    print("SATISFIABLE")
    logging.info("SATISFIABLE")
    res = ""
    for key in sorted(list(bool_assn.keys())):
        res += f"{int(bool_assn[key])}"
    logging.debug(res)

    return time.time() - start_time


def strongly_connected_components(graph):
    
    index_counter = 0
    stack = []
    result = []

    def tarjan(node):
        nonlocal index_counter, result
        node.index = index_counter
        node.lowlink = index_counter
        index_counter += 1
        stack.append(node)

        neighbors = graph.get(node, [])
        for neighbor in neighbors:
            if neighbor.lowlink == None:
                tarjan(neighbor)
                node.lowlink = min(node.lowlink, neighbor.lowlink)
            elif neighbor in stack:
                node.lowlink = min(node.lowlink, neighbor.index)

        if node.lowlink == node.index:
            connected_component = []
            while True:
                neighbor = stack.pop()
                connected_component.append(neighbor)
                if neighbor == node: 
                    break
            component = tuple(connected_component)
            result = [component] + result

    for node in graph:
        if node.lowlink == None:
            tarjan(node)
    return result


def implication_graph(cnf):
    graph = defaultdict(list)
    for clause in cnf:
        if len(clause) == 2:
            lit_0 = Variable(clause[0])
            lit_1 = Variable(clause[1])
            graph[lit_1.get_negated()].append(lit_0)
            graph[lit_0.get_negated()].append(lit_1)
    return graph

def get_graph(file_path):
    cnf = []
    with open(file_path) as f:
        for line in f.readlines():
            literals = tuple(line.split(" "))
            if literals[0] == "c" or literals[0] == "p":
                continue
            cnf.append(literals[:-1])
    graph = implication_graph(cnf)
    return graph

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, help='Path to CNF file', default='largeSat.cnf')
    args = parser.parse_args()

    logging.basicConfig(handlers=[logging.FileHandler(filename="test.log",
                                                    encoding='utf-8', mode='w')],
                        format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                        datefmt="%F %A %T",
                        level=logging.DEBUG)
    
    deterministic_dfs(args.path)

# Linear Time complexity


# why wouldnt our solution work for 3 sat
# O(2N) where N is the number of Variables
# V = 2N where N is the nubmer of Variables
# E = 2C where C is the Number of clauses

    
