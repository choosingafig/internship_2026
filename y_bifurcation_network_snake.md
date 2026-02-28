1. Node Indexing and Graph Topology
The Y-bifurcation is modeled as three distinct branches sharing a single junction node ($n_j$).
    Branch A (Parent): Nodes $A_0, A_1, \dots, A_{n_j}$
    Branch B (Daughter 1): Nodes $B_{n_j}, B_{n_j+1}, \dots, B_m$
    Branch C (Daughter 2): Nodes $C_{n_j}, C_{n_j+1}, \dots, C_k$
    Shared Identity: In the global system, $A_{n_j} \equiv B_{n_j} \equiv C_{n_j} = \mathbf{Q}_{junction}$.

2. Block-Matrix Structure
To solve the entire tree simultaneously, we build a global stiffness matrix $\mathbf{A}_{net}$. Unlike the pentadiagonal matrix for a single branch, the junction rows couple multiple branches.
    Internal Node Rows: Standard 4th-order central difference terms (based on $\alpha$ and $\beta$).
    Junction Node Row: Sums the $\beta$-driven curvature forces from all three connected branches.
    Boundary Conditions: Inlet and outlet nodes are treated as fixed anchors (Dirichlet boundaries) using strict triangulation from landmark points.
    
3. Force Combination Logic
The movement of the network is governed by a balance of three primary forces:
    Internal Forces ($F_{int}$): Smooths each branch and ensures the junction doesn't develop a sharp, non-physical kink.
    External GGVF Forces ($F_{ext}$): Back-projected from both biplane views to pull the 3D graph toward the vessel centers in the 2D angiograms.
    Topology Penalty ($F_{topo}$): A repulsive potential implemented to prevent daughter branches from overlapping if the 2D projections are ambiguous.





FUNCTION reconstruct_Y_tree(image1, image2, P1, P2, S1, S2, landmarks_2d):

    # 1. Triangulate 3D Anchors (Inlet and two Outlets)
    inlet_3d = strict_triangulate(landmarks_2d.inlet1, landmarks_2d.inlet2, P1, P2)
    out1_3d  = strict_triangulate(landmarks_2d.out1_1, landmarks_2d.out1_2, P1, P2)
    out2_3d  = strict_triangulate(landmarks_2d.out2_1, landmarks_2d.out2_2, P1, P2)

    # 2. Initialize Y-Graph
    # Create 3 branches meeting at a central 3D junction point
    G = init_Y_graph(inlet_3d, out1_3d, out2_3d, num_nodes)

    # 3. Precompute GGVF for both images to establish capture range
    F1 = compute_ggvf(edge_map(image1), K, dt, N_iters)
    F2 = compute_ggvf(edge_map(image2), K, dt, N_iters)

    # 4. Build coupling matrix with junction logic
    A_net = build_network_internal_matrix(G, alpha, beta)
    M_net = inverse(A_net + gamma * I)

    # 5. Global Evolution Loop
    WHILE not converged:
        # Project all 3D nodes to 2D, sample GGVF, and re-triangulate
        X_ext = backproject_external_forces_network(G, F1, F2, P1, P2, S1, S2)
        
        # Apply repulsion between daughter branches B and C
        X_ext = apply_topology_penalty(X_ext, G, d_min=1.0)
        
        # Update entire tree position
        X_new = M_net * X_ext

        IF max_distance(X_new, G.nodes) < eps: BREAK
        G.nodes = X_new

    RETURN G