# uv 패키지 관리자 사용법

## 프로젝트 개요
- **패키지 관리자**: uv (Python 패키지 관리의 현대적 도구)
- **설정 파일**: pyproject.toml (pip의 requirements.txt 대신)
- **프로젝트명**: pyproj
- **Python 버전**: 3.12+

## 현재 pyproject.toml 의존성

### 웹 프레임워크
- `flask>=3.1.1` - 메인 웹 서버

### 수학 및 과학 계산
- `numpy>=2.3.0` - 수치 계산
- `scipy>=1.15.3` - 과학 계산  
- `sympy>=1.14.0` - 기호 수학
- `pandas>=2.3.0` - 데이터 분석

### 시각화 라이브러리
- `matplotlib>=3.10.3` - 기본 그래프
- `seaborn>=0.13.2` - 통계 시각화
- `plotly>=6.1.2` - 인터랙티브 시각화
- `pillow` - 이미지 처리 (base64 인코딩용)

### 기타 도구
- `streamlit>=1.45.1` - 대체 웹 인터페이스
- `pymongo[srv]>=4.13.1` - MongoDB 연결
- `langchain-core>=0.3.65` - AI/LLM 통합
- `langchain-ollama>=0.3.3` - Ollama 연결
- `networkx>=3.5` - 그래프 이론

## uv 주요 명령어

### 프로젝트 설정
```bash
# 의존성 설치 및 가상환경 생성
uv sync

# 새 패키지 추가
uv add package-name

# 개발 의존성 추가
uv add --dev package-name

# 패키지 제거
uv remove package-name
```

### 실행 및 관리
```bash
# 가상환경에서 명령 실행
uv run python app_bagua.py

# 가상환경 활성화 (Windows)
.venv\Scripts\activate

# 의존성 목록 확인
uv tree

# 버전 업데이트
uv sync --upgrade
```

## 실제 사용 사례

### 웹 서버 실행
```bash
cd D:\dev\html-prj\thinking_lenses\change_view\pyproj
uv sync
uv run python app_bagua.py
```

### 수학 검증 스크립트 실행
```bash
uv run python math_verification_web.py
```

### 새 시각화 라이브러리 추가
```bash
# 예: bokeh 추가
uv add bokeh
```

## uv vs pip 비교

### 장점
- **속도**: pip보다 10-100배 빠름
- **의존성 해결**: 더 정확하고 안정적
- **lock 파일**: uv.lock으로 정확한 재현 가능
- **Python 버전 관리**: 자동 Python 설치 및 관리

### 설정 파일 차이
```toml
# pyproject.toml (uv)
[project]
dependencies = [
    "flask>=3.1.1",
    "numpy>=2.3.0"
]

# requirements.txt (pip)
flask>=3.1.1
numpy>=2.3.0
```

## 문제 해결

### 일반적인 이슈
1. **가상환경 문제**: `uv sync` 재실행
2. **의존성 충돌**: `uv lock --upgrade` 
3. **캐시 문제**: `uv cache clean`

### Windows 특화 이슈
- 경로 구분자: `\` vs `/` 
- 권한 문제: 관리자 권한으로 실행
- 인코딩: UTF-8 설정 확인

## 프로젝트 상태

### ✅ 설치 완료
- 모든 수학/시각화 라이브러리 설치됨
- Flask 웹 서버 구동 가능  
- base64 이미지 인코딩 지원 (pillow)

### 🔄 진행 중
- 나머지 4개 괘 검증 라이브러리 추가 예정
- plotly 대화형 그래프 통합
- 성능 최적화 관련 패키지 검토

### 📋 향후 계획
- AI 분야 확장 시 PyTorch/TensorFlow 추가
- 물리학 분야 확장 시 관련 라이브러리 추가
- 배포용 패키지 설정 추가

## 메모리 뱅크 업데이트 사항

이 파일은 uv 패키지 관리자 사용에 대한 모든 정보를 담고 있으며, 
프로젝트의 의존성 관리와 실행 방법을 명확히 제시합니다.

**마지막 업데이트**: 2025-06-16 (pillow 라이브러리 추가 완료)
