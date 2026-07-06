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
    1400: 273.80,  # Reverted: Original tariff (data too thin to avoid extrapolation error)
    1650: 305.50,  # Reverted: Original tariff
    2200: 339.10,  # unchanged - insufficient sample
    9999: 372.60   # unchanged - insufficient sample
}
# Reverted to original tariff rate to avoid steep slope / negative intercept extrapolation
ADDITIONAL_VALUE_RATE_PENINSULAR = 26.00

CC_RATES_EAST_MALAYSIA = {
    1400: 196.20,  # unchanged - insufficient sample (n=13)
    1650: 220.00,  # unchanged - insufficient sample (n=11)
    2200: 243.90,  # unchanged - insufficient sample (n=0)
    9999: 266.50   # unchanged - insufficient sample (n=0)
}
ADDITIONAL_VALUE_RATE_EAST_MALAYSIA = 20.30  # unchanged - insufficient sample
