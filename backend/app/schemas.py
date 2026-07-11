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

class AssemblyType(str, Enum):
    CBU = "CBU"
    CKD = "CKD"

class NCDPercentage(float, Enum):
    NCD_0 = 0.0
    NCD_25 = 25.0
    NCD_30 = 30.0
    NCD_38_33 = 38.33
    NCD_45 = 45.0
    NCD_55 = 55.0

# ----------------- 23 NEW SCHEMA GAPS ENUMS -----------------

class Gender(str, Enum):
    MALE = "M"
    FEMALE = "F"

class YearsLicensed(str, Enum):
    LESS_THAN_2 = "<2 years"
    TWO_TO_FOUR = "2-4 years"
    FIVE_PLUS = "5+ years"

class Occupation(str, Enum):
    PROFESSIONAL = "Professional/Exec"
    CLERICAL = "Clerical/Sales"
    MANUAL = "Manual/Delivery"

class PreviousClaims3Yr(str, Enum):
    ZERO = "0 claims"
    ONE = "1 claim"
    TWO_PLUS = "2+ claims"

class ModificationStatus(str, Enum):
    STANDARD = "Stock/standard"
    MINOR = "Minor mods"
    MAJOR = "Major mods"

class SafetyFeatures(str, Enum):
    ADVANCED = "ADAS, AEB, ESC"
    SOME = "Some safety"
    MINIMAL = "Minimal"

class TyreCondition(str, Enum):
    GOOD = "New/good"
    MODERATE = "Moderate"
    WORN = "Worn/illegal"

class ParkingNight(str, Enum):
    GARAGED = "Garaged"
    DRIVEWAY = "Driveway/carpark"
    STREET = "Street parking"

class AnnualTrips(str, Enum):
    LOW = "<5,000"
    MEDIUM = "5,000-10,000"
    HIGH = ">10,000"

class FaultProfile(str, Enum):
    NOT_AT_FAULT = "Not at fault"
    PARTIAL = "Partial fault"
    AT_FAULT = "At fault"

class FraudIndicators(str, Enum):
    NONE = "None"
    MINOR = "Minor"
    SUSPICIOUS = "Suspicious"

class CrimeRate(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class RoadType(str, Enum):
    HIGHWAY = "Highway primary"
    URBAN = "Urban mixed"
    RURAL = "Rural/unlit"

class SeasonalRisk(str, Enum):
    YEAR_ROUND = "Year-round"
    MONSOON = "Monsoon seasonal"
    HIGH = "High exposure"

class Immobiliser(str, Enum):
    FACTORY = "Factory fitted"
    AFTERMARKET = "Aftermarket"
    NONE = "None"

class GPSTracking(str, Enum):
    ACTIVE = "Active tracking"
    PASSIVE = "Passive"
    NONE = "None"

class AlarmSystem(str, Enum):
    OEM = "OEM alarm"
    AFTERMARKET = "Aftermarket"
    NONE = "None"

class ExcessChosen(str, Enum):
    HIGH = "High (>1,000)"
    STANDARD = "Standard"
    MINIMUM = "Minimum"

class NamedDrivers(str, Enum):
    ONE = "1 (owner only)"
    TWO_TO_THREE = "2-3"
    FOUR_PLUS = "4+"

class PolicyLapseHistory(str, Enum):
    NO_LAPSE = "No lapse"
    ONE_LAPSE = "1 lapse"
    TWO_PLUS = "2+ lapses"

class SumInsuredAccuracy(str, Enum):
    ACCURATE = "Accurate"
    PLUS_MINUS_10 = "±10%"
    UNDERINSURED = "Underinsured >10%"

class PremiumPayment(str, Enum):
    ANNUAL = "Annual full"
    SEMI_ANNUAL = "Semi-annual"
    MONTHLY = "Monthly"

# -------------------------------------------------------------

class QuoteRequest(BaseModel):
    # Driver factors
    driver_age: int = Field(..., ge=17, le=90, description="Driver age between 17 and 90")
    traffic_violations: int = Field(default=0, ge=0)
    telematics_risk: TelematicsRisk = Field(default=TelematicsRisk.LOW)
    gender: Gender = Field(default=Gender.FEMALE)
    years_licensed: YearsLicensed = Field(default=YearsLicensed.FIVE_PLUS)
    occupation: Occupation = Field(default=Occupation.PROFESSIONAL)
    previous_claims_3yr: PreviousClaims3Yr = Field(default=PreviousClaims3Yr.ZERO)
    
    # Claims factors
    ncd_percentage: NCDPercentage
    prior_claims_count: int = Field(default=0, ge=0)
    average_prior_severity: Severity = Field(default=Severity.LOW)
    fault_profile: FaultProfile = Field(default=FaultProfile.NOT_AT_FAULT)
    fraud_indicators: FraudIndicators = Field(default=FraudIndicators.NONE)
    
    # Geographic / Environmental factors
    territory: Territory
    flood_zone: FloodZone
    crime_rate: CrimeRate = Field(default=CrimeRate.LOW)
    road_type: RoadType = Field(default=RoadType.HIGHWAY)
    seasonal_risk: SeasonalRisk = Field(default=SeasonalRisk.YEAR_ROUND)
    
    # Vehicle factors
    vehicle_value: float = Field(..., gt=0)
    engine_capacity: int = Field(..., gt=0)
    vehicle_category: VehicleCategory
    valuation_type: ValuationType
    vehicle_age: int = Field(default=0, ge=0)
    modification_status: ModificationStatus = Field(default=ModificationStatus.STANDARD)
    safety_features: SafetyFeatures = Field(default=SafetyFeatures.ADVANCED)
    tyre_condition: TyreCondition = Field(default=TyreCondition.GOOD)
    assembly_type: Optional[AssemblyType] = Field(default=None)
    
    # Usage factors
    annual_mileage: int = Field(default=10000, ge=0)
    usage_type: UsageType
    parking_night: ParkingNight = Field(default=ParkingNight.GARAGED)
    annual_trips: AnnualTrips = Field(default=AnnualTrips.LOW)
    
    # Security factors
    immobiliser: Immobiliser = Field(default=Immobiliser.FACTORY)
    gps_tracking: GPSTracking = Field(default=GPSTracking.ACTIVE)
    alarm_system: AlarmSystem = Field(default=AlarmSystem.OEM)
    
    # Policy factors
    excess_chosen: ExcessChosen = Field(default=ExcessChosen.HIGH)
    named_drivers: NamedDrivers = Field(default=NamedDrivers.ONE)
    policy_lapse_history: PolicyLapseHistory = Field(default=PolicyLapseHistory.NO_LAPSE)
    sum_insured_accuracy: SumInsuredAccuracy = Field(default=SumInsuredAccuracy.ACCURATE)
    premium_payment: PremiumPayment = Field(default=PremiumPayment.ANNUAL)
    
    # Add-ons
    windscreen_cover: bool = Field(default=False)
    ncd_protector: bool = Field(default=False)
    special_perils_cover: bool = Field(default=False)
