from typing import Dict, List, Any
from datetime import datetime

class CostOptimizer:
    def __init__(self):
        pass
    
    def analyze_costs(self, cost_data: List[Dict]) -> Dict[str, Any]:
        """Analyze cost data and generate optimization insights"""
        total_monthly_cost = sum(c['monthly_cost'] for c in cost_data)
        total_optimization_potential = sum(c['optimization_potential'] for c in cost_data)
        
        # Find top 5 most expensive resources
        expensive_resources = sorted(cost_data, key=lambda x: x['monthly_cost'], reverse=True)[:5]
        
        # Find top optimization opportunities
        optimization_opportunities = sorted(
            [c for c in cost_data if c['optimization_potential'] > 0],
            key=lambda x: x['optimization_potential'],
            reverse=True
        )[:5]
        
        # Group by resource type for cost analysis
        cost_by_type = {}
        for cost in cost_data:
            # Extract resource type from name (simplified)
            resource_type = cost['resource_name'].split('-')[1] if '-' in cost['resource_name'] else 'Other'
            cost_by_type[resource_type] = cost_by_type.get(resource_type, 0) + cost['monthly_cost']
        
        # Calculate potential savings percentage
        savings_percentage = (total_optimization_potential / total_monthly_cost * 100) if total_monthly_cost > 0 else 0
        
        # Generate optimization plan
        optimization_plan = self._generate_optimization_plan(optimization_opportunities, savings_percentage)
        
        return {
            'total_monthly_cost': round(total_monthly_cost, 2),
            'total_optimization_potential': round(total_optimization_potential, 2),
            'potential_savings_percentage': round(savings_percentage, 1),
            'top_expensive_resources': expensive_resources,
            'top_optimization_opportunities': optimization_opportunities,
            'cost_by_resource_type': cost_by_type,
            'optimization_plan': optimization_plan,
            'analyzed_at': datetime.now().isoformat()
        }
    
    def _generate_optimization_plan(self, opportunities: List[Dict], savings_percentage: float) -> List[str]:
        """Generate actionable optimization recommendations"""
        plan = []
        
        if savings_percentage > 20:
            plan.append(f"🚀 Significant savings opportunity: {savings_percentage}% potential reduction")
        
        if opportunities:
            plan.append(f"💰 Quick wins: Implement top {len(opportunities[:3])} recommendations immediately")
        
        for opp in opportunities[:3]:
            plan.append(f"   • {opp['resource_name']}: {opp['optimization_recommendation']} (Save ${opp['optimization_potential']}/month)")
        
        plan.append("📊 Implement automated rightsizing recommendations")
        plan.append("🎯 Consider reserved instances for stable workloads")
        plan.append("🗑️ Regularly review and delete unused resources")
        plan.append("📈 Set up budget alerts and cost anomaly detection")
        
        return plan
    
    def generate_cost_report(self, cost_analysis: Dict) -> str:
        """Generate a human-readable cost report"""
        report = f"""
COST OPTIMIZATION REPORT
{'='*50}

TOTAL MONTHLY COST: ${cost_analysis['total_monthly_cost']:,.2f}
OPTIMIZATION POTENTIAL: ${cost_analysis['total_optimization_potential']:,.2f}
POTENTIAL SAVINGS: {cost_analysis['potential_savings_percentage']}%

TOP EXPENSIVE RESOURCES:
"""
        for resource in cost_analysis['top_expensive_resources'][:3]:
            report += f"  • {resource['resource_name']}: ${resource['monthly_cost']:,.2f}/month\n"
        
        report += f"""
TOP OPTIMIZATION OPPORTUNITIES:
"""
        for opp in cost_analysis['top_optimization_opportunities'][:3]:
            report += f"  • {opp['resource_name']}: {opp['optimization_recommendation']} (Save ${opp['optimization_potential']:,.2f})\n"
        
        return report