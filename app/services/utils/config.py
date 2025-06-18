"""
공통 설정 및 상수 정의
"""

import matplotlib
matplotlib.use('Agg')  # 웹 환경에서 사용

import matplotlib.pyplot as plt
import numpy as np
from math import pi, e, sqrt, log

# 한글 폰트 설정
plt.rcParams['font.family'] = ['DejaVu Sans', 'Malgun Gothic', 'AppleGothic']
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
