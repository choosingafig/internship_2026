1. Clinical Motivation: Why 3D Accuracy Matters
Virtual Fractional Flow Reserve (vFFR): 3D models are used to compute blood pressure drops across stenoses without invasive pressure wires. Errors in 3D geometry directly propagate to vFFR, with a typical 95% limit of agreement of $\pm 0.06$.
Stent Sizing & Planning: Accurate 3D length and diameter measurements are critical for selecting the correct stent size, which reduces the risk of restenosis or thrombosis.
Bifurcation Management: 3D representation is essential for understanding complex anatomy at junctions, helping to plan stenting strategies for side branches.

2. Clinically Acceptable Error Tolerances
To be useful in a Cath Lab context, the reconstruction should ideally meet the following accuracy benchmarks:
    Minimum Lumen Diameter (MLD): Errors should be $\le \mathbf{0.05 \pm 0.03 \text{ mm}}$ (often $< 1\%$ deviation compared to physical calipers).
    Spatial Surface Similarity: A global Hausdorff distance of $\approx 0.65 \text{ mm}$ is considered excellent for luminal surface topography.
    Vessel Length: 3D length measurements should maintain a root-mean-square (RMS) error of $< 3.5\%$ (approximately $\le 3.5 \text{ mm}$ for a $100 \text{ mm}$ segment).
    Back-projection Error: The 2D distance between the original angiogram vessel and the projected 3D model should average $1.18 \text{ mm}$ or less.

3. Workflow Constraints
    Runtime: For "online" use during a procedure, reconstruction must be fast, ideally taking between 1 and 3 minutes.
    Input Limitation: Systems must function with only two 2D projections (biplane or non-simultaneous monoplane) to minimize patient radiation exposure.
    Motion Robustness: The model must account for "ghosting" and misalignment caused by cardiac and respiratory motion between views.