import streamlit as st
import random
import logging
from mongodb import ask_hexagram, hexagram_db

# 로깅 설정
logging.basicConfig(level=logging.INFO)

# --- 데이터 정의 섹션 ---

# 🎯 64괘 이름 및 괘상 데이터
HEXAGRAM_DATA = {
    1: {"name": "중천건(重天乾)", "lines": [1, 1, 1, 1, 1, 1], "image": "☰☰"},
    2: {"name": "중지곤(重地坤)", "lines": [0, 0, 0, 0, 0, 0], "image": "☷☷"},
    3: {"name": "수뢰둔(水雷屯)", "lines": [0, 1, 0, 1, 0, 0], "image": "☵☳"},
    4: {"name": "산수몽(山水蒙)", "lines": [1, 0, 0, 0, 1, 0], "image": "☶☵"},
    5: {"name": "수천수(水天需)", "lines": [1, 1, 1, 0, 1, 0], "image": "☵☰"},
    6: {"name": "천수송(天水訟)", "lines": [0, 1, 0, 1, 1, 1], "image": "☰☵"},
    7: {"name": "지수사(地水師)", "lines": [0, 1, 0, 0, 0, 0], "image": "☷☵"},
    8: {"name": "수지비(Water Earth Fellowship)", "lines": [0, 0, 0, 0, 1, 0], "image": "☵☷"},
    9: {"name": "풍천소축(Wind Heaven Small Accumulation)", "lines": [1, 1, 1, 0, 1, 1], "image": "☴☰"},
    10: {"name": "천택리(Heaven Lake Treading)", "lines": [1, 1, 0, 1, 1, 1], "image": "☰☱"},
    11: {"name": "지천태(Earth Heaven Peace)", "lines": [1, 1, 1, 0, 0, 0], "image": "☷☰"},
    12: {"name": "천지비(Heaven Earth Obstruction)", "lines": [0, 0, 0, 1, 1, 1], "image": "☰☷"},
    13: {"name": "천화동인(Heaven Fire Fellowship)", "lines": [1, 0, 1, 1, 1, 1], "image": "☰☲"},
    14: {"name": "화천대유(Fire Heaven Great Possession)", "lines": [1, 1, 1, 1, 0, 1], "image": "☲☰"},
    15: {"name": "지산겸(Earth Mountain Modesty)", "lines": [1, 0, 0, 0, 0, 0], "image": "☷☶"},
    16: {"name": "뇌지예(Thunder Earth Enthusiasm)", "lines": [0, 0, 0, 1, 0, 0], "image": "☳☷"},
    17: {"name": "택뢰수(Lake Thunder Following)", "lines": [0, 1, 1, 1, 0, 0], "image": "☱☳"},
    18: {"name": "산풍고(Mountain Wind Decay)", "lines": [0, 1, 1, 0, 0, 1], "image": "☶☴"},
    19: {"name": "지택림(Earth Lake Approach)", "lines": [1, 1, 0, 0, 0, 0], "image": "☷☱"},
    20: {"name": "풍지관(Wind Earth Viewing)", "lines": [0, 0, 0, 0, 1, 1], "image": "☴☷"},
    21: {"name": "화뢰서합(Fire Thunder Biting Through)", "lines": [1, 0, 0, 1, 0, 1], "image": "☲☳"},
    22: {"name": "산화비(Mountain Fire Grace)", "lines": [1, 0, 1, 0, 0, 1], "image": "☶☲"},
    23: {"name": "산지박(Mountain Earth Splitting Apart)", "lines": [0, 0, 0, 0, 0, 1], "image": "☶☷"},
    24: {"name": "지뢰복(Earth Thunder Return)", "lines": [1, 0, 0, 0, 0, 0], "image": "☷☳"},
    25: {"name": "천뢰무망(Heaven Thunder Innocence)", "lines": [1, 1, 1, 1, 0, 0], "image": "☰☳"},
    26: {"name": "산천대축(Mountain Heaven Great Accumulation)", "lines": [1, 1, 1, 0, 0, 1], "image": "☶☰"},
    27: {"name": "산뢰이(Mountain Thunder Nourishment)", "lines": [1, 0, 0, 0, 0, 1], "image": "☶☳"},
    28: {"name": "택풍대과(Lake Wind Great Exceeding)", "lines": [0, 1, 1, 1, 1, 0], "image": "☱☴"},
    29: {"name": "중수감(Double Water Abyss)", "lines": [0, 1, 0, 0, 1, 0], "image": "☵☵"},
    30: {"name": "중화리(Double Fire Clinging)", "lines": [1, 0, 1, 1, 0, 1], "image": "☲☲"},
    31: {"name": "택산함(Lake Mountain Attraction)", "lines": [1, 0, 0, 1, 1, 0], "image": "☱☶"},
    32: {"name": "뇌풍항(Thunder Wind Perseverance)", "lines": [0, 1, 1, 1, 0, 0], "image": "☳☴"},
    33: {"name": "천산둔(Heaven Mountain Retreat)", "lines": [1, 1, 1, 0, 0, 1], "image": "☰☶"},
    34: {"name": "뇌천대장(Thunder Heaven Great Power)", "lines": [1, 1, 1, 1, 0, 0], "image": "☳☰"},
    35: {"name": "화지진(Fire Earth Progress)", "lines": [0, 0, 0, 1, 0, 1], "image": "☲☷"},
    36: {"name": "지화명이(Earth Fire Darkening of Light)", "lines": [1, 0, 1, 0, 0, 0], "image": "☷☲"},
    37: {"name": "풍화가인(Wind Fire Family)", "lines": [1, 0, 1, 0, 1, 1], "image": "☴☲"},
    38: {"name": "화택규(Fire Lake Opposition)", "lines": [1, 1, 0, 1, 0, 1], "image": "☲☱"},
    39: {"name": "수산건(Water Mountain Obstruction)", "lines": [1, 0, 0, 0, 1, 0], "image": "☵☶"},
    40: {"name": "뇌수해(Thunder Water Deliverance)", "lines": [0, 1, 0, 1, 0, 0], "image": "☳☵"},
    41: {"name": "산택손(Mountain Lake Decrease)", "lines": [1, 1, 0, 0, 0, 1], "image": "☶☱"},
    42: {"name": "풍뢰익(Wind Thunder Increase)", "lines": [1, 0, 0, 0, 1, 1], "image": "☴☳"},
    43: {"name": "택천쾌(Lake Heaven Breakthrough)", "lines": [1, 1, 1, 1, 1, 0], "image": "☱☰"},
    44: {"name": "천풍구(Heaven Wind Coming to Meet)", "lines": [0, 1, 1, 1, 1, 1], "image": "☰☴"},
    45: {"name": "택지췌(Lake Earth Gathering Together)", "lines": [0, 0, 0, 1, 1, 0], "image": "☱☷"},
    46: {"name": "지풍승(Earth Wind Pushing Upward)", "lines": [0, 1, 1, 0, 0, 0], "image": "☷☴"},
    47: {"name": "택수곤(Lake Water Oppression)", "lines": [0, 1, 0, 1, 1, 0], "image": "☱☵"},
    48: {"name": "수풍정(Water Wind The Well)", "lines": [0, 1, 1, 0, 1, 0], "image": "☵☴"},
    49: {"name": "택화혁(Lake Fire Revolution)", "lines": [1, 0, 1, 1, 1, 0], "image": "☱☲"},
    50: {"name": "화풍정(Fire Wind The Cauldron)", "lines": [0, 1, 1, 1, 0, 1], "image": "☲☴"},
    51: {"name": "중뢰진(Double Thunder Shock)", "lines": [1, 0, 0, 1, 0, 0], "image": "☳☳"},
    52: {"name": "중산간(Double Mountain Stillness)", "lines": [0, 0, 1, 0, 0, 1], "image": "☶☶"},
    53: {"name": "풍산점(Wind Mountain Development)", "lines": [1, 0, 0, 0, 1, 1], "image": "☴☶"},
    54: {"name": "뇌택귀매(Thunder Lake Marrying Maiden)", "lines": [1, 1, 0, 1, 0, 0], "image": "☳☱"},
    55: {"name": "뇌화풍(Thunder Fire Abundance)", "lines": [1, 0, 1, 1, 0, 0], "image": "☳☲"},
    56: {"name": "화산려(Fire Mountain The Wanderer)", "lines": [0, 0, 1, 1, 0, 1], "image": "☲☶"},
    57: {"name": "중풍손(Double Wind Gentle)", "lines": [0, 1, 1, 0, 1, 1], "image": "☴☴"},
    58: {"name": "중택태(Double Lake Joyous)", "lines": [1, 1, 0, 1, 1, 0], "image": "☱☱"},
    59: {"name": "풍수환(Wind Water Dispersion)", "lines": [0, 1, 0, 0, 1, 1], "image": "☴☵"},
    60: {"name": "수택절(Water Lake Limitation)", "lines": [1, 1, 0, 0, 1, 0], "image": "☵☱"},
    61: {"name": "풍택중부(Wind Lake Inner Truth)", "lines": [1, 1, 0, 0, 1, 1], "image": "☴☱"},
    62: {"name": "뇌산소과(Thunder Mountain Small Exceeding)", "lines": [0, 0, 1, 1, 0, 0], "image": "☶☳"},
    63: {"name": "수화기제(Water Fire After Completion)", "lines": [1, 0, 1, 0, 1, 0], "image": "☵☲"},
    64: {"name": "화수미제(Fire Water Before Completion)", "lines": [0, 1, 0, 1, 0, 1], "image": "☲☵"},
}

