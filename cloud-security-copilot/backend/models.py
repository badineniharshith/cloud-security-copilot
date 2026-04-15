from datetime import datetime
from typing import List, Dict, Optional, Any
from enum import Enum
from dataclasses import dataclass, asdict
import json

class Severity(Enum):
    """Security severity levels"""
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class CloudProvider(Enum):
    """Supported cloud providers"""
    AWS = "AWS"
    AZURE = "Azure"
    GCP = "GCP"

class ResourceStatus(Enum):
    """Resource operational status"""
    ACTIVE = "active"
    IDLE = "idle"
    STOPPED = "stopped"
    TERMINATED = "terminated"

class ResourceType(Enum):
    """Cloud resource types"""
    # AWS
    EC2 = "EC2"
    S3 = "S3"
    RDS = "RDS"
    LAMBDA = "Lambda"
    EKS = "EKS"
    # Azure
    VM = "VM"
    BLOB = "Blob"
    SQL = "SQL"
    FUNCTIONS = "Functions"
    AKS = "AKS"
    # GCP
    COMPUTE = "Compute"
    STORAGE = "Storage"
    CLOUD_SQL = "Cloud SQL"
    CLOUD_FUNCTIONS = "Cloud Functions"
    GKE = "GKE"

@dataclass
class ResourceTag:
    """Resource metadata tags"""
    key: str
    value: str
    
    def to_dict(self):
        return {self.key: self.value}

@dataclass
class CloudResource:
    """Cloud resource model"""
    id: str
    name: str
    provider: CloudProvider
    type: ResourceType
    region: str
    created_at: datetime
    cost_per_hour: float
    status: ResourceStatus
    tags: Dict[str, str]
    
    def __post_init__(self):
        """Convert string enums to proper enum types if needed"""
        if isinstance(self.provider, str):
            self.provider = CloudProvider(self.provider)
        if isinstance(self.type, str):
            self.type = ResourceType(self.type)
        if isinstance(self.status, str):
            self.status = ResourceStatus(self.status)
        if isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(self.created_at)
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'provider': self.provider.value,
            'type': self.type.value,
            'region': self.region,
            'created_at': self.created_at.isoformat(),
            'cost_per_hour': self.cost_per_hour,
            'status': self.status.value,
            'tags': self.tags
        }
    
    def calculate_monthly_cost(self) -> float:
        """Calculate monthly cost (30 days)"""
        return self.cost_per_hour * 24 * 30
    
    def is_idle(self) -> bool:
        """Check if resource is idle based on status and age"""
        if self.status == ResourceStatus.IDLE:
            return True
        # Consider resources older than 30 days without active tags as idle
        if self.status == ResourceStatus.ACTIVE:
            days_old = (datetime.now() - self.created_at).days
            if days_old > 30 and not self.tags.get('environment') == 'prod':
                return True
        return False

@dataclass
class Misconfiguration:
    """Security misconfiguration model"""
    id: str
    resource_id: str
    resource_name: str
    type: str
    severity: Severity
    description: str
    detected_at: datetime
    remediation_steps: str
    estimated_risk_score: int
    
    def __post_init__(self):
        """Convert string enums to proper enum types if needed"""
        if isinstance(self.severity, str):
            self.severity = Severity(self.severity)
        if isinstance(self.detected_at, str):
            self.detected_at = datetime.fromisoformat(self.detected_at)
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'resource_id': self.resource_id,
            'resource_name': self.resource_name,
            'type': self.type,
            'severity': self.severity.value,
            'description': self.description,
            'detected_at': self.detected_at.isoformat(),
            'remediation_steps': self.remediation_steps,
            'estimated_risk_score': self.estimated_risk_score
        }
    
    def get_priority(self) -> int:
        """Get priority level (higher = more urgent)"""
        priority_map = {
            Severity.CRITICAL: 4,
            Severity.HIGH: 3,
            Severity.MEDIUM: 2,
            Severity.LOW: 1
        }
        return priority_map.get(self.severity, 0)

