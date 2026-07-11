"""
Malaysia Motor Insurance Underwriting Engine (Scorecard v1.2.1)
"""
from .schemas import *
from .config import PREMIUM_FLOOR, SST_RATE, WINDSCREEN_FLAT, FLOOD_RATE, EHAILING_SURCHARGE, NCD_PROTECTOR_LOADING, STAMP_DUTY, CC_RATES_PENINSULAR, ADDITIONAL_VALUE_RATE_PENINSULAR, CC_RATES_EAST_MALAYSIA, ADDITIONAL_VALUE_RATE_EAST_MALAYSIA, SCORECARD_VERSION
import math

def calculate_driver_score(req: QuoteRequest) -> dict:
    pts = {}
    max_pts = {}
    supplied = req.model_fields_set
    
    # Age (mandatory)
    max_pts["age"] = 4
    if req.driver_age <= 25: pts["age"] = 4
    elif req.driver_age <= 60: pts["age"] = 0
    elif req.driver_age <= 75: pts["age"] = 2
    else: pts["age"] = 4
        
    # Gender + Age combo
    if "gender" in supplied:
        max_pts["gender_age"] = 2
        if req.gender == Gender.MALE:
            if req.driver_age < 18: pts["gender_age"] = 2
            elif req.driver_age <= 24: pts["gender_age"] = 1
            else: pts["gender_age"] = 0
        else:
            if req.driver_age < 20: pts["gender_age"] = 2
            else: pts["gender_age"] = 0
    else:
        pts["gender_age"] = "not scored, no data"
        max_pts["gender_age"] = 0
            
    # Years Licensed
    if "years_licensed" in supplied:
        max_pts["years_licensed"] = 3
        if req.years_licensed == YearsLicensed.LESS_THAN_2: pts["years_licensed"] = 3
        elif req.years_licensed == YearsLicensed.TWO_TO_FOUR: pts["years_licensed"] = 1
        else: pts["years_licensed"] = 0
    else:
        pts["years_licensed"] = "not scored, no data"
        max_pts["years_licensed"] = 0
        
    # Occupation
    if "occupation" in supplied:
        max_pts["occupation"] = 3
        if req.occupation == Occupation.MANUAL: pts["occupation"] = 3
        elif req.occupation == Occupation.CLERICAL: pts["occupation"] = 1
        else: pts["occupation"] = 0
    else:
        pts["occupation"] = "not scored, no data"
        max_pts["occupation"] = 0
        
    # Annual Mileage
    if "annual_mileage" in supplied:
        max_pts["annual_mileage"] = 3
        if req.annual_mileage > 30000: pts["annual_mileage"] = 3
        elif req.annual_mileage >= 15000: pts["annual_mileage"] = 1
        else: pts["annual_mileage"] = 0
    else:
        pts["annual_mileage"] = "not scored, no data"
        max_pts["annual_mileage"] = 0
        
    # Previous Claims (3yr)
    if "previous_claims_3yr" in supplied:
        max_pts["previous_claims_3yr"] = 4
        if req.previous_claims_3yr == PreviousClaims3Yr.TWO_PLUS: pts["previous_claims_3yr"] = 4
        elif req.previous_claims_3yr == PreviousClaims3Yr.ONE: pts["previous_claims_3yr"] = 2
        else: pts["previous_claims_3yr"] = 0
    else:
        pts["previous_claims_3yr"] = "not scored, no data"
        max_pts["previous_claims_3yr"] = 0
        
    # Traffic Violations
    if "traffic_violations" in supplied:
        max_pts["traffic_violations"] = 3
        if req.traffic_violations >= 3: pts["traffic_violations"] = 3
        elif req.traffic_violations >= 1: pts["traffic_violations"] = 1
        else: pts["traffic_violations"] = 0
    else:
        pts["traffic_violations"] = "not scored, no data"
        max_pts["traffic_violations"] = 0
        
    return {"total": sum(v for v in pts.values() if isinstance(v, int)), "max": sum(max_pts.values()), "breakdown": pts}

