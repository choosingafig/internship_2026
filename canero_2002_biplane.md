1. The Biplane Snake Concept
Unlike a 2D snake that lives in the image plane, a biplane snake is a 3D curve $\mathbf{Q}(s) = [x(s), y(s), z(s)]^T$. It is deformed by external forces derived from two different 2D views simultaneously. The goal is to find a 3D shape whose projections $P_1(\mathbf{Q})$ and $P_2(\mathbf{Q})$ align perfectly with the vessel centerlines in both Image 1 and Image 2.

2. 3D Snake Energy Function
The total energy $E$ of the 3D snake is the sum of internal and external energies:
$$E = \int_{0}^{1} (E_{int}(\mathbf{Q}(s)) + E_{ext}(\mathbf{Q}(s))) ds$$
    Internal Energy ($E_{int}$): Controls smoothness (beta) and continuity (alpha) in 3D space.
    External Energy ($E_{ext}$): Defined as the sum of potential fields from both 2D views:
        $$E_{ext}(\mathbf{Q}) = E_{ext,1}(P_1(\mathbf{Q})) + E_{ext,2}(P_2(\mathbf{Q}))$$

3. Update Step Derivation (Discrete Scheme)
To evolve the snake, we use the External Force Projection Iterative Method (EFPIM). Instead of calculating a complex 3D gradient, we project the 3D nodes to 2D, find the 2D displacement from the GGVF field, and back-project those forces into 3D.The matrix update equation is:
$$\mathbf{X}_{new} = (\mathbf{A} + \gamma \mathbf{I})^{-1} (\gamma \mathbf{X}_{old} + \mathbf{F}_{ext, 3D})$$
Where:
    $\mathbf{A}$ is the pentadiagonal stiffness matrix containing $\alpha$ and $\beta$.
    $\gamma$ is the step size (damping factor).
    $\mathbf{F}_{ext, 3D}$ is the tentative 3D position calculated by triangulating the projected points moved by 2D GGVF forces.
    
    
FUNCTION reconstruct_branch_3d(image1, image2, P1, P2, S1, S2,
                               start_2d_1, end_2d_1, start_2d_2, end_2d_2):

    # 1. Triangulate fixed endpoints to lock the branch in 3D space
    start_3d = strict_triangulate(start_2d_1, start_2d_2, P1, P2)
    end_3d   = strict_triangulate(end_2d_1,   end_2d_2,   P1, P2)

    # 2. Initialize 3D snake nodes (X) along a straight line between anchors
    X = generate_straight_3D_line(start_3d, end_3d, m)

    # 3. Precompute 2D GGVF fields for both views
    F1x, F1y = compute_ggvf(edge_map(image1), K, dt, N_ggvf)
    F2x, F2y = compute_ggvf(edge_map(image2), K, dt, N_ggvf)

    # 4. Build internal energy matrix A and precompute inverse for efficiency
    A = build_internal_matrix(m, alpha, beta)
    M = inverse(A + gamma * I)

    # 5. Iterative EFPIM Evolution
    WHILE not converged:
        X_temp = copy(X)

        FOR i = 1 .. m-2:   # Iterate through internal nodes, skipping anchors
            q = X[i]

            # Project 3D node to each 2D view
            (u1, v1) = project(P1, q)
            (u2, v2) = project(P2, q)

            # Sample 2D GGVF forces at those projected coordinates
            f1 = sample(F1x, F1y, u1, v1)
            f2 = sample(F2x, F2y, u2, v2)

            # Move 2D points by the force and form new visual rays
            (u1n, v1n) = (u1 + f1.x, v1 + f1.y)
            (u2n, v2n) = (u2 + f2.x, v2 + f2.y)
            r1 = ray_from_source(S1, P1, u1n, v1n)
            r2 = ray_from_source(S2, P2, u2n, v2n)

            # Re-triangulate to find the "suggested" 3D position
            X_temp[i] = least_squares_intersection(S1, r1, S2, r2)

        # Re-enforce fixed anchors (start/end points)
        X_temp[0] = start_3d
        X_temp[m-1] = end_3d

        # Apply smoothing via the internal energy matrix
        X_new = M * X_temp

        # Convergence check
        if max_distance(X_new, X) < eps: break
        X = X_new

    RETURN X