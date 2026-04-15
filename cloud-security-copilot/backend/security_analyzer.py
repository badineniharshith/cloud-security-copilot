import json
from typing import Dict, List, Any
from datetime import datetime

class SecurityAnalyzer:
    def __init__(self, api_key=None):
        """Initialize security analyzer"""
        self.use_ai = False
    
    def analyze_misconfigurations(self, misconfigurations: List[Dict]) -> Dict[str, Any]:
        """Analyze misconfigurations and generate insights"""
        # Group by severity
        severity_counts = {
            'Critical': 0,
            'High': 0,
            'Medium': 0,
            'Low': 0
        }
        
        # Group by type
        type_counts = {}
        
        for misconfig in misconfigurations:
            severity_counts[misconfig['severity']] += 1
            config_type = misconfig['type']
            type_counts[config_type] = type_counts.get(config_type, 0) + 1
        
        # Sort and get top 5 misconfiguration types
        top_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Calculate overall risk score
        risk_weights = {'Critical': 10, 'High': 7, 'Medium': 4, 'Low': 2}
        total_weighted_score = sum(
            count * risk_weights[severity] 
            for severity, count in severity_counts.items()
        )
        total_misconfigs = len(misconfigurations)
        overall_risk_score = total_weighted_score / total_misconfigs if total_misconfigs > 0 else 0
        
        # Generate AI insights (simplified without OpenAI)
        ai_insights = [
            "🔍 Focus on fixing critical and high severity issues first",
            "🔄 Implement automated security scanning in your CI/CD pipeline",
            "🔐 Review and enforce least privilege access for all IAM roles",
            "📊 Set up real-time security monitoring and alerting",
            "🎯 Prioritize remediation based on risk score and business impact"
        ]
        
        # Generate recommendations
        recommendations = self._generate_recommendations(severity_counts, top_types)
        
        return {
            'severity_distribution': severity_counts,
            'top_misconfiguration_types': [{'type': t, 'count': c} for t, c in top_types],
            'total_misconfigurations': total_misconfigs,
            'overall_risk_score': round(overall_risk_score, 2),
            'risk_level': self._get_risk_level(overall_risk_score),
            'critical_findings': [m for m in misconfigurations if m['severity'] in ['Critical', 'High']],
            'ai_insights': ai_insights,
            'recommendations': recommendations,
            'analyzed_at': datetime.now().isoformat()
        }
    
    def _generate_recommendations(self, severity_counts: Dict, top_types: List) -> List[str]:
        """Generate security recommendations based on findings"""
        recommendations = []
        
        if severity_counts['Critical'] > 0:
            recommendations.append(f"⚠️ IMMEDIATE ACTION: Address {severity_counts['Critical']} critical security issues right now")
        
        if severity_counts['High'] > 0:
            recommendations.append(f"🔴 HIGH PRIORITY: Review and fix {severity_counts['High']} high severity misconfigurations within 24 hours")
        
        if top_types:
            recommendations.append(f"📊 Focus Areas: {', '.join([t[0] for t in top_types[:3]])}")
        
        recommendations.append("🛡️ Implement automated security scanning in CI/CD pipeline")
        recommendations.append("📝 Enable comprehensive audit logging for all resources")
        recommendations.append("🔐 Implement least privilege access principle across all IAM roles")
        recommendations.append("🔄 Set up regular security compliance checks")
        
        return recommendations
    
    def _get_risk_level(self, score: float) -> str:
        """Determine risk level based on score"""
        if score >= 7:
            return "Critical Risk"
        elif score >= 5:
            return "High Risk"
        elif score >= 3:
            return "Medium Risk"
        else:
            return "Low Risk"