# 逆引き용: 효 리스트로 괘 번호를 찾기 위한 맵
LINES_TO_HEXNUM = {tuple(data["lines"]): num for num, data in HEXAGRAM_DATA.items()}

# --- 핵심 로직 함수 ---

def cast_divination():
    """
    연속적 점괘 시스템
    - 첫 번째 점괘: 완전히 랜덤하게 생성
    - 이후 점괘: 이전 지괘가 새로운 본괘가 되어 연속적 흐름 생성
    """
    
    # 첫 번째 점괘이거나 이전 지괘가 없으면 랜덤하게 시작
    if st.session_state.previous_target_hex is None:
        logging.info("첫 번째 점괘 - 완전 랜덤 생성")
        max_attempts = 10  # 최대 10번 시도
        
        for attempt in range(max_attempts):
            raw_lines = [random.choice([6, 7, 8, 9]) for _ in range(6)]
            
            original_lines = []
            target_lines = []
            changing_lines_pos = []

            # raw_lines는 아래(1효)부터 위(6효)로 구성되므로, 역순으로 처리합니다.
            for i, val in enumerate(raw_lines):
                line_pos = i + 1
                if val == 9: # 노양
                    original_lines.append(1)
                    target_lines.append(0)
                    changing_lines_pos.append(line_pos)
                elif val == 7: # 소양
                    original_lines.append(1)
                    target_lines.append(1)
                elif val == 8: # 소음
                    original_lines.append(0)
                    target_lines.append(0)
                elif val == 6: # 노음
                    original_lines.append(0)
                    target_lines.append(1)
                    changing_lines_pos.append(line_pos)

            # 괘는 위(6효)부터 아래(1효)로 저장되므로, 리스트를 뒤집습니다.
            original_lines.reverse()
            target_lines.reverse()

            original_hex_num = LINES_TO_HEXNUM.get(tuple(original_lines))
            target_hex_num = LINES_TO_HEXNUM.get(tuple(target_lines))
            
            # 유효한 괘 조합인지 확인
            if original_hex_num is not None and target_hex_num is not None:
                st.session_state.divination_count = 1
                st.session_state.previous_target_hex = target_hex_num
                logging.info(f"첫 점괘 생성 성공 (시도 {attempt + 1}): 본괘={original_hex_num}, 지괘={target_hex_num}, 변효={changing_lines_pos}")
                return original_hex_num, target_hex_num, changing_lines_pos
            else:
                logging.warning(f"첫 점괘 생성 시도 {attempt + 1} 실패: original_lines={original_lines}, target_lines={target_lines}")
        
        # 모든 시도가 실패한 경우 기본값 반환
        logging.error(f"첫 점괘 생성 {max_attempts}번 시도 모두 실패, 기본값(1, 2) 반환")
        st.session_state.divination_count = 1
        st.session_state.previous_target_hex = 2
        return 1, 2, []  # 중천건 -> 중지곤
    
    else:
        # 연속적 점괘: 이전 지괘를 본괘로 사용
        original_hex_num = st.session_state.previous_target_hex
        original_lines = HEXAGRAM_DATA[original_hex_num]["lines"].copy()
        
        logging.info(f"연속 점괘 {st.session_state.divination_count + 1}번째 - 이전 지괘 {original_hex_num}번을 본괘로 사용")
        
        # 새로운 변효 생성 (1-3개 정도의 적당한 변화)
        num_changes = random.randint(1, 3)
        changing_lines_pos = random.sample(range(1, 7), num_changes)
        changing_lines_pos.sort(reverse=True)  # 6효부터 1효 순서로 정렬
        
        # 변효 적용하여 지괘 생성
        target_lines = original_lines.copy()
        for pos in changing_lines_pos:
            line_index = 6 - pos  # 6효=index 0, 1효=index 5
            target_lines[line_index] = 1 - target_lines[line_index]  # 0->1, 1->0
            
        target_hex_num = LINES_TO_HEXNUM.get(tuple(target_lines))
        
        if target_hex_num is None:
            # 안전장치: 유효하지 않은 조합이면 랜덤 지괘 선택
            target_hex_num = random.randint(1, 64)
            logging.warning(f"유효하지 않은 지괘 조합 - 랜덤 지괘 {target_hex_num} 사용")
        
        st.session_state.divination_count += 1
        st.session_state.previous_target_hex = target_hex_num
        
        logging.info(f"연속 점괘 성공: 본괘={original_hex_num} → 지괘={target_hex_num}, 변효={changing_lines_pos}")
        return original_hex_num, target_hex_num, changing_lines_pos


