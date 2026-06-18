import pytest
from app.schemas import QuoteRequest, Territory, TelematicsRisk, Severity, FloodZone, VehicleCategory, ValuationType, UsageType, NCDPercentage
from app.engine import generate_quote
from app.config import PREMIUM_FLOOR, SST_RATE, STAMP_DUTY, SCORECARD_VERSION

def test_case_1_baseline_national_car():
    req = QuoteRequest(
        driver_age=40,
        traffic_violations=0,
        telematics_risk=TelematicsRisk.LOW,
        ncd_percentage=NCDPercentage.NCD_55,
        prior_claims_count=0,
        average_prior_severity=Severity.LOW,
        territory=Territory.URBAN_KL_SELANGOR_PENANG_JOHOR,
        flood_zone=FloodZone.LOW,
        vehicle_value=45000.0,
        engine_capacity=1600,
        vehicle_category=VehicleCategory.PRIVATE_CAR,
        valuation_type=ValuationType.MARKET_VALUE,
        vehicle_age=3,
        annual_mileage=10000,
        usage_type=UsageType.PRIVATE,
        windscreen_cover=False,
        ncd_protector=False,
        special_perils_cover=False
    )
    res = generate_quote(req)
    assert res["scorecard_version"] == SCORECARD_VERSION
    assert "score_breakdown" in res
    assert res["score_breakdown"]["concentration_penalty"] == 0
    bk = res["premium_breakdown"]
    assert bk["base_premium"] == 1449.50
    assert bk["ncd_discount_amount"] == 797.23
    assert bk["core_premium_post_floor"] == 652.27
    assert bk["rate_floor_triggered"] is False
    assert bk["total_payable"] == 714.45

def test_case_6_premium_floor_boundary():
    req = QuoteRequest(
        driver_age=65,
        traffic_violations=0,
        telematics_risk=TelematicsRisk.LOW,
        ncd_percentage=NCDPercentage.NCD_55,
        prior_claims_count=0,
        average_prior_severity=Severity.LOW,
        territory=Territory.RURAL_EAST_MALAYSIA,
        flood_zone=FloodZone.LOW,
        vehicle_value=5000.0,
        engine_capacity=1400,
        vehicle_category=VehicleCategory.PRIVATE_CAR,
        valuation_type=ValuationType.MARKET_VALUE,
        vehicle_age=15,
        annual_mileage=5000,
        usage_type=UsageType.PRIVATE,
        windscreen_cover=False,
        ncd_protector=False,
        special_perils_cover=False
    )
    res = generate_quote(req)
    bk = res["premium_breakdown"]
    assert bk["base_premium"] == 277.40
    assert bk["ncd_discount_amount"] == 152.57
    assert bk["core_premium_pre_floor"] == 124.83
    assert bk["rate_floor_triggered"] is True
    assert bk["core_premium_post_floor"] == 350.00
    assert bk["total_payable"] == 388.00

def test_case_7_ehailing_ncd_interaction():
    req = QuoteRequest(
        driver_age=29,
        traffic_violations=0,
        telematics_risk=TelematicsRisk.LOW,
        ncd_percentage=NCDPercentage.NCD_0,
        prior_claims_count=0,
        average_prior_severity=Severity.LOW,
        territory=Territory.URBAN_KL_SELANGOR_PENANG_JOHOR,
        flood_zone=FloodZone.MED,
        vehicle_value=55000.0,
        engine_capacity=1600,
        vehicle_category=VehicleCategory.PRIVATE_CAR,
        valuation_type=ValuationType.MARKET_VALUE,
        vehicle_age=4,
        annual_mileage=50000,
        usage_type=UsageType.EHAILING_COMMERCIAL,
        windscreen_cover=False,
        ncd_protector=False,
        special_perils_cover=False
    )
    res = generate_quote(req)
    bk = res["premium_breakdown"]
    assert bk["ehailing_surcharge"] == 400.00
    assert bk["ncd_discount_amount"] == 0.00
    assert bk["core_premium_pre_floor"] == round(bk["discounted_premium"] + 400.00, 2)

