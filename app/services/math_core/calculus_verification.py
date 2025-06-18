"""
진(☳)손(☴): 미적분학 검증 및 시각화 모듈
"""

import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from math import pi, e
from ..utils.config import MATH_CONSTANTS, PLOT_CONFIG
from ..visualization.base64_encoder import save_plot_to_base64
from ...services.utils.config import configure_matplotlib

configure_matplotlib()

class CalculusVerification:
    """미적분학 검증 클래스"""
    
    def __init__(self):
        self.results = {}
        self.plots = {}
    
    def verify_calculus_with_visualization(self):
        """진(☳): 미분, 손(☴): 적분 검증 및 시각화"""
        print("\\n" + "=" * 50)
        print("📈 진(☳)손(☴): 미적분학 검증 및 시각화")
        print("=" * 50)
        
        # 1. 미분 검증 - f(x) = x³
        x = sp.Symbol('x')
        f = x**3
        f_prime = sp.diff(f, x)  # 3x²
        
        # 수치적 미분과 해석적 미분 비교
        x_vals = np.linspace(-2, 2, 100)
        h_vals = [0.1, 0.01, 0.001, 0.0001]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 원함수와 도함수
        y_vals = x_vals**3
        y_prime_vals = 3 * x_vals**2
        
        ax1.plot(x_vals, y_vals, 'b-', linewidth=2, label='f(x) = x³')
        ax1.plot(x_vals, y_prime_vals, 'r-', linewidth=2, label="f'(x) = 3x²")
        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
        ax1.set_title('Function and its Derivative')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 수치적 미분 오차 분석
        x_test = 1.0
        analytical_derivative = 3 * x_test**2  # x=1에서 f'(x) = 3
        
        errors = []
        for h in h_vals:
            numerical_derivative = (f.subs(x, x_test + h) - f.subs(x, x_test - h)) / (2 * h)
            error = abs(float(numerical_derivative) - analytical_derivative)
            errors.append(error)
        
        ax2.loglog(h_vals, errors, 'go-', linewidth=2, markersize=8)
        ax2.set_xlabel('h (Interval)')
        ax2.set_ylabel('Absolute Error')
        ax2.set_title('Error of Numerical Differentiation (at x=1)')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plot1_base64 = save_plot_to_base64(fig)
        
        # 2. 적분 검증 - ∫x²dx from 0 to 3
        integrand = x**2
        analytical_integral = sp.integrate(integrand, (x, 0, 3))  # x³/3 = 9
        
        # 리만 합으로 수치적 적분
        a, b = 0, 3
        n_subdivisions = [10, 50, 100, 500]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 리만 합 시각화 (n=20)
        n_demo = 20
        dx = (b - a) / n_demo
        x_riemann = np.linspace(a, b, n_demo + 1)
        y_riemann = x_riemann**2
        
        x_smooth = np.linspace(a, b, 200)
        y_smooth = x_smooth**2
        
        ax1.plot(x_smooth, y_smooth, 'b-', linewidth=2, label='f(x) = x²')
        
        # 리만 사각형 그리기
        for i in range(n_demo):
            x_left = x_riemann[i]
            x_right = x_riemann[i + 1]
            y_height = x_left**2  # 왼쪽 끝점 사용
            
            rect = plt.Rectangle((x_left, 0), dx, y_height, 
                               alpha=0.3, facecolor='red', edgecolor='black')
            ax1.add_patch(rect)
        
        ax1.set_xlabel('x')
        ax1.set_ylabel('f(x)')
        ax1.set_title(f'Riemann Sum (n={n_demo})')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 수렴성 분석
        riemann_sums = []
        for n in n_subdivisions:
            dx = (b - a) / n
            x_points = np.linspace(a, b - dx, n)
            riemann_sum = sum(x_i**2 * dx for x_i in x_points)
            riemann_sums.append(riemann_sum)
        
        ax2.plot(n_subdivisions, riemann_sums, 'ro-', linewidth=2, markersize=8, label='Riemann Sum')
        ax2.axhline(y=float(analytical_integral), color='g', linestyle='--', 
                   linewidth=2, label=f'Analytical Value = {float(analytical_integral):.3f}')
        ax2.set_xlabel('Number of Subdivisions (n)')
        ax2.set_ylabel('Integral Value')
        ax2.set_title('Convergence of Riemann Sum')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plot2_base64 = save_plot_to_base64(fig)
        
        print(f"\\n📊 미적분 검증 결과:")
        print(f"해석적 적분값: {float(analytical_integral):.6f}")
        print(f"리만 합 근사값 (n=500): {riemann_sums[-1]:.6f}")
        print(f"오차: {abs(riemann_sums[-1] - float(analytical_integral)):.6f}")
        
        # 결과 저장
        self.results['calculus'] = {
            'analytical_integral': float(analytical_integral),
            'riemann_approximations': riemann_sums,
            'subdivisions': n_subdivisions,
            'final_error': abs(riemann_sums[-1] - float(analytical_integral))
        }
        
        self.plots['calculus'] = {
            'derivative_analysis': plot1_base64,
            'integration_convergence': plot2_base64
        }
        
        return self.results['calculus'], self.plots['calculus']
