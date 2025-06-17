"""
자연상수 e 검증 및 시각화 모듈
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.special
from visualization.base64_encoder import save_plot_to_base64

class EVerification:
    """자연상수 e 관련 수학적 검증 클래스"""
    
    def factorial(self, n):
        """팩토리얼 계산"""
        if n <= 1:
            return 1
        return n * self.factorial(n-1)
    
    def e_series_approximation(self, n_terms):
        """e = Σ(1/n!) 급수 근사"""
        return sum(1/self.factorial(n) for n in range(n_terms))
    
    def e_limit_approximation(self, n):
        """e = lim(n→∞) (1 + 1/n)^n 근사"""
        return (1 + 1/n) ** n
    
    def verify_e_with_visualization(self):
        """자연상수 e 검증 및 시각화"""
        print("\n" + "=" * 50)
        print("📈 자연상수 e 검증 및 시각화")
        print("=" * 50)
        
        # 1. 다양한 방법으로 e 근사
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # 급수 근사: e = Σ(1/n!)
        n_terms = range(1, 21)
        series_values = [self.e_series_approximation(n) for n in n_terms]
        actual_e = np.e
        
        ax1.plot(n_terms, series_values, 'bo-', label='Series Approximation', markersize=4)
        ax1.axhline(y=actual_e, color='red', linestyle='--', linewidth=2, label=f'Actual e = {actual_e:.6f}')
        ax1.set_xlabel('Number of Terms (n)')
        ax1.set_ylabel('e Approximation')
        ax1.set_title('Series Approximation: e = Σ(1/n!)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(2.0, 2.8)
        
        # 극한 근사: e = lim(n→∞) (1 + 1/n)^n
        n_values = np.logspace(1, 6, 100)  # 10^1 to 10^6
        limit_values = [self.e_limit_approximation(n) for n in n_values]
        
        ax2.semilogx(n_values, limit_values, 'g-', linewidth=2, label='Limit Approximation')
        ax2.axhline(y=actual_e, color='red', linestyle='--', linewidth=2, label=f'Actual e = {actual_e:.6f}')
        ax2.set_xlabel('n (log scale)')
        ax2.set_ylabel('e Approximation')
        ax2.set_title('Limit Approximation: e = lim(n→∞) (1 + 1/n)ⁿ')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(2.7, 2.73)
        
        # 2. 지수함수와 자연로그
        x = np.linspace(-2, 3, 1000)
        y_exp = np.exp(x)
        y_ln = np.log(x[x > 0])
        x_ln = x[x > 0]
        
        ax3.plot(x, y_exp, 'b-', linewidth=2, label='y = eˣ')
        ax3.plot(x_ln, y_ln, 'r-', linewidth=2, label='y = ln(x)')
        ax3.plot(x, x, 'k--', alpha=0.5, label='y = x')
        
        # e^1 = e, ln(e) = 1 포인트 표시
        ax3.plot(1, np.e, 'ro', markersize=8, label=f'(1, e) = (1, {np.e:.3f})')
        ax3.plot(np.e, 1, 'bo', markersize=8, label=f'(e, 1) = ({np.e:.3f}, 1)')
        
        ax3.set_xlim(-0.5, 4)
        ax3.set_ylim(-0.5, 4)
        ax3.set_xlabel('x')
        ax3.set_ylabel('y')
        ax3.set_title('Exponential Function and Natural Log Inverse Relationship')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 3. 복리 계산과 연속 복리
        # P(1 + r/n)^(nt) vs Pe^(rt)
        principal = 1000  # 원금
        rate = 0.05  # 연 5% 이자율
        time = 10  # 10년
        
        n_compounds = [1, 2, 4, 12, 52, 365, 8760, np.inf]  # 연, 반기, 분기, 월, 주, 일, 시간, 연속
        compound_names = ['Annual', 'Semi-annual', 'Quarterly', 'Monthly', 'Weekly', 'Daily', 'Hourly', 'Continuous']
        final_amounts = []
        
        for n in n_compounds[:-1]:
            amount = principal * (1 + rate/n) ** (n * time)
            final_amounts.append(amount)
        
        # 연속 복리: Pe^(rt)
        continuous_amount = principal * np.exp(rate * time)
        final_amounts.append(continuous_amount)
        
        colors = plt.cm.viridis(np.linspace(0, 1, len(compound_names)))
        bars = ax4.bar(range(len(compound_names)), final_amounts, color=colors, alpha=0.8)
        
        ax4.set_xlabel('Compounding Period')
        ax4.set_ylabel('Final Amount ($)')
        ax4.set_title(f'Compound Interest Effect (Principal ${principal}, Annual {rate*100}%, {time} years)')
        ax4.set_xticks(range(len(compound_names)))
        ax4.set_xticklabels(compound_names, rotation=45, ha='right')
        ax4.grid(True, alpha=0.3)
        
        # 값 표시
        for i, (bar, amount) in enumerate(zip(bars, final_amounts)):
            ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                    f'${amount:.0f}', ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        plot1_base64 = save_plot_to_base64(fig)
        
        # 검증 결과 계산
        e_approximations = {
            '급수 (20항)': self.e_series_approximation(20),
            '극한 (n=1000000)': self.e_limit_approximation(1000000),
            'NumPy e': np.e,
            '오일러 공식': complex(np.exp(1j * np.pi) + 1).real  # e^(iπ) + 1 = 0
        }
        
        results = {
            'e_approximations': e_approximations,
            'convergence': {
                '급수 수렴속도': '매우 빠름 (factorial!)',
                '극한 수렴속도': '느림 (1/n)',
                '20항 급수 오차': abs(e_approximations['급수 (20항)'] - np.e)
            },
            'applications': {
                '연속복리 최종금액': continuous_amount,
                '일복리 vs 연속복리 차이': continuous_amount - final_amounts[-2],
                'e의 역수 (1/e)': 1/np.e
            },
            'mathematical_properties': {
                'e^1': np.exp(1),
                'ln(e)': np.log(np.e),
                'e^(iπ) + 1': abs(complex(np.exp(1j * np.pi) + 1))  # Should be 0
            }
        }
        
        plots = {
            'e_analysis': plot1_base64
        }
        
        print(f"📊 자연상수 e 검증 완료:")
        print(f"   급수 근사 (20항): {results['e_approximations']['급수 (20항)']:.6f}")
        print(f"   NumPy e: {results['e_approximations']['NumPy e']:.6f}")
        print(f"   수렴 오차: {results['convergence']['20항 급수 오차']:.2e}")
        print(f"   연속복리 효과: ${results['applications']['연속복리 최종금액']:.0f}")
        
        return results, plots