def test_case_8_ncd_protector_pricing():
    req = QuoteRequest(
        driver_age=45,
        traffic_violations=0,
        telematics_risk=TelematicsRisk.LOW,
        ncd_percentage=NCDPercentage.NCD_55,
        prior_claims_count=1,
        average_prior_severity=Severity.MED,
        territory=Territory.RURAL_WEST_MALAYSIA,
        flood_zone=FloodZone.LOW,
        vehicle_value=120000.0,
        engine_capacity=1500,
        vehicle_category=VehicleCategory.PRIVATE_CAR,
        valuation_type=ValuationType.MARKET_VALUE,
        vehicle_age=3,
        annual_mileage=15000,
        usage_type=UsageType.PRIVATE,
        windscreen_cover=False,
        ncd_protector=True,
        special_perils_cover=False
    )
    res = generate_quote(req)
    bk = res["premium_breakdown"]
    expected_protector_cost = round(bk["ncd_discount_amount"] * 0.15, 2)
    assert bk["ncd_protector"] == expected_protector_cost

def test_glm_concentration_penalty():
    req = QuoteRequest(
        # Max out driver score (30 max)
        driver_age=18,             # 12
        traffic_violations=3,      # 10
        telematics_risk=TelematicsRisk.HIGH, # 8 (total 30) -> 30/30 = 100% > 70%
        
        ncd_percentage=NCDPercentage.NCD_0,  # 15
        prior_claims_count=2,                # Med(5) * 1.5 = 7 (total 22)
        average_prior_severity=Severity.MED,
        
        territory=Territory.URBAN_KL_SELANGOR_PENANG_JOHOR, # 15
        flood_zone=FloodZone.LOW,            # 0 (total 15)
        
        vehicle_value=45000.0,
        engine_capacity=1600,
        vehicle_category=VehicleCategory.PRIVATE_CAR,
        valuation_type=ValuationType.MARKET_VALUE,
        vehicle_age=3,
        
        annual_mileage=10000,
        usage_type=UsageType.PRIVATE
    )
    res = generate_quote(req)
    # The score should be AUTO_APPROVED because 77 < 80.
    assert res["decision"] == "AUTO_APPROVED"
    # Driver score = 30. Claims = 22. Geo = 15. Veh = 5. Usage = 0. Total = 72
    # Driver is 30/30 (100% > 70%). Total > 60. So penalty = +5.
    # Total composite = 72 + 5 = 77.
    # Wait, if total is 77, it does NOT get auto-rejected! Wait.
    # Let's check math: 30 + 22 + 15 + 5 + 0 = 72. 72 + 5 = 77.
    # 77 < 80, so it's NOT rejected! It returns a premium breakdown!
    
    assert "score_breakdown" in res
    assert res["score_breakdown"]["concentration_penalty"] == 5
    assert res["composite_score"] == 77
    assert res["premium_breakdown"]["risk_loading_pct"] == 0.50

def test_frequency_severity_math():
    req = QuoteRequest(
        driver_age=40,
        traffic_violations=0,
        telematics_risk=TelematicsRisk.LOW,
        ncd_percentage=NCDPercentage.NCD_55,
        
        # 4+ claims * HIGH severity = 3.0 * 10 = 30 -> capped at 25
        prior_claims_count=5,
        average_prior_severity=Severity.HIGH,
        
        territory=Territory.URBAN_KL_SELANGOR_PENANG_JOHOR,
        flood_zone=FloodZone.LOW,
        vehicle_value=45000.0,
        engine_capacity=1600,
        vehicle_category=VehicleCategory.PRIVATE_CAR,
        valuation_type=ValuationType.MARKET_VALUE,
        vehicle_age=3,
        annual_mileage=10000,
        usage_type=UsageType.PRIVATE
    )
    res = generate_quote(req)
    assert res["score_breakdown"]["claims"]["frequency_severity"] == 25
