import pandas as pd
df = pd.read_excel('backend/data/BITs_Sample_Data_Workbook.xlsx', sheet_name='MV_Risk_Factors', header=3)
df.to_csv('backend/scripts/temp_factors.csv', index=False)
