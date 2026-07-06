"""
Malaysia Motor Insurance Underwriting Engine (Scorecard v1.1.0)

CRITICAL ACTUARIAL FIXES IMPLEMENTED:
1. NCD vs. E-Hailing Surcharge Interaction: E-hailing surcharge is applied AFTER the NCD deduction, 
   ensuring the commercial risk penalty is not incorrectly discounted by private motor NCD.
2. NCD Protector Pricing Inversion: NCD Protector is priced at 15% of the NCD Discount Amount 
   (the actual value being protected) rather than the residual premium.
3. Rate Adequacy Floor Placement: The RM 350 floor is applied to the Core Premium (after NCD and 
   commercial surcharges) BEFORE optional add-ons (Flood, Windscreen) are calculated.
4. Sequence Lock: Risk Loading -> NCD -> E-Hailing -> Floor -> Add-ons.
5. Scorecard v1.2.0 Updates: Aligned scoring bands with MV_Risk_Factors dataset, refactored frequency/severity calculation, mapped exact point values.

SCHEMA GAPS IDENTIFIED:
The following underwriting factors are in the MV_Risk_Factors matrix but lack corresponding fields in schemas.py:
- Gender (required for Gender + Age combo)
- Years Licensed
- Occupation
- Previous Claims (3yr) (prior_claims_count lacks explicit time horizon)
- Engine CC (present for premium, but not used in risk scorecard)
- Modification Status
- Safety Features
- Tyre Condition
- Parking (night)
- Annual Trips
- Fault Profile
- Fraud Indicators
- Crime Rate (area)
- Road Type
- Seasonal Risk
- Immobiliser
- GPS Tracking
- Alarm System
- Excess Chosen
- Named Drivers
- Policy Lapse History
- Sum Insured Accuracy
- Premium Payment (Frequency)
"""
from .schemas import QuoteRequest, Territory, TelematicsRisk, Severity, FloodZone, VehicleCategory, ValuationType, UsageType
from .config import PREMIUM_FLOOR, SST_RATE, WINDSCREEN_FLAT, FLOOD_RATE, EHAILING_SURCHARGE, NCD_PROTECTOR_LOADING, STAMP_DUTY, CC_RATES_PENINSULAR, ADDITIONAL_VALUE_RATE_PENINSULAR, CC_RATES_EAST_MALAYSIA, ADDITIONAL_VALUE_RATE_EAST_MALAYSIA, SCORECARD_VERSION
import math

def calculate_driver_score(req: QuoteRequest) -> dict:
    pts = {"age": 0, "violations": 0, "telematics": 0}
    
    # Age
    if req.driver_age <= 25:
        pts["age"] = 4  # Match MV_Risk_Factors Driver Age (High Risk <21 / Low 25-55)
    elif req.driver_age <= 30:
        pts["age"] = 0  # Match MV_Risk_Factors Low Risk (25-55)
    elif req.driver_age <= 60:
        pts["age"] = 0  # Match MV_Risk_Factors Low Risk (25-55) / Med (56-65)
    elif req.driver_age <= 75:
        pts["age"] = 2  # Match MV_Risk_Factors Medium Risk (56-65) / High (>65)
    else:
        pts["age"] = 4  # Match MV_Risk_Factors High Risk (>65)
        
    # Violations
    if req.traffic_violations == 0:
        pts["violations"] = 0  # Match MV_Risk_Factors Traffic Violations Low Risk
    elif req.traffic_violations == 1:
        pts["violations"] = 1  # Match MV_Risk_Factors Traffic Violations Medium Risk
    else:
        pts["violations"] = 3  # Match MV_Risk_Factors Traffic Violations High Risk
        
    # Telematics
    if req.telematics_risk == TelematicsRisk.LOW:
        pts["telematics"] = 0
    elif req.telematics_risk == TelematicsRisk.MED:
        pts["telematics"] = 0  # Not in MV_Risk_Factors, assigned 0
    elif req.telematics_risk == TelematicsRisk.HIGH:
        pts["telematics"] = 0  # Not in MV_Risk_Factors, assigned 0
        
    return {"total": sum(pts.values()), "breakdown": pts}

