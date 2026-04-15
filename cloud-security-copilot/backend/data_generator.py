import json
import random
from datetime import datetime, timedelta
import uuid

class CloudDataGenerator:
    def __init__(self):
        self.cloud_providers = ['AWS', 'Azure', 'GCP']
        self.resource_types = {
            'AWS': ['EC2', 'S3', 'RDS', 'Lambda', 'EKS'],
            'Azure': ['VM', 'Blob', 'SQL', 'Functions', 'AKS'],
            'GCP': ['Compute', 'Storage', 'SQL', 'Functions', 'GKE']
        }
        self.severity_levels = ['Critical', 'High', 'Medium', 'Low']
        self.misconfigurations = [
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
        ]
    
    def generate_resources(self, count=50):
        resources = []
        for _ in range(count):
            provider = random.choice(self.cloud_providers)
            resource = {
                'id': str(uuid.uuid4()),
                'name': f"{provider}-{random.choice(self.resource_types[provider])}-{random.randint(1000, 9999)}",
                'provider': provider,
                'type': random.choice(self.resource_types[provider]),
                'region': random.choice(['us-east-1', 'us-west-2', 'eu-west-1', 'ap-southeast-1']),
                'created_at': (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(),
                'cost_per_hour': round(random.uniform(0.01, 5.0), 2),
                'status': random.choice(['active', 'idle', 'stopped']),
                'tags': self.generate_tags()
            }
            resources.append(resource)
        return resources
    
    def generate_tags(self):
        tags = {}
        if random.random() > 0.7:
            tags['environment'] = random.choice(['prod', 'staging', 'dev'])
        if random.random() > 0.8:
            tags['owner'] = f"team-{random.choice(['platform', 'data', 'app', 'security'])}"
        return tags
    
    def generate_misconfigurations(self, resources):
        misconfigs = []
        for resource in resources:
            # Generate 0-3 misconfigurations per resource
            num_misconfigs = random.randint(0, 3)
            for _ in range(num_misconfigs):
                severity = random.choices(self.severity_levels, weights=[0.1, 0.2, 0.3, 0.4])[0]
                misconfig = {
                    'id': str(uuid.uuid4()),
                    'resource_id': resource['id'],
                    'resource_name': resource['name'],
                    'type': random.choice(self.misconfigurations),
                    'severity': severity,
                    'description': self.generate_description(severity),
                    'detected_at': (datetime.now() - timedelta(hours=random.randint(1, 168))).isoformat(),
                    'remediation_steps': self.generate_remediation(severity),
                    'estimated_risk_score': self.calculate_risk_score(severity)
                }
                misconfigs.append(misconfig)
        return misconfigs
    
    def generate_description(self, severity):
        descriptions = {
            'Critical': 'Immediate security threat detected. Potential for data breach or unauthorized access.',
            'High': 'Significant security risk. Could lead to serious security incidents if exploited.',
            'Medium': 'Moderate security concern. Should be addressed in regular maintenance cycles.',
            'Low': 'Minor security best practice violation. Recommended to fix for compliance.'
        }
        return descriptions.get(severity, 'Security misconfiguration detected')
    
    def generate_remediation(self, severity):
        remediations = {
            'Critical': 'Immediate action required: Restrict public access, rotate credentials, and apply security patches.',
            'High': 'High priority: Update security group rules, enable encryption, and review IAM policies.',
            'Medium': 'Medium priority: Implement logging, remove unused resources, and update configurations.',
            'Low': 'Low priority: Follow best practices, document changes, and plan for next sprint.'
        }
        return remediations.get(severity, 'Follow security best practices')
    
    def calculate_risk_score(self, severity):
        scores = {'Critical': 9, 'High': 7, 'Medium': 4, 'Low': 2}
        return scores.get(severity, 5)
    
    def generate_cost_data(self, resources):
        cost_data = []
        for resource in resources:
            daily_cost = resource['cost_per_hour'] * 24
            monthly_cost = daily_cost * 30
            
            # Calculate optimization potential
            optimization_potential = 0
            if resource['status'] == 'idle':
                optimization_potential = monthly_cost * 0.8  # 80% savings if stopped
            elif resource['status'] == 'stopped':
                optimization_potential = monthly_cost * 0.95  # 95% savings if deleted
            elif random.random() > 0.8:
                optimization_potential = monthly_cost * random.uniform(0.1, 0.5)
            
            cost_data.append({
                'resource_id': resource['id'],
                'resource_name': resource['name'],
                'hourly_cost': resource['cost_per_hour'],
                'daily_cost': round(daily_cost, 2),
                'monthly_cost': round(monthly_cost, 2),
                'optimization_potential': round(optimization_potential, 2),
                'optimization_recommendation': self.get_optimization_recommendation(resource, optimization_potential)
            })
        return cost_data
    
    def get_optimization_recommendation(self, resource, potential):
        if resource['status'] == 'idle':
            return 'Resource is idle - consider stopping or downsizing'
        elif resource['status'] == 'stopped':
            return 'Resource is stopped - consider deletion if not needed'
        elif potential > 0:
            return 'Consider rightsizing or moving to reserved instances'
        return 'Currently optimized'
    
    def generate_complete_dataset(self):
        resources = self.generate_resources(50)
        misconfigurations = self.generate_misconfigurations(resources)
        cost_data = self.generate_cost_data(resources)
        
        return {
            'resources': resources,
            'misconfigurations': misconfigurations,
            'cost_data': cost_data,
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_resources': len(resources),
                'total_misconfigurations': len(misconfigurations),
                'critical_misconfigurations': len([m for m in misconfigurations if m['severity'] == 'Critical']),
                'high_misconfigurations': len([m for m in misconfigurations if m['severity'] == 'High']),
                'total_monthly_cost': sum(c['monthly_cost'] for c in cost_data),
                'total_optimization_potential': sum(c['optimization_potential'] for c in cost_data)
            }
        }

# Generate and save sample data
if __name__ == "__main__":
    generator = CloudDataGenerator()
    data = generator.generate_complete_dataset()
    
    with open('../data/simulated_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("Sample data generated successfully!")