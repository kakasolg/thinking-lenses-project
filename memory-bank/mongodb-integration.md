# MongoDB 통합 시스템 정보

## 데이터베이스 연결 정보

### 기본 설정
- **연결 도구**: MCP MongoDB Tools
- **연결 상태**: 활성화됨 (switch-connection 도구 사용 가능)
- **접근 권한**: 읽기/쓰기 가능

### 데이터베이스 목록
```
- admin (40KB)
### 컴렉션 구조
```
wisdom_lenses/
├── memorize_cards
├── memorize_subjects  
├── mathematical_trigrams ⭐ 수학적 8괘 데이터 (9개)
├── mathematical_hexagrams ⭐ 수학적 64괘 조합 (8개) **신규 완성**
└── hexagrams ⭐ 64괘 정신 모델 데이터 (64개)
```
wisdom_lenses/
├── memorize_cards
├── memorize_subjects  
├── hexagrams ⭐ 64괘 정신 모델 데이터
└── mathematical_trigrams ⭐ 수학적 8괘 데이터 (신규 생성)
```

### hexagrams 컬렉션 스키마
### 컬렉션 구조
```
wisdom_lenses/
├── memorize_cards
├── memorize_subjects  
└── hexagrams ⭐ 64괘 정신 모델 데이터
```

### hexagrams 컬렉션 스키마

#### 기본 필드
```javascript
{
  "_id": ObjectId,
  "number": 1-64,           // 괘 번호
  "symbol": "☰/☰",          // 주역 기호 (상괘/하괘)
  "name": "중천건",          // 괘명 (한글)
  "coreViewpoint": "...",   // 핵심 관점 설명
  "mentalModels": "...",    // 찰리 멍거 정신 모델 (영문)
  "summary": "...",         // 핵심 요약
  "keywords": [...],        // 키워드 배열
  "perspectives": {         // 다학제적 관점
    "ancient": {...},
    "physics": {...},
    "biology": {...}, 
    "business": {...},
    "psychology": {...},
    "military": {...}
  },
  "createdAt": Date,
  "updatedAt": Date,
  "__v": 0
}
```

#### 정신 모델 예시
- **Activation Energy** (활성화 에너지)
- **Network Effects** (네트워크 효과)
- **Circle of Competence** (능력의 범위)
- **Opportunity Cost** (기회비용)
- **Hanlon's Razor** (핸런의 면도날)
- **First Principles Thinking** (제1원칙 사고)
- **Comparative Advantage** (비교우위)
- **Compounding** (복리효과)
- **Margin of Safety** (안전마진)
- **Pareto Principle** (파레토 법칙)
- 기타 54개 고유 정신 모델...

## 사용법 및 쿼리 예시

### 모든 64괘 조회
```javascript
find("wisdom_lenses", "hexagrams", {}, 64)
```

### 특정 괘 조회
```javascript
find("wisdom_lenses", "hexagrams", {"number": 1}, 1)
find("wisdom_lenses", "hexagrams", {"name": "중천건"}, 1)
```

### 정신 모델별 검색
```javascript
find("wisdom_lenses", "hexagrams", {"mentalModels": "Pareto Principle"}, 1)
```

### mathematical_trigrams 컬렉션 스키마 (신규 생성)