# --- UI 렌더링 함수 ---

def get_hexagram_info_from_db(hex_num):
    """MongoDB에서 괘 정보를 가져오는 함수"""
    try:
        hexagram_data = hexagram_db.get_hexagram_by_number(hex_num)
        if hexagram_data:
            return hexagram_data
        else:
            logging.warning(f"MongoDB에서 {hex_num}번 괘 정보를 찾을 수 없습니다.")
            return None
    except Exception as e:
        logging.error(f"MongoDB에서 괘 정보 조회 중 오류: {e}")
        return None

def display_hexagram(hex_num, changing_lines_pos=None):
    """괘상과 효를 시각적으로 표시하는 함수"""
    if not hex_num:
        st.error("괘 정보를 찾을 수 없습니다.")
        return
        
    # MongoDB에서 상세 정보 가져오기
    db_data = get_hexagram_info_from_db(hex_num)
    
    # 기본 괘상 정보 (하드코딩)
    data = HEXAGRAM_DATA[hex_num]
    
    # MongoDB 데이터가 있으면 사용, 없으면 기본 이름 사용
    display_name = db_data.get('name', data['name']) if db_data else data['name']
    
    st.markdown(f"<h3 style='text-align: center;'>{display_name} ({hex_num})</h3>", unsafe_allow_html=True)
    
    # MongoDB에서 가져온 추가 정보 표시
    if db_data:
        if 'coreViewpoint' in db_data and db_data['coreViewpoint']:
            st.markdown(f"<p style='text-align: center; font-style: italic; color: #666;'>🎯 핵심관점: {db_data['coreViewpoint']}</p>", unsafe_allow_html=True)
        
        if 'keywords' in db_data and db_data['keywords']:
            keywords_str = ', '.join(db_data['keywords']) if isinstance(db_data['keywords'], list) else str(db_data['keywords'])
            st.markdown(f"<p style='text-align: center; font-size: 14px; color: #888;'>🏷️ {keywords_str}</p>", unsafe_allow_html=True)
    
    # 괘상 이미지 표시
    st.markdown(f"<div style='text-align: center; font-size: 80px; line-height: 1.2;'>{data['image'][0]}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center; font-size: 80px; line-height: 1.2;'>{data['image'][1]}</div>", unsafe_allow_html=True)

    st.markdown("---")
    
    # 6개 효를 위에서부터 아래로 표시
    for i in range(6):
        line_pos = 6 - i # 6, 5, 4, 3, 2, 1
        line_symbol = "⚊" if data["lines"][i] == 1 else "⚋"
        
        # 변효인 경우 특별히 표시
        if changing_lines_pos and line_pos in changing_lines_pos:
            st.markdown(f"<p style='text-align: center; font-weight: bold; color: #FF4B4B; font-size: 24px;'>{line_pos}효: {line_symbol}  &nbsp; 🔄 변화</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='text-align: center; font-size: 24px;'>{line_pos}효: {line_symbol}</p>", unsafe_allow_html=True)


