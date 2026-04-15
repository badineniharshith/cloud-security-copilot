const API_BASE_URL = 'http://localhost:5001/api';

let severityChart = null;
let costChart = null;

// Initialize dashboard
async function initDashboard() {
    console.log('Initializing dashboard...');
    await loadSummary();
    await loadSecurityAnalysis();
    await loadCostAnalysis();
    await loadRecommendations();
    updateLastUpdate();
}

// Load summary statistics
async function loadSummary() {
    try {
        const response = await fetch(`${API_BASE_URL}/summary`);
        const data = await response.json();
        
        document.getElementById('totalResources').textContent = data.summary.total_resources;
        document.getElementById('totalIssues').textContent = data.summary.total_misconfigurations;
        document.getElementById('criticalIssues').textContent = `Critical: ${data.summary.critical_misconfigurations}`;
        document.getElementById('monthlyCost').textContent = `$${data.summary.total_monthly_cost.toLocaleString()}`;
        document.getElementById('potentialSavings').textContent = `Potential savings: $${data.summary.total_optimization_potential.toLocaleString()}`;
        
        console.log('Summary loaded:', data.summary);
    } catch (error) {
        console.error('Error loading summary:', error);
        showError('Failed to load summary data');
    }
}

// Load security analysis
async function loadSecurityAnalysis() {
    try {
        const response = await fetch(`${API_BASE_URL}/security/analysis`);
        const data = await response.json();
        
        document.getElementById('riskScore').textContent = data.overall_risk_score;
        document.getElementById('riskLevel').textContent = `Risk Level: ${data.risk_level}`;
        
        createSeverityChart(data.severity_distribution);
        displayAIInsights(data.ai_insights);
        displayCriticalFindings(data.critical_findings);
        displayTopMisconfigurations(data.top_misconfiguration_types);
        
        console.log('Security analysis loaded');
    } catch (error) {
        console.error('Error loading security analysis:', error);
        showError('Failed to load security analysis');
    }
}

// Load cost analysis
async function loadCostAnalysis() {
    try {
        const response = await fetch(`${API_BASE_URL}/cost/analysis`);
        const data = await response.json();
        
        createCostChart(data.cost_by_resource_type);
        displayOptimizationOpportunities(data.top_optimization_opportunities);
        
        console.log('Cost analysis loaded');
    } catch (error) {
        console.error('Error loading cost analysis:', error);
        showError('Failed to load cost analysis');
    }
}

// Load recommendations
async function loadRecommendations() {
    try {
        const response = await fetch(`${API_BASE_URL}/recommendations`);
        const data = await response.json();
        
        displayRecommendations(data.security_recommendations, data.cost_recommendations);
        
        console.log('Recommendations loaded');
    } catch (error) {
        console.error('Error loading recommendations:', error);
        showError('Failed to load recommendations');
    }
}

// Create severity chart
function createSeverityChart(severityData) {
    const ctx = document.getElementById('severityChart').getContext('2d');
    
    if (severityChart) {
        severityChart.destroy();
    }
    
    severityChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Object.keys(severityData),
            datasets: [{
                label: 'Number of Issues',
                data: Object.values(severityData),
                backgroundColor: ['#dc3545', '#fd7e14', '#ffc107', '#28a745'],
                borderColor: '#fff',
                borderWidth: 2,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { position: 'bottom' },
                tooltip: { callbacks: { label: (ctx) => `${ctx.raw} issues` } }
            },
            scales: {
                y: { beginAtZero: true, title: { display: true, text: 'Number of Issues' } },
                x: { title: { display: true, text: 'Severity Level' } }
            }
        }
    });
}

// Create cost chart
function createCostChart(costData) {
    const ctx = document.getElementById('costChart').getContext('2d');
    
    if (costChart) {
        costChart.destroy();
    }
    
    const labels = Object.keys(costData);
    const values = Object.values(costData);
    
    costChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe', '#43e97b', '#fa709a'],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { position: 'right' },
                tooltip: { callbacks: { label: (ctx) => `${ctx.label}: $${ctx.raw.toLocaleString()}` } }
            }
        }
    });
}

// Display AI insights
function displayAIInsights(insights) {
    const container = document.getElementById('aiInsights');
    container.innerHTML = '';
    
    if (!insights || insights.length === 0) {
        container.innerHTML = '<div class="insight-item">No insights available</div>';
        return;
    }
    
    insights.forEach(insight => {
        const div = document.createElement('div');
        div.className = 'insight-item';
        div.innerHTML = `<div class="insight-text">🤖 ${insight}</div>`;
        container.appendChild(div);
    });
}

