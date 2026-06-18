from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class TelematicsRisk(str, Enum):
    LOW = "Low"
    MED = "Med"
    HIGH = "High"

class Severity(str, Enum):
    LOW = "Low"
    MED = "Med"
    HIGH = "High"

class FloodZone(str, Enum):
    LOW = "Low"
    MED = "Med"
    HIGH = "High"

class Territory(str, Enum):
    URBAN_KL_SELANGOR_PENANG_JOHOR = "Urban (KL, Selangor, Penang, Johor)"
    URBAN_OTHER = "Urban (Other)"
    RURAL_WEST_MALAYSIA = "Rural (West Malaysia)"
    RURAL_EAST_MALAYSIA = "Rural (East Malaysia)"

class VehicleCategory(str, Enum):
    PRIVATE_CAR = "Private Car"
    COMMERCIAL_PICKUP = "Commercial Pickup"
    LUXURY_CAR = "Luxury Car"

class ValuationType(str, Enum):
    AGREED_VALUE = "Agreed Value"
    MARKET_VALUE = "Market Value"

class UsageType(str, Enum):
    PRIVATE = "Private"
    COMMERCIAL = "Commercial"
    EHAILING_COMMERCIAL = "E-hailing Commercial"

class NCDPercentage(float, Enum):
    NCD_0 = 0.0
    NCD_25 = 25.0
    NCD_30 = 30.0
    NCD_38_33 = 38.33
    NCD_45 = 45.0
    NCD_55 = 55.0

class QuoteRequest(BaseModel):
    # Driver factors
    driver_age: int = Field(..., ge=17, le=90, description="Driver age between 17 and 90")
    traffic_violations: int = Field(default=0, ge=0)
    telematics_risk: TelematicsRisk = Field(default=TelematicsRisk.LOW)
    
    # Claims factors
    ncd_percentage: NCDPercentage
    prior_claims_count: int = Field(default=0, ge=0)
    average_prior_severity: Severity = Field(default=Severity.LOW)
    
    # Geographic factors
    territory: Territory
    flood_zone: FloodZone
    
    # Vehicle factors
    vehicle_value: float = Field(..., gt=0)
    engine_capacity: int = Field(..., gt=0)
    vehicle_category: VehicleCategory
    valuation_type: ValuationType
    vehicle_age: int = Field(default=0, ge=0)
    
    # Usage factors
    annual_mileage: int = Field(default=10000, ge=0)
    usage_type: UsageType
    
    # Add-ons
    windscreen_cover: bool = Field(default=False)
    ncd_protector: bool = Field(default=False)
    special_perils_cover: bool = Field(default=False)
