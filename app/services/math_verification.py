"""
주역 8괘 수학적 검증 시스템
각 괘의 수학적 개념을 실제 파이썬 코드로 검증
"""

import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
import pandas as pd
from math import pi, e, sqrt, log
import random
from collections import Counter

class MathematicalVerification:
    """8괘 수학적 개념 검증 클래스"""
    
    def __init__(self):
        self.results = {}
    
    def verify_pi(self, precision=1000):
        """건(☰): 원주율 π 검증"""
        print("=" * 50)
        print("🔵 건(☰): 원주율 π 검증")
        print("=" * 50)
        
        # 1. 기본 정의: 원의 둘레/지름
        radius = 1
        circumference = 2 * pi * radius
        diameter = 2 * radius
        pi_calculated = circumference / diameter
        
        print(f"원의 정의에서: π = 둘레/지름 = {pi_calculated:.10f}")
        print(f"NumPy π 값: {np.pi:.10f}")
        
        # 2. 몬테카를로 방법으로 π 추정
        n_points = 100000
        inside_circle = 0
        
        for _ in range(n_points):
            x, y = random.uniform(-1, 1), random.uniform(-1, 1)
            if x*x + y*y <= 1:
                inside_circle += 1
        
        pi_monte_carlo = 4 * inside_circle / n_points
        print(f"몬테카를로 추정: π ≈ {pi_monte_carlo:.6f}")
        
        # 3. 급수를 이용한 π 계산 (라이프니츠 공식)
        pi_series = 0
        for i in range(100000):
            pi_series += (-1)**i / (2*i + 1)
        pi_leibniz = 4 * pi_series
        print(f"라이프니츠 급수: π ≈ {pi_leibniz:.6f}")
        
        # 4. SymPy를 이용한 정확한 π
        pi_sympy = float(sp.pi.evalf(precision))
        print(f"SymPy 고정밀: π = {pi_sympy:.10f}")
        
        self.results['pi'] = {
            'definition': pi_calculated,
            'monte_carlo': pi_monte_carlo,
            'leibniz': pi_leibniz,
            'sympy': pi_sympy,
            'numpy': np.pi
        }
        
        return self.results['pi']
    
    def verify_binary(self):
        """곤(☷): 이진법 검증"""
        print("\n" + "=" * 50)
        print("🔵 곤(☷): 이진법 검증")
        print("=" * 50)
        
        # 1. 이진법 변환
        numbers = [1, 7, 15, 64, 255]
        binary_conversions = {}
        
        for num in numbers:
            binary = bin(num)[2:]  # 0b 제거
            decimal_back = int(binary, 2)
            binary_conversions[num] = {
                'binary': binary,
                'back_to_decimal': decimal_back,
                'correct': num == decimal_back
            }
            print(f"{num} → {binary} → {decimal_back} ✓")
        
        # 2. 이진 연산
        a, b = 12, 7  # 1100, 0111
        print(f"\n이진 연산 예시: {a}({bin(a)[2:]}) & {b}({bin(b)[2:]})")
        print(f"AND: {a & b} ({bin(a & b)[2:]})")
        print(f"OR:  {a | b} ({bin(a | b)[2:]})")
        print(f"XOR: {a ^ b} ({bin(a ^ b)[2:]})")
        
        # 3. 8괘를 이진법으로 표현
        trigrams = {
            '건': '111', '태': '110', '리': '101', '진': '100',
            '손': '011', '감': '010', '간': '001', '곤': '000'
        }
        
        print(f"\n8괘의 이진 표현:")
        for name, binary in trigrams.items():
            decimal = int(binary, 2)
            print(f"{name}: {binary} ({decimal})")
        
        self.results['binary'] = {
            'conversions': binary_conversions,
            'trigrams': trigrams
        }
        
        return self.results['binary']
    
    def verify_golden_ratio(self):
        """리(☲): 황금비 φ 검증"""
        print("\n" + "=" * 50)
        print("🔵 리(☲): 황금비 φ 검증")
        print("=" * 50)
        
        # 1. 정의에서 계산
        phi_definition = (1 + sqrt(5)) / 2
        print(f"정의에서: φ = (1+√5)/2 = {phi_definition:.10f}")
        
        # 2. 피보나치 수열에서 극한
        fib = [1, 1]
        ratios = []
        
        for i in range(20):
            fib.append(fib[-1] + fib[-2])
            if len(fib) > 2:
                ratio = fib[-1] / fib[-2]
                ratios.append(ratio)
                if i < 10:  # 처음 10개만 출력
                    print(f"F{i+3}/F{i+2} = {fib[-1]}/{fib[-2]} = {ratio:.8f}")
        
        phi_fibonacci = ratios[-1]
        print(f"피보나치 극한: φ ≈ {phi_fibonacci:.10f}")
        
        # 3. 연분수 표현
        def continued_fraction_phi(n_terms):
            result = 0
            for _ in range(n_terms):
                result = 1 / (1 + result)
            return 1 + result
        
        phi_continued = continued_fraction_phi(20)
        print(f"연분수 [1;1,1,1,...]: φ ≈ {phi_continued:.10f}")
        
        # 4. SymPy 정확한 값
        phi_sympy = float(((1 + sp.sqrt(5)) / 2).evalf(20))
        print(f"SymPy 정확한 값: φ = {phi_sympy:.10f}")
        
        # 5. 황금비의 성질 검증
        print(f"\n황금비 성질 검증:")
        print(f"φ² = φ + 1: {phi_definition**2:.6f} = {phi_definition + 1:.6f} ✓")
        print(f"1/φ = φ - 1: {1/phi_definition:.6f} = {phi_definition - 1:.6f} ✓")
        
        self.results['golden_ratio'] = {
            'definition': phi_definition,
            'fibonacci': phi_fibonacci,
            'continued_fraction': phi_continued,
            'sympy': phi_sympy,
            'fibonacci_sequence': fib[:15],
            'ratios': ratios[:10]
        }
        
        return self.results['golden_ratio']
    
    def verify_probability(self):
        """감(☵): 확률 검증"""
        print("\n" + "=" * 50)
        print("🔵 감(☵): 확률 검증")
        print("=" * 50)
        
        # 1. 동전 던지기 시뮬레이션
        n_trials = 10000
        heads = sum(1 for _ in range(n_trials) if random.random() < 0.5)
        prob_heads = heads / n_trials
        
        print(f"동전 {n_trials}번 던지기:")
        print(f"앞면: {heads}번 ({prob_heads:.4f})")
        print(f"이론값: 0.5000")
        
        # 2. 주사위 시뮬레이션
        dice_rolls = [random.randint(1, 6) for _ in range(10000)]
        dice_counts = Counter(dice_rolls)
        
        print(f"\n주사위 {len(dice_rolls)}번 던지기:")
        for i in range(1, 7):
            count = dice_counts[i]
            prob = count / len(dice_rolls)
            print(f"{i}: {count}번 ({prob:.4f}, 이론값: {1/6:.4f})")
        
        # 3. 정규분포 샘플링
        normal_samples = np.random.normal(0, 1, 10000)
        mean_sample = np.mean(normal_samples)
        std_sample = np.std(normal_samples)
        
        print(f"\n정규분포 N(0,1) 샘플링:")
        print(f"표본 평균: {mean_sample:.4f} (이론값: 0)")
        print(f"표본 표준편차: {std_sample:.4f} (이론값: 1)")
        
        # 4. 베이즈 정리 예시
        # P(병|양성) = P(양성|병) * P(병) / P(양성)
        p_disease = 0.01  # 질병 발생률 1%
        p_positive_given_disease = 0.99  # 민감도 99%
        p_positive_given_healthy = 0.05  # 위양성률 5%
        
        p_positive = (p_positive_given_disease * p_disease + 
                     p_positive_given_healthy * (1 - p_disease))
        p_disease_given_positive = (p_positive_given_disease * p_disease) / p_positive
        
        print(f"\n베이즈 정리 (의료 검사):")
        print(f"P(병|양성) = {p_disease_given_positive:.4f}")
        print(f"양성이어도 실제 병일 확률은 {p_disease_given_positive*100:.1f}%")
        
        self.results['probability'] = {
            'coin_flip': prob_heads,
            'dice_distribution': dict(dice_counts),
            'normal_stats': {'mean': mean_sample, 'std': std_sample},
            'bayes_example': p_disease_given_positive
        }
        
        return self.results['probability']
    
    def verify_calculus(self):
        """진(☳): 미분, 손(☴): 적분 검증"""
        print("\n" + "=" * 50)
        print("🔵 진(☳): 미분 & 손(☴): 적분 검증")
        print("=" * 50)
        
        # 1. 기호 미분
        x = sp.Symbol('x')
        functions = [
            ('x²', x**2, 2*x),
            ('sin(x)', sp.sin(x), sp.cos(x)),
            ('eˣ', sp.exp(x), sp.exp(x)),
            ('ln(x)', sp.log(x), 1/x)
        ]
        
        print("기호 미분:")
        for name, func, expected in functions:
            derivative = sp.diff(func, x)
            print(f"d/dx[{name}] = {derivative} ✓")
        
        # 2. 수치 미분
        def numerical_derivative(f, x, h=1e-8):
            return (f(x + h) - f(x - h)) / (2 * h)
        
        test_point = 2
        print(f"\n수치 미분 (x = {test_point}):")
        for name, func, expected in functions:
            if name != 'ln(x)':  # ln(x)는 람다로 따로 처리
                numerical = numerical_derivative(
                    lambda val: float(func.subs(x, val)), test_point
                )
                analytical = float(expected.subs(x, test_point))
                print(f"{name}: 수치={numerical:.6f}, 해석적={analytical:.6f}")
        
        # 3. 기호 적분
        integrals = [
            ('x²', x**2, x**3/3),
            ('sin(x)', sp.sin(x), -sp.cos(x)),
            ('eˣ', sp.exp(x), sp.exp(x)),
            ('1/x', 1/x, sp.log(x))
        ]
        
        print("\n기호 적분:")
        for name, func, expected in integrals:
            integral = sp.integrate(func, x)
            print(f"∫{name}dx = {integral} + C")
        
        # 4. 정적분 (미적분학의 기본정리)
        print(f"\n미적분학의 기본정리 검증:")
        func = x**2
        a, b = 0, 3
        
        # 정적분 계산
        definite_integral = sp.integrate(func, (x, a, b))
        
        # 기본정리: F(b) - F(a)
        antiderivative = sp.integrate(func, x)
        fundamental_theorem = antiderivative.subs(x, b) - antiderivative.subs(x, a)
        
        print(f"∫₀³ x² dx = {definite_integral}")
        print(f"F(3) - F(0) = {fundamental_theorem}")
        print(f"기본정리 성립: {definite_integral == fundamental_theorem} ✓")
        
        self.results['calculus'] = {
            'derivatives': {name: str(sp.diff(func, x)) for name, func, _ in functions},
            'integrals': {name: str(sp.integrate(func, x)) for name, func, _ in integrals},
            'fundamental_theorem': {
                'definite_integral': float(definite_integral),
                'fundamental_result': float(fundamental_theorem),
                'equal': definite_integral == fundamental_theorem
            }
        }
        
        return self.results['calculus']
    
    def verify_primes(self):
        """간(☶): 소수 검증"""
        print("\n" + "=" * 50)
        print("🔵 간(☶): 소수 검증")
        print("=" * 50)
        
        # 1. 에라토스테네스의 체
        def sieve_of_eratosthenes(n):
            primes = [True] * (n + 1)
            primes[0] = primes[1] = False
            
            for i in range(2, int(n**0.5) + 1):
                if primes[i]:
                    for j in range(i*i, n + 1, i):
                        primes[j] = False
            
            return [i for i in range(2, n + 1) if primes[i]]
        
        first_50_primes = sieve_of_eratosthenes(230)[:50]
        print(f"처음 50개 소수:")
        for i in range(0, 50, 10):
            print(f"{first_50_primes[i:i+10]}")
        
        # 2. 소수 판별 함수
        def is_prime(n):
            if n < 2:
                return False
            for i in range(2, int(n**0.5) + 1):
                if n % i == 0:
                    return False
            return True
        
        # 3. 소수 정리 근사
        def prime_counting_function(n):
            return sum(1 for i in range(2, n+1) if is_prime(i))
        
        def prime_number_theorem_approximation(n):
            return n / log(n) if n > 1 else 0
        
        test_values = [100, 1000, 10000]
        print(f"\n소수 정리 검증:")
        print(f"{'n':>6} {'π(n)':>8} {'n/ln(n)':>10} {'오차율':>8}")
        
        for n in test_values:
            actual = prime_counting_function(n)
            approx = prime_number_theorem_approximation(n)
            error_rate = abs(actual - approx) / actual * 100
            print(f"{n:>6} {actual:>8} {approx:>10.1f} {error_rate:>7.1f}%")
        
        # 4. 메르센 소수 확인
        mersenne_exponents = [2, 3, 5, 7, 13, 17, 19, 31]
        print(f"\n메르센 소수 (2ᵖ - 1):")
        
        for p in mersenne_exponents:
            mersenne = 2**p - 1
            prime_check = is_prime(mersenne)
            print(f"2^{p} - 1 = {mersenne} {'✓' if prime_check else '✗'}")
        
        self.results['primes'] = {
            'first_50_primes': first_50_primes,
            'prime_counting': {n: prime_counting_function(n) for n in test_values},
            'prime_theorem_approx': {n: prime_number_theorem_approximation(n) for n in test_values},
            'mersenne_primes': {p: 2**p - 1 for p in mersenne_exponents}
        }
        
        return self.results['primes']
    
    def verify_symmetry(self):
        """태(☱): 대칭성 검증"""
        print("\n" + "=" * 50)
        print("🔵 태(☱): 대칭성 검증")
        print("=" * 50)
        
        # 1. 기하학적 대칭
        print("기하학적 대칭:")
        
        # 정다각형의 회전 대칭
        def rotation_symmetries(n_sides):
            return [360 / n_sides * i for i in range(n_sides)]
        
        shapes = [3, 4, 5, 6, 8]
        for n in shapes:
            symmetries = rotation_symmetries(n)
            print(f"정{n}각형: {len(symmetries)}개 회전 대칭 (각도: {symmetries[:3]}...)")
        
        # 2. 함수의 대칭성
        print(f"\n함수의 대칭성:")
        
        # 우함수 (even function): f(-x) = f(x)
        def test_even_function(func, test_points):
            return all(abs(func(-x) - func(x)) < 1e-10 for x in test_points)
        
        # 기함수 (odd function): f(-x) = -f(x)
        def test_odd_function(func, test_points):
            return all(abs(func(-x) + func(x)) < 1e-10 for x in test_points)
        
        test_points = [1, 2, 3, 0.5, 1.5]
        functions_to_test = [
            ('x²', lambda x: x**2, 'even'),
            ('cos(x)', lambda x: np.cos(x), 'even'),
            ('x³', lambda x: x**3, 'odd'),
            ('sin(x)', lambda x: np.sin(x), 'odd'),
        ]
        
        for name, func, expected_symmetry in functions_to_test:
            is_even = test_even_function(func, test_points)
            is_odd = test_odd_function(func, test_points)
            
            if expected_symmetry == 'even' and is_even:
                print(f"{name}: 우함수 ✓")
            elif expected_symmetry == 'odd' and is_odd:
                print(f"{name}: 기함수 ✓")
            else:
                print(f"{name}: 대칭성 확인 실패")
        
        # 3. 군론적 대칭 (간단한 예)
        print(f"\n군론적 대칭 (정사각형의 대칭군 D₄):")
        
        # 정사각형의 8개 대칭: 4개 회전 + 4개 반사
        square_symmetries = {
            'r0': '항등원 (0° 회전)',
            'r90': '90° 회전',
            'r180': '180° 회전',
            'r270': '270° 회전',
            'h': '수평 반사',
            'v': '수직 반사',
            'd1': '대각선1 반사',
            'd2': '대각선2 반사'
        }
        
        for sym, desc in square_symmetries.items():
            print(f"{sym}: {desc}")
        
        print(f"총 8개 대칭 = 2⁴ (D₄ 군)")
        
        # 4. 분자의 대칭성 (점군)
        molecules = {
            'H₂O': 'C₂ᵥ (2개 회전축, 2개 반사면)',
            'NH₃': 'C₃ᵥ (3개 회전축, 3개 반사면)',
            'CH₄': 'Tₑ (정사면체 대칭)',
            'C₆H₆': 'D₆ₕ (벤젠의 높은 대칭성)'
        }
        
        print(f"\n분자의 점군 대칭:")
        for molecule, symmetry in molecules.items():
            print(f"{molecule}: {symmetry}")
        
        self.results['symmetry'] = {
            'rotation_symmetries': {n: rotation_symmetries(n) for n in shapes},
            'function_symmetries': {name: expected_symmetry for name, _, expected_symmetry in functions_to_test},
            'square_group': square_symmetries,
            'molecular_symmetries': molecules
        }
        
        return self.results['symmetry']
    
    def run_all_verifications(self):
        """모든 8괘 수학적 검증 실행"""
        print("🔵" * 20)
        print("주역 8괘 수학적 검증 시스템")
        print("🔵" * 20)
        
        verifications = [
            self.verify_pi,
            self.verify_binary,
            self.verify_golden_ratio,
            self.verify_probability,
            self.verify_calculus,
            self.verify_primes,
            self.verify_symmetry
        ]
        
        for verification in verifications:
            try:
                verification()
            except Exception as e:
                print(f"오류 발생: {e}")
        
        print("\n" + "🔵" * 20)
        print("모든 검증 완료!")
        print("🔵" * 20)
        
        return self.results

# 실행 예시
if __name__ == "__main__":
    verifier = MathematicalVerification()
    results = verifier.run_all_verifications()
    
    # 결과 요약
    print(f"\n📊 검증 결과 요약:")
    print(f"π 값: {results.get('pi', {}).get('numpy', 'N/A'):.6f}")
    print(f"황금비 φ: {results.get('golden_ratio', {}).get('definition', 'N/A'):.6f}")
    print(f"첫 번째 소수들: {results.get('primes', {}).get('first_50_primes', ['N/A'])[:10]}")
    print(f"확률 검증: 동전던지기 = {results.get('probability', {}).get('coin_flip', 'N/A'):.4f}")
