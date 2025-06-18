from flask import Flask, render_template, jsonify, request
from bagua_generator import BaguaSystem, MathModel
from web_routes.verification_routes import register_verification_routes
import json

app = Flask(__name__)
system = BaguaSystem()

# 검증 라우트 등록
register_verification_routes(app)

@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/api/models')
def get_models():
    """사용 가능한 모델 목록"""
    return jsonify({
        'models': [
            {
                'id': 'abstract',
                'name': '추상적 모델',
                'description': '자연수, 집합, 함수, 관계, 측도, 구조, 극한, 연산'
            },
            {
                'id': 'concrete', 
                'name': '구체적 모델',
                'description': 'π, 이진법, φ, 확률, 미분, 적분, 소수, 대칭성'
            }
        ]
    })

@app.route('/api/trigrams/<model_type>')
def get_trigrams(model_type):
    """8괘 데이터 반환"""
    model = MathModel.ABSTRACT if model_type == 'abstract' else MathModel.CONCRETE
    trigrams = system.get_trigrams(model)
    
    result = []
    for name, trigram in trigrams.items():
        result.append({
            'name': name,
            'symbol': trigram.symbol,
            'korean': trigram.korean,
            'description': trigram.description,
            'concept': trigram.concept
        })
    
    return jsonify({'trigrams': result})

@app.route('/api/hexagrams/<model_type>')
def get_hexagrams(model_type):
    """64괘 데이터 반환"""
    model = MathModel.ABSTRACT if model_type == 'abstract' else MathModel.CONCRETE
    hexagrams = system.generate_hexagrams(model)
    
    result = []
    for hex in hexagrams:
        result.append({
            'number': hex.number,
            'name': hex.name,
            'upper': {
                'name': hex.upper.name,
                'symbol': hex.upper.symbol,
                'description': hex.upper.description
            },
            'lower': {
                'name': hex.lower.name,
                'symbol': hex.lower.symbol,
                'description': hex.lower.description
            },
            'mathematical_meaning': hex.mathematical_meaning,
            'description': hex.description,
            'examples': hex.examples
        })
    
    return jsonify({'hexagrams': result})

@app.route('/api/analysis/<model_type>')
def get_analysis(model_type):
    """모델 분석 데이터 반환"""
    model = MathModel.ABSTRACT if model_type == 'abstract' else MathModel.CONCRETE
    analysis = system.analyze_completeness(model)
    
    return jsonify(analysis)

@app.route('/api/duality/<model_type>')
def get_duality_pairs(model_type):
    """대대 관계 반환"""
    model = MathModel.ABSTRACT if model_type == 'abstract' else MathModel.CONCRETE
    pairs = system.get_duality_pairs(model)
    trigrams = system.get_trigrams(model)
    
    result = []
    for pair in pairs:
        t1, t2 = trigrams[pair[0]], trigrams[pair[1]]
        result.append({
            'pair1': {
                'name': pair[0],
                'symbol': t1.symbol,
                'description': t1.description
            },
            'pair2': {
                'name': pair[1], 
                'symbol': t2.symbol,
                'description': t2.description
            }
        })
    
    return jsonify({'duality_pairs': result})

@app.route('/api/search/<model_type>')
def search_hexagrams(model_type):
    """64괘 검색"""
    query = request.args.get('q', '').lower()
    model = MathModel.ABSTRACT if model_type == 'abstract' else MathModel.CONCRETE
    hexagrams = system.generate_hexagrams(model)
    
    if not query:
        return jsonify({'hexagrams': []})
    
    filtered = []
    for hex in hexagrams:
        if (query in hex.mathematical_meaning.lower() or 
            query in hex.name.lower() or
            query in hex.upper.description.lower() or
            query in hex.lower.description.lower()):
            filtered.append({
                'number': hex.number,
                'name': hex.name,
                'upper': hex.upper.name,
                'lower': hex.lower.name,
                'mathematical_meaning': hex.mathematical_meaning
            })
    
    return jsonify({'hexagrams': filtered[:20]})  # 최대 20개

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    