def calculate_vehicle_score(req: QuoteRequest) -> dict:
    pts = {}
    max_pts = {}
    supplied = req.model_fields_set
    
    # Engine CC (mandatory)
    max_pts["engine_cc"] = 3
    if req.engine_capacity > 2000: pts["engine_cc"] = 3
    elif req.engine_capacity >= 1300: pts["engine_cc"] = 1
    else: pts["engine_cc"] = 0
        
    # Vehicle Age
    if "vehicle_age" in supplied:
        max_pts["vehicle_age"] = 3
        if req.vehicle_age > 10: pts["vehicle_age"] = 3
        elif req.vehicle_age >= 5: pts["vehicle_age"] = 1
        else: pts["vehicle_age"] = 0
    else:
        pts["vehicle_age"] = "not scored, no data"
        max_pts["vehicle_age"] = 0
        
    # Vehicle Value (mandatory)
    max_pts["vehicle_value"] = 3
    if req.vehicle_value > 150000: pts["vehicle_value"] = 3
    elif req.vehicle_value >= 50000: pts["vehicle_value"] = 1
    else: pts["vehicle_value"] = 0
        
    # Modification Status
    if "modification_status" in supplied:
        max_pts["modification_status"] = 4
        if req.modification_status == ModificationStatus.MAJOR: pts["modification_status"] = 4
        elif req.modification_status == ModificationStatus.MINOR: pts["modification_status"] = 2
        else: pts["modification_status"] = 0
    else:
        pts["modification_status"] = "not scored, no data"
        max_pts["modification_status"] = 0
        
    # Safety Features
    if "safety_features" in supplied:
        max_pts["safety_features"] = 3
        if req.safety_features == SafetyFeatures.MINIMAL: pts["safety_features"] = 3
        elif req.safety_features == SafetyFeatures.SOME: pts["safety_features"] = 1
        else: pts["safety_features"] = 0
    else:
        pts["safety_features"] = "not scored, no data"
        max_pts["safety_features"] = 0
        
    # Tyre Condition
    if "tyre_condition" in supplied:
        max_pts["tyre_condition"] = 3
        if req.tyre_condition == TyreCondition.WORN: pts["tyre_condition"] = 3
        elif req.tyre_condition == TyreCondition.MODERATE: pts["tyre_condition"] = 1
        else: pts["tyre_condition"] = 0
    else:
        pts["tyre_condition"] = "not scored, no data"
        max_pts["tyre_condition"] = 0
        
    # Assembly Type
    if "assembly_type" in supplied and req.assembly_type is not None:
        max_pts["assembly_type"] = 5
        if req.assembly_type == "CBU": pts["assembly_type"] = 5
        else: pts["assembly_type"] = 0
    else:
        pts["assembly_type"] = "not scored, no data"
        max_pts["assembly_type"] = 0
        
    return {"total": sum(v for v in pts.values() if isinstance(v, int)), "max": sum(max_pts.values()), "breakdown": pts}

def calculate_usage_score(req: QuoteRequest) -> dict:
    pts = {}
    max_pts = {}
    supplied = req.model_fields_set
    
    # Primary Use (mandatory)
    max_pts["primary_use"] = 4
    if req.usage_type == UsageType.EHAILING_COMMERCIAL: pts["primary_use"] = 4
    elif req.usage_type == UsageType.COMMERCIAL: pts["primary_use"] = 2
    else: pts["primary_use"] = 0
        
    # Parking Night
    if "parking_night" in supplied:
        max_pts["parking_night"] = 3
        if req.parking_night == ParkingNight.STREET: pts["parking_night"] = 3
        elif req.parking_night == ParkingNight.DRIVEWAY: pts["parking_night"] = 1
        else: pts["parking_night"] = 0
    else:
        pts["parking_night"] = "not scored, no data"
        max_pts["parking_night"] = 0
        
    # Annual Trips
    if "annual_trips" in supplied:
        max_pts["annual_trips"] = 2
        if req.annual_trips == AnnualTrips.HIGH: pts["annual_trips"] = 2
        elif req.annual_trips == AnnualTrips.MEDIUM: pts["annual_trips"] = 1
        else: pts["annual_trips"] = 0
    else:
        pts["annual_trips"] = "not scored, no data"
        max_pts["annual_trips"] = 0
        
    return {"total": sum(v for v in pts.values() if isinstance(v, int)), "max": sum(max_pts.values()), "breakdown": pts}

