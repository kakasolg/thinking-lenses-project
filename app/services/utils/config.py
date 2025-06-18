"""
공통 설정 및 상수 정의
"""

import matplotlib
matplotlib.use('Agg')  # 웹 환경에서 사용

import matplotlib.pyplot as plt
import numpy as np
from math import pi, e, sqrt, log

def configure_matplotlib():
    # 기본 폰트를 DejaVu Sans로 설정하여 한글 깨짐 및 폰트 없음 오류 방지
    plt.rcParams['font.family'] = 'DejaVu Sans'
    # 마이너스 부호 깨짐 방지
    plt.rcParams['axes.unicode_minus'] = False

# 수학 상수
MATH_CONSTANTS = {
    'pi': pi,
    'e': e,
    'golden_ratio': (1 + sqrt(5)) / 2,
    'sqrt_2': sqrt(2)
}

# 시각화 설정
PLOT_CONFIG = {
    'figsize': (12, 8),
    'dpi': 100,
    'style': 'seaborn-v0_8-whitegrid'
}
