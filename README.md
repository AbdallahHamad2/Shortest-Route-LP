# Shortest-Route Problem: A Linear Programming Approach

This project implements a generalized Linear Programming (LP) model for the shortest-route problem, as formulated in **Taha's Operations Research**. By treating the shortest path as a network flow problem, this model achieves the same results as Floyd's Algorithm but with the added flexibility of mathematical programming side-constraints.

## 1. Mathematical Formulation

We define a network as a set of $n$ nodes. To find the shortest route between a source node $s$ and a destination node $t$, we assume that **one unit of flow** enters the network at node $s$ and leaves at node $t$.

### Decision Variables
Define $x_{ij}$ as the amount of flow in arc $(i, j)$:

$$
x_{ij} = 
\begin{cases} 
1, & \text{if arc } (i, j) \text{ is on the shortest route} \\
0, & \text{otherwise} 
\end{cases}
$$

### Objective Function
Minimize the total distance $z$:
$$\text{Minimize } z = \sum_{\text{all defined arcs } (i, j)} c_{ij}x_{ij}$$
where $c_{ij}$ is the length of arc $(i, j)$.

### Constraints (Conservation of Flow)
For each node $j$ in the network, the total input flow must equal the total output flow. Following Taha's balance equation:

$$\left( \text{External input into node } j \right) + \sum_{i} x_{ij} = \left( \text{External output from node } j \right) + \sum_{k} x_{jk}$$

Specifically:
- **Source node ($s$):** External input = 1, External output = 0.
- **Sink node ($t$):** External input = 0, External output = 1.
- **Intermediate nodes:** External input = 0, External output = 0.

## 2. Implementation Insights

### Total Unimodularity (TUM)
While the variables $x_{ij}$ are logically binary, this project utilizes the **Total Unimodularity** property of the node-arc incidence matrix. This property guarantees that the optimal solution to the LP relaxation ($x_{ij} \in [0, 1]$) will inherently be integer-valued ($0$ or $1$). This allows for the use of high-performance continuous solvers like **GLOP**.

### Generalization
Unlike static implementations, this solver is decoupled from the graph data, allowing users to input any directed weighted graph to determine the optimal path between arbitrary nodes $s$ and $t$.

## 3. Technology Stack
- **Language:** Python 3.x
- **Optimization Engine:** Google OR-Tools (pywraplp)
- **Solver:** GLOP (Google Linear Optimization Package)