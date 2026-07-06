import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from .engine import generate_quote
from .schemas import QuoteRequest, Territory, TelematicsRisk, Severity, FloodZone, VehicleCategory, ValuationType, UsageType, NCDPercentage

def get_cc_band(cc):
    if pd.isna(cc): return 'Unknown'
    if cc <= 1400: return '<=1400'
    elif cc <= 1650: return '<=1650'
    elif cc <= 2200: return '<=2200'
    else: return '>2200'

def map_row_to_quote_request(row):
    return QuoteRequest(
        driver_age=row['Age'],
        traffic_violations=0,  # Proxy or missing
        telematics_risk=TelematicsRisk.LOW, # Missing
        ncd_percentage=NCDPercentage.NCD_0, # Just using default for missing mapping or try to map
        prior_claims_count=row['Claim_Flag'], # Rough proxy for count
        average_prior_severity=Severity.LOW,
        territory=Territory.URBAN_KL_SELANGOR_PENANG_JOHOR if row['State'] in ['Kuala Lumpur', 'Selangor', 'Penang', 'Johor'] else Territory.URBAN_OTHER,
        flood_zone=FloodZone.LOW,
        vehicle_value=row['Sum_Insured_MYR'],
        engine_capacity=row['Engine_CC'],
        vehicle_category=VehicleCategory.PRIVATE_CAR,
        valuation_type=ValuationType.MARKET_VALUE,
        vehicle_age=row['Vehicle_Age_Yrs'],
        annual_mileage=15000,
        usage_type=UsageType.PRIVATE if row['Vehicle_Use'] == 'PRIVATE' else UsageType.COMMERCIAL,
        windscreen_cover=False,
        ncd_protector=False,
        special_perils_cover=False
    )

def run_validation():
    file_path = r'C:\Users\lenovo\Downloads\BITs_Sample_Data_Workbook.xlsx'
    policies = pd.read_excel(file_path, sheet_name='MV_Policies', header=3)
    claims = pd.read_excel(file_path, sheet_name='MV_Claims', header=3)
    
    policies['Final_Premium_MYR'] = pd.to_numeric(policies['Final_Premium_MYR'], errors='coerce')
    policies['Engine_CC'] = pd.to_numeric(policies['Engine_CC'], errors='coerce')
    policies['Sum_Insured_MYR'] = pd.to_numeric(policies['Sum_Insured_MYR'], errors='coerce')
    
    total_premium = policies['Final_Premium_MYR'].sum()
    if 'Net_Payout_MYR' in claims.columns:
        claims['Net_Payout_MYR'] = pd.to_numeric(claims['Net_Payout_MYR'], errors='coerce')
        total_payout = claims['Net_Payout_MYR'].sum()
    else:
        total_payout = 0
    
    loss_ratio = total_payout / total_premium if total_premium else 0
    print(f"=== Recomputed Loss Ratio: {loss_ratio:.4f} ===")
    
    if 'Risk_Category' in policies.columns:
        claims_agg = claims.groupby('Policy_ID').size().reset_index(name='claim_count')
        df_claim = pd.merge(policies, claims_agg, on='Policy_ID', how='left')
        df_claim['Claim_Flag'] = df_claim['claim_count'].notnull().astype(int)
        summary = df_claim.groupby('Risk_Category')['Claim_Flag'].agg(['count', 'sum', 'mean'])
        print("\n=== Risk_Category/Claim_Flag Correlation ===")
        print(summary)
        
        policies['Claim_Flag'] = df_claim['Claim_Flag']

    policies['CC_Band'] = policies['Engine_CC'].apply(get_cc_band)
    
    # Recalibrated buckets (run on 20% held out)
    recal_buckets = ['<=1400', '<=1650']
    
    print("\n=== Variance Analysis ===")
    for band in ['<=1400', '<=1650', '<=2200', '>2200']:
        subset = policies[(policies['CC_Band'] == band) & (policies['Vehicle_Use'] == 'PRIVATE')].copy()
        if len(subset) == 0:
            continue
            
        if band in recal_buckets:
            train, test = train_test_split(subset, test_size=0.20, random_state=42)
            eval_set = test
            label = "held-out test"
        else:
            eval_set = subset
            label = "not a held-out test - full bucket, uncalibrated"
            
        variances = []
        for idx, row in eval_set.iterrows():
            req = map_row_to_quote_request(row)
            try:
                res = generate_quote(req)
                base_prem_engine = res["premium_breakdown"]["base_premium"]
                base_prem_actual = row['Base_Premium_MYR']
                variance = abs(base_prem_engine - base_prem_actual)
                variances.append(variance)
            except Exception as e:
                pass
                
        if variances:
            avg_var = np.mean(variances)
            max_var = np.max(variances)
            print(f"Bucket {band} PRIVATE ({label}):")
            print(f"  Avg Variance: RM {avg_var:.2f}")
            print(f"  Max Variance: RM {max_var:.2f}")

if __name__ == "__main__":
    run_validation()
