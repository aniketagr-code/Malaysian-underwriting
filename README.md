# Zensung Underwriting Risk Engine

An enterprise-grade, modular InsurTech underwriting engine designed to dynamically calculate motor insurance risk profiles and compute standardized premiums based on real-world actuarial logic (PIAM proxy tariffs, NCD step-backs, and GLM interaction penalties).

##  Architecture Overview

The system is built as a **Modular Monorepo**, strictly separating the presentation layer from the core actuarial business logic.

- **Backend (`/backend`)**: A highly decoupled REST API built with FastAPI. It handles complex mathematical operations, data validation (via Pydantic), and acts as a stateless calculation "black-box".
- **Frontend (`/frontend`)**: A pure vanilla JavaScript, HTML, and CSS single-page application (SPA). It acts as a lightweight presentation layer to visualize the JSON outputs from the engine.
- **Documentation (`/docs`)**: Contains the system design philosophy and detailed actuarial pricing rules.

### System Flow
```mermaid
graph TD
    Client[Frontend UI / Mobile App] -->|POST /quote| API[FastAPI Gateway]
    API --> Validator[Pydantic Schema Validation]
    Validator --> Engine[Underwriting Engine]
    
    subgraph "Underwriting Core"
        Engine --> Driver[Driver Risk Score]
        Engine --> Claim[Claims Risk Score]
        Engine --> Geo[Geographic Risk]
        Engine --> Vehicle[Vehicle Risk]
    end
    
    Driver --> Calc[Premium Calculator]
    Claim --> Calc
    Geo --> Calc
    Vehicle --> Calc
    
    Calc -->|JSON Response| API
    API -->|Premium Breakdown & Scorecard| Client
```

##  Getting Started

## Prerequisites

Before running the project, ensure you have:

- Python 3.9 or later installed
- A modern web browser (Chrome, Edge, or Firefox)

Verify your Python installation:

```bash
python --version
```

---

## 1. Start the Backend API

Open the project in Visual Studio Code and navigate to the backend directory:

```bash
cd backend
```

Start the FastAPI server.

### Windows (using the project virtual environment)

```bash
..\venv\Scripts\uvicorn app.main:app --port 8015 --reload
```

### macOS / Linux

```bash
../venv/bin/uvicorn app.main:app --port 8015 --reload
```

> **Note:** If you are not using the project's virtual environment, you can instead run:

```bash
python -m uvicorn app.main:app --port 8015 --reload
```

If the server starts successfully, you should see:

```text
INFO: Uvicorn running on http://127.0.0.1:8015
INFO: Application startup complete.
```

Keep this terminal running while using the application.

---

## 2. Start the Frontend Application

Open a **new terminal** (leave the backend terminal running) and navigate to the project root directory (the folder containing both `backend` and `frontend`).

Run:

```bash
python -m http.server 8080
```

If successful, the terminal will display:

```text
Serving HTTP on 0.0.0.0 port 8080
```

Keep this terminal running while using the application.

---

## 3. Launch the Application

Open your web browser and navigate to:

```
http://localhost:8080/frontend/index.html
```

The underwriting dashboard should now load successfully.

---

## Stopping the Application

When you are finished using the application, press **Ctrl + C** in both terminal windows to stop the backend and frontend servers.

##  Core Underwriting Logic

The pricing engine simulates enterprise insurance logic by calculating a **Composite Risk Score** out of 100 points, broken into functional domains:

1. **Driver Risk (30 pts):** Evaluates age, traffic violations, and telematics behavior. High-risk ages (under 25 or over 70) and frequent violators trigger steep penalties.
2. **Claims Risk (25 pts):** Tracks claim frequency and severity. Crucially, the engine mathematically enforces the **NCD Step-Back Rule**. If a prior claim exists and the driver has no NCD Protector, the engine overrides the requested NCD to `0%`.
3. **Geographic Risk (20 pts):** Uses territorial zoning. High-density urban areas (Klang Valley, Penang, Johor) carry heavy weight due to traffic density and theft frequencies, whereas rural East Malaysia carries a baseline score of `0`.
4. **Vehicle Risk (15 pts):** Categorizes assets (e.g., Luxury vs. Commercial Pickup) and applies valuation penalties.
5. **Usage Risk (10 pts):** Penalizes high annual mileage and commercial/e-hailing usage.

### Enterprise Edge Cases Handled:
- **GLM Concentration Penalty**: If a profile scores dangerously high (>70%) across multiple domains simultaneously, a synergistic risk penalty is applied.
- **Minimum Premium Floors**: The engine enforces a strict base premium floor; if aggressive discounts drop the rate below the sustainable threshold, the engine automatically floors it.
- **Mandatory Add-ons**: If a user is located in a High-Risk Flood Zone, the engine automatically injects Flood Endorsement pricing and flags the metadata to notify the user dynamically.
