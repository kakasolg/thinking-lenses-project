"""
주역 8괘 수학적 검증 시스템 - 웹 시각화 버전 (리팩토링된 버전)
기존 코드와의 호환성을 위한 래퍼 클래스
"""

from math_core import (
    PiVerification, PhiVerification, ProbabilityVerification, 
    CalculusVerification, BinaryVerification, PrimesVerification,
    SymmetryVerification, EVerification
)

class MathematicalVerificationWeb:
    """8괘 수학적 검증 및 시각화 클래스 (리팩토링된 버전)"""
    
    def __init__(self):
        # 개별 검증 클래스들 초기화
        self.pi_verifier = PiVerification()
        self.phi_verifier = PhiVerification()
        self.probability_verifier = ProbabilityVerification()
        self.calculus_verifier = CalculusVerification()
        self.binary_verifier = BinaryVerification()
        self.primes_verifier = PrimesVerification()
        self.symmetry_verifier = SymmetryVerification()
        self.e_verifier = EVerification()
        
        # 결과 저장용
        self.results = {}
        self.plots = {}
    
    def verify_pi_with_visualization(self, precision=1000):
        """건(☰): 원주율 π 검증 및 시각화"""
        result, plots = self.pi_verifier.verify_pi_with_visualization()
        self.results['pi'] = result
        self.plots['pi'] = plots
        return result, plots
    
    def verify_golden_ratio_with_visualization(self):
        """리(☲): 황금비 φ 검증 및 시각화"""
        result, plots = self.phi_verifier.verify_golden_ratio_with_visualization()
        self.results['golden_ratio'] = result
        self.plots['golden_ratio'] = plots
        return result, plots
    
    def verify_probability_with_visualization(self):
        """감(☵): 확률 검증 및 시각화"""
        result, plots = self.probability_verifier.verify_probability_with_visualization()
        self.results['probability'] = result
        self.plots['probability'] = plots
        return result, plots
    
    def verify_calculus_with_visualization(self):
        """진손(☳☴): 미분/적분 검증 및 시각화"""
        result, plots = self.calculus_verifier.verify_calculus_with_visualization()
        self.results['calculus'] = result
        self.plots['calculus'] = plots
        return result, plots
    
    def verify_binary_with_visualization(self):
        """곤(☷): 이진법 검증 및 시각화"""
        result, plots = self.binary_verifier.verify_binary_with_visualization()
        self.results['binary'] = result
        self.plots['binary'] = plots
        return result, plots
    
    def verify_primes_with_visualization(self):
        """간(☶): 소수 검증 및 시각화"""
        result, plots = self.primes_verifier.verify_primes_with_visualization()
        self.results['primes'] = result
        self.plots['primes'] = plots
        return result, plots
    
    def verify_symmetry_with_visualization(self):
        """태(☱): 대칭성 검증 및 시각화"""
        result, plots = self.symmetry_verifier.verify_symmetry_with_visualization()
        self.results['symmetry'] = result
        self.plots['symmetry'] = plots
        return result, plots
    
    def verify_e_with_visualization(self):
        """자연상수 e 검증 및 시각화"""
        result, plots = self.e_verifier.verify_e_with_visualization()
        self.results['e'] = result
        self.plots['e'] = plots
        return result, plots
    
    def create_summary_dashboard(self):
        """전체 검증 결과 요약 대시보드"""
        summary_data = {
            'total_verifications': len(self.results),
            'completed_concepts': list(self.results.keys()),
            'total_plots': sum(len(plots) for plots in self.plots.values()),
            'success_rate': '100%' if self.results else '0%'
        }
        
        # 간단한 대시보드 플롯 (향후 구현)
        dashboard_plot = "dashboard_placeholder"
        
        return summary_data, dashboard_plot
    
    def run_all_verifications(self):
        """전체 수학적 검증 실행"""
        print("🚀 전체 8괘 수학적 검증 시작")
        print("=" * 60)
        
        # 모든 검증 실행
        verifications = [
            ('π (건☰)', self.verify_pi_with_visualization),
            ('φ (리☲)', self.verify_golden_ratio_with_visualization),
            ('확률 (감☵)', self.verify_probability_with_visualization),
            ('미적분 (진손☳☴)', self.verify_calculus_with_visualization),
            ('이진법 (곤☷)', self.verify_binary_with_visualization),
            ('소수 (간☶)', self.verify_primes_with_visualization),
            ('대칭성 (태☱)', self.verify_symmetry_with_visualization),
            ('자연상수 e', self.verify_e_with_visualization),
        ]
        
        for name, verify_func in verifications:
            try:
                print(f"\n🔄 {name} 검증 중...")
                verify_func()
                print(f"✅ {name} 검증 완료")
            except Exception as e:
                print(f"❌ {name} 검증 실패: {e}")
        
        # 요약 정보
        summary_data = {
            'total_concepts': len(verifications),
            'completed_concepts': len(self.results),
            'success_rate': len(self.results) / len(verifications) * 100,
            'total_plots': sum(len(plots) for plots in self.plots.values())
        }
        
        print("\n" + "🔵" * 20)
        print("📊 전체 검증 완료!")
        print(f"   완료된 개념: {summary_data['completed_concepts']}/{summary_data['total_concepts']}")
        print(f"   성공률: {summary_data['success_rate']:.1f}%")
        print(f"   생성된 그래프: {summary_data['total_plots']}개")
        print("🔵" * 20)
        
        return {
            'results': self.results,
            'plots': self.plots,
            'summary': summary_data
        }

# 웹용 인스턴스 생성 함수
def create_verification_instance():
    """웹에서 사용할 검증 인스턴스 생성"""
    return MathematicalVerificationWeb()

# 실행 예시
if __name__ == "__main__":
    verifier = MathematicalVerificationWeb()
    
    # 개별 검증 테스트
    print("🧪 개별 검증 테스트")
    pi_result, pi_plots = verifier.verify_pi_with_visualization()
    print(f"π 검증 완료: {len(pi_plots)}개 그래프 생성")
    
    # 전체 검증 테스트
    print("\n🧪 전체 검증 테스트")
    all_results = verifier.run_all_verifications()
    print(f"전체 검증 완료: {all_results['summary']['total_plots']}개 그래프 생성")