def calculate_claims_score(req: QuoteRequest) -> dict:
    pts = {"ncd_stepback": 0, "frequency_severity": 0}
    
    if req.ncd_protector:
        return {"total": 0, "breakdown": {"ncd_stepback": 0, "frequency_severity": 0}}
        
    # NCD Step-back proxy
    if req.ncd_percentage == 0.0:
        pts["ncd_stepback"] = 4  # Match MV_Risk_Factors implied frequency risk
    elif req.ncd_percentage <= 25.0:
        pts["ncd_stepback"] = 3
    elif req.ncd_percentage <= 30.0:
        pts["ncd_stepback"] = 2
    elif req.ncd_percentage <= 38.33:
        pts["ncd_stepback"] = 1
    elif req.ncd_percentage <= 45.0:
        pts["ncd_stepback"] = 0
    elif req.ncd_percentage == 55.0:
        pts["ncd_stepback"] = 0  # Match MV_Risk_Factors implied low risk
 
    # Frequency vs Severity math
    if req.prior_claims_count == 0:
        pts["frequency_severity"] = 0  # Match MV_Risk_Factors Claim Frequency Low Risk
    else:
        # Match MV_Risk_Factors Claim Frequency
        freq_pts = 1 if req.prior_claims_count == 1 else 4
        
        # Match MV_Risk_Factors Severity History
        sev_pts = 0
        if req.average_prior_severity == Severity.LOW:
            sev_pts = 1
        elif req.average_prior_severity == Severity.MED:
            sev_pts = 2
        elif req.average_prior_severity == Severity.HIGH:
            sev_pts = 3
            
        pts["frequency_severity"] = freq_pts + sev_pts
        
    return {"total": sum(pts.values()), "breakdown": pts}

def calculate_geographic_score(req: QuoteRequest) -> dict:
    pts = {"territory": 0, "flood": 0}
    
    if req.territory == Territory.URBAN_KL_SELANGOR_PENANG_JOHOR:
        pts["territory"] = 3  # Match MV_Risk_Factors Geographic Area High Risk
    elif req.territory == Territory.URBAN_OTHER:
        pts["territory"] = 2  # Match MV_Risk_Factors Geographic Area Medium Risk
    elif req.territory == Territory.RURAL_WEST_MALAYSIA:
        pts["territory"] = 0  # Match MV_Risk_Factors Geographic Area Low Risk
    elif req.territory == Territory.RURAL_EAST_MALAYSIA:
        pts["territory"] = 0  # Match MV_Risk_Factors Geographic Area Low Risk
        
    if req.flood_zone == FloodZone.LOW:
        pts["flood"] = 0  # Match MV_Risk_Factors Flood Zone Low Risk
    elif req.flood_zone == FloodZone.MED:
        pts["flood"] = 1  # Match MV_Risk_Factors Flood Zone Medium Risk
    elif req.flood_zone == FloodZone.HIGH:
        pts["flood"] = 3  # Match MV_Risk_Factors Flood Zone High Risk
        
    return {"total": sum(pts.values()), "breakdown": pts}

def calculate_vehicle_score(req: QuoteRequest) -> dict:
    pts = {"category": 0, "valuation": 0, "age": 0}
    
    if req.vehicle_category == VehicleCategory.LUXURY_CAR:
        pts["category"] = 0  # Not in MV_Risk_Factors
    elif req.vehicle_category == VehicleCategory.COMMERCIAL_PICKUP:
        pts["category"] = 0  # Not in MV_Risk_Factors
    elif req.vehicle_category == VehicleCategory.PRIVATE_CAR:
        pts["category"] = 0  # Not in MV_Risk_Factors
        
    if req.valuation_type == ValuationType.MARKET_VALUE:
        pts["valuation"] = 0  # Not in MV_Risk_Factors
    elif req.valuation_type == ValuationType.AGREED_VALUE:
        pts["valuation"] = 0  # Not in MV_Risk_Factors
        
    if req.vehicle_age <= 10:
        pts["age"] = 0  # Match MV_Risk_Factors Vehicle Age Low/Med Risk
    else:
        pts["age"] = 3  # Match MV_Risk_Factors Vehicle Age High Risk
        
    return {"total": sum(pts.values()), "breakdown": pts}

