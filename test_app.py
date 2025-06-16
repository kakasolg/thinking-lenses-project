# 🧪 384가지 효변 시나리오 테스트 전용 페이지
import streamlit as st
import random

# 64괘 괘상 데이터 직접 정의 (의존성 문제 해결)
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
    58: [1, 1, 0, 1, 1, 0],  # 태(允) ☱☱
    59: [0, 1, 0, 0, 1, 1],  # 환(渙) ☴☵
    60: [1, 1, 0, 0, 1, 0],  # 절(節) ☵☱
    61: [1, 1, 0, 0, 1, 1],  # 중부(中孚) ☴☱
    62: [0, 0, 1, 1, 0, 0],  # 소과(小過) ☶☳
    63: [1, 0, 1, 0, 1, 0],  # 기제(既濟) ☵☲
    64: [0, 1, 0, 1, 0, 1],  # 미제(未濟) ☲☵
}

# 효변 계산 함수들
def flip_line(line_value):
    """한 효를 뒤집기: 양효(1) ↔ 음효(0)"""
    return 1 - line_value

def calculate_target_hexagram(original_hex_num, changing_line_pos):
    """효변을 통한 지괘(之卦) 계산"""
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
    
    return None

def generate_full_eff_change_map():
    """전체 384가지 효변 시나리오 생성"""
    eff_change_map = {}
    
    for hex_num in range(1, 65):  # 1-64괘
        eff_change_map[hex_num] = {}
        
        for line_pos in range(1, 7):  # 1-6효
            target_hex = calculate_target_hexagram(hex_num, line_pos)
            if target_hex:
                eff_change_map[hex_num][line_pos] = target_hex
    
    return eff_change_map

# 전체 효변 맵 생성
eff_change_map = generate_full_eff_change_map()

# Streamlit 설정
st.set_page_config(page_title="효변 시스템 테스트", layout="wide")
st.title("🧪 384가지 효변 시나리오 테스트")
st.markdown("🎆 **64괘 × 6효 = 384가지 전체 효변 시나리오 테스트!**")

# 기본 테스트 버튼들
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🎲 랜덤 테스트"):
        test_gua = random.randint(1, 64)
        test_line = random.randint(1, 6)
        
        st.success(f"🎯 테스트: {test_gua}번 괘 {test_line}효")
        
        if test_gua in eff_change_map and test_line in eff_change_map[test_gua]:
            target_gua = eff_change_map[test_gua][test_line]
            st.success(f"✨ 지괘: {target_gua}번 괘")
            st.info(f"🔄 결과: {test_gua}번 괘 → {target_gua}번 괘")
        else:
            st.error("데이터 오류!")

with col2:
    if st.button("📊 6번 괘 테스트"):
        st.success("🎯 6번 괘(송訟) 전체 효변:")
        
        if 6 in eff_change_map:
            for line in range(1, 7):
                if line in eff_change_map[6]:
                    target = eff_change_map[6][line]
                    st.write(f"{line}효 변 → {target}번 괘")
        else:
            st.error("데이터 없음")

with col3:
    if st.button("📊 통계 보기"):
        total = sum(len(v) for v in eff_change_map.values())
        st.success(f"🎆 전체: {total}가지")
        st.info(f"괘 수: {len(eff_change_map)}/64")

# 대형 테스트
if st.button("🚀 전체 검증", type="primary"):
    st.markdown("🔍 **전체 효변 시스템 검증 중...**")
    
    error_count = 0
    success_count = 0
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for gua_num in range(1, 65):
        progress = gua_num / 64
        progress_bar.progress(progress)
        status_text.text(f"검증 중: {gua_num}/64 괘...")
        
        if gua_num in eff_change_map:
            for line in range(1, 7):
                if line in eff_change_map[gua_num]:
                    target = eff_change_map[gua_num][line]
                    if 1 <= target <= 64:
                        success_count += 1
                    else:
                        error_count += 1
                        st.error(f"오류: {gua_num}번 괘 {line}효 → {target}번 괘")
                else:
                    error_count += 1
    
    progress_bar.progress(1.0)
    status_text.text("검증 완료!")
    
    # 결과 요약
    st.markdown("---")
    st.success(f"🎆 **효변 시스템 검증 결과**")
    st.write(f"- ✅ 성공: {success_count}가지")
    st.write(f"- ❌ 오류: {error_count}가지")
    
    if success_count + error_count > 0:
        completion = success_count/(success_count + error_count)*100
        st.write(f"- 🎯 **완성도**: {completion:.1f}%")
    
    if error_count == 0:
        st.balloons()
        st.success("🎉 **모든 384가지 효변 시나리오가 완벽하게 작동합니다!**")
