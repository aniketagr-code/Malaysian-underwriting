import pandas as pd
from backend.app.engine import generate_quote
from backend.app.schemas import QuoteRequest, Territory, TelematicsRisk, Severity, FloodZone, VehicleCategory, ValuationType, UsageType, NCDPercentage

def get_variance(row):
    req = QuoteRequest(
        driver_age=row['Age'],
        traffic_violations=0,
        telematics_risk=TelematicsRisk.LOW,
        ncd_percentage=NCDPercentage.NCD_0,
        prior_claims_count=row['Claim_Flag'],
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
    res = generate_quote(req)
    # The requirement is: "assert engine output is within a stated tolerance of Final_Premium_MYR"
    final_prem_engine = res["final_premium"]
    final_prem_actual = row['Final_Premium_MYR']
    variance = abs(final_prem_engine - final_prem_actual)
    return req, final_prem_engine, final_prem_actual, variance

file_path = 'backend/data/BITs_Sample_Data_Workbook.xlsx'
df = pd.read_excel(file_path, sheet_name='MV_Policies', header=3)
# We need claim flags
claims = pd.read_excel(file_path, sheet_name='MV_Claims', header=3)
claims_agg = claims.groupby('Policy_ID').size().reset_index(name='claim_count')
df = pd.merge(df, claims_agg, on='Policy_ID', how='left')
df['Claim_Flag'] = df['claim_count'].notnull().astype(int)

df['Final_Premium_MYR'] = pd.to_numeric(df['Final_Premium_MYR'], errors='coerce')
df['Sum_Insured_MYR'] = pd.to_numeric(df['Sum_Insured_MYR'], errors='coerce')
df['Engine_CC'] = pd.to_numeric(df['Engine_CC'], errors='coerce')

samples = df.groupby('Risk_Category').head(2)

print("test_cases = [")
for idx, row in samples.iterrows():
    req, engine, actual, var = get_variance(row)
    print(f"    # {row['Risk_Category']} Risk, Policy: {row['Policy_ID']}")
    print(f"    ({req.dict()}, {actual}, {var + 0.1}),")
print("]")