@dataclass
class CostData:
    """Resource cost data model"""
    resource_id: str
    resource_name: str
    hourly_cost: float
    daily_cost: float
    monthly_cost: float
    optimization_potential: float
    optimization_recommendation: str
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'resource_id': self.resource_id,
            'resource_name': self.resource_name,
            'hourly_cost': self.hourly_cost,
            'daily_cost': self.daily_cost,
            'monthly_cost': self.monthly_cost,
            'optimization_potential': self.optimization_potential,
            'optimization_recommendation': self.optimization_recommendation
        }
    
    def get_savings_percentage(self) -> float:
        """Calculate savings percentage"""
        if self.monthly_cost > 0:
            return (self.optimization_potential / self.monthly_cost) * 100
        return 0

@dataclass
class SecurityAnalysisResult:
    """Security analysis result model"""
    severity_distribution: Dict[str, int]
    top_misconfiguration_types: List[Dict[str, Any]]
    total_misconfigurations: int
    overall_risk_score: float
    risk_level: str
    critical_findings: List[Misconfiguration]
    ai_insights: List[str]
    recommendations: List[str]
    analyzed_at: datetime
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'severity_distribution': self.severity_distribution,
            'top_misconfiguration_types': self.top_misconfiguration_types,
            'total_misconfigurations': self.total_misconfigurations,
            'overall_risk_score': self.overall_risk_score,
            'risk_level': self.risk_level,
            'critical_findings': [f.to_dict() for f in self.critical_findings],
            'ai_insights': self.ai_insights,
            'recommendations': self.recommendations,
            'analyzed_at': self.analyzed_at.isoformat()
        }

@dataclass
class CostAnalysisResult:
    """Cost analysis result model"""
    total_monthly_cost: float
    total_optimization_potential: float
    potential_savings_percentage: float
    top_expensive_resources: List[CostData]
    top_optimization_opportunities: List[CostData]
    cost_by_resource_type: Dict[str, float]
    optimization_plan: List[str]
    analyzed_at: datetime
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'total_monthly_cost': self.total_monthly_cost,
            'total_optimization_potential': self.total_optimization_potential,
            'potential_savings_percentage': self.potential_savings_percentage,
            'top_expensive_resources': [r.to_dict() for r in self.top_expensive_resources],
            'top_optimization_opportunities': [o.to_dict() for o in self.top_optimization_opportunities],
            'cost_by_resource_type': self.cost_by_resource_type,
            'optimization_plan': self.optimization_plan,
            'analyzed_at': self.analyzed_at.isoformat()
        }

@dataclass
class CloudEnvironment:
    """Complete cloud environment model"""
    resources: List[CloudResource]
    misconfigurations: List[Misconfiguration]
    cost_data: List[CostData]
    generated_at: datetime
    summary: Dict[str, Any]
    
    def __post_init__(self):
        """Convert string dates to datetime objects"""
        if isinstance(self.generated_at, str):
            self.generated_at = datetime.fromisoformat(self.generated_at)
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return {
            'resources': [r.to_dict() for r in self.resources],
            'misconfigurations': [m.to_dict() for m in self.misconfigurations],
            'cost_data': [c.to_dict() for c in self.cost_data],
            'generated_at': self.generated_at.isoformat(),
            'summary': self.summary
        }
    
    def get_resources_by_provider(self, provider: CloudProvider) -> List[CloudResource]:
        """Get resources filtered by provider"""
        return [r for r in self.resources if r.provider == provider]
    
    def get_resources_by_type(self, resource_type: ResourceType) -> List[CloudResource]:
        """Get resources filtered by type"""
        return [r for r in self.resources if r.type == resource_type]
    
    def get_misconfigurations_by_severity(self, severity: Severity) -> List[Misconfiguration]:
        """Get misconfigurations filtered by severity"""
        return [m for m in self.misconfigurations if m.severity == severity]
    
    def get_total_cost(self) -> float:
        """Calculate total monthly cost"""
        return sum(c.monthly_cost for c in self.cost_data)
    
    def get_total_optimization_potential(self) -> float:
        """Calculate total optimization potential"""
        return sum(c.optimization_potential for c in self.cost_data)