def calculate_claims_score(req: QuoteRequest) -> dict:
    pts = {}
    max_pts = {}
    supplied = req.model_fields_set
    
    if req.ncd_protector:
        return {"total": 0, "max": 0, "breakdown": {"frequency_severity": 0, "ncd_stepback": 0, "fault_profile": 0, "fraud_indicators": 0}}
        
    # Frequency vs Severity math
    if "prior_claims_count" in supplied:
        max_pts["frequency_severity"] = 7
        if req.prior_claims_count == 0:
            pts["frequency_severity"] = 0
        else:
            freq_pts = 4 if req.prior_claims_count >= 2 else 1
            sev_pts = 3 if req.average_prior_severity == Severity.HIGH else 2 if req.average_prior_severity == Severity.MED else 1
            pts["frequency_severity"] = freq_pts + sev_pts
    else:
        pts["frequency_severity"] = "not scored, no data"
        max_pts["frequency_severity"] = 0
        
    # NCD Step-back (mandatory)
    max_pts["ncd_stepback"] = 4
    if req.ncd_percentage == 0.0: pts["ncd_stepback"] = 4
    elif req.ncd_percentage <= 25.0: pts["ncd_stepback"] = 3
    elif req.ncd_percentage <= 30.0: pts["ncd_stepback"] = 2
    elif req.ncd_percentage <= 38.33: pts["ncd_stepback"] = 1
    else: pts["ncd_stepback"] = 0
        
    # Fault Profile
    if "fault_profile" in supplied:
        max_pts["fault_profile"] = 3
        if req.fault_profile == FaultProfile.AT_FAULT: pts["fault_profile"] = 3
        elif req.fault_profile == FaultProfile.PARTIAL: pts["fault_profile"] = 1
        else: pts["fault_profile"] = 0
    else:
        pts["fault_profile"] = "not scored, no data"
        max_pts["fault_profile"] = 0
        
    # Fraud Indicators
    if "fraud_indicators" in supplied:
        max_pts["fraud_indicators"] = 4
        if req.fraud_indicators == FraudIndicators.SUSPICIOUS: pts["fraud_indicators"] = 4
        elif req.fraud_indicators == FraudIndicators.MINOR: pts["fraud_indicators"] = 2
        else: pts["fraud_indicators"] = 0
    else:
        pts["fraud_indicators"] = "not scored, no data"
        max_pts["fraud_indicators"] = 0
        
    return {"total": sum(v for v in pts.values() if isinstance(v, int)), "max": sum(max_pts.values()), "breakdown": pts}

def calculate_environmental_score(req: QuoteRequest) -> dict:
    pts = {}
    max_pts = {}
    supplied = req.model_fields_set
    
    # Flood Zone (mandatory)
    max_pts["flood_zone"] = 3
    if req.flood_zone == FloodZone.HIGH: pts["flood_zone"] = 3
    elif req.flood_zone == FloodZone.MED: pts["flood_zone"] = 1
    else: pts["flood_zone"] = 0
        
    # Territory (mandatory)
    max_pts["territory"] = 3
    if req.territory == Territory.URBAN_KL_SELANGOR_PENANG_JOHOR: pts["territory"] = 3
    elif req.territory == Territory.URBAN_OTHER: pts["territory"] = 2
    else: pts["territory"] = 0

    # Crime Rate
    if "crime_rate" in supplied:
        max_pts["crime_rate"] = 3
        if req.crime_rate == CrimeRate.HIGH: pts["crime_rate"] = 3
        elif req.crime_rate == CrimeRate.MEDIUM: pts["crime_rate"] = 1
        else: pts["crime_rate"] = 0
    else:
        pts["crime_rate"] = "not scored, no data"
        max_pts["crime_rate"] = 0
        
    # Road Type
    if "road_type" in supplied:
        max_pts["road_type"] = 2
        if req.road_type == RoadType.RURAL: pts["road_type"] = 2
        elif req.road_type == RoadType.URBAN: pts["road_type"] = 1
        else: pts["road_type"] = 0
    else:
        pts["road_type"] = "not scored, no data"
        max_pts["road_type"] = 0
        
    # Seasonal Risk
    if "seasonal_risk" in supplied:
        max_pts["seasonal_risk"] = 2
        if req.seasonal_risk == SeasonalRisk.HIGH: pts["seasonal_risk"] = 2
        elif req.seasonal_risk == SeasonalRisk.MONSOON: pts["seasonal_risk"] = 1
        else: pts["seasonal_risk"] = 0
    else:
        pts["seasonal_risk"] = "not scored, no data"
        max_pts["seasonal_risk"] = 0
        
    return {"total": sum(v for v in pts.values() if isinstance(v, int)), "max": sum(max_pts.values()), "breakdown": pts}

