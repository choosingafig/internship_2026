1. The Concept of Network Snakes
Traditional snakes are defined by a sequence of nodes where each node has exactly two neighbors (degree 2). Network Snakes extend this to allow nodes to have a degree $D \neq 2$, representing junctions where multiple branches meet.

2. Internal Energy at Junctions
The standard internal energy (controlled by $\alpha$ for tension and $\beta$ for curvature) must be modified at the junction node $n_j$ because the standard finite difference approximations for derivatives assume a linear sequence.
    Tension ($\alpha$): Usually set to zero at the junction node itself to prevent the branches from "pulling" the junction unnaturally toward one specific branch.
    Curvature ($\beta$): Computed independently for each branch reaching the junction using one-sided finite differences.
    
3. Shared Node Constraints
In a network snake, the junction node is a single 3D coordinate shared by all connecting branches. In the global optimization matrix: 
    The rows corresponding to the end of the parent branch and the starts of the daughter branches are coupled.
    This ensures that as the "tree" evolves, the branches never physically detach from one another.

4. Topology-Preserving Energy ($E_{topo}$)
To prevent branches from overlapping or crossing incorrectly in 3D space, a repulsive energy term is added:
$$E_{topo} = \frac{1}{d(C(s))^2}$$
Where $d$ is the distance between non-adjacent segments. 
If two branches get too close, this force pushes them apart to maintain the correct vessel tree structure.

FUNCTION optimize_network_snake(G, GGVF_fields, alpha, beta, gamma):
    # G is a graph structure containing:
    # G.nodes: list of 3D coordinates
    # G.edges: connectivity list (which nodes form which branch)
    # G.junctions: indices of nodes where degree > 2

    # 1. Build the Global Internal Matrix (Block-Stiffness Matrix)
    # This matrix couples all branches sharing junction nodes.
    A_net = build_network_stiffness_matrix(G, alpha, beta)
    M_net = inverse(A_net + gamma * I)

    WHILE not converged:
        # 2. Compute 3D external forces for the entire tree
        # Uses the biplane projection/back-projection for every node in G
        X_ext = compute_tree_external_forces(G, GGVF_fields)

        # 3. Add Topology Penalty (Self-avoidance)
        # Prevents branch B from intersecting branch C
        F_topo = compute_topology_repulsion(G, d_min=1.0)
        X_temp = X_ext + F_topo

        # 4. Simultaneous Update of all nodes
        # The junction nodes move based on the average pull of all connected branches
        X_new = M_net * X_temp

        IF max_distance(X_new, G.nodes) < eps: BREAK
        G.nodes = X_new

    RETURN G