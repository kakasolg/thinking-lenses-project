class BaguaApp {
    constructor() {
        this.currentModel = 'abstract';
        this.trigrams = [];
        this.hexagrams = [];
        this.selectedHexagram = null;
        
        this.init();
    }
    
    async init() {
        await this.loadData();
        this.renderAll();
        this.setupEventListeners();
        
        // KaTeX 자동 렌더링
        if (window.renderMathInElement) {
            renderMathInElement(document.body);
        }
    }
    
    async loadData() {
        try {
            const [trigramsRes, hexagramsRes, analysisRes, dualityRes] = await Promise.all([
                fetch(`/api/trigrams/${this.currentModel}`),
                fetch(`/api/hexagrams/${this.currentModel}`),
                fetch(`/api/analysis/${this.currentModel}`),
                fetch(`/api/duality/${this.currentModel}`)
            ]);
            
            this.trigrams = (await trigramsRes.json()).trigrams;
            this.hexagrams = (await hexagramsRes.json()).hexagrams;
            this.analysis = await analysisRes.json();
            this.duality = (await dualityRes.json()).duality_pairs;
            
        } catch (error) {
            console.error('데이터 로딩 실패:', error);
        }
    }
    
    setupEventListeners() {
        // 모델 선택기
        document.getElementById('modelSelector').addEventListener('change', async (e) => {
            this.currentModel = e.target.value;
            await this.loadData();
            this.renderAll();
        });
        
        // 검색 기능
        document.getElementById('hexagramSearch').addEventListener('input', (e) => {
            this.searchHexagrams(e.target.value);
        });
    }
    
    renderAll() {
        this.renderTrigrams();
        this.renderHexagrams();
        this.renderDuality();
        this.renderAnalysis();
        this.updateStats();
    }
    
    renderTrigrams() {
        const container = document.getElementById('trigramsContainer');
        container.innerHTML = '';
        
        this.trigrams.forEach(trigram => {
            const card = document.createElement('div');
            card.className = 'trigram-card';
            card.innerHTML = `
                <div class="trigram-symbol">${trigram.symbol}</div>
                <h4 style="margin: 0.5rem 0; text-align: center;">${trigram.name}</h4>
                <p style="margin: 0.5rem 0; font-weight: bold; text-align: center;">${trigram.description}</p>
                <p style="margin: 0; font-size: 0.9rem; color: #666; text-align: center;">${trigram.concept}</p>
            `;
            container.appendChild(card);
        });
    }
    
    renderHexagrams() {
        const grid = document.getElementById('hexagramGrid');
        grid.innerHTML = '';
        
        this.hexagrams.forEach((hex) => {
            const cell = document.createElement('div');
            cell.className = 'hexagram-cell';
            cell.innerHTML = `
                <div style="font-weight: bold;">${hex.number}</div>
                <div style="font-size: 0.7rem;">${hex.name}</div>
                <div style="font-size: 0.8rem;">${hex.upper.symbol}${hex.lower.symbol}</div>
            `;
            
            cell.addEventListener('click', () => {
                this.selectHexagram(hex, cell);
            });
            
            grid.appendChild(cell);
        });
    }
    
    selectHexagram(hex, cellElement) {
        // 이전 선택 해제
        document.querySelectorAll('.hexagram-cell.selected').forEach(cell => {
            cell.classList.remove('selected');
        });
        
        // 새로운 선택
        cellElement.classList.add('selected');
        this.selectedHexagram = hex;
        
        // 상세 정보 표시
        const detail = document.getElementById('hexagramDetail');
        detail.style.display = 'block';
        detail.innerHTML = `
            <h3>${hex.number}. ${hex.name}</h3>
            
            <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 2rem; margin: 1rem 0;">
                <div>
                    <h4>괘 구성</h4>
                    <p><strong>상괘:</strong> ${hex.upper.symbol} ${hex.upper.name}<br>
                    <em>${hex.upper.description}</em></p>
                    <p><strong>하괘:</strong> ${hex.lower.symbol} ${hex.lower.name}<br>
                    <em>${hex.lower.description}</em></p>
                </div>
                <div>
                    <h4>수학적 의미</h4>
                    <div class="math-formula">
                        ${hex.mathematical_meaning}
                    </div>
                    <h4>예시</h4>
                    <ul>
                        ${hex.examples.map(ex => `<li>${ex}</li>`).join('')}
                    </ul>
                </div>
            </div>
        `;
    }
    
    renderDuality() {
        const container = document.getElementById('dualityContainer');
        container.innerHTML = '';
        
        this.duality.forEach(pair => {
            const div = document.createElement('div');
            div.className = 'duality-pair';
            div.innerHTML = `
                <div class="duality-item">
                    <div style="font-size: 1.5rem;">${pair.pair1.symbol}</div>
                    <strong>${pair.pair1.name}</strong>
                    <div style="font-size: 0.9rem; color: #666;">${pair.pair1.description}</div>
                </div>
                <div class="duality-arrow">
                    <i class="fas fa-exchange-alt"></i>
                </div>
                <div class="duality-item">
                    <div style="font-size: 1.5rem;">${pair.pair2.symbol}</div>
                    <strong>${pair.pair2.name}</strong>
                    <div style="font-size: 0.9rem; color: #666;">${pair.pair2.description}</div>
                </div>
            `;
            container.appendChild(div);
        });
    }
    
    renderAnalysis() {
        const container = document.getElementById('analysisResults');
        container.innerHTML = `
            <div class="stats-grid">
                <div class="stats-card">
                    <strong>모델 타입</strong><br>
                    ${this.analysis.model_type === 'abstract' ? '추상적 모델' : '구체적 모델'}
                </div>
                <div class="stats-card">
                    <strong>총 괘 수</strong><br>
                    ${this.analysis.total_hexagrams}개
                </div>
                <div class="stats-card">
                    <strong>수학적 커버리지</strong><br>
                    ${this.analysis.mathematical_coverage.toFixed(1)}%
                </div>
                <div class="stats-card">
                    <strong>대대 관계</strong><br>
                    ${this.analysis.duality_pairs.length}쌍
                </div>
            </div>
        `;
        
        // 흥미로운 조합 예시
        const combinations = document.getElementById('interestingCombinations');
        if (this.currentModel === 'concrete') {
            combinations.innerHTML = `
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem;">
                    <div class="example-section">
                        <h4>π + 이진법</h4>
                        <p>디지털 신호처리에서의 FFT (Fast Fourier Transform)</p>
                        <div class="math-formula">
                            연속적인 원주율과 이산적인 이진법의 조합으로 주파수 영역 변환 실현
                        </div>
                    </div>
                    <div class="example-section">
                        <h4>미분 + 적분</h4>
                        <p>미적분학의 기본정리</p>
                        <div class="math-formula">
                            순간적 변화율과 누적적 변화의 상호 보완적 관계
                        </div>
                    </div>
                    <div class="example-section">
                        <h4>소수 + 확률</h4>
                        <p>소수 정리의 확률적 해석</p>
                        <div class="math-formula">
                            리만 제타함수와 양자 카오스 이론의 연결점
                        </div>
                    </div>
                    <div class="example-section">
                        <h4>황금비 + 대칭성</h4>
                        <p>자연의 아름다운 비례와 불변성</p>
                        <div class="math-formula">
                            정다면체와 피보나치 수열에서 나타나는 기하학적 조화
                        </div>
                    </div>
                </div>
            `;
        } else {
            combinations.innerHTML = `
                <div class="example-section">
                    <p><em>추상적 모델의 흥미로운 조합 분석이 개발 중입니다.</em></p>
                </div>
            `;
        }
    }
    
    updateStats() {
        document.getElementById('totalHexagrams').textContent = this.analysis.total_hexagrams;
        document.getElementById('coverage').textContent = this.analysis.mathematical_coverage.toFixed(1);
        document.getElementById('dualityCount').textContent = this.analysis.duality_pairs.length;
    }
    
    async searchHexagrams(query) {
        if (!query.trim()) {
            document.getElementById('searchResults').innerHTML = '';
            return;
        }
        
        try {
            const response = await fetch(`/api/search/${this.currentModel}?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            
            const resultsDiv = document.getElementById('searchResults');
            if (data.hexagrams.length === 0) {
                resultsDiv.innerHTML = `
                    <div class="example-section" style="background: #fff3cd; border-color: #ffeaa7;">
                        <strong>검색 결과:</strong> "${query}"과 관련된 괘를 찾을 수 없습니다.
                    </div>
                `;
                return;
            }
            
            resultsDiv.innerHTML = `
                <h4>검색 결과: "${query}" (${data.hexagrams.length}개 발견)</h4>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 1rem;">
                    ${data.hexagrams.map(hex => `
                        <div class="hexagram-detail">
                            <h4>${hex.number}. ${hex.name}</h4>
                            <p style="font-size: 0.9rem; color: #666;">${hex.upper} + ${hex.lower}</p>
                            <div class="math-formula" style="font-size: 0.9rem;">
                                ${hex.mathematical_meaning}
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;
            
        } catch (error) {
            console.error('검색 실패:', error);
        }
    }
}

// 탭 전환 함수
function showTab(tabName) {
    // 모든 탭 숨기기
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // 모든 탭 버튼 비활성화
    document.querySelectorAll('.tab-button').forEach(button => {
        button.classList.remove('active');
    });
    
    // 선택된 탭 표시
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
}

// 앱 초기화
document.addEventListener('DOMContentLoaded', () => {
    new BaguaApp();
});
