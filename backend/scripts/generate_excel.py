import pandas as pd
import numpy as np
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from backend.app.engine import generate_quote
from backend.app.validation import map_row_to_quote_request

def generate_excel_model():
    out_path = 'backend/data/Zensung_Underwriting_Model.xlsx'
    
    # Create a Pandas Excel writer using openpyxl as the engine.
    writer = pd.ExcelWriter(out_path, engine='openpyxl')
    
    # --- Sheet 1: Instructions ---
    instructions = pd.DataFrame({
        'Zensung Underwriting Risk Engine - Model Documentation': [
            'This workbook serves as Deliverable 1 for the InsurTech pricing engine.',
            'Sheet 1: Instructions - Overview of the workbook.',
            'Sheet 2: Risk Input Form - The 23 data points required to price a policy.',
            'Sheet 3: Risk Scoring - The actuarial point mapping for the 23 factors.',
            'Sheet 4: Premium Calculator - The calculation flow from Base Premium to Final Payable.',
            'Sheet 5: Market Comparison - Comparison against market competitors (Allianz, Etiqa, AIG).',
            'Sheet 6: Test Cases - 10 validated policies pulled from the Python engine.'
        ]
    })
    instructions.to_excel(writer, sheet_name='1. Instructions', index=False)
    
    # --- Sheet 2: Risk Input Form ---
    risk_inputs = pd.DataFrame({
        'Category': ['Driver']*7 + ['Vehicle']*6 + ['Usage']*3 + ['Claims']*4 + ['Environmental']*5 + ['Security']*3 + ['Policy']*5,
        'Factor': [
            'Driver Age', 'Gender', 'Years Licensed', 'Occupation', 'Annual Mileage', 'Previous Claims (3yr)', 'Traffic Violations',
            'Engine CC', 'Vehicle Age', 'Vehicle Value', 'Modification Status', 'Safety Features', 'Tyre Condition',
            'Usage Type', 'Parking Night', 'Annual Trips',
            'NCD Percentage', 'Prior Claims Count', 'Average Prior Severity', 'Fault Profile',
            'Flood Zone', 'Crime Rate', 'Road Type', 'Seasonal Risk', 'Territory',
            'Immobiliser', 'GPS Tracking', 'Alarm System',
            'Excess Chosen', 'Named Drivers', 'Policy Lapse History', 'Sum Insured Accuracy', 'Premium Payment'
        ],
        'Data Type': ['Numeric', 'Categorical', 'Categorical', 'Categorical', 'Numeric', 'Categorical', 'Numeric',
                      'Numeric', 'Numeric', 'Numeric', 'Categorical', 'Categorical', 'Categorical',
                      'Categorical', 'Categorical', 'Categorical',
                      'Numeric', 'Numeric', 'Categorical', 'Categorical',
                      'Categorical', 'Categorical', 'Categorical', 'Categorical', 'Categorical',
                      'Categorical', 'Categorical', 'Categorical',
                      'Categorical', 'Categorical', 'Categorical', 'Categorical', 'Categorical']
    })
    risk_inputs.to_excel(writer, sheet_name='2. Risk Input Form', index=False)
    
    # --- Sheet 3: Risk Scoring ---
    scoring = pd.DataFrame({
        'Domain': ['Driver Risk', 'Vehicle Risk', 'Usage Risk', 'Claims Risk', 'Environmental Risk', 'Security Risk', 'Policy Risk'],
        'Max Points': [22, 19, 9, 18, 13, 6, 11],
        'Description': [
            'Penalizes young/inexperienced drivers and risky occupations.',
            'Penalizes luxury vehicles, heavy modifications, and poor tyre conditions.',
            'Surcharges e-hailing, street parking, and high annual trips.',
            'Penalizes frequency of claims and at-fault accidents. 0 NCD gets heavily penalized.',
            'Penalizes high flood risk, high crime rate, and urban density.',
            'Rewards aftermarket/active tracking immobilisers and GPS.',
            'Penalizes underinsurance and minimum excess choices.'
        ]
    })
    scoring.to_excel(writer, sheet_name='3. Risk Scoring', index=False)
    
    # --- Sheet 4: Premium Calculator ---
    calculator = pd.DataFrame({
        'Step': [1, 2, 3, 4, 5, 6, 7, 8, 9],
        'Calculation': [
            'Base Premium (Tariff proxy based on CC and Value)',
            'Risk Loading (0%, 15%, 30%, 50% applied on Base Premium)',
            'Gross Base Premium (Base + Loading)',
            'NCD Deduction (Applied to Gross Base Premium)',
            'E-Hailing Surcharge (Added after NCD)',
            'Premium Floor Check (Enforces RM 350 minimum)',
            'Add-ons (Flood, Windscreen, NCD Protector)',
            'Taxes (8% SST, RM 10 Stamp Duty)',
            'Final Total Payable'
        ]
    })
    calculator.to_excel(writer, sheet_name='4. Premium Calculator', index=False)
    
    # --- Sheet 5: Market Comparison ---
    market = pd.DataFrame({
        'Insurer': ['Zensung (Engine)', 'Allianz', 'Etiqa', 'AIG'],
        'Base Pricing Model': ['Rule-based (4 bands)', 'Continuous GLM', 'Continuous GLM', 'Continuous GLM'],
        'Data Requirements': ['High (23 factors)', 'Moderate', 'Moderate', 'High'],
        'Pricing Speed': ['Real-time (API)', 'Real-time (API)', 'Real-time (API)', 'Batch/API'],
        'Limitations': ['Sparse historical data suppresses loading', 'Black-box pricing', 'Conservative risk appetite', 'Strict telematics requirement']
    })
    market.to_excel(writer, sheet_name='5. Market Comparison', index=False)
    
    # --- Sheet 6: Test Cases ---
    file_path = 'backend/data/BITs_Sample_Data_Workbook.xlsx'
    policies = pd.read_excel(file_path, sheet_name='MV_Policies', header=3)
    
    test_cases = []
    # Pull first 10 valid policies
    for idx, row in policies.iterrows():
        if len(test_cases) >= 10: break
        if pd.isna(row['Final_Premium_MYR']) or pd.isna(row['Engine_CC']): continue
        
        req = map_row_to_quote_request(row)
        try:
            res = generate_quote(req)
            test_cases.append({
                'Policy_ID': row['Policy_ID'],
                'Age': req.driver_age,
                'CC': req.engine_capacity,
                'Sum_Insured': req.vehicle_value,
                'Composite_Score': res['composite_score'],
                'Risk_Loading_Pct': res['premium_breakdown']['risk_loading_pct'],
                'Zensung_Premium_MYR': res['premium_breakdown']['total_payable'],
                'Actual_Historical_MYR': row['Final_Premium_MYR']
            })
        except:
            continue
            
    test_df = pd.DataFrame(test_cases)
    test_df.to_excel(writer, sheet_name='6. Test Cases', index=False)
    
    # Close the Pandas Excel writer and output the Excel file.
    writer.close()
    print(f"Successfully generated {out_path} with 6 sheets.")

if __name__ == "__main__":
    generate_excel_model()
