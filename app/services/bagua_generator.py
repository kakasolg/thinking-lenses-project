"""
주역 8괘-64괘 수학적 매핑 시스템
Charlie Munger의 Mental Models과 수학적 기초 개념을 연결하는 프로젝트
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

@dataclass
class Trigram:
    """8괘(팔괘) 개별 정의"""
    name: str
    symbol: str
    korean: str
    description: str
    concept: str
    
@dataclass
class Hexagram:
    """64괘 개별 정의"""
    upper: Trigram
    lower: Trigram
    number: int
    name: str
    description: str
    mathematical_meaning: str
    examples: List[str]

class MathModel(Enum):
    """두 가지 수학 모델"""
    ABSTRACT = "abstract"  # 추상적 기초
    CONCRETE = "concrete"  # 구체적 대상

class BaguaSystem:
    """주역 8괘-64괘 수학 매핑 시스템"""
    
    def __init__(self):
        self.models = {
            MathModel.ABSTRACT: self._create_abstract_model(),
            MathModel.CONCRETE: self._create_concrete_model()
        }
        
    def _create_abstract_model(self) -> Dict[str, Trigram]:
        """모델 A: 추상적 수학 기초 개념"""
        return {
            "건": Trigram("건", "☰", "乾", "자연수", "counting - 가장 기본적인 셈의 개념"),
            "곤": Trigram("곤", "☷", "坤", "집합", "membership - 포함과 원소관계"),
            "진": Trigram("진", "☳", "震", "함수", "transformation - 입력에서 출력으로의 변환"),
            "손": Trigram("손", "☴", "巽", "관계", "ordering - 순서, 동치, 대응 관계"),
            "감": Trigram("감", "☵", "坎", "측도", "measure - 크기와 불확실성의 척도"),
            "리": Trigram("리", "☲", "離", "구조", "structure - 불변성과 패턴"),
            "간": Trigram("간", "☶", "艮", "극한", "limit - 수렴과 발산의 경계"),
            "태": Trigram("태", "☱", "兌", "연산", "operation - 덧셈, 곱셈 등 기본 연산")
        }
    
    def _create_concrete_model(self) -> Dict[str, Trigram]:
        """모델 B: 구체적 수학 대상"""
        return {
            "건": Trigram("건", "☰", "乾", "원주율(π)", "circularity - 완벽한 원과 주기성"),
            "곤": Trigram("곤", "☷", "坤", "이진법", "discreteness - 0과 1의 이분법"),
            "리": Trigram("리", "☲", "離", "황금비(φ)", "proportion - 자연의 아름다운 비례"),
            "감": Trigram("감", "☵", "坎", "확률", "uncertainty - 불확실성과 측정"),
            "진": Trigram("진", "☳", "震", "미분", "rate - 순간적 변화율"),
            "손": Trigram("손", "☴", "巽", "적분", "accumulation - 점진적 누적"),
            "간": Trigram("간", "☶", "艮", "소수", "primality - 더 이상 분해 불가능한 기본 단위"),
            "태": Trigram("태", "☱", "兌", "대칭성", "invariance - 변환에 대한 불변성")
        }
    
    def get_trigrams(self, model: MathModel) -> Dict[str, Trigram]:
        """특정 모델의 8괘 반환"""
        return self.models[model]
    
    def generate_hexagrams(self, model: MathModel) -> List[Hexagram]:
        """64괘 생성 (8×8 조합)"""
        trigrams = self.get_trigrams(model)
        trigram_list = list(trigrams.values())
        hexagrams = []
        
        number = 1
        for upper in trigram_list:
            for lower in trigram_list:
                # 64괘 조합 생성
                name = f"{upper.korean}{lower.korean}"
                
                # 수학적 의미 생성
                math_meaning = self._generate_mathematical_meaning(
                    upper, lower, model
                )
                
                # 예시 생성
                examples = self._generate_examples(upper, lower, model)
                
                hexagram = Hexagram(
                    upper=upper,
                    lower=lower,
                    number=number,
                    name=name,
                    description=f"{upper.name}(상괘) + {lower.name}(하괘)",
                    mathematical_meaning=math_meaning,
                    examples=examples
                )
                
                hexagrams.append(hexagram)
                number += 1
                
        return hexagrams
    
    def _generate_mathematical_meaning(self, upper: Trigram, lower: Trigram, 
                                     model: MathModel) -> str:
        """두 괘의 조합으로 수학적 의미 생성"""
        if model == MathModel.ABSTRACT:
            return self._abstract_combination(upper, lower)
        else:
            return self._concrete_combination(upper, lower)
    
    def _abstract_combination(self, upper: Trigram, lower: Trigram) -> str:
        """추상적 모델의 조합 의미"""
        combinations = {
            ("자연수", "자연수"): "자연수 체계의 완전성",
            ("자연수", "집합"): "가산 집합과 무한성",
            ("자연수", "함수"): "수열과 점화식",
            ("자연수", "관계"): "순서관계와 동치관계",
            ("자연수", "측도"): "계수 측도와 확률",
            ("자연수", "구조"): "군, 환, 체의 대수구조",
            ("자연수", "극한"): "무한급수와 수렴성",
            ("자연수", "연산"): "사칙연산과 합성함수",
            
            ("집합", "자연수"): "집합의 크기와 기수성",
            ("집합", "집합"): "집합의 연산(합집합, 교집합)",
            ("집합", "함수"): "함수의 정의역과 치역",
            ("집합", "관계"): "관계의 집합론적 정의",
            ("집합", "측도"): "측도론과 확률공간",
            ("집합", "구조"): "위상공간과 연결성",
            ("집합", "극한"): "극한점과 근방",
            ("집합", "연산"): "집합 연산의 대수법칙",
            
            ("함수", "자연수"): "함수의 차수와 복잡도",
            ("함수", "집합"): "함수의 상과 역상",
            ("함수", "함수"): "함수의 합성과 역함수",
            ("함수", "관계"): "함수관계와 그래프",
            ("함수", "측도"): "측도의 변환과 적분",
            ("함수", "구조"): "동형사상과 준동형사상",
            ("함수", "극한"): "함수의 연속성과 극한",
            ("함수", "연산"): "함수의 연산과 함수공간",
        }
        
        key = (upper.description, lower.description)
        return combinations.get(key, f"{upper.description}와 {lower.description}의 조합")
    
    def _concrete_combination(self, upper: Trigram, lower: Trigram) -> str:
        """구체적 모델의 조합 의미"""
        combinations = {
            ("원주율(π)", "원주율(π)"): "원의 성질과 삼각함수",
            ("원주율(π)", "이진법"): "디지털 신호 처리에서의 FFT",
            ("원주율(π)", "황금비(φ)"): "자연에서의 나선과 피보나치",
            ("원주율(π)", "확률"): "원주율의 몬테카를로 추정",
            ("원주율(π)", "미분"): "삼각함수의 미분과 오일러 공식",
            ("원주율(π)", "적분"): "원의 넓이와 적분",
            ("원주율(π)", "소수"): "π와 소수 분포의 연관성",
            ("원주율(π)", "대칭성"): "회전 대칭과 주기함수",
            
            ("이진법", "원주율(π)"): "컴퓨터에서의 π 근사",
            ("이진법", "이진법"): "불대수와 논리회로",
            ("이진법", "황금비(φ)"): "이진 트리와 황금비",
            ("이진법", "확률"): "베르누이 시행과 이항분포",
            ("이진법", "미분"): "디지털 미분과 차분",
            ("이진법", "적분"): "리만 합과 수치적분",
            ("이진법", "소수"): "소수 판별 알고리즘",
            ("이진법", "대칭성"): "대칭키 암호화",
            
            ("미분", "적분"): "미적분학의 기본정리",
            ("소수", "확률"): "소수 정리와 확률적 해석",
            ("대칭성", "황금비(φ)"): "정다면체와 황금비",
        }
        
        key = (upper.description, lower.description)
        return combinations.get(key, f"{upper.description}와 {lower.description}의 상호작용")
    
    def _generate_examples(self, upper: Trigram, lower: Trigram, 
                          model: MathModel) -> List[str]:
        """구체적인 수학 예시 생성"""
        if model == MathModel.ABSTRACT:
            return [
                f"{upper.concept} + {lower.concept}",
                "추상적 예시 개발 중..."
            ]
        else:
            return [
                f"{upper.description} × {lower.description}",
                "구체적 예시 개발 중..."
            ]
    
    def get_duality_pairs(self, model: MathModel) -> List[Tuple[str, str]]:
        """대대(對待) 관계 쌍 반환"""
        if model == MathModel.ABSTRACT:
            return [
                ("건", "곤"),  # 자연수 ↔ 집합
                ("진", "손"),  # 함수 ↔ 관계  
                ("감", "리"),  # 측도 ↔ 구조
                ("간", "태")   # 극한 ↔ 연산
            ]
        else:
            return [
                ("건", "곤"),  # π ↔ 이진법
                ("리", "감"),  # 황금비 ↔ 확률
                ("진", "손"),  # 미분 ↔ 적분
                ("간", "태")   # 소수 ↔ 대칭성
            ]
    
    def analyze_completeness(self, model: MathModel) -> Dict[str, any]:
        """모델의 완전성 분석"""
        hexagrams = self.generate_hexagrams(model)
        trigrams = self.get_trigrams(model)
        
        analysis = {
            "total_hexagrams": len(hexagrams),
            "total_trigrams": len(trigrams),
            "mathematical_coverage": self._calculate_coverage(hexagrams),
            "duality_pairs": self.get_duality_pairs(model),
            "empty_combinations": self._find_empty_combinations(hexagrams),
            "model_type": model.value
        }
        
        return analysis
    
    def _calculate_coverage(self, hexagrams: List[Hexagram]) -> float:
        """수학적 개념 커버리지 계산"""
        # 실제 수학 개념과 매칭되는 비율 (향후 구현)
        meaningful_combinations = sum(1 for h in hexagrams 
                                    if "개발 중" not in h.mathematical_meaning)
        return meaningful_combinations / len(hexagrams) * 100
    
    def _find_empty_combinations(self, hexagrams: List[Hexagram]) -> List[str]:
        """의미있는 매핑이 없는 조합 찾기"""
        empty = []
        for h in hexagrams:
            if ("조합" in h.mathematical_meaning and 
                h.mathematical_meaning.endswith("의 조합")):
                empty.append(f"{h.upper.name}-{h.lower.name}")
        return empty

# 테스트 및 예시 실행
if __name__ == "__main__":
    system = BaguaSystem()
    
    print("=== 주역 8괘-64괘 수학적 매핑 시스템 ===\n")
    
    for model in [MathModel.ABSTRACT, MathModel.CONCRETE]:
        print(f"\n📊 {model.value.upper()} 모델 분석:")
        print("-" * 50)
        
        # 8괘 출력
        trigrams = system.get_trigrams(model)
        print("\n🔸 8괘 (기초 개념):")
        for name, trigram in trigrams.items():
            print(f"  {trigram.symbol} {name}: {trigram.description}")
        
        # 분석 결과
        analysis = system.analyze_completeness(model)
        print(f"\n📈 분석 결과:")
        print(f"  - 총 64괘 생성: {analysis['total_hexagrams']}개")
        print(f"  - 수학적 커버리지: {analysis['mathematical_coverage']:.1f}%")
        print(f"  - 대대 관계: {len(analysis['duality_pairs'])}쌍")
        
        # 몇 가지 예시 64괘
        hexagrams = system.generate_hexagrams(model)
        print(f"\n🔹 예시 64괘 (첫 5개):")
        for i, hex in enumerate(hexagrams[:5]):
            print(f"  {hex.number:2d}. {hex.name}: {hex.mathematical_meaning}")
        
        print("\n" + "="*60)