def calculate_security_score(req: QuoteRequest) -> dict:
    pts = {}
    max_pts = {}
    supplied = req.model_fields_set
    
    if "immobiliser" in supplied:
        max_pts["immobiliser"] = 2
        if req.immobiliser == Immobiliser.NONE: pts["immobiliser"] = 2
        elif req.immobiliser == Immobiliser.AFTERMARKET: pts["immobiliser"] = 1
        else: pts["immobiliser"] = 0
    else:
        pts["immobiliser"] = "not scored, no data"
        max_pts["immobiliser"] = 0
        
    if "gps_tracking" in supplied:
        max_pts["gps_tracking"] = 2
        if req.gps_tracking == GPSTracking.NONE: pts["gps_tracking"] = 2
        elif req.gps_tracking == GPSTracking.PASSIVE: pts["gps_tracking"] = 1
        else: pts["gps_tracking"] = 0
    else:
        pts["gps_tracking"] = "not scored, no data"
        max_pts["gps_tracking"] = 0
        
    if "alarm_system" in supplied:
        max_pts["alarm_system"] = 2
        if req.alarm_system == AlarmSystem.NONE: pts["alarm_system"] = 2
        elif req.alarm_system == AlarmSystem.AFTERMARKET: pts["alarm_system"] = 1
        else: pts["alarm_system"] = 0
    else:
        pts["alarm_system"] = "not scored, no data"
        max_pts["alarm_system"] = 0
        
    return {"total": sum(v for v in pts.values() if isinstance(v, int)), "max": sum(max_pts.values()), "breakdown": pts}

def calculate_policy_score(req: QuoteRequest) -> dict:
    pts = {}
    max_pts = {}
    supplied = req.model_fields_set
    
    if "excess_chosen" in supplied:
        max_pts["excess_chosen"] = 2
        if req.excess_chosen == ExcessChosen.MINIMUM: pts["excess_chosen"] = 2
        elif req.excess_chosen == ExcessChosen.STANDARD: pts["excess_chosen"] = 1
        else: pts["excess_chosen"] = 0
    else:
        pts["excess_chosen"] = "not scored, no data"
        max_pts["excess_chosen"] = 0
        
    if "named_drivers" in supplied:
        max_pts["named_drivers"] = 2
        if req.named_drivers == NamedDrivers.FOUR_PLUS: pts["named_drivers"] = 2
        elif req.named_drivers == NamedDrivers.TWO_TO_THREE: pts["named_drivers"] = 1
        else: pts["named_drivers"] = 0
    else:
        pts["named_drivers"] = "not scored, no data"
        max_pts["named_drivers"] = 0
        
    if "policy_lapse_history" in supplied:
        max_pts["policy_lapse_history"] = 3
        if req.policy_lapse_history == PolicyLapseHistory.TWO_PLUS: pts["policy_lapse_history"] = 3
        elif req.policy_lapse_history == PolicyLapseHistory.ONE_LAPSE: pts["policy_lapse_history"] = 1
        else: pts["policy_lapse_history"] = 0
    else:
        pts["policy_lapse_history"] = "not scored, no data"
        max_pts["policy_lapse_history"] = 0
        
    if "sum_insured_accuracy" in supplied:
        max_pts["sum_insured_accuracy"] = 3
        if req.sum_insured_accuracy == SumInsuredAccuracy.UNDERINSURED: pts["sum_insured_accuracy"] = 3
        elif req.sum_insured_accuracy == SumInsuredAccuracy.PLUS_MINUS_10: pts["sum_insured_accuracy"] = 1
        else: pts["sum_insured_accuracy"] = 0
    else:
        pts["sum_insured_accuracy"] = "not scored, no data"
        max_pts["sum_insured_accuracy"] = 0
        
    if "premium_payment" in supplied:
        max_pts["premium_payment"] = 1
        if req.premium_payment == PremiumPayment.MONTHLY: pts["premium_payment"] = 1
        else: pts["premium_payment"] = 0
    else:
        pts["premium_payment"] = "not scored, no data"
        max_pts["premium_payment"] = 0
        
    return {"total": sum(v for v in pts.values() if isinstance(v, int)), "max": sum(max_pts.values()), "breakdown": pts}