#### 기본 필드
```javascript
{
  "_id": ObjectId,
  "number": 1-9,              // 괘 번호 (1-8: 8괘, 9: 자연상수 e)
  "symbol": "☰",              // 주역 기호
  "name": "건",                // 괘명 (한글)
  "englishName": "Creative/Heaven", // 영문명
  "mathematicalConcept": "π (Pi)", // 수학적 개념
  "coreTheory": "...",        // 핵심 이론
  "summary": "...",           // 요약
  "verificationMethods": [...], // 검증 방법 배열
  "computationalAspects": {    // 계산적 측면
    "convergenceRate": "...",
    "accuracy": "...",
    "computationTime": "...",
    "memoryUsage": "..."
  ### mathematical_hexagrams 컴렉션 스키마 (신규 완성)
  
  #### 기본 필드
  ```javascript
  {
    "_id": ObjectId,
    "number": 1-8,              // 조합 번호
    "upperTrigram": {           // 상괘 정보
      "number": 1-8,
      "symbol": "☰",
      "name": "건",
      "concept": "π (원주율)",
      "meaning": "창조, 완전성"
    },
    "lowerTrigram": {           // 하괘 정보
      "number": 1-8,
      "symbol": "☴",
      "name": "손",
      "concept": "적분 (Integral)",
      "meaning": "누적합"
    },
    "symbol": "☰/☴",          // 조합 기호
    "name": "미적분학의 기본정리", // 조합명
    "englishName": "Fundamental Theorem of Calculus",
    "mathematicalConcept": "...", // 수학적 개념
    "coreTheory": "...",        // 핵심 이론
    "formula": "...",           // 수학 공식
    "summary": "...",           // 요약
    "significance": "...",      // 중요성
    "verificationMethods": [...], // 검증 방법
    "computationalAspects": {    // 계산적 측면
      "convergenceRate": "...",
      "accuracy": "...",
      "computationTime": "...",
      "memoryUsage": "..."
    },
    "applications": [...],      // 응용 분야
    "philosophicalAspect": "...", // 철학적 측면
    "keywords": [...],          // 키워드
    "difficulty": "고급",      // 난이도
    "visualizations": [...],    // 시각화 요소
    "trigrams": {               // 8괘 매핑
      "upper": 4,
      "lower": 5
    },
    "createdAt": Date,
    "updatedAt": Date
  }
  ```
  
  #### 수학적 8개 핵심 조합
  | 번호 | 조합 | 수학 이론 | 중요도 | 상태 |
  |------|------|-----------|--------|------|
  | 1 | 진☳/손☴ | 미적분학의 기본정리 | ⭐⭐⭐ | ✅ |
  | 2 | 건☰/e | 오일러의 항등식 | ⭐⭐⭐ | ✅ |
  | 3 | 건☰/리☲ | 기하학적 조화 | ⭐⭐ | ✅ |
  | 4 | 간☶/곤☷ | RSA 암호학 | ⭐⭐⭐ | ✅ |
  | 5 | 태☱/리☲ | 완벽한 조화 | ⭐⭐ | ✅ |
  | 6 | 곤☷/건☰ | 디지털-아날로그 변환 | ⭐⭐⭐ | ✅ |
  | 7 | 리☲/감☵ | 최적화 이론 | ⭐⭐⭐ | ✅ |
  | 8 | 감☵/e | 정규분포와 포아송분포 | ⭐⭐⭐ | ✅ |
  
  **전체 가능 조합**: 8×8 = 64가지
  **현재 완성**: 8개 (핵심 조합)
  **대기 중**: 56개 조합
  
  
  "applications": [...],      // 응용 분야 배열
  "philosophicalAspect": "...", // 철학적 측면
  "keywords": [...],          // 키워드 배열
  "relatedHexagrams": [...],  // 연관 64괘 번호
  "difficulty": "중급",      // 난이도
  "visualizations": [...],    // 시각화 요소
  "createdAt": Date,
  "updatedAt": Date
}
```

#### 수학적 8괘 매핑
| 번호 | 기호 | 괘명 | 수학 개념 | 핵심 이론 | 난이도 |
|------|------|------|-----------|-----------|-------|
| 1 | ☰ | 건 | π (Pi) | 원주율의 무한급수 전개 | 중급 |
| 2 | ☲ | 리 | φ (Golden Ratio) | 황금비와 피보나치 수열 | 초급 |
| 3 | ☵ | 감 | 확률론 | 불확실성의 수학적 모델링 | 고급 |
| 4 | ☳ | 진 | 미적분 (도함수) | 함수의 순간변화율 | 중급 |
| 5 | ☴ | 손 | 미적분 (적분) | 함수의 누적합과 면적 | 중급 |
| 6 | ☷ | 곤 | 이진법 | 0과 1로 맨든 정보 표현 | 초급 |
| 7 | ☶ | 간 | 소수론 | 분해 불가능한 기본 단위 | 고급 |
| 8 | ☱ | 태 | 대칭성 | 기하학적 변환과 불변성 | 중급 |
| 9 | e | 자연상수 | e (Euler) | 자연 성장과 연속 복리 | 중급 |


```javascript
find("wisdom_lenses", "hexagrams", {"keywords": "복리효과"}, 10)
```
## 통합 가능성 분석

### 현재 프로젝트와의 연관성

#### 1. 원래 목표 달성
- ✅ **초기 목표**: "주역 64괘를 찰리 멍거 격자틀 정신 모델에 매핑"
- ✅ **현재 상태**: MongoDB에 완전한 매핑 시스템 구축 완료
- 🔄 **진화된 목표**: 수학적 기반 검증 시스템과 통합

#### 2. **완전한 2단계 시스템 구축 완료** 🎉
**수학 8괘 (mathematical_trigrams)** + **정신 모델 64괘 (hexagrams)**

