from ortools.linear_solver import pywraplp

def solve_shortest_path(nodes_list, edges_list, start_node, end_node):
    # 1. INITIALIZE SOLVER
    # We use GLOP (Linear Programming) because TUM guarantees integer results.
    solver = pywraplp.Solver.CreateSolver('GLOP')
    
    # 2. DEFINE VARIABLES (x_ij)
    # x is a dictionary mapping (i, j) to a continuous variable between 0 and 1.
    x = {}
    for i, j, cost in edges_list:
        x[i, j] = solver.NumVar(0, 1, f'x_{i}_{j}')

    # 3. DEFINE OBJECTIVE (Min Z)
    # Min Z = Sum of (cost_ij * x_ij)
    objective = solver.Objective()
    for i, j, cost in edges_list:
        objective.SetCoefficient(x[i, j], cost)
    objective.SetMinimization()

    # 4. DEFINE CONSTRAINTS (Flow Conservation)
    # Translates to: Outflow - Inflow = Balance
    for n in nodes_list:
        # Determine the RHS (Right Hand Side) of your equation
        if n == start_node:
            rhs = 1   # Source pushes 1 unit out
        elif n == end_node:
            rhs = -1  # Sink pulls 1 unit in
        else:
            rhs = 0   # Intermediate nodes just pass flow through
            
        # Create the equation: "Sum(Out) - Sum(In) = rhs"
        constraint = solver.Constraint(rhs, rhs)
        for i, j, cost in edges_list:
            if i == n: # Flow LEAVING node n
                constraint.SetCoefficient(x[i, j], 1)
            if j == n: # Flow ENTERING node n
                constraint.SetCoefficient(x[i, j], -1)

    # 5. SOLVE
    status = solver.Solve()

    # 6. EXTRACT RESULT
    if status == pywraplp.Solver.OPTIMAL:
        print(f"Success! Minimum Cost (Z): {solver.Objective().Value()}")
        print("Optimal Path:")
        for (i, j), var in x.items():
            if var.solution_value() > 0.5:
                print(f"  Node {i} -> Node {j}")
    else:
        print("No optimal path found.")

# --- DATA INPUT SECTION ---
# You can change these to any graph you want!
my_nodes = [1, 2, 3, 4, 5]
my_edges = [
    (1, 2, 10), (1, 3, 5),   # Node 1 edges
    (2, 3, 2),  (2, 4, 1),   # Node 2 edges
    (3, 2, 3),  (3, 4, 9), (3, 5, 2), # Node 3 edges
    (4, 5, 4),  (4, 2, 6)    # Node 4 edges
]

# Run the solver from Node 1 to Node 5
solve_shortest_path(my_nodes, my_edges, 1, 5)