def generate_quote(req: QuoteRequest):
    metadata = {
        "Standard Own-Damage Excess: RM200": True
    }
    d_score = calculate_driver_score(req)
    v_score = calculate_vehicle_score(req)
    u_score = calculate_usage_score(req)
    c_score = calculate_claims_score(req)
    e_score = calculate_environmental_score(req)
    s_score = calculate_security_score(req)
    p_score = calculate_policy_score(req)
    
    # Calculate Dynamic Denominator for Base Composite Score
    domains = {
        "driver": d_score,
        "vehicle": v_score,
        "usage": u_score,
        "claims": c_score,
        "environmental": e_score,
        "security": s_score,
        "policy": p_score
    }
    
    total_supplied_points = sum(d["total"] for d in domains.values())
    total_max_supplied = sum(d["max"] for d in domains.values())
    
    # Scale to 100 percentage points (handling div/0 just in case)
    if total_max_supplied > 0:
        base_composite_score = round((total_supplied_points / total_max_supplied) * 100)
    else:
        base_composite_score = 0
    
    
    composite_score = base_composite_score
    
    # Reinsurance Referral
    reinsurance_referral = False
    if req.vehicle_value > 150000 or req.usage_type == UsageType.COMMERCIAL:
        reinsurance_referral = True
        
    if composite_score >= 80:
        base_decision = "Declined"
    elif composite_score >= 40:
        base_decision = "Sub-standard"
    else:
        base_decision = "Standard"

        
    is_east_malaysia = req.territory in [Territory.RURAL_EAST_MALAYSIA]
    cc_rates = CC_RATES_EAST_MALAYSIA if is_east_malaysia else CC_RATES_PENINSULAR
    additional_rate = ADDITIONAL_VALUE_RATE_EAST_MALAYSIA if is_east_malaysia else ADDITIONAL_VALUE_RATE_PENINSULAR
    
    first_1000_rate = 0.0
    for limit in sorted(cc_rates.keys()):
        if req.engine_capacity <= limit:
            first_1000_rate = cc_rates[limit]
            break
            
    # STEP 1: BASE PREMIUM (PIAM Tariff Proxy)
    if req.vehicle_value <= 1000:
        base_premium = first_1000_rate
    else:
        additional_value = max(0, req.vehicle_value - 1000)
        blocks = math.ceil(additional_value / 1000.0)
        base_premium = first_1000_rate + (blocks * additional_rate)
    
    # STEP 2: RISK LOADING
    risk_loading_pct = 0.0
    if composite_score >= 75:
        risk_loading_pct = 0.50
    elif composite_score >= 60:
        risk_loading_pct = 0.30
    elif composite_score >= 40:
        risk_loading_pct = 0.15
        
    risk_loading_amount = round(base_premium * risk_loading_pct, 2)
    gross_base_premium = round(base_premium + risk_loading_amount, 2)
    
    # Format final decision string
    if base_decision == "Declined":
        decision_label = base_decision
    elif reinsurance_referral:
        decision_label = f"{base_decision} (Reinsurance Referral)"
    else:
        decision_label = f"{base_decision} ({int(risk_loading_pct*100)}% loading)"
    
    
    # STEP 3: NCD DEDUCTION
    actual_ncd_percentage = float(req.ncd_percentage)
    
    if req.prior_claims_count > 0 and not req.ncd_protector:
        actual_ncd_percentage = 0.0
        metadata["NCD STEP-BACK APPLIED DUE TO PRIOR CLAIMS"] = True
        
    ncd_discount_amount = round(gross_base_premium * (actual_ncd_percentage / 100.0), 2)
    discounted_premium = round(gross_base_premium - ncd_discount_amount, 2)
    
    # STEP 4: COMMERCIAL SURCHARGES & CORE RISK ADEQUACY
    ehailing_surcharge = 0.0
    if req.usage_type == UsageType.EHAILING_COMMERCIAL:
        ehailing_surcharge = EHAILING_SURCHARGE
        metadata["MANDATORY E-HAILING ENDORSEMENT APPLIED"] = True

    core_premium_pre_floor = round(discounted_premium + ehailing_surcharge, 2)
    
    rate_floor_triggered = False
    core_premium_post_floor = core_premium_pre_floor
    if core_premium_post_floor < PREMIUM_FLOOR:
        core_premium_post_floor = PREMIUM_FLOOR
        rate_floor_triggered = True
        
    # STEP 5: OPTIONAL ADD-ONS
    flood_endorsement = 0.0
    has_flood = req.special_perils_cover
    if req.flood_zone == FloodZone.HIGH:
        has_flood = True
    if has_flood:
        flood_endorsement = round(req.vehicle_value * FLOOD_RATE, 2)
        
    windscreen_cover = 0.0
    if req.windscreen_cover:
        windscreen_cover = WINDSCREEN_FLAT
        
    ncd_protector = 0.0
    if req.ncd_protector and req.ncd_percentage > 0:
        ncd_protector = round(ncd_discount_amount * NCD_PROTECTOR_LOADING, 2)
        
    total_add_ons = round(flood_endorsement + windscreen_cover + ncd_protector, 2)
    premium_excl_tax = round(core_premium_post_floor + total_add_ons, 2)
    
    # STEP 6: TAXES AND FINAL PAYABLE
    sst_amount = round(premium_excl_tax * SST_RATE, 2)
    total_payable = round(premium_excl_tax + sst_amount + STAMP_DUTY, 2)
    
    if req.flood_zone == FloodZone.HIGH and not req.special_perils_cover:
        metadata["MANDATORY FLOOD COVER APPLIED"] = True
        
    return {
        "scorecard_version": SCORECARD_VERSION,
        "decision": decision_label,
        "composite_score": composite_score,
        "score_breakdown": {
            "driver": d_score["breakdown"],
            "vehicle": v_score["breakdown"],
            "usage": u_score["breakdown"],
            "claims": c_score["breakdown"],
            "environmental": e_score["breakdown"],
            "security": s_score["breakdown"],
            "policy": p_score["breakdown"]
        },
        "reinsurance_referral": reinsurance_referral,
        "premium_breakdown": {
            "base_premium": round(base_premium, 2),
            "risk_loading_pct": risk_loading_pct,
            "risk_loading_amount": risk_loading_amount,
            "gross_base_premium": gross_base_premium,
            "ncd_pct": actual_ncd_percentage,
            "ncd_discount_amount": ncd_discount_amount,
            "discounted_premium": discounted_premium,
            "ehailing_surcharge": ehailing_surcharge,
            "core_premium_pre_floor": core_premium_pre_floor,
            "rate_floor_triggered": rate_floor_triggered,
            "core_premium_post_floor": core_premium_post_floor,
            "flood_endorsement": flood_endorsement,
            "windscreen_cover": windscreen_cover,
            "ncd_protector": ncd_protector,
            "total_add_ons": total_add_ons,
            "premium_excl_tax": premium_excl_tax,
            "sst_amount": sst_amount,
            "stamp_duty": round(STAMP_DUTY, 2),
            "total_payable": total_payable
        },
        "metadata": metadata
    }
