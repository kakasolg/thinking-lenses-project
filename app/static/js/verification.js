class VerificationApp {
    constructor() {
        this.currentTab = 'dashboard';
        this.init();
    }

    init() {
        this.updateDashboardStatus();
    }

    async updateDashboardStatus() {
        // 기본 상태 표시
        document.getElementById('verificationCount').textContent = '0';
        document.getElementById('plotCount').textContent = '0';
        document.getElementById('accuracyRate').textContent = '0%';
    }

    showLoading(containerId) {
        const container = document.getElementById(containerId);
        container.innerHTML = `
            <div class="loading">
                <div class="spinner"></div>
                <p>수학적 검증을 수행하고 있습니다...</p>
                <p style="font-size: 0.9rem; color: #666;">
                    복잡한 계산과 시각화 생성 중입니다. 잠시만 기다려주세요.
                </p>
            </div>
        `;
    }

    showError(containerId, error) {
        const container = document.getElementById(containerId);
        container.innerHTML = `
            <div class="alert alert-error">
                <strong>오류 발생:</strong> ${error}
            </div>
        `;
    }

    showSuccess(containerId, message) {
        const container = document.getElementById(containerId);
        container.innerHTML = `
            <div class="alert alert-success">
                <strong>성공:</strong> ${message}
            </div>
        `;
    }

    async loadDashboard() {
        this.showLoading('dashboardResults');

        try {
            const response = await fetch('/math/api/verification/dashboard');
            const data = await response.json();

            if (data.success) {
                this.renderDashboardResults(data);
                this.updateDashboardStatus(data);
            } else {
                this.showError('dashboardResults', data.error);
            }
        } catch (error) {
            this.showError('dashboardResults', '네트워크 오류가 발생했습니다.');
        }
    }

    renderDashboardResults(data) {
        const container = document.getElementById('dashboardResults');

        let html = `
            <div class="alert alert-success">
                <strong>검증 완료!</strong> ${data.verification_count}개 개념, ${data.plot_count}개 그래프 생성
            </div>
        `;

        if (data.dashboard_plot) {
            html += `
                <div class="plot-container">
                    <div class="plot-title">8괘 수학적 검증 종합 결과</div>
                    <img src="data:image/png;base64,${data.dashboard_plot}" 
                         alt="종합 대시보드" class="plot-image">
                    <div class="plot-description">
                        각 괘별 수학적 개념의 검증 정확도와 8괘의 원형 배치를 보여줍니다.
                    </div>
                </div>
            `;
        }

        if (data.summary && data.summary.length > 0) {
            html += `
                <h4>검증 결과 요약</h4>
                <table class="results-table">
                    <thead>
                        <tr>
                            <th>괘</th>
                            <th>수학적 개념</th>
                            <th>검증값</th>
                            <th>실제값</th>
                            <th>오차</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            data.summary.forEach(item => {
                html += `
                    <tr>
                        <td>${item.괘}</td>
                        <td>${item.개념}</td>
                        <td>${item.검증값}</td>
                        <td>${item.실제값}</td>
                        <td>${item.오차}</td>
                    </tr>
                `;
            });

            html += `
                    </tbody>
                </table>
            `;
        }

        container.innerHTML = html;
    }

    async loadPiVerification() {
        this.showLoading('piResults');

        try {
            const response = await fetch('/math/api/verification/pi');
            const data = await response.json();

            if (data.success) {
                this.renderVerificationResults('piResults', data);
            } else {
                this.showError('piResults', data.error);
            }
        } catch (error) {
            this.showError('piResults', '네트워크 오류가 발생했습니다.');
        }
    }

    async loadGoldenRatioVerification() {
        this.showLoading('goldenResults');

        try {
            const response = await fetch('/math/api/verification/golden-ratio');
            const data = await response.json();

            if (data.success) {
                this.renderVerificationResults('goldenResults', data);
            } else {
                this.showError('goldenResults', data.error);
            }
        } catch (error) {
            this.showError('goldenResults', '네트워크 오류가 발생했습니다.');
        }
    }

    async loadProbabilityVerification() {
        this.showLoading('probabilityResults');

        try {
            const response = await fetch('/math/api/verification/probability');
            const data = await response.json();

            if (data.success) {
                this.renderVerificationResults('probabilityResults', data);
            } else {
                this.showError('probabilityResults', data.error);
            }
        } catch (error) {
            this.showError('probabilityResults', '네트워크 오류가 발생했습니다.');
        }
    }

    async loadCalculusVerification() {
        this.showLoading('calculusResults');

        try {
            const response = await fetch('/math/api/verification/calculus');
            const data = await response.json();

            if (data.success) {
                this.renderVerificationResults('calculusResults', data);
            } else {
                this.showError('calculusResults', data.error);
            }
        } catch (error) {
            this.showError('calculusResults', '네트워크 오류가 발생했습니다.');
        }
    }

    async loadBinaryVerification() {
        this.showLoading('binaryResults');

        try {
            const response = await fetch('/math/api/verification/binary');
            const data = await response.json();

            if (data.success) {
                this.renderVerificationResults('binaryResults', data);
            } else {
                this.showError('binaryResults', data.error);
            }
        } catch (error) {
            this.showError('binaryResults', '네트워크 오류가 발생했습니다.');
        }
    }

    async loadPrimesVerification() {
        this.showLoading('primesResults');

        try {
            const response = await fetch('/math/api/verification/primes');
            const data = await response.json();

            if (data.success) {
                this.renderVerificationResults('primesResults', data);
            } else {
                this.showError('primesResults', data.error);
            }
        } catch (error) {
            this.showError('primesResults', '네트워크 오류가 발생했습니다.');
        }
    }

    async loadSymmetryVerification() {
        this.showLoading('symmetryResults');

        try {
            const response = await fetch('/math/api/verification/symmetry');
            const data = await response.json();

            if (data.success) {
                this.renderVerificationResults('symmetryResults', data);
            } else {
                this.showError('symmetryResults', data.error);
            }
        } catch (error) {
            this.showError('symmetryResults', '네트워크 오류가 발생했습니다.');
        }
    }

    async loadEVerification() {
        this.showLoading('eResults');

        try {
            const response = await fetch('/math/api/verification/e');
            const data = await response.json();

            if (data.success) {
                this.renderVerificationResults('eResults', data);
            } else {
                this.showError('eResults', data.error);
            }
        } catch (error) {
            this.showError('eResults', '네트워크 오류가 발생했습니다.');
        }
    }

    async loadAllVerifications() {
                const resultsContainer = document.getElementById('dashboardResults');
                resultsContainer.innerHTML = '<pre id="log-container" style="white-space: pre-wrap; word-wrap: break-word; background: #f4f4f4; border: 1px solid #ddd; padding: 15px; border-radius: 5px;"></pre>';
                const logContainer = document.getElementById('log-container');

                const eventSource = new EventSource('/math/api/verification/all');

                logContainer.textContent = '서버에 연결 중...';

                eventSource.onmessage = function(event) {
                    if (event.data === '[DONE]') {
                        eventSource.close();
                        logContainer.textContent += '\n\n스트림 연결이 종료되었습니다.';
                        return;
                    }

                    const data = JSON.parse(event.data);

                    if (logContainer.textContent === '서버에 연결 중...') {
                        logContainer.textContent = ''; // 첫 메시지 수신 시 초기화
                    }

                    if (data.log) {
                        logContainer.textContent += data.log + '\n';
                    } else if (data.error) {
                        logContainer.textContent += `[오류] ${data.error}\n`;
                        logContainer.style.color = 'red';
                    }
                    
                    // 자동 스크롤
                    resultsContainer.scrollTop = resultsContainer.scrollHeight;
                };

                eventSource.onerror = function(err) {
                    logContainer.textContent += '\n\n스트림 연결 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.';
                    logContainer.style.color = 'red';
                    console.error("EventSource failed:", err);
                    eventSource.close();
                };
            }

    renderVerificationResults(containerId, data) {
        const container = document.getElementById(containerId);

        let html = `
            <div class="alert alert-success">
                <strong>${data.concept} 검증 완료!</strong> ${data.description}
            </div>
        `;

        // 그래프들 표시
        if (data.plots) {
            Object.entries(data.plots).forEach(([plotName, plotData]) => {
                const plotTitle = this.getPlotTitle(plotName);
                html += `
                    <div class="plot-container">
                        <div class="plot-title">${plotTitle}</div>
                        <img src="data:image/png;base64,${plotData}" 
                             alt="${plotTitle}" class="plot-image">
                    </div>
                `;
            });
        }

        // 수치 결과 표시
        if (data.result) {
            html += `<div class="math-formula">`;
            Object.entries(data.result).forEach(([key, value]) => {
                if (typeof value === 'number') {
                    html += `<strong>${key}:</strong> ${value.toFixed(6)}<br>`;
                } else if (typeof value === 'object' && !Array.isArray(value)) {
                    html += `<strong>${key}:</strong><br>`;
                    Object.entries(value).forEach(([subkey, subvalue]) => {
                        if (typeof subvalue === 'number') {
                            html += `&nbsp;&nbsp;${subkey}: ${subvalue.toFixed(6)}<br>`;
                        } else {
                            html += `&nbsp;&nbsp;${subkey}: ${subvalue}<br>`;
                        }
                    });
                } else {
                    html += `<strong>${key}:</strong> ${value}<br>`;
                }
            });
            html += `</div>`;
        }

        container.innerHTML = html;
    }

    renderAllResults(data) {
        const container = document.getElementById('dashboardResults');
        let html = `
            <div class="alert alert-success">
                <strong>전체 검증 완료!</strong> 총 ${Object.keys(data.results).length}개의 개념을 검증했습니다.
            </div>
        `;

        Object.entries(data.results).forEach(([concept, result]) => {
            html += `
                <div class="verification-card">
                    <h3>${result.concept}</h3>
                    <p>${result.description}</p>
            `;

            if (result.plots) {
                Object.entries(result.plots).forEach(([plotName, plotData]) => {
                    const plotTitle = this.getPlotTitle(plotName);
                    html += `
                        <div class="plot-container">
                            <div class="plot-title">${plotTitle}</div>
                            <img src="data:image/png;base64,${plotData}" 
                                 alt="${plotTitle}" class="plot-image">
                        </div>
                    `;
                });
            }

            if (result.result) {
                html += `<div class="math-formula">`;
                Object.entries(result.result).forEach(([key, value]) => {
                    if (typeof value === 'number') {
                        html += `<strong>${key}:</strong> ${value.toFixed(6)}<br>`;
                    } else {
                        html += `<strong>${key}:</strong> ${value}<br>`;
                    }
                });
                html += `</div>`;
            }

            html += `</div>`;
        });

        container.innerHTML = html;
    }

    getPlotTitle(plotName) {
        const titles = {
            'pi_monte_carlo': 'π 검증: 몬테카를로 시뮬레이션',
            'pi_series': 'π 검증: 라이프니츠 급수 수렴',
            'golden_ratio_fibonacci': 'φ 검증: 피보나치 수열 비율',
            'golden_ratio_spiral': 'φ 검증: 황금 나선',
            'clt_simulation': '확률론: 중심극한정리 시뮬레이션',
            'distribution_comparison': '확률론: 다양한 확률분포 비교',
            'derivative_visualization': '미적분학: 도함수의 기하학적 의미',
            'integral_visualization': '미적분학: 정적분의 기하학적 의미',
            'binary_representation': '이진법: 4비트 이진수 표현',
            'bernoulli_trials': '이진법: 베르누이 시행과 이항분포',
            'sieve_of_eratosthenes': '소수: 에라토스테네스의 체',
            'prime_number_theorem': '소수: 소수 정리 (π(x) vs x/ln(x))',
            'geometric_transformations': '대칭성: 기하학적 변환',
            'd4_group_cayley_graph': '대칭성: D₄ 점군의 케일리 그래프',
            'e_series_convergence': '자연상수 e: 급수 근사 수렴',
            'e_limit_convergence': '자연상수 e: 극한 정의 수렴'
        };
        return titles[plotName] || '결과 그래프';
    }
}

const app = new VerificationApp();

function showTab(tabName) {
    // 모든 탭 콘텐츠 숨기기
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => {
        content.style.display = 'none';
    });

    // 모든 탭 비활성화
    const navTabs = document.querySelectorAll('.nav-tab');
    navTabs.forEach(tab => {
        tab.classList.remove('active');
    });

    // 선택된 탭 콘텐츠 보이기
    document.getElementById(tabName).style.display = 'block';

    // 선택된 탭 활성화
    const activeTab = document.querySelector(`.nav-tab[onclick="showTab('${tabName}')"]`);
    activeTab.classList.add('active');

    app.currentTab = tabName;
}

// 각 검증 버튼에 대한 이벤트 리스너
function loadPiVerification() { app.loadPiVerification(); }
function loadGoldenRatioVerification() { app.loadGoldenRatioVerification(); }
function loadProbabilityVerification() { app.loadProbabilityVerification(); }
function loadCalculusVerification() { app.loadCalculusVerification(); }
function loadBinaryVerification() { app.loadBinaryVerification(); }
function loadPrimesVerification() { app.loadPrimesVerification(); }
function loadSymmetryVerification() { app.loadSymmetryVerification(); }
function loadEVerification() { app.loadEVerification(); }
// function loadAllVerifications() { app.loadAllVerifications(); }
function loadDashboard() { app.loadDashboard(); }

// 초기 대시보드 로드 및 이벤트 리스너 설정
document.addEventListener('DOMContentLoaded', () => {
    // 각 개념 요약 카드를 클릭하면 해당 탭으로 이동
    document.querySelectorAll('.concept-summary').forEach(card => {
        card.addEventListener('click', () => {
            const targetTab = card.dataset.target;
            if (targetTab) {
                showTab(targetTab);
            }
        });
    });

    // 종합 검증 실행 버튼 (현재 비활성화)
    // const runAllBtn = document.getElementById('run-all-verifications');
    // if (runAllBtn) {
    //     runAllBtn.addEventListener('click', () => {
    //         app.loadAllVerifications();
    //     });
    // }
});
