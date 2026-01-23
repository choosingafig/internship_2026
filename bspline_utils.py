import numpy as np
from scipy.interpolate import make_interp_spline
from scipy.integrate import cumulative_trapezoid

class CoronaryCurve:

    def __init__(self, control_points, k=3):
        self.control_points = np.asarray(control_points)
        num_pts = len(self.control_points)
        self.k = min(k, num_pts - 1)
        
        self.t_indices = np.linspace(0, 1, num_pts)
        self.spline = make_interp_spline(self.t_indices, self.control_points, k=self.k)
        self._compute_arc_length()

    def _compute_arc_length(self, num_samples=1000):
        self.t_samples = np.linspace(0, 1, num_samples)
        X_samples = self.spline(self.t_samples)
        
        dX = np.diff(X_samples, axis=0)
        segment_lengths = np.linalg.norm(dX, axis=1)
        
        self.arc_lengths = cumulative_trapezoid(
            y=segment_lengths, 
            x=self.t_samples[:-1], 
            initial=0
        )
        
        # Ensure parity between t_samples and arc_lengths
        last_seg = np.linalg.norm(X_samples[-1] - X_samples[-2])
        total = self.arc_lengths[-1] + last_seg
        self.arc_lengths = np.append(self.arc_lengths, total)
        self.total_length = self.arc_lengths[-1]

    def evaluate(self, t):
        return self.spline(t)

    def derivative(self, t, order=1):
        return self.spline(t, nu=order)
    def curvature(self, t):
        d1 = self.derivative(t, 1)
        d2 = self.derivative(t, 2)
        cross_product = np.cross(d1, d2)
        return np.linalg.norm(cross_product) / (np.linalg.norm(d1)**3 + 1e-9)

    def point_at_arc_length(self, s):
        s = np.clip(s, 0, self.total_length)
        t_target = np.interp(s, self.arc_lengths, self.t_samples)
        return self.spline(t_target)

    def sample_by_arc_length(self, num_points):
        s_samples = np.linspace(0, self.total_length, num_points)
        return np.array([self.point_at_arc_length(s) for s in s_samples])