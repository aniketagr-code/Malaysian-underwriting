import pandas as pd

file_path = 'backend/data/BITs_Sample_Data_Workbook.xlsx'
risk_factors = pd.read_excel(file_path, sheet_name='MV_Risk_Factors', header=3)

print("=== 2. MV_Risk_Factors ===")
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 15)
# 'Category', 'Risk Factor', 'Low Risk', 'Medium Risk', 'High Risk', 'Score Range', 'Underwriting Action'
print(risk_factors[['Category', 'Risk Factor', 'Low Risk', 'Medium Risk', 'High Risk', 'Score Range']])