def get_interpretation_guideline(changing_lines_count):
    """변효 개수에 따른 해석 가이드라인 반환"""
    if changing_lines_count == 0:
        return "변효 없음: **본괘(本卦)**의 전체적인 의미(괘사)로 현재 상황을 깊이 이해하세요."
    elif changing_lines_count == 1:
        return "변효 1개: **변하는 효의 의미(효사)**가 현재 상황의 핵심이자 당신을 위한 가장 중요한 메시지입니다."
    elif changing_lines_count == 2:
        return "변효 2개: 두 변화 중 **위에 있는 변효**가 더 중요하고 미래에 가까운 변화를 암시합니다."
    elif changing_lines_count == 3:
        return "변효 3개: 상황의 절반이 변화하는 시점입니다. **본괘(현재)**와 **지괘(미래)**의 의미를 모두 참고하여 전체적인 흐름을 읽어야 합니다."
    else: # 4, 5, 6개
        return f"변효 {changing_lines_count}개: 상황이 곧 완전히 새로운 국면으로 전환됩니다. 현재보다 **미래의 모습인 지괘(之卦)**의 의미에 더 집중하여 다음 단계를 준비해야 합니다."


# --- Streamlit 앱 메인 ---

st.set_page_config(page_title="🔮 지혜의 렌즈 - 주역 점괘 시스템", layout="wide")