def calculate_usage_score(req: QuoteRequest) -> dict:
    pts = {"mileage": 0, "type": 0}
    
    if req.annual_mileage <= 14999:
        pts["mileage"] = 0  # Match MV_Risk_Factors Annual Mileage Low Risk
    elif req.annual_mileage <= 30000:
        pts["mileage"] = 1  # Match MV_Risk_Factors Annual Mileage Medium Risk
    else:
        pts["mileage"] = 3  # Match MV_Risk_Factors Annual Mileage High Risk
        
    if req.usage_type == UsageType.PRIVATE:
        pts["type"] = 0  # Match MV_Risk_Factors Primary Use Low Risk
    elif req.usage_type == UsageType.COMMERCIAL:
        pts["type"] = 2  # Match MV_Risk_Factors Primary Use Medium Risk
    elif req.usage_type == UsageType.EHAILING_COMMERCIAL:
        pts["type"] = 4  # Match MV_Risk_Factors Primary Use High Risk
        
    return {"total": sum(pts.values()), "breakdown": pts}

def generate_quote(req: QuoteRequest):
    metadata = {
        "Standard Own-Damage Excess: RM200": True
    }
    d_score = calculate_driver_score(req)
    c_score = calculate_claims_score(req)
    g_score = calculate_geographic_score(req)
    v_score = calculate_vehicle_score(req)
    u_score = calculate_usage_score(req)
    
    # Calculate Concentration Penalty (GLM interaction terms proxy)
    domains = {
        "driver": {"val": d_score["total"], "max": 30},
        "claims": {"val": c_score["total"], "max": 25},
        "geo": {"val": g_score["total"], "max": 20},
        "vehicle": {"val": v_score["total"], "max": 15},
        "usage": {"val": u_score["total"], "max": 10}
    }
    
    base_composite_score = sum(d["val"] for d in domains.values())
    
    concentration_penalty = 0
    if base_composite_score > 60:
        for d in domains.values():
            if d["val"] / d["max"] > 0.70:
                concentration_penalty = 5
                break
                
    composite_score = base_composite_score + concentration_penalty
    
    # Reinsurance Referral
    reinsurance_referral = False
    # Explicit Rule: E-Hailing is excluded from individual reinsurance trigger (handled via fleet-level cession).
    # Commercial triggers individually. High-value E-Hailing (>RM150k) still triggers because of the value threshold.
    if req.vehicle_value > 150000 or req.usage_type == UsageType.COMMERCIAL:
        reinsurance_referral = True
        
    if composite_score >= 80:
        return {
            "scorecard_version": SCORECARD_VERSION,
            "decision": "REFER_TO_UNDERWRITER",
            "composite_score": composite_score,
            "reinsurance_referral": reinsurance_referral,
            "message": "Risk score too high. Referred to underwriter."
        }
        
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
        # Note: max(0, ...) prevents negative blocks if vehicle_value < 1000
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
    
    # STEP 3: NCD DEDUCTION (Private Motor Discount Only)
    actual_ncd_percentage = float(req.ncd_percentage)
    
    if req.prior_claims_count > 0 and not req.ncd_protector:
        actual_ncd_percentage = 0.0
        metadata["NCD STEP-BACK APPLIED DUE TO PRIOR CLAIMS"] = True
        
    ncd_discount_amount = round(gross_base_premium * (actual_ncd_percentage / 100.0), 2)
    discounted_premium = round(gross_base_premium - ncd_discount_amount, 2)
    
    # STEP 4: COMMERCIAL SURCHARGES & CORE RISK ADEQUACY
    ehailing_surcharge = EHAILING_SURCHARGE if req.usage_type == UsageType.EHAILING_COMMERCIAL else 0.0
    core_premium_pre_floor = round(discounted_premium + ehailing_surcharge, 2)
    
    rate_floor_triggered = False
    core_premium_post_floor = core_premium_pre_floor
    if core_premium_post_floor < PREMIUM_FLOOR:
        core_premium_post_floor = PREMIUM_FLOOR
        rate_floor_triggered = True
        
    # STEP 5: OPTIONAL ADD-ONS (Separate Peril Pricing)
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
        "decision": "AUTO_APPROVED",
        "composite_score": composite_score,
        "score_breakdown": {
            "driver": d_score["breakdown"],
            "claims": c_score["breakdown"],
            "geographic": g_score["breakdown"],
            "vehicle": v_score["breakdown"],
            "usage": u_score["breakdown"],
            "concentration_penalty": concentration_penalty
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
