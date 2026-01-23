import json
import numpy as np
from bspline_utils import CoronaryCurve

class CoronaryTemplate:
  
    def __init__(self, template_file='coronary_template_hk.json'):
        with open(template_file, 'r') as f:
            self.template = json.load(f)
        self.vessels = {}
        self._build_vessels()

    def _build_vessels(self):
        for vessel_name, vessel_data in self.template['vessels'].items():
            points = np.array(vessel_data['control_points'])
            self.vessels[vessel_name] = CoronaryCurve(points)

    def project_template(self, P):

        projections = {}
        for name, curve in self.vessels.items():
            # Sample 100 points for a smooth projection
            points_3d = curve.sample_by_arc_length(100)
            
            # Convert to homogeneous coordinates
            points_homo = np.hstack([points_3d, np.ones((len(points_3d), 1))])
            
            # Project: x = P * X
            projected_homo = (P @ points_homo.T).T
            points_2d = projected_homo[:, :2] / projected_homo[:, 2:3]
            projections[name] = points_2d
            
        return projections

    def get_bifurcations(self):
        return {name: data.get('bifurcations', []) 
                for name, data in self.template['vessels'].items()}

    def validate_finet_law(self, parent_diameter, child1_diameter, child2_diameter):
        coeff = self.template.get('anatomy', {}).get('finet_law_coeff', 0.58)
        expected = coeff * np.sqrt(child1_diameter**2 + child2_diameter**2)
        error = abs(parent_diameter - expected)
        return {
            'measured': parent_diameter,
            'expected': expected,
            'valid': error < 0.3
        }