# 세션 상태 초기화
if 'result' not in st.session_state:
    st.session_state.result = None
if 'question_to_llm' not in st.session_state:
    st.session_state.question_to_llm = ""
if 'previous_target_hex' not in st.session_state:
    st.session_state.previous_target_hex = None
if 'divination_count' not in st.session_state:
    st.session_state.divination_count = 0

# --- 화면 구성 ---

st.title("🔮 지혜의 렌즈 - 연속적인 주역 점괘 시스템")

# 점괘 히스토리 표시
if st.session_state.divination_count > 0:
    if st.session_state.divination_count == 1:
        st.markdown("🎯 **첫 번째 점괘 - 하늘의 뜻을 묻습니다**")
    else:
        st.markdown(f"🔄 **{st.session_state.divination_count}번째 연속 점괘 - 흐름이 계속됩니다**")
        
    # 리셋 버튼 추가
    col_reset, col_continue = st.columns([1, 3])
    with col_reset:
        if st.button("🔄 새로운 시작", help="점괘 히스토리를 리셋하고 새로운 첫 점괘를 시작합니다"):
            st.session_state.previous_target_hex = None
            st.session_state.divination_count = 0
            st.session_state.result = None
            st.rerun()
else:
    st.markdown("🎯 **64가지 관점으로 보는 세상의 모든 문제**")

st.markdown("당신의 마음에 질문을 품고, 아래 버튼을 눌러 현재 상황과 변화의 흐름에 대한 통찰을 얻어보세요.")

# MongoDB 연결 상태 확인 및 표시
try:
    test_data = hexagram_db.get_hexagram_by_number(1)
    if test_data:
        st.success("✅ MongoDB 연결됨 - 64괘 데이터베이스 사용 가능")
    else:
        st.warning("⚠️ MongoDB 연결되었으나 64괘 데이터가 없습니다")
except Exception as e:
    st.error(f"❌ MongoDB 연결 실패: {e}")
    st.info("💡 기본 괘상 정보로만 동작합니다. MongoDB 연결을 확인해주세요.")

st.markdown("---")
st.markdown("🎯 **64가지 관점으로 보는 세상의 모든 문제**")
st.markdown("당신의 마음에 질문을 품고, 아래 버튼을 눌러 현재 상황과 변화의 흐름에 대한 통찰을 얻어보세요.")

# 점괘 뽑기 버튼 - 상황에 맞는 텍스트
if st.session_state.divination_count == 0:
    button_text = "🎲 첫 번째 점괘 뽑기"
    spinner_text = "하늘의 뜻을 묻는 중..."
else:
    button_text = f"🔄 다음 점괘 뽑기 ({st.session_state.divination_count + 1}번째)"
    spinner_text = "흐름의 변화를 읽는 중..."

if st.button(button_text, type="primary", use_container_width=True):
    with st.spinner(spinner_text):
        st.session_state.result = cast_divination()

st.markdown("---")

