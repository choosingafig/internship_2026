import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json
from bspline_utils import CoronaryCurve

# 1. Load the anatomical data
with open('coronary_template.json', 'r') as f:
    template_data = json.load(f)

lad_data = template_data['vessels']['LAD']
lad_points = np.array(lad_data['control_points'])

# 2. Fit the B-spline
curve = CoronaryCurve(lad_points)

# 3. Generate smooth path for plotting
t_samples = np.linspace(0, 1, 200)
curve_points = curve.spline(t_samples)

# 4. Create the 3D Plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot original control points
ax.scatter(lad_points[:, 0], lad_points[:, 1], lad_points[:, 2], 
           color='red', label='Control Points', s=40)

# Plot the interpolated B-spline path
ax.plot(curve_points[:, 0], curve_points[:, 1], curve_points[:, 2], 
        color='blue', label='LAD Spline Path', linewidth=2.5)

# Plot the D1 Bifurcation point using arc-length mapping
for bif in lad_data.get('bifurcations', []):
    dist = bif['distance_mm']
    point = curve.point_at_arc_length(dist)
    ax.scatter(point[0], point[1], point[2], color='green', marker='X', s=100, 
               label=f'Bifurcation {bif["name"]} (@{dist}mm)')

# Plot Styling
ax.set_title('3D Parametric Reconstruction: LAD Artery', fontsize=15)
ax.set_xlabel('X (mm)')
ax.set_ylabel('Y (mm)')
ax.set_zlabel('Z (mm)')
ax.legend()
ax.view_init(elev=20, azim=45)

plt.tight_layout()
plt.show()