| 수학 8괘 | 주역 8괘 | 연결 정신 모델 | 통합 가능성 |
|----------|----------|-------------|-------------|
| 1. π (건☰) | 중천건(☰/☰) | 활성화 에너지 | 창조적 에너지, 초기 투입 |
| 2. φ (리☲) | 중화리(☲/☲) | 상호의존성 | 황금비, 조화와 균형 |
| 3. 확률론 (감☵) | 중수감(☵/☵) | 회복탄력성 | 불확실성, 위기관리 |
| 4. 도함수 (진☳) | 중놰진(☳/☳) | 가용성 휴리스틱 | 순간적 변화, 돌발 상황 |
| 5. 적분 (손☴) | 중풍손(☴/☴) | 습관의 힘 | 점진적 축적, 부드러운 침투 |
| 6. 이진법 (곤☷) | 중지곤(⚏/⚏) | 네트워크 효과 | 기초 단위, 수용적 기반 |
| 7. 소수론 (간☶) | 중산간(☶/☶) | 성찰과 명상 | 분해불가능, 정지와 견고함 |
| 8. 대칭성 (태☱) | 중택태(☱/☱) | 긍정적 강화 | 균형과 조화, 기쁨과 소통 |
| 9. 자연상수 e | 전체 64괘 | 자연 성장 원리 | 복리효과, 점진적 성장 |

#### 3. 3단계 위계구조 검증 준비 완료
```
Level 1: 8괘 (기초 원자) ← 수학적 검증 완료 + MongoDB 저장 완료
    ↓
Level 2: 64괘 (방정식/연산) ← MongoDB 데이터 완성
    ↓  
Level 3: 응용 이론 (복합 시스템) ← 구축 대기
```

#### 3. 3단계 위계구조 검증
```
Level 1: 8괘 (기초 원자) ← 수학적 검증 완료
    ↓
Level 2: 64괘 (방정식/연산) ← MongoDB 데이터 완성
    ↓  
Level 3: 응용 이론 (복합 시스템) ← 구축 대기
```

### 통합 개발 방향

#### Option A: 병렬 개발
- 수학 시스템 Phase 1.5 최적화 계속
- 64괘 웹 인터페이스 별도 구축
- 추후 Phase 2에서 통합

#### Option B: 64괘 우선 개발  
- MongoDB 64괘 웹 시스템 우선 구축
- 사용자 가치 극대화 (실용적 도구)
- 수학 시스템과 점진적 통합

#### Option C: 즉시 통합 분석
- 수학 8괘 ↔ 정신 모델 64괘 대응 분석
- 공통 패턴 및 차이점 연구
- 새로운 발견 및 누락 요소 탐색

## 기술적 구현 방안

### 1. 웹 인터페이스 구축
```python
# Flask 라우트 예시
@app.route('/api/hexagram/<int:number>')
def get_hexagram(number):
    # MongoDB 쿼리
    result = find("wisdom_lenses", "hexagrams", {"number": number}, 1)
    return jsonify(result)

@app.route('/api/mental-model/<model_name>')  
def get_by_mental_model(model_name):
    result = find("wisdom_lenses", "hexagrams", {"mentalModels": model_name}, 1)
    return jsonify(result)
```

### 2. 검색 및 필터링
- 괘명/번호 검색
- 정신 모델 필터링  
- 키워드 기반 검색
- 상황별 괘 추천

### 3. 시각화 요소
- 64괘 전체 매트릭스 
- 8괘별 그룹핑
- 정신 모델 카테고리별 분류
## 사용법 및 쿼리 예시

### 모든 64괘 조회
```javascript
find("wisdom_lenses", "hexagrams", {}, 64)
```

### 수학적 8괘 조회
```javascript
find("wisdom_lenses", "mathematical_trigrams", {}, 9)
```

### 특정 수학 개념 조회
```javascript
find("wisdom_lenses", "mathematical_trigrams", {"mathematicalConcept": "π (Pi)"}, 1)
find("wisdom_lenses", "mathematical_trigrams", {"name": "건"}, 1)
```

### 난이도별 검색
```javascript
find("wisdom_lenses", "mathematical_trigrams", {"difficulty": "고급"}, 5)
```

### 연관 64괘 매핑
```javascript
// 1괘 건(π)과 연결된 64괘 찾기
find("wisdom_lenses", "mathematical_trigrams", {"number": 1}, 1) // relatedHexagrams: [1]
find("wisdom_lenses", "hexagrams", {"number": 1}, 1) // 중천건
```

