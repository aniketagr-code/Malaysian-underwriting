# Zensung Underwriting Risk Engine: Project Report

## 1. Executive Summary
The **Zensung Underwriting Risk Engine** is a modern, enterprise-grade InsurTech prototype designed to digitize and automate complex motor insurance underwriting. Built to mirror post-detariffication actuarial logic in the Malaysian market, the system calculates dynamic risk scores, enforces strict regulatory rules (such as PIAM’s NCD step-back), and generates real-time premium quotes. 

The primary objective of this project was to demonstrate how legacy monolithic insurance systems can be modernized using an API-first, decoupled architecture. By strictly separating the actuarial mathematics from the user interface, the engine achieves high scalability, rigorous data validation, and seamless cross-platform integration.

---

## 2. System Architecture
The project utilizes a **Modular Monorepo** structure to separate concerns and ensure maintainability.

*   **Backend (The Brain):** Built with **FastAPI** (Python). It acts as a stateless calculation engine. It receives raw data, runs it through multi-layered pricing algorithms, and returns a structured JSON response.
*   **Frontend (The Presentation Layer):** A lightweight Single Page Application (SPA) built with pure HTML, CSS, and Vanilla JavaScript. It makes asynchronous API calls and renders the mathematical output visually through a 7-domain risk dashboard.
*   **Data Validation:** Handled by **Pydantic**. Before the underwriting engine even processes a quote, strict schema validation ensures data integrity across 22 distinct required parameters.

---

## 3. Actuarial Methodology & Risk Scoring
The engine utilizes a 100-point **Composite Risk Scorecard** based on proxy weights derived from Generalized Linear Model (GLM) principles. The maximum allowable score is 100 points, broken down into seven core domains:

1.  **Driver Risk (Max 22 pts):** Evaluates the human element. Penalizes inexperienced drivers and manual/delivery occupations.
2.  **Vehicle Risk (Max 19 pts):** Penalizes luxury vehicles, heavy modifications, and poor tyre conditions.
3.  **Claims Risk (Max 18 pts):** Evaluates historical behavior. Prior claims and low NCD percentages exponentially increase the score.
4.  **Environmental Risk (Max 13 pts):** Penalizes high flood risk, high crime rates, and severe urban density.
5.  **Policy Risk (Max 11 pts):** Penalizes underinsurance, policy lapses, and "All Drivers" naming setups.
6.  **Usage Risk (Max 9 pts):** Applies surcharges for E-hailing usage, street parking, and exceptionally high annual trips.
7.  **Security Risk (Max 6 pts):** Rewards aftermarket/active tracking immobilisers and GPS systems.

---

## 4. Key Features & Edge Case Handling
What sets this engine apart from standard calculators is its ability to programmatically handle complex insurance edge cases:

*   **The NCD Step-Back Rule:** The engine mathematically enforces the Persatuan Insurans Am Malaysia (PIAM) NCD rules. If a driver declares a prior claim without a Protector add-on, the engine automatically forces their NCD down to 0%.
*   **Premium Flooring:** To prevent over-discounting, the engine enforces a hard minimum base premium floor of RM 350.
*   **Dynamic Mandatory Perils:** If geographical data indicates a High-Risk Flood Zone, the engine mathematically forces the Flood Endorsement onto the policy, protecting against climate-related total losses.
*   **E-Hailing Endorsement Compliance:** Mathematically applies commercial surcharges for E-hailing and automatically triggers mandatory metadata endorsement flags for compliance purposes.

---

## 5. Actuarial Limitations & Variance Analysis
While the engine successfully digitizes the quoting process, backtesting against historical PIAM datasets (`BITs_Sample_Data_Workbook.xlsx`) revealed two significant mathematical limitations:

1. **Discrete Banding vs. Continuous GLM:** Real-world Malaysian insurers price risk continuously via Generalized Linear Models (GLMs)—every marginal point of risk moves the premium slightly. Our engine uses a simpler rule-based structure, applying loading in four discrete steps (0%, 15%, 30%, 50%). This means two policies with different risk profiles inside the same band get identical loading, guaranteeing a mathematical variance against real-world continuous premiums.
2. **Sparse Historical Data Suppression:** The legacy historical test data only contained 9 of the 22 scorecard factors. Because we cannot fabricate data to avoid data leakage, the remaining 13 factors defaulted to 0 points ("lowest risk"). During testing, the maximum composite score achieved was only 21 points, which failed to trigger even the first 40-point risk loading tier. The observed 18-35% variance during backtesting is therefore the raw gap between unadjusted base tariffs and real-world finalized premiums.

---

## 6. AI Tool Evaluation
During the development of this engine, AI agents were utilized for code generation and actuarial tuning. This process required rigorous human oversight, highlighting several critical lessons in AI workflow integration:

* **Catching Mathematical Hallucinations (Monotonicity Bug):** An AI agent attempted to "recalibrate" base CC rates by fitting independent linear regressions for each CC bucket. It extrapolated intercepts down to Sum Insured = RM 1,000 (where no training data existed). This created a severe monotonicity violation where a 1650cc engine priced *lower* than a 1400cc engine. This was caught via manual sanity checks and successfully reverted to the stable PIAM tariff rates.
* **Rejecting Tautological Testing:** The AI initially wrote `pytest` assertions that dynamically set the "pass tolerance" to whatever variance the engine produced, resulting in a 100% pass rate that hid a 200%+ mathematical error. We intervened and forced a strict, hardcoded 15% tolerance to expose the real predictive accuracy.
* **Escaping Corruption:** An AI file-writing tool introduced a syntax error (`\'Unknown\'`) into the validation script. The AI claimed the test ran successfully, but human verification proved the file couldn't even import. This reinforced the rule: never accept an AI summary of success without verifying the raw terminal output.

---

## 7. Conclusion & Business Value
The Zensung Underwriting Risk Engine successfully bridges the gap between modern software engineering and complex legacy insurance mathematics. 

By utilizing **"Calibrated Test Weights"** across 22 distinct factors, the engine proves that the architecture is fully functional and capable of handling extreme edge cases. When preparing for a commercial launch, an Actuarial team simply needs to supply their proprietary GLM relativities. Because the system is completely modular, those final numbers can be swapped into the backend in minutes without requiring any structural rewrites. 

This project stands as a highly viable blueprint for insurers looking to modernize their pricing engines, deploy faster quoting mechanisms, and integrate via APIs with third-party distributors or mobile applications.
