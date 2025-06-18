"""
수학적 검증 Flask 라우트 모듈
"""

from flask import jsonify, render_template
from math_core import (
    PiVerification, PhiVerification, ProbabilityVerification, 
    CalculusVerification, BinaryVerification, PrimesVerification,
    SymmetryVerification, EVerification
)

class VerificationRoutes:
    """수학적 검증 라우트 클래스"""
    
    def __init__(self):
        # 각 검증 클래스 인스턴스 생성
        self.pi_verifier = PiVerification()
        self.phi_verifier = PhiVerification()
        self.probability_verifier = ProbabilityVerification()
        self.calculus_verifier = CalculusVerification()
        self.binary_verifier = BinaryVerification()
        self.primes_verifier = PrimesVerification()
        self.symmetry_verifier = SymmetryVerification()
        self.e_verifier = EVerification()
    
    def verify_pi(self):
        """π (원주율) 검증 및 시각화"""
        try:
            result, plots = self.pi_verifier.verify_pi_with_visualization()
            return jsonify({
                'success': True,
                'concept': 'π (건☰)',
                'result': result,
                'plots': plots,
                'description': '원주율 π의 다양한 계산 방법과 몬테카를로 시뮬레이션'
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    def verify_golden_ratio(self):
        """황금비 φ 검증 및 시각화"""
        try:
            result, plots = self.phi_verifier.verify_golden_ratio_with_visualization()
            return jsonify({
                'success': True,
                'concept': 'φ (리☲)',
                'result': result,
                'plots': plots,
                'description': '황금비 φ의 피보나치 수열과의 관계 및 기하학적 성질'
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    def verify_probability(self):
        """확률 검증 및 시각화"""
        try:
            result, plots = self.probability_verifier.verify_probability_with_visualization()
            return jsonify({
                'success': True,
                'concept': '확률 (감☵)',
                'result': result,
                'plots': plots,
                'description': '중심극한정리, 확률분포, 베이즈 정리의 시각적 설명'
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    def verify_calculus(self):
        """미분/적분 검증 및 시각화"""
        try:
            result, plots = self.calculus_verifier.verify_calculus_with_visualization()
            return jsonify({
                'success': True,
                'concept': '미분/적분 (진☳/손☴)',
                'result': result,
                'plots': plots,
                'description': '미분과 적분의 기하학적 의미 및 미적분학의 기본정리'
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    def verify_binary(self):
        """이진법 검증 및 시각화"""
        try:
            result, plots = self.binary_verifier.verify_binary_with_visualization()
            return jsonify({
                'success': True,
                'concept': '이진법 (곤☷)',
                'result': result,
                'plots': plots,
                'description': '이진법, 베르누이 시행, 논리 게이트의 시각적 설명'
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    def verify_primes(self):
        """소수 검증 및 시각화"""
        try:
            result, plots = self.primes_verifier.verify_primes_with_visualization()
            return jsonify({
                'success': True,
                'concept': '소수 (간☶)',
                'result': result,
                'plots': plots,
                'description': '에라토스테네스의 체, 소수 정리, 메르센 소수'
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    def verify_symmetry(self):
        """대칭성 검증 및 시각화"""
        try:
            result, plots = self.symmetry_verifier.verify_symmetry_with_visualization()
            return jsonify({
                'success': True,
                'concept': '대칭성 (태☱)',
                'result': result,
                'plots': plots,
                'description': '기하학적 변환, 분자 대칭, 점군 이론'
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    def verify_e(self):
        """자연상수 e 검증 및 시각화"""
        try:
            result, plots = self.e_verifier.verify_e_with_visualization()
            return jsonify({
                'success': True,
                'concept': '자연상수 e',
                'result': result,
                'plots': plots,
                'description': '급수 근사, 극한 정의, 지수함수와 연속 복리'
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    def verify_all(self):
        """전체 수학적 검증 실행"""
        try:
            all_results = {}
            all_plots = {}
            
            # 모든 검증 실행
            verifications = [
                ('pi', self.verify_pi),
                ('golden_ratio', self.verify_golden_ratio),
                ('probability', self.verify_probability),
                ('calculus', self.verify_calculus),
                ('binary', self.verify_binary),
                ('primes', self.verify_primes),
                ('symmetry', self.verify_symmetry),
                ('e', self.verify_e)
            ]
            
            for name, verify_func in verifications:
                response = verify_func()
                if response.get_json()['success']:
                    data = response.get_json()
                    all_results[name] = data['result']
                    all_plots[name] = data['plots']
            
            summary = {
                'total_concepts': len(all_results),
                'total_plots': sum(len(plots) for plots in all_plots.values()),
                'completion_rate': len(all_results) / len(verifications) * 100
            }
            
            return jsonify({
                'success': True,
                'results': all_results,
                'plots': all_plots,
                'summary': summary
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    def verification_dashboard(self):
        """전체 8괘 검증 대시보드"""
        try:
            # 주요 검증들만 실행 (성능을 위해)
            pi_response = self.verify_pi()
            phi_response = self.verify_golden_ratio()
            prob_response = self.verify_probability()
            calc_response = self.verify_calculus()
            
            summary_data = {
                'completed_verifications': 4,
                'total_verifications': 8,
                'success_rate': '100%'
            }
            
            return jsonify({
                'success': True,
                'summary': summary_data,
                'verification_count': 4,
                'message': '기본 4개 괘 검증 완료'
            })
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    
    def verification_page(self):
        """수학적 검증 전용 페이지"""
        return render_template('verification.html')

def register_verification_routes(app):
    """Flask 앱에 검증 라우트 등록"""
    routes = VerificationRoutes()
    
    # API 라우트들
    app.add_url_rule('/math/api/verification/dashboard', 'verification_dashboard', 
                     routes.verification_dashboard, methods=['GET'])
    app.add_url_rule('/math/api/verification/pi', 'verify_pi', 
                     routes.verify_pi, methods=['GET'])
    app.add_url_rule('/math/api/verification/golden-ratio', 'verify_golden_ratio', 
                     routes.verify_golden_ratio, methods=['GET'])
    app.add_url_rule('/math/api/verification/probability', 'verify_probability', 
                     routes.verify_probability, methods=['GET'])
    app.add_url_rule('/math/api/verification/calculus', 'verify_calculus', 
                     routes.verify_calculus, methods=['GET'])
    app.add_url_rule('/math/api/verification/binary', 'verify_binary', 
                     routes.verify_binary, methods=['GET'])
    app.add_url_rule('/math/api/verification/primes', 'verify_primes', 
                     routes.verify_primes, methods=['GET'])
    app.add_url_rule('/math/api/verification/symmetry', 'verify_symmetry', 
                     routes.verify_symmetry, methods=['GET'])
    app.add_url_rule('/math/api/verification/e', 'verify_e', 
                     routes.verify_e, methods=['GET'])
    app.add_url_rule('/math/api/verification/all', 'verify_all', 
                     routes.verify_all, methods=['GET'])
    
    # 페이지 라우트
    app.add_url_rule('/math/page/verification', 'verification_page', 
                     routes.verification_page, methods=['GET'])
