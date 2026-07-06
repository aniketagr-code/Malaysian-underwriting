# Zensung Underwriting Risk Engine: Project Report

## 1. Executive Summary
The **Zensung Underwriting Risk Engine** is a modern, enterprise-grade InsurTech prototype designed to digitize and automate complex motor insurance underwriting. Built to mirror post-detariffication actuarial logic in the Malaysian market, the system calculates dynamic risk scores, enforces strict regulatory rules (such as PIAM’s NCD step-back), and generates real-time premium quotes. 

The primary objective of this project was to demonstrate how legacy monolithic insurance systems can be modernized using an API-first, decoupled architecture. By strictly separating the actuarial mathematics from the user interface, the engine achieves high scalability, rigorous data validation, and seamless cross-platform integration.

---

## 2. System Architecture
The project utilizes a **Modular Monorepo** structure to separate concerns and ensure maintainability.

*   **Backend (The Brain):** Built with **FastAPI** (Python). It acts as a stateless calculation engine. It receives raw data, runs it through multi-layered pricing algorithms, and returns a structured JSON response.
*   **Frontend (The Presentation Layer):** A lightweight Single Page Application (SPA) built with pure HTML, CSS (Inter font, modern tonal shadows), and Vanilla JavaScript. It makes asynchronous `fetch()` calls to the API and renders the mathematical output visually.
*   **Data Validation:** Handled by **Pydantic**. Before the underwriting engine even processes a quote, strict schema validation ensures data integrity (e.g., verifying the driver’s age is mathematically logical).

---

## 3. Actuarial Methodology & Risk Scoring
The engine utilizes a 100-point **Composite Risk Scorecard** based on proxy weights derived from Generalized Linear Model (GLM) principles. The maximum allowable score is 100 points, broken down into five core domains:

1.  **Driver Risk (Max 30 pts):** Evaluates the human element. High-risk age bands (<25 and >70) and drivers with multiple traffic violations receive severe mathematical penalties due to statistically higher accident frequencies.
2.  **Claims Risk (Max 25 pts):** Evaluates historical behavior. Prior claims exponentially increase the score.
3.  **Geographic Risk (Max 20 pts):** Uses territorial zoning. High-density urban areas (Klang Valley, Penang, Johor) carry heavy point loads due to severe traffic density and elevated vehicle theft rates compared to rural zones.
4.  **Vehicle Risk (Max 15 pts):** Penalizes luxury vehicles and commercial pickups due to the higher severity (cost) of repairs and replacement parts.
5.  **Usage Risk (Max 10 pts):** Applies surcharges for E-hailing usage, accounting for the exponentially higher hours spent on the road compared to private usage.

---

## 4. Key Features & Edge Case Handling
What sets this engine apart from standard calculators is its ability to programmatically handle complex insurance edge cases:

*   **The NCD Step-Back Rule:** The engine mathematically enforces the Persatuan Insurans Am Malaysia (PIAM) NCD rules. If a driver declares a prior claim but does not possess an active NCD Protector add-on, the engine intercepts the calculation and automatically forces their No Claim Discount down to 0%, overriding any user input.
*   **GLM Concentration Penalty (Synergistic Risk):** If a profile scores dangerously high (>70%) across multiple domains simultaneously (e.g., a 19-year-old driving a luxury sports car in Kuala Lumpur), the engine applies a synergistic risk penalty. It overrides the `AUTO_APPROVED` status and forces a `MANUAL_REFERRAL` to protect the insurer.
*   **Premium Flooring:** To protect the insurer's Loss Ratio from over-discounting, the engine enforces a hard minimum base premium floor. 
*   **Dynamic Mandatory Perils:** If the geographical data indicates a High-Risk Flood Zone, the engine mathematically forces the Flood Endorsement onto the policy, protecting both the consumer and the insurer from climate-related total losses.

---

## 5. Actuarial Limitations & Variance Analysis
While the engine successfully digitizes the quoting process, backtesting against historical PIAM datasets (`BITs_Sample_Data_Workbook.xlsx`) revealed two significant mathematical limitations:

1. **Discrete Banding vs. Continuous GLM:** Real-world Malaysian insurers price risk continuously via Generalized Linear Models (GLMs)—every marginal point of risk moves the premium slightly. Our engine uses a simpler rule-based structure, applying loading in four discrete steps (0%, 15%, 30%, 50%). This means two policies with different risk profiles inside the same band get identical loading, guaranteeing a variance against real-world premiums.
2. **Sparse Historical Data Suppression:** The historical test data only contains 2 of the 23 scorecard factors (Gender and Occupation). Because we cannot fabricate data to avoid data leakage, the remaining 21 factors default to 0 points ("lowest risk"). During testing, the maximum composite score achieved was 21 points, which failed to trigger even the first 40-point risk loading tier. The observed 18-35% variance is therefore the raw gap between unadjusted base tariffs and real-world Final Premiums.

---

## 6. AI Tool Evaluation
During the development of this engine, AI agents were utilized for code generation and actuarial tuning. This process required rigorous human oversight, highlighting several critical lessons in AI workflow integration:

* **Catching Mathematical Hallucinations (Monotonicity Bug):** An AI agent attempted to "recalibrate" base CC rates by fitting independent linear regressions for each CC bucket. It extrapolated intercepts down to Sum Insured = RM 1,000 (where no data existed). This created a monotonicity violation where a 1650cc engine priced *lower* than a 1400cc engine. This was caught via manual sanity checks and reverted to the stable PIAM tariff rates.
* **Rejecting Tautological Testing:** The AI initially wrote `pytest` assertions that dynamically set the "pass tolerance" to whatever variance the engine produced, resulting in a 100% pass rate that hid a 200%+ mathematical error. We forced a strict, hardcoded 15% tolerance to expose the real accuracy.
* **Escaping Corruption:** An AI file-writing tool introduced a syntax error (`\'Unknown\'`) into the validation script. The AI claimed the test ran successfully, but human verification proved the file couldn't even import. This reinforced the rule: never accept an AI summary of success without verifying the raw terminal output.

---

## 7. Conclusion & Business Value
The Zensung Underwriting Risk Engine successfully bridges the gap between modern software engineering and complex legacy insurance mathematics. 

By utilizing **"Calibrated Test Weights,"** the engine proves that the architecture is fully functional and capable of handling extreme edge cases. When preparing for a commercial launch, an Actuarial team simply needs to supply their proprietary GLM relativities. Because the system is completely modular, those final numbers can be swapped into the backend in minutes without requiring any structural rewrites. 

This project stands as a highly viable blueprint for insurers looking to modernize their pricing engines, deploy faster quoting mechanisms, and integrate via APIs with third-party distributors or mobile applications.
