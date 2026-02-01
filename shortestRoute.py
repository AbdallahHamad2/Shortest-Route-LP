from ortools.linear_solver import pywraplp
import time

def solve_shortest_path(nodes_list, edges_list, start_node, end_node):
    """
    Solves the shortest path problem using Linear Programming.
    Optimized for large-scale graphs using adjacency mapping.
    """
    # 0. PRE-PROCESS EDGES
    # This reduces complexity from O(N*E) to O(E)
    out_edges = {n: [] for n in nodes_list}
    in_edges = {n: [] for n in nodes_list}
    for i, j, cost in edges_list:
        out_edges[i].append((i, j))
        in_edges[j].append((i, j))

    # 1. INITIALIZE SOLVER
    # GLOP is used because the Node-Arc Incidence Matrix is Totally Unimodular (TUM)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return

    # 2. DEFINE VARIABLES (x_ij)
    x = {}
    for i, j, cost in edges_list:
        x[i, j] = solver.NumVar(0, 1, f'x_{i}_{j}')

    # 3. DEFINE OBJECTIVE (Minimize Z)
    objective = solver.Objective()
    for i, j, cost in edges_list:
        objective.SetCoefficient(x[i, j], cost)
    objective.SetMinimization()

    # 4. DEFINE CONSTRAINTS (Flow Conservation)
    for n in nodes_list:
        if n == start_node:
            rhs = 1   # Source
        elif n == end_node:
            rhs = -1  # Sink
        else:
            rhs = 0   # Intermediate
            
        constraint = solver.Constraint(rhs, rhs)
        # Efficiently pull only relevant edges for this node
        for i, j in out_edges[n]:
            constraint.SetCoefficient(x[i, j], 1)
        for i, j in in_edges[n]:
            constraint.SetCoefficient(x[i, j], -1)

    # 5. SOLVE
    status = solver.Solve()

    # 6. EXTRACT RESULT
    if status == pywraplp.Solver.OPTIMAL:
        print(f"Success! Minimum Cost (Z): {solver.Objective().Value()}")
        # For large graphs, you might want to comment out the path printing 
        # and only print the first/last few edges.
        # for (i, j), var in x.items():
        #     if var.solution_value() > 0.5:
        #         print(f"  Node {i} -> Node {j}")
    else:
        print("No optimal path found.")

# --- HOW TO RUN THE 10,000 NODE TEST ---
import random

def run_large_test():
    N = 10000
    nodes = list(range(N))
    edges = []
    
    # Create a chain + random shortcuts
    for i in range(N):
        if i < N - 1:
            edges.append((i, i+1, random.randint(1, 5)))
        for _ in range(2): # 2 extra shortcuts per node
            target = random.randint(0, N-1)
            edges.append((i, target, random.randint(5, 50)))

    print(f"Testing with {N} nodes and {len(edges)} edges...")
    start = time.time()
    solve_shortest_path(nodes, edges, 0, N-1)
    print(f"Solve Time: {time.time() - start:.4f} seconds")

if __name__ == "__main__":
    run_large_test()