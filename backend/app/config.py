# Constants for Actuarial Calculation
SCORECARD_VERSION = "1.2.0"

PREMIUM_FLOOR = 350.00
SST_RATE = 0.08
WINDSCREEN_FLAT = 100.00
FLOOD_RATE = 0.005
EHAILING_SURCHARGE = 400.00
# Validated against NCD_Rules from BITs_Sample_Data_Workbook
NCD_PROTECTOR_LOADING = 0.15
STAMP_DUTY = 10.00

CC_RATES_PENINSULAR = {
    1400: 180.18,  # Derived from 80% split of <=1400cc Private Peninsular bucket
    1650: 78.02,   # Derived from 80% split of <=1650cc Private Peninsular bucket
    2200: 339.10,  # unchanged - insufficient sample (n=2)
    9999: 372.60   # unchanged - insufficient sample (n=5)
}
# Using slope derived from <=1400cc Private Peninsular model as it is the most robust sample
ADDITIONAL_VALUE_RATE_PENINSULAR = 39.33

CC_RATES_EAST_MALAYSIA = {
    1400: 196.20,  # unchanged - insufficient sample (n=13)
    1650: 220.00,  # unchanged - insufficient sample (n=11)
    2200: 243.90,  # unchanged - insufficient sample (n=0)
    9999: 266.50   # unchanged - insufficient sample (n=0)
}
ADDITIONAL_VALUE_RATE_EAST_MALAYSIA = 20.30  # unchanged - insufficient sample
