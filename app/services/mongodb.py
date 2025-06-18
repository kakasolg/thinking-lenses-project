from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain_core.runnables import RunnableLambda
from pymongo import MongoClient
from typing import Dict, Optional
import re
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HexagramMongoDB:
    """64괘 MongoDB 연동 클래스"""
    
    def __init__(self, connection_string="mongodb://localhost:27017"):
        self.connection_string = connection_string
        self.client = None
        self.db = None
        self.collection = None
        self._connect()
    
    def _connect(self):
        """MongoDB 연결"""
        try:
            self.client = MongoClient(self.connection_string)
            self.client.admin.command('ping')
            self.db = self.client['wisdom_lenses']
            self.collection = self.db['hexagrams']
            logger.info("MongoDB 연결 성공")
        except Exception as e:
            logger.error(f"MongoDB 연결 실패: {e}")
    
    def get_hexagram_by_number(self, number: int) -> Optional[Dict]:
        """번호로 괘 조회"""
        try:
            if self.collection is None:
                return None
            result = self.collection.find_one({"number": number})
            logger.info(f"MongoDB: get_hexagram_by_number({number}) - result: {result}")
            return result
        except Exception as e:
            logger.error(f"MongoDB: 괘 번호 {number} 조회 실패: {e}")
            return None
    
    def get_hexagram_by_name(self, name: str) -> Optional[Dict]:
        """이름으로 괘 조회"""
        try:
            if self.collection is None:
                return None
            result = self.collection.find_one({
                "name": {"$regex": name, "$options": "i"}
            })
            logger.info(f"MongoDB: get_hexagram_by_name('{name}') - result: {result}")
            return result
        except Exception as e:
            logger.error(f"MongoDB: 괘 이름 '{name}' 조회 실패: {e}")
            return None
    
    def search_hexagrams_by_keyword(self, keyword: str) -> list:
        """키워드로 괘 검색"""
        try:
            if self.collection is None:
                return []
            results = list(self.collection.find({
                "$or": [
                    {"name": {"$regex": keyword, "$options": "i"}},
                    {"coreViewpoint": {"$regex": keyword, "$options": "i"}},
                    {"summary": {"$regex": keyword, "$options": "i"}},
                    {"mentalModels": {"$regex": keyword, "$options": "i"}},
                    {"keywords": {"$regex": keyword, "$options": "i"}}
                ]
            }).limit(5))
            logger.info(f"MongoDB: search_hexagrams_by_keyword('{keyword}') - found {len(results)} items.")
            return results
        except Exception as e:
            logger.error(f"MongoDB: 키워드 '{keyword}' 검색 실패: {e}")
            return []

# MongoDB 인스턴스 생성
hexagram_db = HexagramMongoDB()

def parse_hexagram_query(query: str) -> Dict:
    """사용자 질문을 파싱하여 괘 정보 추출"""
    query = query.strip()
    
    # 번호 패턴 (예: "1번괘", "1번", "괘1번", "첫번째괘")
    number_patterns = [
        r'(\d+)번째?\s*괘?',
        r'괘?\s*(\d+)번?',
        r'^(\d+)$'
    ]
    
    for pattern in number_patterns:
        match = re.search(pattern, query)
        if match:
            number = int(match.group(1))
            if 1 <= number <= 64:
                logger.info(f"Parser: Attempting to get hexagram by number: {number}")
                hexagram = hexagram_db.get_hexagram_by_number(number)
                if hexagram:
                    return {
                        "type": "hexagram_found",
                        "query": query,
                        "hexagram": hexagram
                    }
    
    # 이름 패턴 (예: "건괘", "중천건")
    name_patterns = [
        r'([가-힣]+)괘?',
        r'괘?\s*([가-힣]+)'
    ]
    
    for pattern in name_patterns:
        match = re.search(pattern, query)
        if match:
            name = match.group(1)
            logger.info(f"Parser: Attempting to get hexagram by name: {name}")
            hexagram = hexagram_db.get_hexagram_by_name(name)
            if hexagram:
                return {
                    "type": "hexagram_found",
                    "query": query,
                    "hexagram": hexagram
                }
    
    # 키워드 검색
    logger.info(f"Parser: Attempting to search by keyword: {query}")
    hexagrams = hexagram_db.search_hexagrams_by_keyword(query)
    if hexagrams:
        result_data = {
            "type": "keyword_search",
            "query": query,
            "hexagrams": hexagrams
        }
        logger.info(f"Parser: Keyword search successful. Result: {result_data}")
        return result_data
    
    # 일반 질문
    result_data = {
            "type": "general_question",
            "query": query,
            "hexagram": None
        }
    logger.info(f"Parser: No specific hexagram found, treating as general question. Result: {result_data}")
    return result_data

