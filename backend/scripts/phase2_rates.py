import pandas as pd
import math
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np

file_path = 'backend/data/BITs_Sample_Data_Workbook.xlsx'
df = pd.read_excel(file_path, sheet_name='MV_Policies', header=3)
df['Engine_CC'] = pd.to_numeric(df['Engine_CC'], errors='coerce')
df['Sum_Insured_MYR'] = pd.to_numeric(df['Sum_Insured_MYR'], errors='coerce')
df['Base_Premium_MYR'] = pd.to_numeric(df['Base_Premium_MYR'], errors='coerce')

def get_cc_band(cc):
    if pd.isna(cc): return 'Unknown'
    if cc <= 1400: return '<=1400'
    elif cc <= 1650: return '<=1650'
    elif cc <= 2200: return '<=2200'
    else: return '>2200'
df['CC_Band'] = df['Engine_CC'].apply(get_cc_band)
df['Blocks'] = df['Sum_Insured_MYR'].apply(lambda v: math.ceil(max(0, v - 1000) / 1000.0) if pd.notna(v) else 0)

east_malaysia_states = ['Sabah', 'Sarawak', 'Labuan']

for band in ['<=1400', '<=1650']:
    for region, is_east in [('East Malaysia', True), ('Peninsular', False)]:
        if is_east:
            subset = df[(df['CC_Band'] == band) & (df['Vehicle_Use'] == 'PRIVATE') & (df['State'].isin(east_malaysia_states))].copy()
        else:
            subset = df[(df['CC_Band'] == band) & (df['Vehicle_Use'] == 'PRIVATE') & (~df['State'].isin(east_malaysia_states))].copy()
        
        if len(subset) == 0:
            print(f"Bucket: {band} PRIVATE {region} (n=0)")
            continue
            
        # The instruction was "split that bucket's rows only (80/20, fixed random_state=42)". 
        # Does the bucket mean the CCxUsage bucket overall, or CCxUsagexRegion? 
        # Let's see if splitting the subset works. If n is too small, train_test_split might complain.
        try:
            train, test = train_test_split(subset, test_size=0.20, random_state=42)
            if len(train) == 0:
                print(f"Bucket: {band} PRIVATE {region} (n={len(subset)}) - insufficient for training")
                continue
                
            X = train[['Blocks']]
            y = train['Base_Premium_MYR']
            model = LinearRegression().fit(X, y)
            print(f"Bucket: {band} PRIVATE {region} (n={len(subset)})")
            print(f"  Intercept (CC Rate): {model.intercept_:.2f}")
            print(f"  Slope (Additional Value Rate): {model.coef_[0]:.2f}")
        except Exception as e:
            print(f"Error on {band} {region}: {e}")
