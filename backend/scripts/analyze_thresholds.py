import pandas as pd
import numpy as np
import sys
import os

# Ensure the backend module can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.app.engine import generate_quote
from backend.app.validation import map_row_to_quote_request

def run_analysis():
    file_path = 'backend/data/BITs_Sample_Data_Workbook.xlsx'
    policies = pd.read_excel(file_path, sheet_name='MV_Policies', header=3)
    claims = pd.read_excel(file_path, sheet_name='MV_Claims', header=3)
    
    policies['Final_Premium_MYR'] = pd.to_numeric(policies['Final_Premium_MYR'], errors='coerce')
    policies['Engine_CC'] = pd.to_numeric(policies['Engine_CC'], errors='coerce')
    policies['Sum_Insured_MYR'] = pd.to_numeric(policies['Sum_Insured_MYR'], errors='coerce')
    
    if 'Risk_Category' in policies.columns:
        claims_agg = claims.groupby('Policy_ID').size().reset_index(name='claim_count')
        df_claim = pd.merge(policies, claims_agg, on='Policy_ID', how='left')
        policies['Claim_Flag'] = df_claim['claim_count'].notnull().astype(int)

    results = []
    
    for idx, row in policies.iterrows():
        if pd.isna(row['Final_Premium_MYR']) or pd.isna(row['Engine_CC']):
            continue
            
        req = map_row_to_quote_request(row)
        try:
            res = generate_quote(req)
            engine_premium = res["premium_breakdown"]["total_payable"]
            actual_premium = row['Final_Premium_MYR']
            variance = abs(engine_premium - actual_premium)
            variance_pct = (variance / actual_premium) * 100
            
            comp_score = res["composite_score"]
            
            # Find distance to nearest threshold (40, 60, 75)
            thresholds = [40, 60, 75]
            nearest_threshold = min(thresholds, key=lambda x: abs(x - comp_score))
            distance = comp_score - nearest_threshold # positive means above, negative means below
            
            results.append({
                'Policy_ID': row['Policy_ID'],
                'Composite_Score': comp_score,
                'Actual_Premium': actual_premium,
                'Engine_Premium': engine_premium,
                'Variance_MYR': variance,
                'Variance_Pct': variance_pct,
                'Nearest_Threshold': nearest_threshold,
                'Distance_To_Threshold': distance
            })
        except Exception as e:
            print(f"Error processing {row.get('Policy_ID')}: {e}")
            
    df_res = pd.DataFrame(results)
    
    print("\n--- Variance Analysis by Proximity to Threshold ---")
    # Group by distance bucket
    df_res['Distance_Bucket'] = pd.cut(df_res['Distance_To_Threshold'], bins=[-np.inf, -3, 0, 3, np.inf], labels=['<-3 (Below)', '-3 to 0 (Just Below/At)', '1 to 3 (Just Above)', '>3 (Above)'])
    
    summary = df_res.groupby('Distance_Bucket')['Variance_Pct'].agg(['count', 'mean', 'median'])
    print(summary)
    
    print("\n--- Variance Analysis by Threshold ---")
    summary2 = df_res.groupby(['Nearest_Threshold', 'Distance_Bucket'])['Variance_Pct'].mean().unstack()
    print(summary2)
    
if __name__ == "__main__":
    run_analysis()
