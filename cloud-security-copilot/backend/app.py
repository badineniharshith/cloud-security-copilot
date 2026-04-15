from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import random
import uuid
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Simple data generator
def generate_sample_data():
    """Generate sample cloud data"""
    resources = []
    misconfigs = []
    cost_data = []
    
    # Generate 30 resources
    providers = ['AWS', 'Azure', 'GCP']
    resource_types = ['EC2', 'S3', 'VM', 'Storage', 'Database', 'Lambda', 'Kubernetes']
    severities = ['Critical', 'High', 'Medium', 'Low']
    
    total_cost = 0
    total_savings = 0
    
    for i in range(30):
        provider = random.choice(providers)
        resource_type = random.choice(resource_types)
        hourly_cost = round(random.uniform(0.05, 2.5), 2)
        monthly_cost = hourly_cost * 24 * 30
        
        resource = {
            'id': str(uuid.uuid4()),
            'name': f"{provider}-{resource_type}-{i+1}",
            'provider': provider,
            'type': resource_type,
            'region': random.choice(['us-east-1', 'us-west-2', 'eu-west-1', 'ap-southeast-1']),
            'created_at': datetime.now().isoformat(),
            'cost_per_hour': hourly_cost,
            'status': random.choice(['active', 'idle', 'stopped']),
            'tags': {'environment': random.choice(['prod', 'staging', 'dev', 'test'])}
        }
        resources.append(resource)
        
        # Generate 0-3 misconfigurations per resource
        num_misconfigs = random.randint(0, 3)
        for _ in range(num_misconfigs):
            severity = random.choices(severities, weights=[0.1, 0.2, 0.3, 0.4])[0]
            misconfig = {
                'id': str(uuid.uuid4()),
                'resource_id': resource['id'],
                'resource_name': resource['name'],
                'type': random.choice([
                    'Publicly accessible storage bucket',
                    'Open security group rules (0.0.0.0/0)',
                    'Unencrypted data at rest',
                    'Missing MFA enforcement',
                    'Overprivileged IAM roles',
                    'Unused access keys',
                    'Outdated software versions',
                    'Missing security patches',
                    'Unrestricted outbound traffic',
                    'Missing audit logging'
                ]),
                'severity': severity,
                'description': f'{severity} severity security issue detected in {resource["name"]}',
                'detected_at': (datetime.now() - timedelta(hours=random.randint(1, 168))).isoformat(),
                'remediation_steps': self.generate_remediation(severity) if 'self' in locals() else f'Fix the {severity.lower()} severity issue immediately',
                'estimated_risk_score': {'Critical': 9, 'High': 7, 'Medium': 4, 'Low': 2}.get(severity, 5)
            }
            misconfigs.append(misconfig)
        
        # Cost data with optimization potential
        savings = 0
        recommendation = 'Optimized'
        if resource['status'] == 'idle':
            savings = monthly_cost * 0.7
            recommendation = 'Resource is idle - consider stopping or downsizing'
        elif resource['status'] == 'stopped':
            savings = monthly_cost * 0.9
            recommendation = 'Resource is stopped - consider deletion if not needed'
        elif random.random() > 0.8:
            savings = monthly_cost * random.uniform(0.1, 0.4)
            recommendation = 'Consider rightsizing or moving to reserved instances'
        
        cost_item = {
            'resource_id': resource['id'],
            'resource_name': resource['name'],
            'hourly_cost': hourly_cost,
            'daily_cost': round(hourly_cost * 24, 2),
            'monthly_cost': round(monthly_cost, 2),
            'optimization_potential': round(savings, 2),
            'optimization_recommendation': recommendation
        }
        cost_data.append(cost_item)
        
        total_cost += monthly_cost
        total_savings += savings
    
    return {
        'resources': resources,
        'misconfigurations': misconfigs,
        'cost_data': cost_data,
        'generated_at': datetime.now().isoformat(),
        'summary': {
            'total_resources': len(resources),
            'total_misconfigurations': len(misconfigs),
            'critical_misconfigurations': len([m for m in misconfigs if m['severity'] == 'Critical']),
            'high_misconfigurations': len([m for m in misconfigs if m['severity'] == 'High']),
            'total_monthly_cost': round(total_cost, 2),
            'total_optimization_potential': round(total_savings, 2)
        }
    }