class ValidationError(Exception):
    """Custom validation error"""
    pass

class DataValidator:
    """Data validation utilities"""
    
    @staticmethod
    def validate_resource(resource: Dict) -> bool:
        """Validate resource data"""
        required_fields = ['id', 'name', 'provider', 'type', 'region', 
                          'created_at', 'cost_per_hour', 'status']
        
        for field in required_fields:
            if field not in resource:
                raise ValidationError(f"Missing required field: {field}")
        
        # Validate cost is positive
        if resource['cost_per_hour'] < 0:
            raise ValidationError("cost_per_hour must be non-negative")
        
        # Validate provider is supported
        if resource['provider'] not in [p.value for p in CloudProvider]:
            raise ValidationError(f"Unsupported provider: {resource['provider']}")
        
        return True
    
    @staticmethod
    def validate_misconfiguration(misconfig: Dict) -> bool:
        """Validate misconfiguration data"""
        required_fields = ['id', 'resource_id', 'resource_name', 'type', 
                          'severity', 'description', 'detected_at', 
                          'remediation_steps', 'estimated_risk_score']
        
        for field in required_fields:
            if field not in misconfig:
                raise ValidationError(f"Missing required field: {field}")
        
        # Validate risk score range
        if not 0 <= misconfig['estimated_risk_score'] <= 10:
            raise ValidationError("estimated_risk_score must be between 0 and 10")
        
        # Validate severity
        if misconfig['severity'] not in [s.value for s in Severity]:
            raise ValidationError(f"Invalid severity: {misconfig['severity']}")
        
        return True
    
    @staticmethod
    def validate_cost_data(cost: Dict) -> bool:
        """Validate cost data"""
        required_fields = ['resource_id', 'resource_name', 'hourly_cost', 
                          'daily_cost', 'monthly_cost', 'optimization_potential']
        
        for field in required_fields:
            if field not in cost:
                raise ValidationError(f"Missing required field: {field}")
        
        # Validate costs are non-negative
        if any(cost[field] < 0 for field in ['hourly_cost', 'daily_cost', 
                                               'monthly_cost', 'optimization_potential']):
            raise ValidationError("Cost values must be non-negative")
        
        return True

# Example usage and testing
if __name__ == "__main__":
    # Test the models
    from datetime import datetime, timedelta
    import uuid
    
    # Create a sample resource
    sample_resource = CloudResource(
        id=str(uuid.uuid4()),
        name="test-ec2-instance",
        provider=CloudProvider.AWS,
        type=ResourceType.EC2,
        region="us-east-1",
        created_at=datetime.now() - timedelta(days=10),
        cost_per_hour=0.42,
        status=ResourceStatus.ACTIVE,
        tags={"environment": "prod", "owner": "team-platform"}
    )
    
    print("Sample Resource:")
    print(json.dumps(sample_resource.to_dict(), indent=2))
    print(f"Monthly Cost: ${sample_resource.calculate_monthly_cost():.2f}")
    print(f"Is Idle: {sample_resource.is_idle()}")
    
    # Create a sample misconfiguration
    sample_misconfig = Misconfiguration(
        id=str(uuid.uuid4()),
        resource_id=sample_resource.id,
        resource_name=sample_resource.name,
        type="Publicly accessible security group",
        severity=Severity.HIGH,
        description="Security group allows inbound traffic from 0.0.0.0/0 on port 22",
        detected_at=datetime.now(),
        remediation_steps="Restrict SSH access to specific IP ranges",
        estimated_risk_score=7
    )
    
    print("\nSample Misconfiguration:")
    print(json.dumps(sample_misconfig.to_dict(), indent=2))
    print(f"Priority: {sample_misconfig.get_priority()}")
    
    # Test validation
    validator = DataValidator()
    try:
        validator.validate_resource(sample_resource.to_dict())
        print("\n✓ Resource validation passed")
    except ValidationError as e:
        print(f"\n✗ Validation failed: {e}")