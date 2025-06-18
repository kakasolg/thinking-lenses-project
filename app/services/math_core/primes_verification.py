"""
간(☶): 소수 검증 및 시각화 모듈
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
from ..visualization.base64_encoder import save_plot_to_base64

class PrimesVerification:
    """소수 관련 수학적 검증 클래스"""
    
    def sieve_of_eratosthenes(self, limit):
        """에라토스테네스의 체로 소수 찾기"""
        is_prime = [True] * (limit + 1)
        is_prime[0] = is_prime[1] = False
        
        for i in range(2, int(limit**0.5) + 1):
            if is_prime[i]:
                for j in range(i*i, limit + 1, i):
                    is_prime[j] = False
        
        return [i for i in range(2, limit + 1) if is_prime[i]]
    
    def is_prime(self, n):
        """소수 판별 함수"""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    def verify_primes_with_visualization(self):
        """간(☶): 소수 검증 및 시각화"""
        print("\n" + "=" * 50)
        print("🔢 간(☶): 소수 검증 및 시각화")
        print("=" * 50)
        
        # 1. 에라토스테네스의 체 시각화
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # 100까지의 소수 찾기
        limit = 100
        primes = self.sieve_of_eratosthenes(limit)
        
        # 격자로 표시 (10x10)
        grid = np.zeros((10, 10))
        for i in range(1, 101):
            row, col = (i-1) // 10, (i-1) % 10
            if i in primes:
                grid[row, col] = 1
        
        ax1.imshow(grid, cmap='RdYlBu', alpha=0.8)
        
        # 숫자 표시
        for i in range(1, 101):
            row, col = (i-1) // 10, (i-1) % 10
            color = 'red' if i in primes else 'gray'
            weight = 'bold' if i in primes else 'normal'
            ax1.text(col, row, str(i), ha='center', va='center', 
                    fontsize=8, color=color, weight=weight)
        
        ax1.set_title(f'에라토스테네스의 체 (1-100)\n소수: {len(primes)}개')
        ax1.set_xticks([])
        ax1.set_yticks([])
        
        # 2. 소수 분포 (Prime Number Theorem)
        x_range = np.arange(2, 1000, 10)
        actual_count = []
        theoretical_count = []
        
        for x in x_range:
            primes_up_to_x = self.sieve_of_eratosthenes(x)
            actual_count.append(len(primes_up_to_x))
            # 소수 정리: π(x) ~ x/ln(x)
            theoretical_count.append(x / np.log(x))
        
        ax2.plot(x_range, actual_count, 'bo-', label='실제 소수 개수', markersize=3)
        ax2.plot(x_range, theoretical_count, 'r--', label='소수 정리 π(x) ~ x/ln(x)', linewidth=2)
        ax2.set_xlabel('n')
        ax2.set_ylabel('π(n) (n 이하 소수 개수)')
        ax2.set_title('소수 정리 검증')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. 메르센 소수 (2^p - 1 형태의 소수)
        mersenne_primes = []
        mersenne_exponents = [2, 3, 5, 7, 13, 17, 19, 31]  # 알려진 메르센 소수의 지수들
        
        for p in mersenne_exponents:
            if p <= 31:  # 계산 한계
                mersenne_candidate = 2**p - 1
                if self.is_prime(mersenne_candidate):
                    mersenne_primes.append((p, mersenne_candidate))
        
        if mersenne_primes:
            exponents, values = zip(*mersenne_primes)
            ax3.bar(range(len(exponents)), np.log10(values), 
                   color='green', alpha=0.7)
            ax3.set_xlabel('메르센 소수 지수 p')
            ax3.set_ylabel('log₁₀(2ᵖ - 1)')
            ax3.set_title('메르센 소수 (2ᵖ - 1)')
            ax3.set_xticks(range(len(exponents)))
            ax3.set_xticklabels(exponents)
            ax3.grid(True, alpha=0.3)
        
        # 4. 소수 간격 분포
        prime_gaps = []
        for i in range(1, len(primes)):
            gap = primes[i] - primes[i-1]
            prime_gaps.append(gap)
        
        # 간격별 빈도
        gap_counts = {}
        for gap in prime_gaps:
            gap_counts[gap] = gap_counts.get(gap, 0) + 1
        
        gaps = list(gap_counts.keys())
        counts = list(gap_counts.values())
        
        ax4.bar(gaps, counts, color='purple', alpha=0.7)
        ax4.set_xlabel('소수 간격')
        ax4.set_ylabel('빈도')
        ax4.set_title('소수 간격 분포 (100 이하)')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plot1_base64 = save_plot_to_base64(fig)
        
        # 검증 결과 계산
        results = {
            'prime_counts': {
                '100 이하 소수 개수': len(primes),
                '가장 큰 소수 (100 이하)': max(primes),
                '소수 밀도 (100 이하)': len(primes) / 100
            },
            'prime_theorem': {
                '실제 π(100)': len(self.sieve_of_eratosthenes(100)),
                '이론값 100/ln(100)': 100 / np.log(100),
                '오차율': abs(len(self.sieve_of_eratosthenes(100)) - 100/np.log(100)) / (100/np.log(100)) * 100
            },
            'mersenne_primes': {
                '계산된 메르센 소수': len(mersenne_primes),
                '첫 번째 메르센 소수': f"2^{mersenne_primes[0][0]} - 1 = {mersenne_primes[0][1]}" if mersenne_primes else "없음"
            },
            'prime_gaps': {
                '가장 흔한 간격': max(gap_counts, key=gap_counts.get),
                '최대 간격': max(prime_gaps),
                '평균 간격': np.mean(prime_gaps)
            }
        }
        
        plots = {
            'primes_analysis': plot1_base64
        }
        
        print(f"📊 소수 검증 완료:")
        print(f"   100 이하 소수 개수: {results['prime_counts']['100 이하 소수 개수']}")
        print(f"   소수 정리 오차율: {results['prime_theorem']['오차율']:.2f}%")
        print(f"   메르센 소수 개수: {results['mersenne_primes']['계산된 메르센 소수']}")
        
        return results, plots
