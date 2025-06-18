"""
태(☱): Symmetry Verification and Visualization Module
"""

import numpy as np
import matplotlib.pyplot as plt
from ...services.utils.config import configure_matplotlib

configure_matplotlib()

from ..visualization.base64_encoder import save_plot_to_base64

class SymmetryVerification:
    """Mathematical verification class for symmetry"""
    
    def create_rotation_matrix(self, angle):
        """Create a rotation transformation matrix"""
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        return np.array([[cos_a, -sin_a], [sin_a, cos_a]])
    
    def create_reflection_matrix(self, axis='x'):
        """Create a reflection transformation matrix"""
        if axis == 'x':
            return np.array([[1, 0], [0, -1]])
        elif axis == 'y':
            return np.array([[-1, 0], [0, 1]])
        elif axis == 'xy':  # y=x axis
            return np.array([[0, 1], [1, 0]])
        else:
            return np.eye(2)
    
    def verify_symmetry_with_visualization(self):
        """Tae (☱): Symmetry verification and visualization"""
        print("\n" + "=" * 50)
        print("⚖️ Tae (☱): Symmetry Verification & Visualization")
        print("=" * 50)
        
        # 1. Geometric Symmetry Transformations
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # Original shape (triangle)
        triangle = np.array([[0, 1, 0.5, 0], [0, 0, 0.8, 0]])
        
        # Rotation transformations
        colors = ['red', 'blue', 'green', 'orange', 'purple']
        angles = [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]
        
        for i, angle in enumerate(angles):
            R = self.create_rotation_matrix(angle)
            rotated = R @ triangle
            ax1.plot(rotated[0], rotated[1], 'o-', color=colors[i], 
                    label=f'{angle*180/np.pi:.0f}°', linewidth=2, markersize=4)
        
        ax1.set_xlim(-1.5, 1.5)
        ax1.set_ylim(-1.5, 1.5)
        ax1.set_aspect('equal')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        ax1.set_title('Rotational Symmetry (Triangle)')
        
        # 2. Reflection Symmetry
        original = np.array([[0, 1, 0.5, 0], [0, 0, 0.8, 0]])
        
        # Reflections across various axes
        reflections = ['x', 'y', 'xy']
        reflection_names = ['x-axis reflection', 'y-axis reflection', 'y=x reflection']
        colors_ref = ['red', 'blue', 'green', 'purple']
        
        ax2.plot(original[0], original[1], 'o-', color='black', 
                linewidth=3, markersize=6, label='Original')
        
        for i, axis in enumerate(reflections):
            R = self.create_reflection_matrix(axis)
            reflected = R @ original
            ax2.plot(reflected[0], reflected[1], 'o--', color=colors_ref[i+1], 
                    linewidth=2, markersize=4, label=reflection_names[i])
        
        ax2.set_xlim(-1.5, 1.5)
        ax2.set_ylim(-1.5, 1.5)
        ax2.set_aspect('equal')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        ax2.set_title('Reflection Symmetry')
        
        # 3. Molecular Symmetry (Point Group)
        # Water molecule (C2v point group) simulation
        # O atom: (0, 0), H atoms: (±0.8, 0.6)
        O_pos = np.array([0, 0])
        H1_pos = np.array([-0.8, 0.6])
        H2_pos = np.array([0.8, 0.6])
        
        # Original molecule
        ax3.scatter(*O_pos, s=200, c='red', label='O', marker='o')
        ax3.scatter(*H1_pos, s=100, c='blue', label='H₁', marker='o')
        ax3.scatter(*H2_pos, s=100, c='blue', label='H₂', marker='o')
        
        # Bonds
        ax3.plot([O_pos[0], H1_pos[0]], [O_pos[1], H1_pos[1]], 'k-', linewidth=2)
        ax3.plot([O_pos[0], H2_pos[0]], [O_pos[1], H2_pos[1]], 'k-', linewidth=2)
        
        # y-axis reflection (σv in C2v symmetry)
        H1_reflected = self.create_reflection_matrix('y') @ H1_pos
        H2_reflected = self.create_reflection_matrix('y') @ H2_pos
        
        ax3.scatter(*H1_reflected, s=100, c='lightblue', marker='s', alpha=0.7)
        ax3.scatter(*H2_reflected, s=100, c='lightblue', marker='s', alpha=0.7)
        ax3.plot([O_pos[0], H1_reflected[0]], [O_pos[1], H1_reflected[1]], 
                'k--', linewidth=1, alpha=0.7)
        ax3.plot([O_pos[0], H2_reflected[0]], [O_pos[1], H2_reflected[1]], 
                'k--', linewidth=1, alpha=0.7)
        
        ax3.set_xlim(-1.5, 1.5)
        ax3.set_ylim(-0.5, 1.2)
        ax3.set_aspect('equal')
        ax3.grid(True, alpha=0.3)
        ax3.legend()
        ax3.set_title('Molecular Symmetry (H₂O, C₂ᵥ Point Group)')
        
        # 4. Group Theory Symmetry (D4 Group)
        # Symmetry operations of a square
        square = np.array([[-1, 1, 1, -1, -1], [-1, -1, 1, 1, -1]])
        
        # 8 elements of D4 group: {e, r, r², r³, s, sr, sr², sr³}
        operations = []
        
        # Rotations (by 90 degrees)
        for i in range(4):
            R = self.create_rotation_matrix(i * np.pi/2)
            operations.append(('rotation', i*90, R @ square))
        
        # Reflection (diagonal)
        diag_reflection = np.array([[0, 1], [1, 0]])
        operations.append(('reflection', 'diagonal', diag_reflection @ square))
        
        # Display results of several symmetry operations
        for i, (op_type, angle, transformed) in enumerate(operations[:5]):
            alpha = 1.0 - i * 0.15
            if op_type == 'rotation':
                ax4.plot(transformed[0], transformed[1], 'o-', 
                        alpha=alpha, linewidth=2, markersize=3,
                        label=f'Rotation {angle}°')
            else:
                ax4.plot(transformed[0], transformed[1], 's--', 
                        alpha=alpha, linewidth=2, markersize=3,
                        label=f'{angle} reflection')
        
        ax4.set_xlim(-1.5, 1.5)
        ax4.set_ylim(-1.5, 1.5)
        ax4.set_aspect('equal')
        ax4.grid(True, alpha=0.3)
        ax4.legend()
        ax4.set_title('D₄ Point Group Symmetry of a Square')
        
        plt.tight_layout()
        plot1_base64 = save_plot_to_base64(fig)
        
        # Calculate verification results
        results = {
            'rotation_symmetry': {
                'Rotational Symmetries of n-gon': 'n',
                'Rotational Symmetries of Circle': 'Infinite',
                'Square Rotation Angles': [0, 90, 180, 270]
            },
            'reflection_symmetry': {
                'Square Reflection Axes': 4,
                'Isosceles Triangle Reflection Axes': 1,
                'Circle Reflection Axes': 'Infinite'
            },
            'point_groups': {
                'H2O Point Group': 'C₂ᵥ',
                'CH4 Point Group': 'Tₐ',
                'Square Point Group': 'D₄'
            },
            'transformation_matrices': {
                'Determinant of 90-deg Rotation Matrix': np.linalg.det(self.create_rotation_matrix(np.pi/2)),
                'Determinant of x-axis Reflection Matrix': np.linalg.det(self.create_reflection_matrix('x')),
                'Transformation Invariance': 'Preserves distance and angles'
            }
        }
        
        plots = {
            'symmetry_analysis': plot1_base64
        }
        
        print(f"📊 Symmetry verification complete:")
        print(f"   Determinant of rotation matrix: {results['transformation_matrices']['Determinant of 90-deg Rotation Matrix']:.0f}")
        print(f"   Determinant of reflection matrix: {results['transformation_matrices']['Determinant of x-axis Reflection Matrix']:.0f}")
        print(f"   H₂O Point Group: {results['point_groups']['H2O Point Group']}")
        
        return results, plots
