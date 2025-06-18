from flask import Blueprint, jsonify, render_template
from ..services.math_core import (
    PiVerification, PhiVerification, ProbabilityVerification,
    CalculusVerification, BinaryVerification, PrimesVerification,
    SymmetryVerification, EVerification
)

math_bp = Blueprint('math', __name__, url_prefix='/math')

# Instantiate verifiers
pi_verifier = PiVerification()
phi_verifier = PhiVerification()
probability_verifier = ProbabilityVerification()
calculus_verifier = CalculusVerification()
binary_verifier = BinaryVerification()
primes_verifier = PrimesVerification()
symmetry_verifier = SymmetryVerification()
e_verifier = EVerification()

@math_bp.route('/api/verification/pi')
def verify_pi_route():
    try:
        result, plots = pi_verifier.verify_pi_with_visualization()
        return jsonify({
            'success': True, 'concept': 'π (건☰)', 'result': result,
            'plots': plots, 'description': '원주율 π의 다양한 계산 방법과 몬테카를로 시뮬레이션'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'concept': 'π (건☰)'})

@math_bp.route('/api/verification/golden-ratio')
def verify_golden_ratio_route():
    try:
        result, plots = phi_verifier.verify_golden_ratio_with_visualization()
        return jsonify({
            'success': True, 'concept': 'φ (리☲)', 'result': result,
            'plots': plots, 'description': '황금비 φ와 피보나치 수열, 황금 사각형 및 나선 구조'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'concept': 'φ (리☲)'})

@math_bp.route('/api/verification/probability')
def verify_probability_route():
    try:
        result, plots = probability_verifier.verify_probability_with_visualization()
        return jsonify({
            'success': True, 'concept': '확률론 (감☵)', 'result': result,
            'plots': plots, 'description': '중심극한정리 및 베이즈 정리 시각화'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'concept': '확률론 (감☵)'})

@math_bp.route('/api/verification/calculus')
def verify_calculus_route():
    try:
        result, plots = calculus_verifier.verify_calculus_with_visualization()
        return jsonify({
            'success': True, 'concept': '미적분학 (진☳손☴)', 'result': result,
            'plots': plots, 'description': '미분과 적분의 기본 원리 및 수치적 검증'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'concept': '미적분학 (진☳손☴)'})

@math_bp.route('/api/verification/binary')
def verify_binary_route():
    try:
        result, plots = binary_verifier.verify_binary_with_visualization()
        return jsonify({
            'success': True, 'concept': '이진법 (곤☷)', 'result': result,
            'plots': plots, 'description': '이진수 표현, 논리 게이트 및 이항 분포'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'concept': '이진법 (곤☷)'})

@math_bp.route('/api/verification/primes')
def verify_primes_route():
    try:
        result, plots = primes_verifier.verify_primes_with_visualization()
        return jsonify({
            'success': True, 'concept': '소수 (간☶)', 'result': result,
            'plots': plots, 'description': '에라토스테네스의 체, 소수 정리 및 메르센 소수'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'concept': '소수 (간☶)'})

@math_bp.route('/api/verification/symmetry')
def verify_symmetry_route():
    try:
        result, plots = symmetry_verifier.verify_symmetry_with_visualization()
        return jsonify({
            'success': True, 'concept': '대칭성 (태☱)', 'result': result,
            'plots': plots, 'description': '기하학적 대칭 변환 및 군론적 대칭성 소개'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'concept': '대칭성 (태☱)'})

@math_bp.route('/api/verification/e')
def verify_e_route():
    try:
        result, plots = e_verifier.verify_e_with_visualization()
        return jsonify({
            'success': True, 'concept': '자연상수 e', 'result': result,
            'plots': plots, 'description': '자연상수 e의 다양한 정의와 지수함수, 복리 계산'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'concept': '자연상수 e'})

@math_bp.route('/api/verification/dashboard')
def verification_dashboard_route():
    # This route would typically fetch summary data or status.
    # For now, let's return a simple status message.
    # In a real app, this might interact with the verifier instances
    # if they stored aggregated results or status.
    core_concepts = [
        {'id': 'pi', 'name': 'π (건☰)', 'description': '원주율과 몬테카를로'},
        {'id': 'golden-ratio', 'name': 'φ (리☲)', 'description': '황금비와 피보나치'},
        {'id': 'probability', 'name': '확률론 (감☵)', 'description': '중심극한정리와 베이즈 정리'},
        {'id': 'calculus', 'name': '미적분학 (진☳손☴)', 'description': '미분과 적분'},
        {'id': 'binary', 'name': '이진법 (곤☷)', 'description': '이진수와 논리 게이트'},
        {'id': 'primes', 'name': '소수 (간☶)', 'description': '소수의 세계'},
        {'id': 'symmetry', 'name': '대칭성 (태☱)', 'description': '기하학적 대칭과 군론'},
        {'id': 'e', 'name': '자연상수 e', 'description': '자연상수 e와 성장'}
    ]
    return jsonify({'success': True, 'core_concepts': core_concepts})

@math_bp.route('/api/verification/all')
def verify_all_route():
    all_results = []
    errors = []

    verifiers_map = {
        'π (건☰)': pi_verifier.verify_pi_with_visualization,
        'φ (리☲)': phi_verifier.verify_golden_ratio_with_visualization,
        '확률론 (감☵)': probability_verifier.verify_probability_with_visualization,
        '미적분학 (진☳손☴)': calculus_verifier.verify_calculus_with_visualization,
        '이진법 (곤☷)': binary_verifier.verify_binary_with_visualization,
        '소수 (간☶)': primes_verifier.verify_primes_with_visualization,
        '대칭성 (태☱)': symmetry_verifier.verify_symmetry_with_visualization,
        '자연상수 e': e_verifier.verify_e_with_visualization
    }

    for concept, verifier_func in verifiers_map.items():
        try:
            result, plots = verifier_func()
            all_results.append({
                'concept': concept,
                'result': result,
                # Plots might be too large for 'all' summary, consider omitting or simplifying
                # 'plots': plots
            })
        except Exception as e:
            errors.append({'concept': concept, 'error': str(e)})

    if errors:
        return jsonify({'success': False, 'results': all_results, 'errors': errors})
    return jsonify({'success': True, 'results': all_results})

@math_bp.route('/page/verification')
def verification_page_route():
    return render_template('verification.html')
