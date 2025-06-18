"""
리(☲): 황금비 φ 검증 및 시각화 모듈
"""

import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from ..utils.config import MATH_CONSTANTS, PLOT_CONFIG
from ..visualization.base64_encoder import save_plot_to_base64

class PhiVerification:
    """황금비 φ 검증 클래스"""
    
    def __init__(self):
        self.results = {}
        self.plots = {}
    
    def verify_golden_ratio_with_visualization(self):
        """리(☲): 황금비 φ 검증 및 시각화"""
        print("\\n" + "=" * 50)
        print("🔵 리(☲): 황금비 φ 검증 및 시각화")
        print("=" * 50)
        
        # 1. 피보나치 수열과 황금비
        n_terms = 30
        fib = [1, 1]
        for i in range(n_terms - 2):
            fib.append(fib[-1] + fib[-2])
        
        ratios = [fib[i+1]/fib[i] for i in range(1, len(fib)-1)]
        phi_actual = (1 + sqrt(5)) / 2
        
        # 시각화 1: 피보나치 수열과 비율의 수렴
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # 피보나치 수열
        ax1.plot(range(len(fib)), fib, 'bo-', markersize=6, linewidth=2)
        ax1.set_xlabel('n')
        ax1.set_ylabel('F(n)')
        ax1.set_title('피보나치 수열 F(n)')
        ax1.grid(True, alpha=0.3)
        ax1.set_yscale('log')
        
        # 비율의 수렴
        ax2.plot(range(len(ratios)), ratios, 'ro-', markersize=4, linewidth=2, label='F(n+1)/F(n)')
        ax2.axhline(y=phi_actual, color='g', linestyle='--', linewidth=2, label=f'황금비 φ = {phi_actual:.6f}')
        ax2.set_xlabel('n')
        ax2.set_ylabel('비율')
        ax2.set_title('피보나치 수열 비율의 황금비로의 수렴')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(1.5, 1.7)
        
        plt.tight_layout()
        plot1_base64 = save_plot_to_base64(fig)
        
        # 2. 황금 사각형과 나선
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
        
        # 황금 사각형과 나선
        rectangles = self._draw_golden_rectangles(ax1, 8)
        ax1.set_xlim(-0.5, 3)
        ax1.set_ylim(-0.5, 2)
        ax1.set_aspect('equal')
        ax1.set_title('황금 사각형과 나선')
        ax1.grid(True, alpha=0.3)
        
        # 황금비의 성질: φ² = φ + 1
        x = np.linspace(1, 2.5, 100)
        y1 = x      # y = x
        y2 = x + 1  # y = x + 1 (φ² = φ + 1)
        y3 = x**2   # y = x²
        
        ax2.plot(x, y1, 'b-', linewidth=2, label='y = x')
        ax2.plot(x, y2, 'r-', linewidth=2, label='y = x + 1')
        ax2.plot(x, y3, 'g-', linewidth=2, label='y = x²')
        ax2.axvline(x=phi_actual, color='orange', linestyle='--', linewidth=2, label=f'φ = {phi_actual:.3f}')
        ax2.set_xlabel('x')
        ax2.set_ylabel('y')
        ax2.set_title('황금비의 성질: φ² = φ + 1')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(1, 2.5)
        ax2.set_ylim(1, 4)
        
        plt.tight_layout()
        plot2_base64 = save_plot_to_base64(fig)
        
        print(f"\\n📊 황금비 검증 결과:")
        print(f"실제 황금비: {phi_actual:.6f}")
        print(f"피보나치 비율 (마지막): {ratios[-1]:.6f}")
        print(f"수렴 오차: {abs(ratios[-1] - phi_actual):.6f}")
        
        # 결과 저장
        self.results['golden_ratio'] = {
            'phi_actual': phi_actual,
            'fibonacci_sequence': fib[:15],
            'ratios': ratios[:10],
            'convergence_error': abs(ratios[-1] - phi_actual)
        }
        
        self.plots['golden_ratio'] = {
            'fibonacci_convergence': plot1_base64,
            'golden_rectangles': plot2_base64
        }
        
        return self.results['golden_ratio'], self.plots['golden_ratio']
    
    def _draw_golden_rectangles(self, ax, n_levels):
        """황금 사각형과 나선 그리기"""
        phi = (1 + sqrt(5)) / 2
        
        x, y = 0, 0
        width, height = 1, 1/phi
        
        colors = plt.cm.Set3(np.linspace(0, 1, n_levels))
        spiral_x, spiral_y = [], []
        
        for i in range(n_levels):
            # 사각형 그리기
            rect = plt.Rectangle((x, y), width, height, 
                               facecolor=colors[i], alpha=0.5, 
                               edgecolor='black', linewidth=1)
            ax.add_patch(rect)
            
            # 나선 점 추가
            spiral_x.append(x + width/2)
            spiral_y.append(y + height/2)
            
            # 다음 사각형 계산
            if i % 4 == 0:  # 오른쪽
                x += width
                width, height = height, width - height
            elif i % 4 == 1:  # 아래
                y -= height
                width, height = height, width - height
            elif i % 4 == 2:  # 왼쪽
                x -= width
                width, height = height, width - height
            else:  # 위
                y += height
                width, height = height, width - height
        
        # 나선 그리기
        ax.plot(spiral_x, spiral_y, 'ro-', markersize=4, linewidth=2, alpha=0.7)
        
        return len(colors)