def generate_remediation(severity):
    """Generate remediation steps based on severity"""
    remediations = {
        'Critical': 'IMMEDIATE ACTION: Restrict public access, rotate credentials, apply security patches, and enable monitoring',
        'High': 'HIGH PRIORITY: Update security group rules, enable encryption, review IAM policies within 24 hours',
        'Medium': 'MEDIUM PRIORITY: Implement logging, remove unused resources, update configurations this week',
        'Low': 'LOW PRIORITY: Follow best practices, document changes, plan for next sprint'
    }
    return remediations.get(severity, 'Follow security best practices')

# Generate data
print("Generating sample cloud data...")
cloud_data = generate_sample_data()
print(f"✅ Generated {cloud_data['summary']['total_resources']} resources")
print(f"⚠️ Found {cloud_data['summary']['total_misconfigurations']} misconfigurations")
print(f"💰 Total monthly cost: ${cloud_data['summary']['total_monthly_cost']:,.2f}")
print(f"💡 Potential savings: ${cloud_data['summary']['total_optimization_potential']:,.2f}")

# Routes
@app.route('/', methods=['GET'])
def home():
    """API Information"""
    return jsonify({
        'name': 'Cloud Security Copilot API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'health': '/api/health',
            'summary': '/api/summary',
            'security_analysis': '/api/security/analysis',
            'cost_analysis': '/api/cost/analysis',
            'recommendations': '/api/recommendations',
            'resources': '/api/resources',
            'regenerate_data': '/api/regenerate-data (POST)'
        }
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'data_loaded': True,
        'timestamp': datetime.now().isoformat(),
        'resources_count': cloud_data['summary']['total_resources']
    })

@app.route('/api/summary', methods=['GET'])
def get_summary():
    """Get summary statistics"""
    return jsonify({
        'summary': cloud_data['summary'],
        'generated_at': cloud_data['generated_at']
    })

@app.route('/api/security/analysis', methods=['GET'])
def get_security_analysis():
    """Get security analysis"""
    # Group by severity
    severity_counts = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0}
    type_counts = {}
    
    for m in cloud_data['misconfigurations']:
        severity_counts[m['severity']] += 1
        type_counts[m['type']] = type_counts.get(m['type'], 0) + 1
    
    top_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    # Calculate risk score
    risk_weights = {'Critical': 10, 'High': 7, 'Medium': 4, 'Low': 2}
    total_weighted_score = sum(severity_counts[s] * risk_weights[s] for s in severity_counts)
    total_misconfigs = len(cloud_data['misconfigurations'])
    risk_score = total_weighted_score / total_misconfigs if total_misconfigs > 0 else 0
    
    # Generate smart insights
    insights = []
    if severity_counts['Critical'] > 0:
        insights.append(f"⚠️ CRITICAL: {severity_counts['Critical']} critical security issues require immediate action!")
    if severity_counts['High'] > 0:
        insights.append(f"🔴 HIGH RISK: {severity_counts['High']} high severity issues need attention within 24 hours")
    
    insights.append("💡 Best Practice: Implement Infrastructure as Code (IaC) scanning")
    insights.append("🔒 Recommendation: Enable cloud-native security services (AWS Config, Azure Policy)")
    insights.append("📈 Tip: Set up automated remediation for common misconfigurations")
    insights.append("🎯 Priority: Focus on fixing issues with highest risk scores first")
    
    # Generate recommendations
    recommendations = []
    if severity_counts['Critical'] > 0:
        recommendations.append(f"⚠️ IMMEDIATE ACTION: Address {severity_counts['Critical']} critical issues right now")
    if severity_counts['High'] > 0:
        recommendations.append(f"🔴 HIGH PRIORITY: Fix {severity_counts['High']} high severity issues within 24 hours")
    if top_types:
        recommendations.append(f"📊 Focus Areas: {', '.join([t[0] for t in top_types[:3]])}")
    
    recommendations.append("🛡️ Enable automated security scanning in CI/CD pipeline")
    recommendations.append("📝 Turn on CloudTrail/Azure Monitor for comprehensive audit logging")
    recommendations.append("🔐 Implement least privilege access principle across all IAM roles")
    
    # Critical findings
    critical_findings = [m for m in cloud_data['misconfigurations'] if m['severity'] in ['Critical', 'High']]
    
    return jsonify({
        'severity_distribution': severity_counts,
        'top_misconfiguration_types': [{'type': t, 'count': c} for t, c in top_types],
        'total_misconfigurations': total_misconfigs,
        'overall_risk_score': round(risk_score, 2),
        'risk_level': 'Critical' if risk_score >= 7 else 'High' if risk_score >= 5 else 'Medium' if risk_score >= 3 else 'Low',
        'critical_findings': critical_findings[:10],  # Limit to top 10
        'ai_insights': insights,
        'recommendations': recommendations,
        'analyzed_at': datetime.now().isoformat()
    })

