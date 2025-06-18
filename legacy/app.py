import streamlit as st
import random
import logging # 로깅 추가
from mongodb import ask_hexagram # mongodb.py에서 ask_hexagram 함수 임포트


# 🎯 64괘 괘상(卦象) 데이터 정의
# 각 괘는 6개 효로 구성: [6효, 5효, 4효, 3효, 2효, 1효] (위에서 아래로)
# 1 = 양효(陽爻), 0 = 음효(陰爻)
HEXAGRAM_LINES = {
    # 1-8괘 (상괘: 건☰)
    1:  [1, 1, 1, 1, 1, 1],  # 건(乾) ☰☰
    2:  [0, 0, 0, 0, 0, 0],  # 곤(坤) ☷☷
    3:  [1, 0, 0, 0, 0, 1],  # 둔(屯) ☳☵
    4:  [0, 0, 1, 1, 0, 0],  # 몽(蒙) ☶☵
    5:  [1, 1, 1, 0, 1, 0],  # 수(需) ☵☰
    6:  [0, 1, 0, 1, 1, 1],  # 송(訟) ☰☵
    7:  [0, 1, 0, 0, 0, 0],  # 사(師) ☷☵
    8:  [0, 0, 0, 0, 1, 0],  # 비(比) ☵☷
    
    # 9-16괘 (상괘: 손☴)
    9:  [1, 1, 0, 1, 1, 1],  # 소축(小畜) ☰☴
    10: [1, 1, 0, 0, 1, 1],  # 리(履) ☱☰
    11: [1, 1, 1, 0, 0, 0],  # 태(泰) ☷☰
    12: [0, 0, 0, 1, 1, 1],  # 비(否) ☰☷
    13: [1, 0, 1, 1, 1, 1],  # 동인(同人) ☰☲
    14: [1, 1, 1, 1, 0, 1],  # 대유(大有) ☲☰
    15: [0, 0, 1, 0, 0, 0],  # 겸(謙) ☷☶
    16: [0, 0, 0, 1, 0, 0],  # 예(豫) ☳☷
    
    # 17-24괘 (상괘: 리☲)
    17: [1, 0, 0, 1, 1, 0],  # 수(隨) ☱☳
    18: [0, 1, 1, 1, 1, 0],  # 고(蠱) ☴☶
    19: [1, 1, 0, 0, 0, 0],  # 림(臨) ☷☱
    20: [0, 0, 0, 0, 1, 1],  # 관(觀) ☴☷
    21: [1, 0, 0, 1, 0, 1],  # 서합(噬嗑) ☲☳
    22: [1, 0, 1, 0, 0, 1],  # 비(賁) ☶☲
    23: [0, 0, 0, 0, 0, 1],  # 박(剝) ☶☷
    24: [1, 0, 0, 0, 0, 0],  # 복(復) ☷☳
    
    # 25-32괘 (상괘: 진☳)
    25: [1, 0, 0, 1, 1, 1],  # 무망(無妄) ☰☳
    26: [1, 1, 1, 0, 0, 1],  # 대축(大畜) ☳☰
    27: [1, 0, 0, 0, 0, 1],  # 이(頤) ☶☳
    28: [0, 1, 1, 1, 1, 0],  # 대과(大過) ☱☴
    29: [0, 1, 0, 0, 1, 0],  # 감(坎) ☵☵
    30: [1, 0, 1, 1, 0, 1],  # 리(離) ☲☲
    
    # 31-40괘 (상괘: 감☵)
    31: [0, 0, 1, 1, 1, 0],  # 감(咸) ☱☶
    32: [0, 1, 1, 1, 0, 0],  # 항(恆) ☳☴
    33: [0, 0, 1, 1, 1, 1],  # 둔(遁) ☰☶
    34: [1, 1, 1, 1, 0, 0],  # 대장(大壯) ☳☰
    35: [0, 0, 0, 1, 0, 1],  # 진(晋) ☲☷
    36: [1, 0, 1, 0, 0, 0],  # 명이(明夷) ☷☲
    37: [1, 0, 1, 0, 1, 1],  # 가인(家人) ☴☲
    38: [1, 1, 0, 1, 0, 1],  # 규(睽) ☲☱
    39: [0, 0, 1, 0, 1, 0],  # 건(蹇) ☵☶
    40: [0, 1, 0, 1, 0, 0],  # 해(解) ☳☵
    
    # 41-48괘 (상괘: 로☱)
    41: [1, 1, 0, 0, 0, 1],  # 손(損) ☶☱
    42: [1, 0, 0, 0, 1, 1],  # 익(益) ☴☳
    43: [1, 1, 1, 1, 1, 0],  # 결(夬) ☱☰
    44: [0, 1, 1, 1, 1, 1],  # 구(姤) ☰☴
    45: [0, 0, 0, 1, 1, 0],  # 취(萃) ☱☷
    46: [0, 1, 1, 0, 0, 0],  # 상(升) ☷☴
    47: [0, 1, 0, 1, 1, 0],  # 곤(困) ☱☵
    48: [0, 1, 1, 0, 1, 0],  # 정(井) ☵☴
    
    # 49-56괘 (상괘: 태☱)
    49: [1, 0, 1, 1, 1, 0],  # 혁(革) ☱☲
    50: [0, 1, 1, 1, 0, 1],  # 정(鼎) ☲☴
    51: [1, 0, 0, 1, 0, 0],  # 진(震) ☳☳
    52: [0, 0, 1, 0, 0, 1],  # 간(艰) ☶☶
    53: [0, 0, 1, 0, 1, 1],  # 점(漸) ☴☶
    54: [1, 1, 0, 1, 0, 0],  # 귀메(歸妹) ☳☱
    55: [1, 0, 1, 1, 0, 0],  # 풍(豐) ☳☲
    56: [0, 0, 1, 1, 0, 1],  # 로(旅) ☲☶
    
    # 57-64괘 (상괘: 손☴, 태☱)
    57: [0, 1, 1, 0, 1, 1],  # 손(巽) ☴☴
    58: [1, 1, 0, 1, 1, 0],  # 태(兑) ☱☱
    59: [0, 1, 0, 0, 1, 1],  # 환(渙) ☴☵
    60: [1, 1, 0, 0, 1, 0],  # 절(節) ☵☱
    61: [1, 1, 0, 0, 1, 1],  # 중부(中孚) ☴☱
    62: [0, 0, 1, 1, 0, 0],  # 소과(小過) ☶☳
    63: [1, 0, 1, 0, 1, 0],  # 기제(既濟) ☵☲
    64: [0, 1, 0, 1, 0, 1],  # 미제(未濟) ☲☵
    }

