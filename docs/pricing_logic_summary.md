# Comprehensive Underwriting Logic & Risk Scoring System (Scorecard v1.1.0)

This document outlines the complete set of underwriting rules, risk point algorithms, and referral triggers currently hardcoded in `backend/engine.py`. Version 1.1.0 introduces explicit 0-point bands, GLM interaction proxies, and decoupled frequency/severity scoring.

---

## 1. The Composite Risk Score
The system aggregates risk points across 5 distinct domains. The total sum becomes the **Composite Risk Score**, which dictates pricing penalties or outright quote rejection.

### A. Driver Score (Max 30 points)
| Risk Factor | Condition | Points |
|-------------|-----------|--------|
| **Driver Age** | 25 or younger | +12 |
| | 26 to 30 | +8 |
| | 31 to 60 | 0 |
| | 61 to 75 | +5 |
| | 76 or older | +10 |
| **Traffic Violations** | 0 | 0 |
| | Exactly 1 | +5 |
| | 2 or more | +10 |
| **Telematics Risk** | Low | 0 |
| | Medium | +4 |
| | High | +8 |

### B. Claims Score (Max 25 points)
*Note: If the user purchases the "NCD Protector" add-on, this entire section is overridden to **0 points**.*
| Risk Factor | Condition | Points |
|-------------|-----------|--------|
| **NCD Level** | 0.0% | +15 |
| | 25.0% | +12 |
| | 30.0% | +9 |
| | 38.33% | +6 |
| | 45.0% | +3 |
| | 55.0% | 0 |
| **Frequency vs Severity** | 0 Claims | 0 |
| | >0 Claims | `min(25, severity_points * claims_multiplier)` |

**Severity Points:** Low = 2, Medium = 5, High = 10
**Claims Multipliers:** 1 Claim = 1.0x, 2 Claims = 1.5x, 3 Claims = 2.0x, 4+ Claims = 3.0x

### C. Geographic Score (Max 20 points)
| Risk Factor | Condition | Points |
|-------------|-----------|--------|
| **Territory** | Urban (KL/Selangor/Penang/Johor) | +15 |
| | Urban (Other)* | +9 |
| | Rural West Malaysia | +6 |
| | Rural East Malaysia | 0 |
| **Flood Zone Risk**| Low | 0 |
| | Medium | +2 |
| | High | +5 |
*\*v1.1.0 Simplification: Conflates all other major urban centers (e.g. Ipoh, Kuantan). Future v2.0.0 will split by density and granular auto-theft rate.*

### D. Vehicle Score (Max 15 points)
| Risk Factor | Condition | Points |
|-------------|-----------|--------|
| **Category** | Luxury Car | +8 |
| | Commercial Pickup | +6 |
| | Private Car | 0 |
| **Valuation Type** | Market Value | +5 |
| | Agreed Value | 0 |
| **Vehicle Age** | 0 to 10 years | 0 |
| | Older than 10 years | +2 |

### E. Usage Score (Max 10 points)
| Risk Factor | Condition | Points |
|-------------|-----------|--------|
| **Annual Mileage** | <= 14,999 km | 0 |
| | 15,000 to 30,000 km | +3 |
| | > 30,000 km | +6 |
| **Usage Type** | Private | 0 |
| | Commercial OR E-Hailing | +4 |

---

## 2. GLM Concentration Penalty (Interaction Terms)

Version 1.1.0 introduces a proxy for Generalized Linear Model (GLM) interaction terms. If a risk is heavily concentrated in a single domain, an interaction penalty applies.
**Rule:** If the pre-penalty Composite Score > 60 AND any single domain exceeds 70% of its maximum possible points, a flat **+5 Concentration Penalty** is added to the Composite Score.

---

## 3. Underwriting Decision Thresholds

### Auto-Rejection (Underwriter Referral)
If the **Composite Score >= 80**, the system immediately rejects auto-pricing. 
* **Result**: "REFER_TO_UNDERWRITER" status. No premium breakdown is returned.

### Premium Risk Loading (Penalties)
If the score is below 80, the engine calculates the Base Premium and applies a percentage penalty based on the score:
* **Score 75 to 79**: +50% Risk Loading on Base Premium
* **Score 60 to 74**: +30% Risk Loading on Base Premium
* **Score 40 to 59**: +15% Risk Loading on Base Premium
* **Score 0 to 39**: 0% Risk Loading (Standard Risk)

---

## 4. Financial & System Flags

### Reinsurance Referral
The quote is flagged for facultative reinsurance review (which alerts the insurer they cannot retain 100% of the risk) if *either* of these are true:
1. **Vehicle Value > RM 150,000**
2. **Usage Type = "Commercial"**
*Note: E-Hailing Commercial usage is EXCLUDED from individual reinsurance triggers because it is typically handled via fleet-level cession. However, a high-value E-Hailing vehicle (>150k) will still trigger purely based on the sum insured.*

### Hardcoded Surcharges & Floors
* **E-Hailing Surcharge**: A flat RM 400.00 is added to the Core Premium if Usage Type = "E-hailing Commercial".
* **Minimum Premium Floor**: Regardless of NCD discounts, the Core Premium (Liability/Collision kernel) can never fall below **RM 350.00**. This ensures baseline rate adequacy before Add-Ons are priced.

---

## 5. Known Limitations & Future Roadmap (v2.0.0)
- **Heuristic Weights**: The current point scoring arrays, risk loading percentages, and interaction penalties detailed in this document are strictly **heuristic and expert-judgment based**. They serve as a deterministic rules engine for proxy pricing but are not mathematically derived from empirical loss ratios.
- **Future Direction (GLM Integration)**: The natural architectural progression for version 2.0.0 is replacing these heuristic point tables with purely statistical Generalized Linear Model (GLM) coefficients fitted against historical claims and loss data to generate statistically accurate relativity multipliers.
- **Data Access Limitations**: It must be explicitly noted that we do not currently have access to actual historical claims and loss datasets required to train a GLM. In the Malaysian motor insurance context, this proprietary empirical data is highly restricted and can typically only be accessed via authorized partnership with **ISM (Insurance Services Malaysia)**, which acts as the central statistical data pool for the industry.
