from collections import defaultdict
import networkx as nx

class variable:
    __cache = {}
    def __init__(self, literal):
        self.lit = literal

    def __new__(cls, x):
        if x in variable.__cache:
            return variable.__cache[x]
        else:
            o = object.__new__(cls)
            o.x = x
            variable.__cache[x] = o
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
            return self.lit[-1]
        return self.lit
    
    def get_negated(self):
        if self.is_negated():
            return variable(self.boolean_var())
        return variable("-"+self.boolean_var())


def implication_graph(cnf):
    graph = defaultdict(list)
    for clause in cnf:
        if len(clause) == 2:
            lit_0 = variable(clause[0])
            lit_1 = variable(clause[1])
            graph[lit_1.get_negated()].append(lit_0)
            graph[lit_0.get_negated()].append(lit_1)
    return graph

def strongly_connected_components(graph):

    index_counter = [0]
    stack = []
    result = []
    lowlinks = {}
    index = {}

    def tarjan(node):

        index[node] = index_counter[0]
        lowlinks[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)

        neighbors = graph.get(node, [])
        for neighbor in neighbors:
            if neighbor not in lowlinks:
                tarjan(neighbor)
                lowlinks[node] = min(lowlinks[node],lowlinks[neighbor])
            elif neighbor in stack:
                lowlinks[node] = min(lowlinks[node],index[neighbor])

        if lowlinks[node] == index[node]:
            connected_component = []
            while True:
                neighbor = stack.pop()
                connected_component.append(neighbor)
                if neighbor == node: 
                    break
            component = tuple(connected_component)
            result.append(component)

    for node in graph:
        if node not in lowlinks:
            tarjan(node)

    return result
    

if __name__ == '__main__':
    cnf = []
    with open("largeSat.cnf") as f:
        for line in f.readlines():
            literals = tuple(line.split(" "))
            if literals[0] == "c" or literals[0] == "p":
                continue
            cnf.append(literals[:-1])
    implication_graph = implication_graph(cnf)
    print(implication_graph)
    sccs = strongly_connected_components(implication_graph)[::-1]
    bool_assn = {}
    breaker = False
    for scc in sccs:
        check_negation = set()
        for node in scc:
            if node.boolean_var() in check_negation:
                print("UNSATISFIABLE")
                breaker == True
                break
            if node.is_negated():
                bool_assn[node.boolean_var()] = False
            else:
                bool_assn[node.boolean_var()] = True
        if breaker:
            break
    if not breaker:
        print("SATISFIABLE")
        res = ""
        for key in sorted(list(bool_assn.keys())):
            print(key)
            res += f"{int(bool_assn[key])}"
        print(res)
    

    