# 🔄 효변 계산 함수들
def flip_line(line_value):
    """한 효를 뒤집기: 양효(1) ↔ 음효(0)"""
    return 1 - line_value

def calculate_target_hexagram(original_hex_num, changing_line_pos):
    """
    효변을 통한 지괘(之卦) 계산
    
    Args:
        original_hex_num (int): 원괘 번호 (1-64)
        changing_line_pos (int): 변하는 효 위치 (1-6)
    
    Returns:
        int: 지괘(之卦) 번호 (1-64)
    """
    if original_hex_num not in HEXAGRAM_LINES:
        return None
        
    # 원괘 바이너리 복사
    original_lines = HEXAGRAM_LINES[original_hex_num][:]
    
    # 효 번호를 인덱스로 변환 (1효=인덱스 5, 6효=인덱스 0)
    line_index = 6 - changing_line_pos
    
    # 해당 효 뒤집기
    original_lines[line_index] = flip_line(original_lines[line_index])
    
    # 새로운 괘 번호 찾기
    for hex_num, lines in HEXAGRAM_LINES.items():
        if lines == original_lines:
            return hex_num
    
    return None  # 에러 케이스

def generate_full_eff_change_map():
    """
    전체 384가지 효변 시나리오 (64괘 × 6효) 자동 생성
    
    Returns:
        dict: eff_change_map 구조
        {
            괘번호: {
                효번호: 지괘번호
            }
        }
    """
    eff_change_map = {}
    
    for hex_num in range(1, 65):  # 1-64괘
        eff_change_map[hex_num] = {}
        
        for line_pos in range(1, 7):  # 1-6효
            target_hex = calculate_target_hexagram(hex_num, line_pos)
            if target_hex:
                eff_change_map[hex_num][line_pos] = target_hex
    
    return eff_change_map