// Display critical findings
function displayCriticalFindings(findings) {
    const container = document.getElementById('criticalFindings');
    container.innerHTML = '';
    
    if (!findings || findings.length === 0) {
        container.innerHTML = '<div class="findings-item">🎉 No critical findings found! Security posture is good.</div>';
        return;
    }
    
    findings.slice(0, 8).forEach(finding => {
        const div = document.createElement('div');
        div.className = `findings-item ${finding.severity.toLowerCase()}`;
        div.innerHTML = `
            <div class="findings-title">⚠️ ${finding.type}</div>
            <div class="findings-desc">${finding.description}</div>
            <div class="remediation">🔧 ${finding.remediation_steps}</div>
            <div class="findings-desc" style="font-size: 11px; color: #999; margin-top: 5px;">Resource: ${finding.resource_name}</div>
        `;
        container.appendChild(div);
    });
    
    if (findings.length > 8) {
        const moreDiv = document.createElement('div');
        moreDiv.className = 'findings-item';
        moreDiv.innerHTML = `<div class="findings-desc">... and ${findings.length - 8} more findings</div>`;
        container.appendChild(moreDiv);
    }
}

// Display optimization opportunities
function displayOptimizationOpportunities(opportunities) {
    const container = document.getElementById('costOptimization');
    container.innerHTML = '';
    
    if (!opportunities || opportunities.length === 0) {
        container.innerHTML = '<div class="optimization-item">✨ No optimization opportunities found! Cost optimized.</div>';
        return;
    }
    
    opportunities.forEach(opp => {
        const div = document.createElement('div');
        div.className = 'optimization-item';
        div.innerHTML = `
            <div class="optimization-name">💡 ${opp.resource_name}</div>
            <div class="optimization-desc">${opp.optimization_recommendation}</div>
            <div class="optimization-savings">💰 Potential savings: $${opp.optimization_potential.toLocaleString()}/month</div>
        `;
        container.appendChild(div);
    });
}

// Display top misconfigurations
function displayTopMisconfigurations(misconfigs) {
    const container = document.getElementById('topMisconfigs');
    container.innerHTML = '';
    
    if (!misconfigs || misconfigs.length === 0) {
        container.innerHTML = '<div class="misconfig-item">No misconfigurations found</div>';
        return;
    }
    
    misconfigs.forEach(misconfig => {
        const div = document.createElement('div');
        div.className = 'misconfig-item';
        div.innerHTML = `
            <div class="misconfig-name">📋 ${misconfig.type}</div>
            <div class="misconfig-count">Occurrences: ${misconfig.count}</div>
        `;
        container.appendChild(div);
    });
}

// Display recommendations
function displayRecommendations(securityRecs, costRecs) {
    const container = document.getElementById('recommendations');
    container.innerHTML = '';
    
    if (securityRecs && securityRecs.length > 0) {
        securityRecs.forEach(rec => {
            const div = document.createElement('div');
            div.className = 'recommendation-item';
            div.innerHTML = `🛡️ ${rec}`;
            container.appendChild(div);
        });
    }
    
    if (costRecs && costRecs.length > 0) {
        costRecs.forEach(rec => {
            const div = document.createElement('div');
            div.className = 'recommendation-item';
            div.innerHTML = `💰 ${rec}`;
            container.appendChild(div);
        });
    }
}

// Refresh data
async function refreshData() {
    try {
        showLoading(true);
        const response = await fetch(`${API_BASE_URL}/regenerate-data`, {
            method: 'POST'
        });
        const data = await response.json();
        
        await initDashboard();
        updateLastUpdate();
        
        showNotification('Data refreshed successfully!', 'success');
        console.log('Data refreshed:', data.summary);
    } catch (error) {
        console.error('Error refreshing data:', error);
        showNotification('Error refreshing data. Please check if backend is running.', 'error');
    } finally {
        showLoading(false);
    }
}

// Update last update timestamp
function updateLastUpdate() {
    const now = new Date();
    document.getElementById('lastUpdate').textContent = `Last updated: ${now.toLocaleTimeString()}`;
}

// Show loading state
function showLoading(show) {
    const btn = document.getElementById('refreshDataBtn');
    if (show) {
        btn.textContent = '🔄 Refreshing...';
        btn.disabled = true;
    } else {
        btn.textContent = '🔄 Refresh Data';
        btn.disabled = false;
    }
}

// Show notification
function showNotification(message, type) {
    // Simple alert for now - you can enhance this
    if (type === 'error') {
        console.error(message);
        alert('❌ ' + message);
    } else {
        console.log(message);
    }
}

// Show error message in UI
function showError(message) {
    console.error(message);
    // You can add a toast notification here if desired
}

// Event listeners
document.addEventListener('DOMContentLoaded', initDashboard);
document.getElementById('refreshDataBtn').addEventListener('click', refreshData);