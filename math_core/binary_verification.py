"""
곤(☷): 이진법 검증 및 시각화 모듈
"""

import sys
import os
# 프로젝트 루트 경로를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
from visualization.base64_encoder import save_plot_to_base64

class BinaryVerification:
    """이진법 관련 수학적 검증 클래스"""
    
    def verify_binary_with_visualization(self):
        """곤(☷): 이진법 검증 및 시각화"""
        print("\n" + "=" * 50)
        print("🟤 곤(☷): 이진법 검증 및 시각화")
        print("=" * 50)
        
        # 1. 이진법 공간 시각화 (2^4 = 16가지 조합)
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        
        # 4비트 이진수 시각화
        for i in range(16):
            binary_str = format(i, '04b')
            row, col = i // 4, i % 4
            
            # 이진수를 시각적으로 표현 (0=흰색, 1=검은색)
            binary_array = np.array([int(b) for b in binary_str]).reshape(2, 2)
            ax1.imshow(binary_array, cmap='gray', vmin=0, vmax=1, alpha=0.8)
            
            # 좌표 계산
            x, y = col * 1.2, (3 - row) * 1.2
            ax1.text(x, y, f'{i:2d}\n{binary_str}', ha='center', va='center', 
                    fontsize=8, weight='bold', color='red')
        
        ax1.set_title('4-bit Binary Space (0-15)')
        ax1.set_xlim(-0.5, 4.3)
        ax1.set_ylim(-0.5, 3.8)
        ax1.axis('off')
        
        # 2. 베르누이 시행과 이항분포
        p = 0.6  # 성공 확률
        n_trials = [5, 10, 20, 50]
        
        colors = ['red', 'blue', 'green', 'orange']
        for i, n in enumerate(n_trials):
            x = np.arange(0, n+1)
            pmf = scipy.stats.binom.pmf(x, n, p)
            ax2.plot(x, pmf, 'o-', label=f'n={n}', color=colors[i], 
                    markersize=4, alpha=0.8)
        
        ax2.set_xlabel('Number of Successes (k)')
        ax2.set_ylabel('Probability P(X=k)')
        ax2.set_title(f'Binomial Distribution: B(n, p={p})')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. 논리 게이트 진리표
        gates = {
            'AND': {'inputs': [(0,0), (0,1), (1,0), (1,1)], 
                   'outputs': [0, 0, 0, 1]},
            'OR': {'inputs': [(0,0), (0,1), (1,0), (1,1)], 
                  'outputs': [0, 1, 1, 1]},
            'XOR': {'inputs': [(0,0), (0,1), (1,0), (1,1)], 
                   'outputs': [0, 1, 1, 0]},
            'NAND': {'inputs': [(0,0), (0,1), (1,0), (1,1)], 
                    'outputs': [1, 1, 1, 0]}
        }
        
        gate_names = list(gates.keys())
        colors_gates = ['red', 'blue', 'green', 'orange']
        
        for i, (gate_name, gate_data) in enumerate(gates.items()):
            outputs = gate_data['outputs']
            ax3.bar(np.arange(4) + i*0.15, outputs, alpha=0.7, color=colors_gates[i], 
                   label=gate_name, width=0.15)
        
        ax3.set_xlabel('Input Combinations (00, 01, 10, 11)')
        ax3.set_ylabel('Output')
        ax3.set_title('Logic Gates Truth Table')
        ax3.set_xticks(range(4))
        ax3.set_xticklabels(['00', '01', '10', '11'])
        ax3.legend()
        ax3.set_ylim(0, 1.2)
        
        # 4. 이진 트리 구조 (3레벨)
        # 트리 노드 위치 계산
        tree_positions = {
            1: (0.5, 0.9),    # 루트
            2: (0.25, 0.7), 3: (0.75, 0.7),    # 레벨 1
            4: (0.125, 0.5), 5: (0.375, 0.5), 6: (0.625, 0.5), 7: (0.875, 0.5),  # 레벨 2
        }
        
        # 이진 트리 시각화
        for node, (x, y) in tree_positions.items():
            ax4.scatter(x, y, s=300, c='lightblue', edgecolor='black', linewidth=2)
            ax4.text(x, y, str(node), ha='center', va='center', fontsize=10, weight='bold')
            
            # 연결선 그리기
            if node > 1:
                parent = node // 2
                px, py = tree_positions[parent]
                ax4.plot([px, x], [py, y], 'k-', linewidth=1)
        
        ax4.set_xlim(0, 1)
        ax4.set_ylim(0.4, 1.0)
        ax4.set_title('Binary Tree Structure (3 levels)')
        ax4.axis('off')
        
        plt.tight_layout()
        plot1_base64 = save_plot_to_base64(fig)
        
        # 검증 결과 계산
        results = {
            'binary_representations': {
                '4비트 조합수': 2**4,
                '8비트 조합수': 2**8,
                '32비트 조합수': 2**32
            },
            'binomial_distribution': {
                'n=10, p=0.6의 평균': 10 * 0.6,
                'n=10, p=0.6의 분산': 10 * 0.6 * 0.4,
                '베르누이 시행 성공확률': 0.6
            },
            'logic_gates': {
                'AND(1,1)': 1,
                'OR(0,1)': 1,
                'XOR(1,1)': 0,
                'NAND(1,1)': 0
            }
        }
        
        plots = {
            'binary_space': plot1_base64
        }
        
        print(f"📊 이진법 검증 완료:")
        print(f"   4비트 조합수: {results['binary_representations']['4비트 조합수']}")
        print(f"   논리 게이트 검증: AND(1,1)={results['logic_gates']['AND(1,1)']}")
        print(f"   베르누이 평균: {results['binomial_distribution']['n=10, p=0.6의 평균']}")
        
        return results, plots