# 🎯 전체 효변 맵 생성 (전역 변수)
eff_change_map = generate_full_eff_change_map()

# 🎉 384가지 효변 시나리오 완성!
print(f"🎆 효변 맵 생성 완료: {len(eff_change_map)}괘 × 6효 = {sum(len(v) for v in eff_change_map.values())}가지 시나리오")

st.set_page_config(page_title="주역 점괘 추천 시스템", layout="wide")
st.title("🔮 주역 점괘 추천 시스템 (테스트 중)")

# 🎲 1. 주사위 결과 입력
st.subheader("🎲 주사위 결과 입력")

# 세션 상태 초기화
if 'high_trigram' not in st.session_state:
    st.session_state.high_trigram = 1
if 'low_trigram' not in st.session_state:
    st.session_state.low_trigram = 1
if 'changing_lines' not in st.session_state:
    st.session_state.changing_lines = []

def generate_random_gua():
    st.session_state.high_trigram = random.randint(1, 8)
    st.session_state.low_trigram = random.randint(1, 8)

def generate_random_changing_lines():
    # 0개, 1개, 2개, 3개, 4개, 5개, 6개 효변 중 랜덤 선택
    num_changes = random.randint(0, 6)
    if num_changes == 0:
        st.session_state.changing_lines = []
    else:
        st.session_state.changing_lines = sorted(random.sample(range(1, 7), num_changes))

col_gua_input, col_gua_button = st.columns([2, 1])
with col_gua_input:
    st.write(f"현재 상괘: **{st.session_state.high_trigram}**")
    st.write(f"현재 하괘: **{st.session_state.low_trigram}**")
with col_gua_button:
    st.button("🎲 랜덤 괘 뽑기", on_click=generate_random_gua)

# 🎰 2. 괘 번호 계산
gua_number = (st.session_state.high_trigram - 1) * 8 + st.session_state.low_trigram
st.write(f"👉 선택된 괘 번호는: **{gua_number}번**")

# 🔄 3. 효변(爻變) 선택
st.subheader("🔄 효변 선택")
st.markdown("""
**효변이란?** 주역에서 변하는 효(爻)를 의미합니다. 각 괘는 6개의 효로 구성되어 있으며,  
효가 변하면 다른 괘로 변화합니다. 변하는 효가 없으면 현재 괘의 의미만 해석합니다.
""")

col_line_input, col_line_button = st.columns([2, 1])
with col_line_input:
    if st.session_state.changing_lines:
        st.write(f"🔄 변하는 효: **{', '.join(map(str, st.session_state.changing_lines))}효**")
        st.write(f"📊 변효 개수: **{len(st.session_state.changing_lines)}개**")
    else:
        st.write("📍 변효 없음: 본괘 중심 해석")
with col_line_button:
    st.button("✨ 랜덤 효변 선택", on_click=generate_random_changing_lines)

# 🎨 4. 괘상 시각화
st.subheader("🎨 괘상 시각화")
# 8괘 기본 상징 매핑
trigram_symbols = {
    1: ("☰", "건(乾)", "하늘"),
    2: ("☱", "태(兌)", "연못"),
    3: ("☲", "이(離)", "불"),
    4: ("☳", "진(震)", "천둥"),
    5: ("☴", "손(巽)", "바람"),
    6: ("☵", "감(坎)", "물"),
    7: ("☶", "간(艮)", "산"),
    8: ("☷", "곤(坤)", "땅")
}

# 상괘와 하괘 정보 가져오기
high_symbol, high_name, high_meaning = trigram_symbols[st.session_state.high_trigram]
low_symbol, low_name, low_meaning = trigram_symbols[st.session_state.low_trigram]

