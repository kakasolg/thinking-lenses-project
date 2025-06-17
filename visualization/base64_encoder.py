"""
이미지 base64 인코딩 유틸리티
"""

import base64
from io import BytesIO
import matplotlib.pyplot as plt

# matplotlib 기본 설정 사용 (폰트 문제 방지)
# 한글은 깨질 수 있지만 오류는 발생하지 않음

def save_plot_to_base64(fig):
    """matplotlib 그래프를 base64 문자열로 변환"""
    img = BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight', dpi=100)
    img.seek(0)
    graphic = base64.b64encode(img.getvalue())
    plt.close(fig)  # 메모리 절약
    return graphic.decode('utf-8')

def create_base64_img_tag(base64_str, alt_text="그래프"):
    """base64 문자열을 HTML img 태그로 변환"""
    return f'<img src="data:image/png;base64,{base64_str}" alt="{alt_text}" style="max-width: 100%; height: auto;">'