@app.route('/api/cost/analysis', methods=['GET'])
def get_cost_analysis():
    """Get cost analysis"""
    total_cost = cloud_data['summary']['total_monthly_cost']
    total_savings = cloud_data['summary']['total_optimization_potential']
    
    expensive = sorted(cloud_data['cost_data'], key=lambda x: x['monthly_cost'], reverse=True)[:5]
    opportunities = sorted([c for c in cloud_data['cost_data'] if c['optimization_potential'] > 0], 
                          key=lambda x: x['optimization_potential'], reverse=True)[:5]
    
    cost_by_type = {}
    for cost in cloud_data['cost_data']:
        resource_type = cost['resource_name'].split('-')[1] if '-' in cost['resource_name'] else 'Other'
        cost_by_type[resource_type] = cost_by_type.get(resource_type, 0) + cost['monthly_cost']
    
    # Sort by cost
    cost_by_type = dict(sorted(cost_by_type.items(), key=lambda x: x[1], reverse=True))
    
    plan = []
    if total_savings > 0:
        plan.append(f"💰 Potential savings: ${total_savings:,.2f} per month ({round(total_savings/total_cost*100, 1)}% reduction)")
    plan.append("🎯 Quick Wins: Stop or delete idle resources immediately")
    plan.append("📊 Implement auto-scaling to match demand")
    plan.append("🏷️ Add proper tagging for better cost allocation")
    plan.append("💎 Consider reserved instances for stable workloads")
    
    return jsonify({
        'total_monthly_cost': round(total_cost, 2),
        'total_optimization_potential': round(total_savings, 2),
        'potential_savings_percentage': round(total_savings / total_cost * 100, 1) if total_cost > 0 else 0,
        'top_expensive_resources': expensive,
        'top_optimization_opportunities': opportunities,
        'cost_by_resource_type': cost_by_type,
        'optimization_plan': plan,
        'analyzed_at': datetime.now().isoformat()
    })

@app.route('/api/resources', methods=['GET'])
def get_resources():
    """Get all resources"""
    return jsonify({
        'resources': cloud_data['resources'],
        'total': len(cloud_data['resources'])
    })

@app.route('/api/misconfigurations', methods=['GET'])
def get_misconfigurations():
    """Get all misconfigurations with optional filtering"""
    severity = request.args.get('severity')
    misconfigs = cloud_data['misconfigurations']
    
    if severity:
        misconfigs = [m for m in misconfigs if m['severity'].lower() == severity.lower()]
    
    return jsonify({
        'misconfigurations': misconfigs,
        'total': len(misconfigs)
    })

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    """Get combined recommendations"""
    security_analysis = get_security_analysis().get_json()
    cost_analysis = get_cost_analysis().get_json()
    
    return jsonify({
        'security_recommendations': security_analysis['recommendations'][:5],
        'cost_recommendations': cost_analysis['optimization_plan'][:5],
        'critical_issues': len(security_analysis['critical_findings']),
        'potential_savings': cost_analysis['total_optimization_potential'],
        'priority_actions': [
            f"Fix {security_analysis['severity_distribution']['Critical']} critical security issues",
            f"Implement cost savings of ${cost_analysis['total_optimization_potential']:,.2f}/month",
            "Enable automated security scanning",
            "Review and optimize resource utilization"
        ]
    })

@app.route('/api/regenerate-data', methods=['POST'])
def regenerate_data():
    """Regenerate simulated data"""
    global cloud_data
    cloud_data = generate_sample_data()
    return jsonify({
        'message': 'Data regenerated successfully',
        'summary': cloud_data['summary']
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Cloud Security Copilot - AI-Powered Risk & Cost Optimization")
    print("="*60)
    print(f"📍 Backend API: http://localhost:5001")
    print(f"📍 Health Check: http://localhost:5001/api/health")
    print(f"📍 API Documentation: http://localhost:5001/")
    print("="*60)
    print("\n✅ Server is ready! Press Ctrl+C to stop\n")
    app.run(debug=True, port=5001, host='0.0.0.0')