# 3열 레이아웃으로 괘상 표시
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown(f"""
    <div style="text-align: center; font-size: 24px; line-height: 1.5;">
        <div style="font-size: 48px; margin-bottom: 10px;">{high_symbol}</div>
        <div style="font-size: 24px; color: #666;"><strong>상괘</strong>: {high_name} ({high_meaning})</div>
        <div style="margin: 20px 0; font-size: 20px;">+</div>
        <div style="font-size: 48px; margin-bottom: 10px;">{low_symbol}</div>
        <div style="font-size: 24px; color: #666;"><strong>하괘</strong>: {low_name} ({low_meaning})</div>
        <div style="margin: 20px 0; font-size: 20px;">↓</div>
        <div style="font-size: 36px; margin-bottom: 10px;">{high_symbol}{low_symbol}</div>
        <div style="font-size: 20px; color: #333; font-weight: bold;">{gua_number}번 괘</div>
    </div>
    """, unsafe_allow_html=True)

# 효변 시각화 (선택된 경우)
if st.session_state.changing_lines:
    st.markdown("🔄 **변하는 효 위치:**")
    # 6효를 위에서부터 아래로 표시 (6, 5, 4, 3, 2, 1)
    for line_num in [6, 5, 4, 3, 2, 1]:
        if line_num in st.session_state.changing_lines:
            st.markdown(f"**{line_num}효**: → 🔄 **변화** ←")
        else:
            st.markdown(f"{line_num}효: ─── 고정")



# 🧠 3. LLM에 전달할 질문 생성
# mongodb.py의 parse_hexagram_query가 이해할 수 있는 형태로 질문을 구성합니다.
question_to_llm = f"{gua_number}번괘에 대해 설명해주세요."

