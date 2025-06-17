import streamlit as st
import pandas as pd
from bagua_generator import BaguaSystem, MathModel
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 페이지 설정
st.set_page_config(
    page_title="주역 8괘-64괘 수학적 매핑",
    page_icon="☯️",
    layout="wide"
)

def create_trigram_matrix(trigrams):
    """8괘를 매트릭스 형태로 시각화"""
    names = list(trigrams.keys())
    symbols = [t.symbol for t in trigrams.values()]
    descriptions = [t.description for t in trigrams.values()]
    
    # 2x4 그리드로 배치
    rows = 2
    cols = 4
    
    fig = make_subplots(
        rows=rows, cols=cols,
        subplot_titles=[f"{symbols[i]} {names[i]}" for i in range(8)],
        specs=[[{"type": "xy"} for _ in range(cols)] for _ in range(rows)]
    )
    
    for i, (name, trigram) in enumerate(trigrams.items()):
        row = i // cols + 1
        col = i % cols + 1
        
        # 각 괘를 원으로 표시
        fig.add_trace(
            go.Scatter(
                x=[0], y=[0],
                mode='markers+text',
                marker=dict(size=100, color='lightblue'),
                text=trigram.symbol,
                textfont=dict(size=30),
                name=f"{name}: {trigram.description}",
                showlegend=False
            ),
            row=row, col=col
        )
        
        # 축 숨기기
        fig.update_xaxes(visible=False, row=row, col=col)
        fig.update_yaxes(visible=False, row=row, col=col)
    
    fig.update_layout(
        title="8괘 (팔괘) 개념 구조",
        height=400,
        showlegend=False
    )
    
    return fig

def create_hexagram_matrix(hexagrams):
    """64괘를 8x8 매트릭스로 시각화"""
    # 8x8 매트릭스 생성
    matrix_data = []
    for i, hex in enumerate(hexagrams):
        row = i // 8
        col = i % 8
        matrix_data.append({
            'row': row,
            'col': col,
            'number': hex.number,
            'name': hex.name,
            'meaning': hex.mathematical_meaning,
            'upper': hex.upper.name,
            'lower': hex.lower.name
        })
    
    df = pd.DataFrame(matrix_data)
    
    # 히트맵 생성
    pivot = df.pivot(index='row', columns='col', values='number')
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        text=[[f"{hexagrams[i*8+j].number}<br>{hexagrams[i*8+j].name}" 
               for j in range(8)] for i in range(8)],
        texttemplate="%{text}",
        textfont={"size": 10},
        colorscale='Viridis',
        showscale=False
    ))
    
    fig.update_layout(
        title="64괘 전체 매트릭스 (8×8)",
        xaxis_title="하괘 →",
        yaxis_title="상괘 ↓",
        height=600
    )
    
    return fig

