"""
감(☵): 확률론 검증 및 시각화 모듈
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
from math import sqrt
from ..utils.config import MATH_CONSTANTS, PLOT_CONFIG
from ..visualization.base64_encoder import save_plot_to_base64

class ProbabilityVerification:
    """확률론 검증 클래스"""
    
    def __init__(self):
        self.results = {}
        self.plots = {}
    
    def verify_probability_with_visualization(self):
        """감(☵): 확률 검증 및 시각화"""
        print("\\n" + "=" * 50)
        print("🎲 감(☵): 확률 검증 및 시각화")
        print("=" * 50)
        
        # 1. 중심극한정리
        sample_sizes = [1, 5, 30, 100]
        n_samples = 1000
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        axes = axes.flatten()
        
        for i, sample_size in enumerate(sample_sizes):
            # 표본평균들 계산
            sample_means = []
            for _ in range(n_samples):
                sample = np.random.uniform(0, 1, sample_size)
                sample_means.append(np.mean(sample))
            
            # 히스토그램
            axes[i].hist(sample_means, bins=50, density=True, alpha=0.7, color='skyblue')
            
            # 이론적 정규분포 오버레이
            mu = 0.5  # 균등분포의 평균
            sigma = 1/sqrt(12*sample_size)  # 표본평균의 표준편차
            x = np.linspace(min(sample_means), max(sample_means), 100)
            y = scipy.stats.norm.pdf(x, mu, sigma)
            axes[i].plot(x, y, 'r-', linewidth=2, label=f'이론적 N({mu}, {sigma:.3f}²)')
            
            axes[i].set_title(f'표본 크기: {sample_size}')
            axes[i].set_xlabel('표본평균')
            axes[i].set_ylabel('밀도')
            axes[i].legend()
            axes[i].grid(True, alpha=0.3)
        
        plt.suptitle('중심극한정리: 표본 크기에 따른 표본평균의 분포', fontsize=14)
        plt.tight_layout()
        plot1_base64 = save_plot_to_base64(fig)
        
        # 2. 베이즈 정리
        prior = 0.01  # 질병 유병률 1%
        sensitivity = 0.99  # 민감도 99%
        specificity = 0.95  # 특이도 95%
        
        # P(양성|질병있음) × P(질병있음) + P(양성|질병없음) × P(질병없음)
        prob_positive = sensitivity * prior + (1 - specificity) * (1 - prior)
        
        # P(질병있음|양성) = P(양성|질병있음) × P(질병있음) / P(양성)
        posterior = (sensitivity * prior) / prob_positive
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 베이즈 정리 시각화
        categories = ['사전확률\\n(Prior)', '우도비\\n(Likelihood)', '사후확률\\n(Posterior)']
        values = [prior, sensitivity/specificity, posterior]
        
        bars = ax1.bar(categories, values, color=['blue', 'green', 'red'], alpha=0.7)
        ax1.set_ylabel('확률')
        ax1.set_title('베이즈 정리: 의료진단 예시')
        ax1.grid(True, alpha=0.3)
        
        # 값 표시
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                    f'{value:.3f}', ha='center', va='bottom')
        
        # 확률 분포 비교
        x = np.linspace(0, 0.1, 1000)
        prior_dist = np.full_like(x, prior)
        posterior_dist = np.full_like(x, posterior)
        
        ax2.axvline(x=prior, color='blue', linestyle='--', linewidth=2, label=f'사전확률 = {prior:.3f}')
        ax2.axvline(x=posterior, color='red', linestyle='-', linewidth=2, label=f'사후확률 = {posterior:.3f}')
        ax2.set_xlabel('확률')
        ax2.set_ylabel('밀도')
        ax2.set_title('검사 후 확률 변화')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(0, 0.5)
        
        plt.tight_layout()
        plot2_base64 = save_plot_to_base64(fig)
        
        print(f"\\n📊 확률 검증 결과:")
        print(f"베이즈 정리 - 사전확률: {prior:.3f}")
        print(f"베이즈 정리 - 사후확률: {posterior:.3f}")
        print(f"민감도: {sensitivity:.3f}, 특이도: {specificity:.3f}")
        
        # 결과 저장
        self.results['probability'] = {
            'prior': prior,
            'posterior': posterior,
            'sensitivity': sensitivity,
            'specificity': specificity,
            'likelihood_ratio': sensitivity / (1 - specificity)
        }
        
        self.plots['probability'] = {
            'central_limit_theorem': plot1_base64,
            'bayes_theorem': plot2_base64
        }
        
        return self.results['probability'], self.plots['probability']