# 🧾 5. 결과 요청
if st.button("🧭 괘 해석 및 다음 괘 추천받기"):
    st.markdown("---")
    st.subheader("💬 AI 응답:")
    st.info("AI가 현재 괘에 대한 심층적인 해석을 제공합니다. 이 해석은 당신의 질문에 대한 통찰을 제공할 것입니다.")
    with st.spinner("AI가 응답을 생성 중입니다... 잠시만 기다려주세요."):
        try:
            # ask_hexagram은 응답 조각(chunk)들을 yield하는 제너레이터입니다.
            # st.write_stream을 사용하여 스트리밍 응답을 표시합니다.
            response_stream = ask_hexagram(question_to_llm)
            st.write_stream(response_stream)
            
            # 🔮 6. 다음 괘 추천
            st.markdown("---")
            st.subheader("🔮 다음 괘 추천")
            st.info("AI가 현재 괘와 연결될 수 있는 다음 괘들을 추천합니다. 이 괘들은 현재 상황의 발전 방향이나 숨겨진 의미를 탐색하는 데 도움이 될 수 있습니다.")
            
            # 64괘 주제적 연결성 매핑 (완전판)
            gua_links = {
                # 상경 (1~30): 천지 원리와 기본 법칙
                1: [2, 44],      # 건(원력) → 곤(수용), 구(만남)
                2: [1, 23],      # 곤(수용) → 건(원력), 박(붕괴)
                3: [4, 20],      # 둥(어려움) → 몽(계몽), 관(관찰)
                4: [3, 22],      # 몽(계몽) → 둥(어려움), 비(꾸미)
                5: [6, 48],      # 수(기다림) → 송(다툼), 정(우물)
                6: [5, 9, 23],   # 솨(다툼) → 수(기다림), 소축(축적), 박(붕괴)
                7: [8, 13],      # 사(군대) → 비(친화), 동인(동지)
                8: [7, 14],      # 비(친화) → 사(군대), 대유(풍요)
                9: [10, 26],     # 소축(준비) → 리(실행), 대축(큰 저축)
                10: [9, 58],     # 리(예의) → 소축(준비), 태(즈거움)
                
                # 대립과 조화의 순환
                11: [12, 19],    # 태(평안) ↔ 비(막힘), 임(다가감)
                12: [11, 20],    # 비(막힘) ↔ 태(평안), 관(관찰)
                13: [14, 49],    # 동인(동지) → 대유(풍요), 혁(변혁)
                14: [13, 43],    # 대유(풍요) → 동인(동지), 결(결단)
                15: [16, 62],    # 겸(겸손) → 예(기쁨), 소과(소과)
                16: [15, 51],    # 예(기쁨) → 겸(겸손), 진(충격)
                17: [18, 45],    # 수(따름) → 고(바로잡기), 취(모이기)
                18: [17, 46],    # 고(바로잡기) → 수(따름), 승(오르기)
                19: [20, 41],    # 임(다가감) → 관(관찰), 손(덜어냄)
                20: [19, 42],    # 관(관찰) → 임(다가감), 익(더함)
                
                # 결단과 아름다움
                21: [22, 27],    # 서합(결단) → 비(장식), 이(기름)
                22: [21, 36],    # 비(장식) → 서합(결단), 명이(어둘)
                23: [24, 2],     # 박(붕괴) → 복(회복), 곤(수용)
                24: [25, 51],    # 복(회복) → 무망(진실), 진(충격)
                25: [26, 17],    # 무망(진실) → 대축(큰 저축), 수(따름)
                26: [9, 18],     # 대축(큰 저축) → 소축(준비), 고(바로잡기)
                27: [28, 50],    # 이(기름) → 대과(과대), 정(우리)
                28: [27, 62],    # 대과(과대) → 이(기름), 소과(소과)
                29: [30, 60],    # 감(험난) → 리(밝음), 절(절도)
                30: [29, 56],    # 리(밝음) → 감(험난), 로(나그네)
                
                # 하경 (31~64): 인간관계와 사회적 상황
                31: [32, 39],    # 함(감응) → 항(지속), 건(어려움)
                32: [31, 34],    # 항(지속) → 함(감응), 대장(큰 장)
                33: [34, 44],    # 둔(물러남) → 대장(큰 장), 구(만남)
                34: [33, 55],    # 대장(큰 장) → 둔(물러남), 풍(풍성)
                35: [36, 64],    # 진(전진) → 명이(어둘), 미제(미완)
                36: [35, 22],    # 명이(어둘) → 진(전진), 비(장식)
                37: [38, 40],    # 가인(가족) → 규(따로) 도운, 해(해결)
                38: [37, 54],    # 규(따로) → 가인(가족), 귀메(시집가기)
                39: [40, 31],    # 건(어려움) → 해(해결), 함(감응)
                40: [39, 16],    # 해(해결) → 건(어려움), 예(기쁨)
                
                # 손익과 변화
                41: [42, 19],    # 손(덜어냄) → 익(더함), 임(다가감)
                42: [41, 20],    # 익(더함) → 손(덜어냄), 관(찰)
                43: [44, 14],    # 결(결단) → 구(만남), 대유(풍요)
                44: [43, 1],     # 구(만남) → 결(결단), 건(원력)
                45: [46, 17],    # 취(모이기) → 승(오르기), 수(따름)
                46: [45, 18],    # 승(오르기) → 취(모이기), 고(바로잡기)
                47: [48, 37],    # 곤(곤란) → 정(우물), 가인(가족)
                48: [47, 5],     # 정(우물) → 곤(곤란), 수(기다림)
                49: [50, 13],    # 혁(변혁) → 정(우리), 동인(동지)
                50: [49, 27],    # 정(우리) → 혁(변혁), 이(기름)
                
                # 충격과 안정
                51: [52, 24],    # 진(충격) → 간(정지), 복(회복)
                52: [51, 15],    # 간(정지) → 진(충격), 겸(겸손)
                53: [54, 39],    # 점(점진) → 귀메(시집가기), 건(어려움)
                54: [53, 38],    # 귀메(시집가기) → 점(점진), 규(따로)
                55: [56, 34],    # 풍(풍성) → 로(나그네), 대장(큰 장)
                56: [55, 30],    # 로(나그네) → 풍(풍성), 리(밝음)
                57: [58, 9],     # 손(바람) → 태(즈거움), 소축(준비)
                58: [57, 10],    # 태(즈거움) → 손(바람), 리(예의)
                59: [60, 6],     # 환(흙어짐) → 절(절도), 송(다툼)
                60: [59, 29],    # 절(절도) → 환(흙어짐), 감(험난)
                
                # 진리와 예의
                61: [62, 33],    # 중부(진리) → 소과(소과), 둔(물러남)
                62: [61, 15],    # 소과(소과) → 중부(진리), 겸(겸손)
                
                # 완성과 미완성의 순환
                63: [64, 1],     # 기제(완성) → 미제(미완), 건(새 시작)
                64: [63, 35, 1], # 미제(미완) → 기제(완성), 진(전진), 건(새 시작)
            }
            
            # 🎉 384가지 효변 시나리오 완성! 
            # 전체 eff_change_map은 상단에서 자동 생성되었습니다.
            
            # 다음 괘 추천 로직
            if st.session_state.changing_lines:
                st.markdown("🔄 **효변 기반 추천:**")
                
                if len(st.session_state.changing_lines) == 1:
                    # 1개 효 변화 시 지괘 계산
                    changing_line = st.session_state.changing_lines[0]
                    if gua_number in eff_change_map and changing_line in eff_change_map[gua_number]:
                        target_gua = eff_change_map[gua_number][changing_line]
                        st.success(f"🎯 **지괘(之卦)**: {target_gua}번 괘")
                        st.write(f"📊 **해석 원칙**: {changing_line}효 변화에 따른 효사(爻辭) 중심 해석")
                    else:
                        st.info("해당 괘의 효변 데이터가 아직 구축되지 않았습니다.")
                        
                elif len(st.session_state.changing_lines) == 2:
                    st.info("📊 **해석 원칙**: 2개 효 변화 시 위쪽 효사 중심 해석")
                    upper_line = max(st.session_state.changing_lines)
                    st.write(f"🔼 **주요 효**: {upper_line}효")
                    
                elif len(st.session_state.changing_lines) == 3:
                    st.info("📊 **해석 원칙**: 3개 효 변화 시 본괘+지괘 종합 해석")
                    
                else:
                    st.info(f"📊 **해석 원칙**: {len(st.session_state.changing_lines)}개 효 변화 시 지괘 중심 해석")
                    
            else:
                st.markdown("🔗 **주제적 연결 추천:**")
                if gua_number in gua_links:
                    linked_guas = gua_links[gua_number]
                    
                    # 유사성 있는 3가지 선택지 제공
                    num_options = min(3, len(linked_guas))
                    if num_options > 0:
                        selected_options = random.sample(linked_guas, num_options)
                        
                        st.write("다음 괘 중 하나를 선택하여 더 깊이 탐구해보세요:")
                        selected_next_gua = st.selectbox(
                            "선택지",
                            options=selected_options,
                            format_func=lambda x: f"{x}번 괘"
                        )
                        st.success(f"🎯 **선택된 다음 괘**: {selected_next_gua}번 괘")
                        st.write(f"• {selected_next_gua}번 괘: 철학적 연결성에 따른 자연스러운 흐름")
                    else:
                        st.info("해당 괘의 주제적 연결 데이터가 아직 구축되지 않았습니다.")
                else:
                    st.info("해당 괘의 주제적 연결 데이터가 아직 구축되지 않았습니다.")
                    
            # 방법론 설명
            with st.expander("📚 주역 점사법 원칙 보기"):
                st.markdown("""
                **변효 수별 해석 원칙:**
                - **0개**: 본괘 괘사(卦辭)로 해석
                - **1개**: 해당 효사(爻辭)로 해석
                - **2개**: 위쪽 효사로 해석
                - **3개**: 본괘와 지괘 종합 해석
                - **4~6개**: 지괘 중심 해석
                
                **괘쌍 관계:**
                주역의 64괘는 서로 철학적으로 연결되어 있으며,  
                현재 상황에서 자연스럽게 전개될 수 있는 다음 단계를 안내합니다.
                """)
            
        except Exception as e:
            logging.error(f"ask_hexagram 호출 중 오류 발생: {e}")
            st.error(f"오류가 발생했습니다: {e}")
            st.info("Ollama 서버가 실행 중이고, mongodb.py에 설정된 모델('exaone3.5:7.8b')이 Ollama에 설치되어 있는지 확인해주세요.")
    
    st.markdown("---")
    st.subheader("✨ 다음 단계:")
    st.markdown("""
    - **새로운 괘 뽑기**: 상단의 '랜덤 괘 뽑기' 또는 '랜덤 효변 선택' 버튼을 눌러 새로운 점괘를 뽑아보세요.
    - **심층 탐구**: 추천된 다음 괘 번호를 사용하여 해당 괘에 대해 더 깊이 탐구할 수 있습니다.
    - **피드백 제공**: 시스템 개선을 위한 의견이 있다면 언제든지 알려주세요!
    """)

