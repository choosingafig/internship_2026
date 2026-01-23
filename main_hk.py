import numpy as np
import matplotlib.pyplot as plt
from coronary_template import CoronaryTemplate

def run_analysis():
    template = CoronaryTemplate('coronary_template_hk.json')
    
    print("Coronary Tree Analysis")
    
    for name, vessel in template.vessels.items():
        # 2. Access vessel properties
        length = vessel.total_length
        print(f"\nVessel: {name}")
        print(f"  Total Arc-Length: {length:.2f} mm")
        
        # 3. Sample points for visualization
        # Getting 3D points at specific arc-length intervals
        sample_points = np.array([vessel.point_at_arc_length(s) 
                                 for s in np.linspace(0, length, 50)])
        
        # 4. Compute Curvature (using the logic for Week 2)
        # We check curvature at the midpoint (t=0.5)
        mid_curvature = vessel.curvature(0.5)
        print(f"  Midpoint Curvature: {mid_curvature:.4f}")

    # 5. Validate Finet's Law
    # Example: Parent diameter 3.5mm, children 2.8mm and 2.5mm
    validation = template.validate_finet_law(3.5, 2.8, 2.5)
    print("\n--- Bifurcation Validation (Finet's Law) ---")
    print(f"  Measured: {validation['measured']}mm")
    print(f"  Expected: {validation['expected']:.2f}mm")
    print(f"  Valid: {'Yes' if validation['valid'] else 'No'} (Tolerance < 0.3mm)")

if __name__ == "__main__":
    run_analysis()