def format_hexagram_context(result: Dict) -> str:
    """괘 정보를 컨텍스트로 포맷팅"""
    logger.info(f"Formatter: Received result for formatting: {result}")
    if result["type"] == "hexagram_found":
        hexagram = result["hexagram"]
        context = f"""
64괘 정보:
- 괘 번호: {hexagram.get('number', 'N/A')}
- 괘 이름: {hexagram.get('name', 'N/A')}
- 괘 심볼: {hexagram.get('symbol', 'N/A')}
- 핵심 관점: {hexagram.get('coreViewpoint', 'N/A')}
- 요약: {hexagram.get('summary', 'N/A')}
- 멘탈 모델: {hexagram.get('mentalModels', 'N/A')}
- 키워드: {', '.join(hexagram.get('keywords', []))}
"""
        logger.info(f"Formatter: Formatted context for hexagram_found: {context[:200]}...") # 로그 길이를 줄이기 위해 일부만 출력
        return context
    
    elif result["type"] == "keyword_search":
        hexagrams = result["hexagrams"]
        context = f"검색된 {len(hexagrams)}개의 괘:\n"
        for i, hexagram in enumerate(hexagrams[:3], 1):  # 최대 3개만
            context += f"""
{i}. {hexagram.get('number')}번 {hexagram.get('name')}
   - 핵심 관점: {hexagram.get('coreViewpoint', 'N/A')}
   - 요약: {hexagram.get('summary', 'N/A')[:100]}...
"""
        logger.info(f"Formatter: Formatted context for keyword_search: {context[:200]}...")
        return context
    
    else:
        context = "64괘 관련 질문이 아닌 것 같습니다."
        logger.info(f"Formatter: Context for general_question: {context}")
        return context

# LangChain 체인 구성
def hexagram_chain_function(inputs: Dict) -> str:
    """MongoDB에서 괘 정보를 조회하고 컨텍스트 생성"""
    question = inputs["question"]
    result = parse_hexagram_query(question)
    logger.info(f"Chain_fn: parse_hexagram_query returned: {result}")
    context = format_hexagram_context(result)
    
    return {
        "question": question,
        "context": context,
        "result_type": result["type"]
    }

# 프롬프트 템플릿 정의
hexagram_template = """당신은 64괘(주역) 전문가입니다. 사용자의 질문에 대해 제공된 괘 정보를 바탕으로 답변해주세요.
**답변은 핵심 내용을 중심으로 간결하게 요약해야 합니다.**

괘 정보:
{context}

사용자 질문: {question}

다음 사항들을 포함하여 간결하게 요약 답변해주세요:
- 괘의 핵심 의미와 상징
- 현실적인 적용 방법
- 멘탈 모델과의 연관성
- 실무적 조언

간결한 답변:"""

general_template = """Question: {question}

Context: {context}

Answer: Let's think step by step."""

# 모델 및 프롬프트 설정
model = OllamaLLM(model="exaone3.5:7.8b", temperature=0.5, max_tokens=500)

hexagram_prompt = ChatPromptTemplate.from_template(hexagram_template)
general_prompt = ChatPromptTemplate.from_template(general_template)

# 조건부 체인 함수
def create_response_chain(inputs: Dict) -> str:
    """결과 타입에 따라 적절한 프롬프트 선택"""
    if inputs["result_type"] in ["hexagram_found", "keyword_search"]:
        chain = hexagram_prompt | model
    else:
        chain = general_prompt | model
    
    # .invoke() 대신 .stream()을 사용하여 응답을 스트리밍합니다.
    return chain.stream({
        "question": inputs["question"],
        "context": inputs["context"]
    })

# 최종 체인 구성
hexagram_chain = (
    RunnableLambda(hexagram_chain_function) | 
    RunnableLambda(create_response_chain)
)

# 사용 예시 함수들
def ask_hexagram(question: str): # 스트리밍을 위해 반환 타입 어노테이션 제거 또는 Iterator[str] 등으로 변경 가능
    """괘 관련 질문하기"""
    try:
        # hexagram_chain.invoke가 이제 스트림(iterator)을 반환합니다.
        response_stream = hexagram_chain.invoke({"question": question})
        for chunk in response_stream:
            yield chunk # 각 응답 조각을 yield 합니다.
    except Exception as e:
        logger.error(f"질문 처리 실패: {e}")
        yield f"죄송합니다. 질문을 처리하는 중 오류가 발생했습니다: {e}"

def interactive_hexagram_chat():
    """대화형 괘 상담"""
    print("=== 64괘 AI 상담사 ===")
    print("사용 예시:")
    print("- '1번괘' 또는 '1번' -> 특정 괘 조회")
    print("- '건괘' 또는 '중천건' -> 이름으로 괘 조회") 
    print("- '리더십' 또는 '창조' -> 키워드로 괘 검색")
    print("- '종료' 또는 'quit' -> 프로그램 종료")
    print("-" * 50)
    
    while True:
        try:
            question = input("\n질문을 입력하세요: ").strip()
            
            if question.lower() in ['종료', 'quit', 'exit', '']:
                print("64괘 상담을 종료합니다.")
                break
            
            print("\n🔮 괘를 해석하고 있습니다...")
            print(f"\n📖 답변:")
            for chunk in ask_hexagram(question):
                print(chunk, end="", flush=True) # 스트리밍된 각 조각을 즉시 출력
            print() # 모든 조각 출력 후 줄바꿈
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\n\n프로그램을 종료합니다.")
            break
        except Exception as e:
            print(f"\n오류가 발생했습니다: {e}")

# 테스트 실행
if __name__ == "__main__":
    # 단일 질문 테스트
    print("=== 단일 질문 테스트 ===")
    test_questions = [
        "1번괘",
        "중천건",
        "리더십",
        "창조적 사고가 필요한 상황에서 어떻게 해야 할까?"
    ]
    
    for question in test_questions:
        print(f"\n질문: {question}")
        print(f"답변: ", end="")
        for chunk in ask_hexagram(question):
            print(chunk, end="", flush=True) # 스트리밍된 각 조각을 즉시 출력
        print() # 모든 조각 출력 후 줄바꿈
        print("-" * 30)
    
    # 대화형 모드 시작 (주석 해제하여 사용)
    # interactive_hexagram_chat()