# 결과가 있으면 화면에 표시
if st.session_state.result:
    original_hex, target_hex, changing_lines = st.session_state.result    # Null 체크 추가
    if original_hex is None or target_hex is None:
        st.error("점괘 생성 중 오류가 발생했습니다. 다시 시도해주세요.")
        st.button("🔄 다시 점괘 뽑기", key="retry")
    else:
        # 연속성 표시
        if st.session_state.divination_count > 1:
            st.info(f"🔗 **연속적 흐름**: 이전 {st.session_state.divination_count-1}번째의 지괘가 이번 {st.session_state.divination_count}번째의 본괘({original_hex}번)가 되었습니다.")
        
        st.subheader("🌟 점괘 결과")
        
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            st.markdown("<h2 style='text-align: center;'>현재 상황 (본괘)</h2>", unsafe_allow_html=True)
            display_hexagram(original_hex, changing_lines)

        with col2:
            st.markdown("<div style='text-align: center; font-size: 100px; margin-top: 200px;'>➡️</div>", unsafe_allow_html=True)

        with col3:
            st.markdown("<h2 style='text-align: center;'>변화의 방향 (지괘)</h2>", unsafe_allow_html=True)
            # 지괘에는 변효 표시를 하지 않음
            display_hexagram(target_hex)

        st.markdown("---")
        
        # 해석 가이드라인 표시
        st.subheader("📖 해석의 열쇠")
        guideline = get_interpretation_guideline(len(changing_lines))
        st.info(guideline)        # AI 해석 섹션
        st.subheader("🤖 AI 지혜의 해석")
        
        # MongoDB에서 본괘와 지괘의 상세 정보 가져오기
        original_hex_data = get_hexagram_info_from_db(original_hex)
        target_hex_data = get_hexagram_info_from_db(target_hex)
        
        # AI에게 질문할 내용 구성 - MongoDB 데이터 포함
        focus = ""
        if len(changing_lines) == 0:
            focus = f"{original_hex}번 {HEXAGRAM_DATA[original_hex]['name']} 괘의 전체적인 의미(괘사)"
        elif len(changing_lines) == 1:
            focus = f"{original_hex}번 괘의 {changing_lines[0]}효의 의미(효사)"
        elif len(changing_lines) >= 4:
            focus = f"{target_hex}번 {HEXAGRAM_DATA[target_hex]['name']} 괘의 의미"
        else:
            focus = "본괘와 지괘의 관계"
        
        # MongoDB 데이터를 포함한 상세한 질문 구성
        question_to_llm = f"본괘는 {original_hex}번 {HEXAGRAM_DATA[original_hex]['name']}이고, 지괘는 {target_hex}번 {HEXAGRAM_DATA[target_hex]['name']}입니다."
        
        # 본괘의 상세 정보 추가
        if original_hex_data:
            question_to_llm += f"\n\n본괘({original_hex}번) 상세 정보:"
            if 'coreViewpoint' in original_hex_data:
                question_to_llm += f"\n- 핵심관점: {original_hex_data['coreViewpoint']}"
            if 'summary' in original_hex_data:
                question_to_llm += f"\n- 요약: {original_hex_data['summary']}"
            if 'mentalModels' in original_hex_data:
                question_to_llm += f"\n- 정신모델: {original_hex_data['mentalModels']}"
            if 'keywords' in original_hex_data:
                keywords_str = ', '.join(original_hex_data['keywords']) if isinstance(original_hex_data['keywords'], list) else str(original_hex_data['keywords'])
                question_to_llm += f"\n- 키워드: {keywords_str}"
        
        # 지괘의 상세 정보 추가
        if target_hex_data:
            question_to_llm += f"\n\n지괘({target_hex}번) 상세 정보:"
            if 'coreViewpoint' in target_hex_data:
                question_to_llm += f"\n- 핵심관점: {target_hex_data['coreViewpoint']}"
            if 'summary' in target_hex_data:
                question_to_llm += f"\n- 요약: {target_hex_data['summary']}"
            if 'mentalModels' in target_hex_data:
                question_to_llm += f"\n- 정신모델: {target_hex_data['mentalModels']}"
            if 'keywords' in target_hex_data:
                keywords_str = ', '.join(target_hex_data['keywords']) if isinstance(target_hex_data['keywords'], list) else str(target_hex_data['keywords'])
                question_to_llm += f"\n- 키워드: {keywords_str}"
        
        # 변효 정보 추가
        question_to_llm += f"\n\n변효는 {changing_lines if changing_lines else '없습니다'}."
        question_to_llm += f"\n\n이 상황에 대해 '{focus}'를 중심으로 종합적으로 설명해주세요."
        
        # 세션 상태에 저장
        st.session_state.question_to_llm = question_to_llm        # AI 해석 버튼과 결과 표시
        if st.button("🧠 AI에게 해석 요청하기", type="secondary"):
            with st.spinner("AI가 고민하고 있습니다..."):
                try:
                    st.success("✨ AI 해석 완료!")
                    st.markdown("### 🌟 맞춤형 통찰")
                    
                    # 스트리밍 응답을 처리하기 위한 placeholder
                    response_placeholder = st.empty()
                    full_response = ""
                    
                    # MongoDB 데이터 포함 여부에 따른 안내
                    if original_hex_data or target_hex_data:
                        st.info("📚 MongoDB의 64괘 상세 데이터를 활용한 해석입니다.")
                    else:
                        st.warning("⚠️ MongoDB 데이터를 사용할 수 없어 기본 정보로 해석합니다.")
                    
                    # ask_hexagram은 generator를 반환하므로 스트리밍 처리
                    for chunk in ask_hexagram(question_to_llm):
                        full_response += chunk
                        response_placeholder.markdown(full_response)
                    
                except Exception as e:
                    logging.error(f"ask_hexagram 호출 중 오류 발생: {e}")
                    st.error(f"AI 해석 중 오류가 발생했습니다: {e}")
                    st.info("💡 현재는 기본 해석 가이드라인을 참고하여 스스로 해석해보세요.")        # 개발자용 디버그 정보
        with st.expander("🔧 개발자 정보 (디버그용)"):
            st.code(st.session_state.question_to_llm, language="text")
            
            debug_info = {
                "original_hex": original_hex,
                "target_hex": target_hex, 
                "changing_lines": changing_lines,
                "interpretation_focus": focus,
                "mongodb_original_data_available": bool(original_hex_data),
                "mongodb_target_data_available": bool(target_hex_data)
            }
            
            if original_hex_data:
                debug_info["original_hex_db_keys"] = list(original_hex_data.keys())
                
            if target_hex_data:
                debug_info["target_hex_db_keys"] = list(target_hex_data.keys())
            
            st.json(debug_info)

