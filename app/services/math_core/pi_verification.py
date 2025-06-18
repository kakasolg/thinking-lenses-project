"""
건(☰): 원주율 π 검증 및 시각화 모듈
"""

import numpy as np
import matplotlib.pyplot as plt
from math import pi, atan
from ..utils.config import MATH_CONSTANTS, PLOT_CONFIG
from ..visualization.base64_encoder import save_plot_to_base64

class PiVerification:
    """원주율 π 검증 클래스"""
    
    def __init__(self):
        self.results = {}
        self.plots = {}
    
    def verify_pi_with_visualization(self, precision=1000):
        """건(☰): 원주율 π 검증 및 시각화"""
        print("=" * 50)
        print("🔵 건(☰): 원주율 π 검증 및 시각화")
        print("=" * 50)
        
        # 1. 몬테카를로 시뮬레이션
        n_points = 50000
        x = np.random.uniform(-1, 1, n_points)
        y = np.random.uniform(-1, 1, n_points)
        distances = np.sqrt(x**2 + y**2)
        inside_circle = distances <= 1
        pi_estimate = 4 * np.sum(inside_circle) / n_points
        
        # 시각화 1: 몬테카를로 시뮬레이션
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 점들 시각화 (샘플만)
        sample_size = 2000
        sample_idx = np.random.choice(n_points, sample_size, replace=False)
        colors = ['red' if inside_circle[i] else 'blue' for i in sample_idx]
        ax1.scatter(x[sample_idx], y[sample_idx], c=colors, alpha=0.6, s=1)
        
        # 단위원 그리기
        theta = np.linspace(0, 2*pi, 100)
        ax1.plot(np.cos(theta), np.sin(theta), 'black', linewidth=2)
        ax1.set_xlim(-1.1, 1.1)
        ax1.set_ylim(-1.1, 1.1)
        ax1.set_aspect('equal')
        ax1.set_title(f'Monte Carlo Simulation\nπ ~ {pi_estimate:.6f}', fontsize=12)
        ax1.grid(True, alpha=0.3)
        
        # 수렴성 시각화
        sample_sizes = np.arange(1000, n_points, 1000)
        pi_estimates = []
        for size in sample_sizes:
            pi_est = 4 * np.sum(inside_circle[:size]) / size
            pi_estimates.append(pi_est)
        
        ax2.plot(sample_sizes, pi_estimates, 'b-', alpha=0.7, label='Monte Carlo Estimate')
        ax2.axhline(y=pi, color='red', linestyle='--', label=f'Actual π = {pi:.6f}')
        ax2.set_xlabel('Sample Size')
        ax2.set_ylabel('π Estimate')
        ax2.set_title('Convergence of π Estimate')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        plt.tight_layout()
        plot1_base64 = save_plot_to_base64(fig)
        
        # 2. 다양한 π 계산 방법들 비교
        methods = {
            'NumPy': np.pi,
            'Leibniz Series': self._calculate_pi_leibniz(10000),
            'Machin-like Formula': self._calculate_pi_machin(100),
            'Monte Carlo': pi_estimate,
            'Wallis Product': self._calculate_pi_wallis(10000)
        }
        
        print("\\n🔢 다양한 π 계산 방법 비교:")
        for method, value in methods.items():
            error = abs(value - pi)
            print(f"{method:12s}: {value:.6f} (오차: {error:.6f})")
        
        # 시각화 2: 방법별 비교
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        method_names = list(methods.keys())
        values = list(methods.values())
        errors = [abs(v - pi) for v in values]
        
        # 막대 그래프
        bars = ax1.bar(method_names, values, alpha=0.7, color=['blue', 'green', 'orange', 'red', 'purple'])
        ax1.axhline(y=pi, color='black', linestyle='--', label=f'Actual π = {pi:.6f}')
        ax1.set_ylabel('π Value')
        ax1.set_title('Results by π Calculation Method')
        ax1.tick_params(axis='x', rotation=45)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 오차 그래프
        ax2.bar(method_names, errors, alpha=0.7, color=['blue', 'green', 'orange', 'red', 'purple'])
        ax2.set_ylabel('Absolute Error')
        ax2.set_title('Error by π Calculation Method')
        ax2.tick_params(axis='x', rotation=45)
        ax2.set_yscale('log')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plot2_base64 = save_plot_to_base64(fig)
        
        # 결과 저장
        self.results['pi'] = {
            'monte_carlo': pi_estimate,
            'leibniz': methods['Leibniz Series'],
            'machin': methods['Machin-like Formula'],
            'wallis': methods['Wallis Product'],
            'numpy': np.pi,
            'actual': pi
        }
        
        self.plots['pi'] = {
            'monte_carlo_simulation': plot1_base64,
            'methods_comparison': plot2_base64
        }
        
        return self.results['pi'], self.plots['pi']
    
    def _calculate_pi_machin(self, n_terms):
        """마친 공식으로 π 계산"""
        def arctan_series(x, n_terms):
            result = 0
            for n in range(n_terms):
                term = (-1)**n * (x**(2*n+1)) / (2*n+1)
                result += term
            return result
        
        pi_estimate = 4 * (4 * arctan_series(1/5, n_terms) - arctan_series(1/239, n_terms))
        return pi_estimate
    
    def _calculate_pi_leibniz(self, n_terms):
        """라이프니츠 급수로 π 계산"""
        pi_estimate = 0
        for i in range(n_terms):
            pi_estimate += (-1)**i / (2*i + 1)
        return 4 * pi_estimate
    
    def _calculate_pi_wallis(self, n_terms):
        """월리스 곱으로 π 계산"""
        product = 1
        for i in range(1, n_terms + 1):
            product *= (4 * i**2) / (4 * i**2 - 1)
        return 2 * product