def main():
    st.title("☯️ 주역 8괘-64괘 수학적 매핑 시스템")
    st.markdown("*Charlie Munger의 Mental Models과 수학적 기초 개념을 연결하는 프로젝트*")
    
    # 시스템 초기화
    system = BaguaSystem()
    
    # 사이드바에서 모델 선택
    st.sidebar.header("🎛️ 설정")
    selected_model = st.sidebar.selectbox(
        "수학 모델 선택:",
        options=[MathModel.ABSTRACT, MathModel.CONCRETE],
        format_func=lambda x: {
            MathModel.ABSTRACT: "📚 추상적 모델 (자연수, 집합, 함수...)",
            MathModel.CONCRETE: "🔢 구체적 모델 (π, φ, 미분, 적분...)"
        }[x]
    )
    
    # 모델별 데이터 로드
    trigrams = system.get_trigrams(selected_model)
    hexagrams = system.generate_hexagrams(selected_model)
    analysis = system.analyze_completeness(selected_model)
    
    # 메인 탭 구성
    tab1, tab2, tab3, tab4 = st.tabs(["📊 개요", "🔸 8괘", "🔹 64괘", "📈 분석"])
    
    with tab1:
        st.header("프로젝트 개요")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 목표")
            st.write("""
            - 주역의 8괘-64괘 체계를 현대 수학에 매핑
            - Charlie Munger의 Mental Models 확장
            - 다학제적 패턴 인식 시스템 구축
            """)
            
            st.subheader("🧮 두 가지 수학 모델")
            st.write("""
            **추상적 모델**: 자연수, 집합, 함수, 관계, 측도, 구조, 극한, 연산
            
            **구체적 모델**: π, 이진법, φ, 확률, 미분, 적분, 소수, 대칭성
            """)
        
        with col2:
            st.subheader(f"📋 {selected_model.value.title()} 모델 분석")
            
            # 지표 표시
            col1_metrics, col2_metrics = st.columns(2)
            with col1_metrics:
                st.metric("총 괘 수", f"{analysis['total_hexagrams']}개")
                st.metric("대대 관계", f"{len(analysis['duality_pairs'])}쌍")
            
            with col2_metrics:
                st.metric("8괘 수", f"{analysis['total_trigrams']}개")
                st.metric("커버리지", f"{analysis['mathematical_coverage']:.1f}%")
    
    with tab2:
        st.header("🔸 8괘 (팔괘) - 기초 개념")
        
        # 8괘 시각화
        fig_trigrams = create_trigram_matrix(trigrams)
        st.plotly_chart(fig_trigrams, use_container_width=True)
        
        # 8괘 상세 정보
        st.subheader("8괘 상세 설명")
        trigram_df = pd.DataFrame([
            {
                "괘": f"{t.symbol} {name}",
                "개념": t.description,
                "설명": t.concept
            }
            for name, t in trigrams.items()
        ])
        st.dataframe(trigram_df, use_container_width=True)
        
        # 대대 관계
        st.subheader("🔄 대대(對待) 관계")
        pairs = system.get_duality_pairs(selected_model)
        for pair in pairs:
            t1, t2 = trigrams[pair[0]], trigrams[pair[1]]
            st.write(f"**{t1.symbol} {pair[0]} ↔ {t2.symbol} {pair[1]}**: {t1.description} ↔ {t2.description}")
    
    with tab3:
        st.header("🔹 64괘 - 수학적 조합")
        
        # 64괘 매트릭스 시각화
        fig_hexagrams = create_hexagram_matrix(hexagrams)
        st.plotly_chart(fig_hexagrams, use_container_width=True)
        
        # 64괘 검색 및 필터
        st.subheader("🔍 64괘 탐색")
        
        col1, col2 = st.columns(2)
        with col1:
            search_term = st.text_input("수학적 의미 검색:", placeholder="예: 미분, 적분, 확률...")
        
        with col2:
            show_count = st.slider("표시할 괘 수:", 1, 64, 10)
        
        # 필터링된 64괘 표시
        filtered_hexagrams = hexagrams
        if search_term:
            filtered_hexagrams = [
                h for h in hexagrams 
                if search_term.lower() in h.mathematical_meaning.lower()
            ]
        
        # 64괘 테이블
        hexagram_data = []
        for i, hex in enumerate(filtered_hexagrams[:show_count]):
            hexagram_data.append({
                "번호": hex.number,
                "괘명": hex.name,
                "상괘": f"{hex.upper.symbol} {hex.upper.name}",
                "하괘": f"{hex.lower.symbol} {hex.lower.name}",
                "수학적 의미": hex.mathematical_meaning
            })
        
        df_hexagrams = pd.DataFrame(hexagram_data)
        st.dataframe(df_hexagrams, use_container_width=True)
        
        if search_term and not filtered_hexagrams:
            st.warning(f"'{search_term}'와 관련된 괘를 찾을 수 없습니다.")
    
    with tab4:
        st.header("📈 모델 분석 및 비교")
        
        # 두 모델 비교
        st.subheader("🔍 모델 비교 분석")
        
        comparison_data = []
        for model in [MathModel.ABSTRACT, MathModel.CONCRETE]:
            analysis_temp = system.analyze_completeness(model)
            comparison_data.append({
                "모델": model.value.title(),
                "총 괘 수": analysis_temp['total_hexagrams'],
                "8괘 수": analysis_temp['total_trigrams'],
                "커버리지": f"{analysis_temp['mathematical_coverage']:.1f}%",
                "대대 관계": len(analysis_temp['duality_pairs'])
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True)
        
        # 흥미로운 조합 예시
        st.subheader("🌟 흥미로운 수학적 조합 예시")
        
        interesting_examples = [
            ("미분", "적분", "미적분학의 기본정리"),
            ("π", "이진법", "디지털 신호처리의 FFT"),
            ("소수", "확률", "소수 정리의 확률적 해석"),
            ("황금비", "대칭성", "정다면체와 자연의 비례")
        ]
        
        for ex in interesting_examples:
            if selected_model == MathModel.CONCRETE:
                st.write(f"**{ex[0]} + {ex[1]}** → {ex[2]}")
        
        # 향후 연구 방향
        st.subheader("🔮 향후 연구 방향")
        st.write("""
        1. **AI 분야 역분해**: Transformer, Attention 메커니즘을 8괘로 분해
        2. **물리학 확장**: 양자역학, 카오스 이론의 기본 요소 추출
        3. **교차 검증**: 다른 분야의 8괘와 비교하여 공통 패턴 발견
        4. **새로운 발견**: 빈 조합에서 미지의 수학 이론 예측
        """)

if __name__ == "__main__":
    main()
