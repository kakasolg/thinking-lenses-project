from flask import Blueprint, jsonify, request
from ..services.bagua_generator import BaguaSystem, MathModel

bagua_bp = Blueprint('bagua', __name__, url_prefix='/bagua')

system = BaguaSystem()

@bagua_bp.route('/api/models', methods=['GET'])
def get_models_bagua():
    models = [model.value for model in MathModel]
    return jsonify(models)

@bagua_bp.route('/api/trigrams/<model_type>', methods=['GET'])
def get_trigrams_bagua(model_type):
    try:
        model = MathModel(model_type)
        trigrams = system.get_trigrams(model)
        return jsonify(trigrams)
    except ValueError:
        return jsonify({"error": "Invalid model type"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bagua_bp.route('/api/hexagrams/<model_type>', methods=['GET'])
def get_hexagrams_bagua(model_type):
    try:
        model = MathModel(model_type)
        count = request.args.get('count', default=64, type=int)
        hexagrams = system.get_hexagrams(model, count)
        return jsonify(hexagrams)
    except ValueError:
        return jsonify({"error": "Invalid model type"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bagua_bp.route('/api/analysis/<model_type>', methods=['GET'])
def get_analysis_bagua(model_type):
    try:
        model = MathModel(model_type)
        analysis = system.get_analysis(model)
        return jsonify(analysis)
    except ValueError:
        return jsonify({"error": "Invalid model type"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bagua_bp.route('/api/duality/<model_type>', methods=['GET'])
def get_duality_bagua(model_type):
    try:
        model = MathModel(model_type)
        duality = system.get_duality_analysis(model)
        return jsonify(duality)
    except ValueError:
        return jsonify({"error": "Invalid model type"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bagua_bp.route('/api/search/<model_type>', methods=['GET'])
def search_bagua(model_type):
    try:
        model = MathModel(model_type)
        query = request.args.get('query', default='', type=str)
        results = system.search(model, query)
        return jsonify(results)
    except ValueError:
        return jsonify({"error": "Invalid model type"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