### 정신 모델별 검색
```javascript
find("wisdom_lenses", "hexagrams", {"mentalModels": "Pareto Principle"}, 1)
```

### 키워드별 검색
```javascript
find("wisdom_lenses", "hexagrams", {"keywords": "복리효과"}, 10)
find("wisdom_lenses", "mathematical_trigrams", {"keywords": "원주율"}, 1)
```
1. **상황별 괘 추천** 시스템
2. **정신 모델 학습** 도구
3. **수학 8괘와 연결점** 분석

### 중장기 목표 (1-2개월)
1. **수학-64괘 통합** 분석 시스템
2. **새로운 발견** 도출 및 검증
3. **교육용 플랫폼** 완성

---

**마지막 업데이트**: 2025-06-17
**데이터 검증**: 64개 문서 모두 확인 완료
## 다음 단계 우선순위 (2025-06-17 업데이트)

---

**마지막 업데이트**: 2025-06-17
**주요 변경**: mathematical_hexagrams 컴렉션 신규 생성 (8개 핵심 조합)
**데이터 검증**: mathematical_trigrams(9개) + mathematical_hexagrams(8개) + hexagrams(64개) = 총 81개 문서 확인
**프로젝트 상태**: Phase 1.8 완전 달성 - 세계 최초 주역-수학-정신모델 통합 시스템 ✅

### 즉시 실행 가능 (다음 세션)

#### Option A: **통합 웹 인터페이스 구축** (추천 ⭐)
1. **MongoDB 연동 API** 개발
   - `/api/math-trigrams/<number>` - 수학적 8괘 조회
   - `/api/hexagrams/<number>` - 64괘 정신 모델 조회
   - `/api/mapping/<trigram_number>` - 8괘-64괘 매핑 조회

2. **통합 대시보드** 생성
   - 수학 검증 + 정신 모델 조합 인터페이스
   - 8괘 ↔ 64괘 상호 네비게이션
   - 실시간 계산 + 정신 모델 조합 제시

#### Option B: **수학 시스템 최적화 계속**
- Phase 1.5 성능 최적화 진행
- MongoDB 데이터는 대기 상태로 유지

#### Option C: **데이터 분석 및 연관성 연구**
- 수학 8괘 과 정신 모델 64괘 간 상관관계 분석
- 공통 패턴 및 차이점 도출
- 새로운 발견 가능성 탐색

### 단기 목표 (1-2주)
1. **전체 시스템 통합**
   - 수학 검증 + 64괘 정신 모델 연결
   - 상황별 괘 추천 시스템
   - 통합 검색 및 필터링 기능

2. **시각화 시스템**
   - 8괘-64괘 매핑 네트워크 다이어그램
   - 수학적 정확도 vs 정신 모델 적용성 비교
   - 대화형 대시보드 (plotly + MongoDB)

3. **교육 도구 기능**
   - 수학 개념 학습 가이드
   - 정신 모델 실전 적용 사례
   - 8괘-64괘 상호 연결고리 학습

### 중장기 목표 (1-2개월)
1. **AI 분야 확장 (Phase 2)**
   - Transformer 아키텍처 역분해
   - 수학-정신모델-AI 삼각 검증

2. **물리학 분야 확장 (Phase 3)**
   - 양자역학, 카오스 이론 역분해
   - 4개 영역 통합 분석 시스템

3. **새로운 발견 및 연구 (Phase 4)**
   - 동서양 지혜 체계 연결의 새로운 패러다임
   - 누락 요소 예측 및 검증
   - 학술적 발표 및 공개

### 기술적 구현 우선순위

#### 높은 가치 + 낮은 복잡도
1. **MongoDB 연동 API** (1-2일)
2. **기본 통합 인터페이스** (3-5일)
3. **상호 매핑 시각화** (3-5일)

#### 중간 가치 + 중간 복잡도
1. **대화형 대시보드** (1-2주)
2. **상황별 추천 시스템** (1-2주)
3. **성능 최적화** (1-2주)

#### 높은 가치 + 높은 복잡도
1. **AI 분야 확장** (2-3개월)
2. **물리학 분야 확장** (2-3개월)
3. **새로운 발견 연구** (3-6개월)

---

**마지막 업데이트**: 2025-06-17
**데이터 검증**: mathematical_trigrams 9개 + hexagrams 64개 모두 확인 완료
**준비 상태**: 즉시 개발 가능 + 배포 준비 완료