"""
태(☱): 대칭성 검증 및 시각화 모듈
"""

import numpy as np
import matplotlib.pyplot as plt
from ..visualization.base64_encoder import save_plot_to_base64

class SymmetryVerification:
    """대칭성 관련 수학적 검증 클래스"""
    
    def create_rotation_matrix(self, angle):
        """회전 변환 행렬 생성"""
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        return np.array([[cos_a, -sin_a], [sin_a, cos_a]])
    
    def create_reflection_matrix(self, axis='x'):
        """반사 변환 행렬 생성"""
        if axis == 'x':
            return np.array([[1, 0], [0, -1]])
        elif axis == 'y':
            return np.array([[-1, 0], [0, 1]])
        elif axis == 'xy':  # y=x 축
            return np.array([[0, 1], [1, 0]])
        else:
            return np.eye(2)
    
    def verify_symmetry_with_visualization(self):
        """태(☱): 대칭성 검증 및 시각화"""
        print("\n" + "=" * 50)
        print("⚖️ 태(☱): 대칭성 검증 및 시각화")
        print("=" * 50)
        
        # 1. 기하학적 대칭 변환
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # 원본 도형 (삼각형)
        triangle = np.array([[0, 1, 0.5, 0], [0, 0, 0.8, 0]])
        
        # 회전 변환들
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
        ax1.set_title('회전 대칭 (삼각형)')
        
        # 2. 반사 대칭
        original = np.array([[0, 1, 0.5, 0], [0, 0, 0.8, 0]])
        
        # 다양한 축에 대한 반사
        reflections = ['x', 'y', 'xy']
        reflection_names = ['x축 반사', 'y축 반사', 'y=x 반사']
        colors_ref = ['red', 'blue', 'green', 'purple']
        
        ax2.plot(original[0], original[1], 'o-', color='black', 
                linewidth=3, markersize=6, label='원본')
        
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
        ax2.set_title('반사 대칭')
        
        # 3. 분자 대칭 (점군)
        # 물 분자 (C2v 점군) 시뮬레이션
        # O원자: (0, 0), H원자들: (±0.8, 0.6)
        O_pos = np.array([0, 0])
        H1_pos = np.array([-0.8, 0.6])
        H2_pos = np.array([0.8, 0.6])
        
        # 원본 분자
        ax3.scatter(*O_pos, s=200, c='red', label='O', marker='o')
        ax3.scatter(*H1_pos, s=100, c='blue', label='H₁', marker='o')
        ax3.scatter(*H2_pos, s=100, c='blue', label='H₂', marker='o')
        
        # 결합선
        ax3.plot([O_pos[0], H1_pos[0]], [O_pos[1], H1_pos[1]], 'k-', linewidth=2)
        ax3.plot([O_pos[0], H2_pos[0]], [O_pos[1], H2_pos[1]], 'k-', linewidth=2)
        
        # y축 반사 (C2v 대칭의 σv)
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
        ax3.set_title('분자 대칭 (H₂O, C₂ᵥ 점군)')
        
        # 4. 군론적 대칭성 (D4 군)
        # 정사각형의 대칭 연산들
        square = np.array([[-1, 1, 1, -1, -1], [-1, -1, 1, 1, -1]])
        
        # D4 군의 8개 원소: {e, r, r², r³, s, sr, sr², sr³}
        operations = []
        
        # 회전 (90도씩)
        for i in range(4):
            R = self.create_rotation_matrix(i * np.pi/2)
            operations.append(('rotation', i*90, R @ square))
        
        # 반사 (대각선)
        diag_reflection = np.array([[0, 1], [1, 0]])
        operations.append(('reflection', 'diagonal', diag_reflection @ square))
        
        # 여러 대칭 연산 결과 표시
        for i, (op_type, angle, transformed) in enumerate(operations[:5]):
            alpha = 1.0 - i * 0.15
            if op_type == 'rotation':
                ax4.plot(transformed[0], transformed[1], 'o-', 
                        alpha=alpha, linewidth=2, markersize=3,
                        label=f'회전 {angle}°')
            else:
                ax4.plot(transformed[0], transformed[1], 's--', 
                        alpha=alpha, linewidth=2, markersize=3,
                        label=f'{angle} 반사')
        
        ax4.set_xlim(-1.5, 1.5)
        ax4.set_ylim(-1.5, 1.5)
        ax4.set_aspect('equal')
        ax4.grid(True, alpha=0.3)
        ax4.legend()
        ax4.set_title('정사각형의 D₄ 점군 대칭')
        
        plt.tight_layout()
        plot1_base64 = save_plot_to_base64(fig)
        
        # 검증 결과 계산
        results = {
            'rotation_symmetry': {
                '정n각형의 회전 대칭': 'n개',
                '원의 회전 대칭': '무한개',
                '정사각형 회전각': [0, 90, 180, 270]
            },
            'reflection_symmetry': {
                '정사각형 반사축': 4,
                '이등변삼각형 반사축': 1,
                '원의 반사축': '무한개'
            },
            'point_groups': {
                'H2O 점군': 'C₂ᵥ',
                'CH4 점군': 'Tₐ',
                '정사각형 점군': 'D₄'
            },
            'transformation_matrices': {
                '90도 회전 행렬 det': np.linalg.det(self.create_rotation_matrix(np.pi/2)),
                'x축 반사 행렬 det': np.linalg.det(self.create_reflection_matrix('x')),
                '변환 보존성': '거리와 각도 보존'
            }
        }
        
        plots = {
            'symmetry_analysis': plot1_base64
        }
        
        print(f"📊 대칭성 검증 완료:")
        print(f"   회전 변환 행렬식: {results['transformation_matrices']['90도 회전 행렬 det']:.0f}")
        print(f"   반사 변환 행렬식: {results['transformation_matrices']['x축 반사 행렬 det']:.0f}")
        print(f"   H₂O 점군: {results['point_groups']['H2O 점군']}")
        
        return results, plots