else:
    st.info("🎯 위에 있는 버튼을 눌러 점괘 흐름을 시작하세요.")
    
    # 사용 안내
    st.markdown("---")
    st.markdown("### 📚 연속적 점괘 시스템 안내")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🎲 연속적 점괘 과정:**
        1. **첫 번째 점괘**: 완전히 랜덤하게 생성
        2. **두 번째부터**: 이전 지괘 → 새로운 본괘
        3. 변효 생성으로 새로운 지괘 결정
        4. 연속적 흐름으로 스토리 형성
        5. 언제든 "새로운 시작" 버튼으로 리셋 가능
        """)
    
    with col2:
        st.markdown("""
        **📖 해석 원칙:**
        - **변효 없음**: 본괘의 괘사 중심
        - **변효 1개**: 해당 효사가 핵심 메시지  
        - **변효 2-3개**: 본괘와 지괘 균형있게 참고
        - **변효 4개 이상**: 지괘 중심으로 해석
        - **연속성**: 이전 점괘와의 연결점 고려
        
        **🗃️ 데이터베이스:**
        - MongoDB 연결 시: 64괘 상세 정보 활용
        - 핵심관점, 정신모델, 키워드 등 포함
        """)
        
    # MongoDB 연결 안내
    st.markdown("---")
    st.markdown("### 🔧 MongoDB 설정 안내")
    st.info("""
    **MongoDB 연결이 필요한 이유:**
    - 64괘의 상세한 정신모델과 키워드 데이터 활용
    - AI 해석의 정확도와 깊이 향상
    - 각 괘의 핵심관점과 실무적 적용 방법 제공
    
    **연결 방법:**
    1. MongoDB 서버 실행 (`mongod`)
    2. `wisdom_lenses` 데이터베이스의 `hexagrams` 컬렉션에 64괘 데이터 입력
    3. 앱 재시작하여 연결 상태 확인
    """)
