import os

INDEX_HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zensung Premium Underwriting</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
    <div class="app-layout">
        <aside class="sidebar">
            <h1>Zensung Risk<br>Engine</h1>
            <ul class="nav-menu">
                <li class="nav-item active"><span>Dashboard</span></li>
                <li class="nav-item">
                    <a href="rules.html" target="_blank" style="color: inherit; text-decoration: none; display: block; width: 100%;">
                        <span>Underwriting Rules Used</span>
                    </a>
                </li>
            </ul>
        </aside>

        <main class="main-content">
            <header>
                <h2>Underwriting Scorecard v1.2.0</h2>
                <div class="controls">
                    <label for="test-cases">Load Test Case:</label>
                    <select id="test-cases">
                        <option value="">-- Select a Profile --</option>
                    </select>
                </div>
            </header>

            <div class="grid-container">
                <section class="panel panel-left">
                    <h3>Risk Input Parameters</h3>
                    <form id="quote-form">
                        <div class="form-grid">
                            <!-- Driver -->
                            <h4 style="grid-column: 1 / -1; margin-bottom: 0;">Driver Factors</h4>
                            <div class="form-group">
                                <label>Driver Age</label>
                                <input type="number" id="driver_age" required min="17" max="90" value="35">
                            </div>
                            <div class="form-group">
                                <label>Gender</label>
                                <select id="gender">
                                    <option value="M">Male</option>
                                    <option value="F">Female</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Years Licensed</label>
                                <select id="years_licensed">
                                    <option value="<2 years"><2 years</option>
                                    <option value="2-4 years">2-4 years</option>
                                    <option value="5+ years" selected>5+ years</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Occupation</label>
                                <select id="occupation">
                                    <option value="Professional/Exec" selected>Professional/Exec</option>
                                    <option value="Clerical/Sales">Clerical/Sales</option>
                                    <option value="Manual/Delivery">Manual/Delivery</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Previous Claims (3yr)</label>
                                <select id="previous_claims_3yr">
                                    <option value="0 claims" selected>0 claims</option>
                                    <option value="1 claim">1 claim</option>
                                    <option value="2+ claims">2+ claims</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Traffic Violations (past 3 yrs)</label>
                                <input type="number" id="traffic_violations" required min="0" value="0">
                            </div>
                            <div class="form-group">
                                <label>Telematics Risk</label>
                                <select id="telematics_risk">
                                    <option value="Low" selected>Low</option>
                                    <option value="Med">Medium</option>
                                    <option value="High">High</option>
                                </select>
                            </div>
                            
                            <!-- Vehicle -->
                            <h4 style="grid-column: 1 / -1; margin-bottom: 0; margin-top: 10px;">Vehicle Factors</h4>
                            <div class="form-group">
                                <label>Engine Capacity (cc)</label>
                                <input type="number" id="engine_capacity" required min="100" value="1600">
                            </div>
                            <div class="form-group">
                                <label>Vehicle Age (yrs)</label>
                                <input type="number" id="vehicle_age" required min="0" value="3">
                            </div>
                            <div class="form-group">
                                <label>Vehicle Value (RM)</label>
                                <input type="number" id="vehicle_value" required min="1" value="50000">
                            </div>
                            <div class="form-group">
                                <label>Vehicle Category</label>
                                <select id="vehicle_category">
                                    <option value="Private Car" selected>Private Car</option>
                                    <option value="Commercial Pickup">Commercial Pickup</option>
                                    <option value="Luxury Car">Luxury Car</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Valuation Type</label>
                                <select id="valuation_type">
                                    <option value="Market Value" selected>Market Value</option>
                                    <option value="Agreed Value">Agreed Value</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Modification Status</label>
                                <select id="modification_status">
                                    <option value="Stock/standard" selected>Stock/standard</option>
                                    <option value="Minor mods">Minor mods</option>
                                    <option value="Major mods">Major mods</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Safety Features</label>
                                <select id="safety_features">
                                    <option value="ADAS, AEB, ESC" selected>ADAS, AEB, ESC</option>
                                    <option value="Some safety">Some safety</option>
                                    <option value="Minimal">Minimal</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Tyre Condition</label>
                                <select id="tyre_condition">
                                    <option value="New/good" selected>New/good</option>
                                    <option value="Moderate">Moderate</option>
                                    <option value="Worn/illegal">Worn/illegal</option>
                                </select>
                            </div>

                            <!-- Usage -->
                            <h4 style="grid-column: 1 / -1; margin-bottom: 0; margin-top: 10px;">Usage Factors</h4>
                            <div class="form-group">
                                <label>Usage Type</label>
                                <select id="usage_type">
                                    <option value="Private" selected>Private</option>
                                    <option value="Commercial">Commercial</option>
                                    <option value="E-hailing Commercial">E-hailing Commercial</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Parking Night</label>
                                <select id="parking_night">
                                    <option value="Garaged" selected>Garaged</option>
                                    <option value="Driveway/carpark">Driveway/carpark</option>
                                    <option value="Street parking">Street parking</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Annual Trips</label>
                                <select id="annual_trips">
                                    <option value="<5,000" selected><5,000</option>
                                    <option value="5,000-10,000">5,000-10,000</option>
                                    <option value=">10,000">>10,000</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Annual Mileage (km)</label>
                                <input type="number" id="annual_mileage" required min="0" value="10000">
                            </div>

                            <!-- Claims -->
                            <h4 style="grid-column: 1 / -1; margin-bottom: 0; margin-top: 10px;">Claims Factors</h4>
                            <div class="form-group">
                                <label>Prior Claims Count</label>
                                <input type="number" id="prior_claims_count" required min="0" value="0">
                            </div>
                            <div class="form-group">
                                <label>Average Prior Severity</label>
                                <select id="average_prior_severity">
                                    <option value="Low" selected>Low</option>
                                    <option value="Med">Medium</option>
                                    <option value="High">High</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>NCD Percentage (%)</label>
                                <select id="ncd_percentage">
                                    <option value="55.0" selected>55.0%</option>
                                    <option value="45.0">45.0%</option>
                                    <option value="38.33">38.33%</option>
                                    <option value="30.0">30.0%</option>
                                    <option value="25.0">25.0%</option>
                                    <option value="0.0">0.0%</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Fault Profile</label>
                                <select id="fault_profile">
                                    <option value="Not at fault" selected>Not at fault</option>
                                    <option value="Partial fault">Partial fault</option>
                                    <option value="At fault">At fault</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Fraud Indicators</label>
                                <select id="fraud_indicators">
                                    <option value="None" selected>None</option>
                                    <option value="Minor">Minor</option>
                                    <option value="Suspicious">Suspicious</option>
                                </select>
                            </div>

                            <!-- Environmental -->
                            <h4 style="grid-column: 1 / -1; margin-bottom: 0; margin-top: 10px;">Environmental Factors</h4>
                            <div class="form-group full-width">
                                <label>Territory</label>
                                <select id="territory">
                                    <option value="Urban (KL, Selangor, Penang, Johor)" selected>Urban (KL, Selangor, Penang, Johor)</option>
                                    <option value="Urban (Other)">Urban (Other)</option>
                                    <option value="Rural (West Malaysia)">Rural (West Malaysia)</option>
                                    <option value="Rural (East Malaysia)">Rural (East Malaysia)</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Flood Zone Risk</label>
                                <select id="flood_zone">
                                    <option value="Low" selected>Low</option>
                                    <option value="Med">Medium</option>
                                    <option value="High">High</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Crime Rate</label>
                                <select id="crime_rate">
                                    <option value="Low" selected>Low</option>
                                    <option value="Medium">Medium</option>
                                    <option value="High">High</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Road Type</label>
                                <select id="road_type">
                                    <option value="Highway primary" selected>Highway primary</option>
                                    <option value="Urban mixed">Urban mixed</option>
                                    <option value="Rural/unlit">Rural/unlit</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Seasonal Risk</label>
                                <select id="seasonal_risk">
                                    <option value="Year-round" selected>Year-round</option>
                                    <option value="Monsoon seasonal">Monsoon seasonal</option>
                                    <option value="High exposure">High exposure</option>
                                </select>
                            </div>

                            <!-- Security -->
                            <h4 style="grid-column: 1 / -1; margin-bottom: 0; margin-top: 10px;">Security Factors</h4>
                            <div class="form-group">
                                <label>Immobiliser</label>
                                <select id="immobiliser">
                                    <option value="Factory fitted" selected>Factory fitted</option>
                                    <option value="Aftermarket">Aftermarket</option>
                                    <option value="None">None</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>GPS Tracking</label>
                                <select id="gps_tracking">
                                    <option value="Active tracking" selected>Active tracking</option>
                                    <option value="Passive">Passive</option>
                                    <option value="None">None</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Alarm System</label>
                                <select id="alarm_system">
                                    <option value="OEM alarm" selected>OEM alarm</option>
                                    <option value="Aftermarket">Aftermarket</option>
                                    <option value="None">None</option>
                                </select>
                            </div>

                            <!-- Policy -->
                            <h4 style="grid-column: 1 / -1; margin-bottom: 0; margin-top: 10px;">Policy Factors</h4>
                            <div class="form-group">
                                <label>Excess Chosen</label>
                                <select id="excess_chosen">
                                    <option value="High (>1,000)" selected>High (>1,000)</option>
                                    <option value="Standard">Standard</option>
                                    <option value="Minimum">Minimum</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Named Drivers</label>
                                <select id="named_drivers">
                                    <option value="1 (owner only)" selected>1 (owner only)</option>
                                    <option value="2-3">2-3</option>
                                    <option value="4+">4+</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Policy Lapse History</label>
                                <select id="policy_lapse_history">
                                    <option value="No lapse" selected>No lapse</option>
                                    <option value="1 lapse">1 lapse</option>
                                    <option value="2+ lapses">2+ lapses</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Sum Insured Accuracy</label>
                                <select id="sum_insured_accuracy">
                                    <option value="Accurate" selected>Accurate</option>
                                    <option value="A\ufffd10%">+/- 10%</option>
                                    <option value="Underinsured >10%">Underinsured >10%</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Premium Payment</label>
                                <select id="premium_payment">
                                    <option value="Annual full" selected>Annual full</option>
                                    <option value="Semi-annual">Semi-annual</option>
                                    <option value="Monthly">Monthly</option>
                                </select>
                            </div>

                            <!-- Addons -->
                            <h4 style="grid-column: 1 / -1; margin-bottom: 0; margin-top: 10px;">Add-ons</h4>
                            <div class="form-group full-width">
                                <div class="checkbox-group">
                                    <label><input type="checkbox" id="windscreen_cover"> Windscreen</label>
                                    <label><input type="checkbox" id="ncd_protector"> NCD Protector</label>
                                    <label><input type="checkbox" id="special_perils_cover"> Special Perils (Flood)</label>
                                </div>
                            </div>
                        </div>

                        <div id="error-msg" class="error-message"></div>
                        
                        <button type="submit" class="btn" id="submit-btn">Generate Quote</button>
                    </form>
                </section>

                <section class="panel-right">
                    <div class="panel">
                        <h3>Risk Analysis</h3>
                        <div class="dashboard-score">
                            <div class="score-circle" id="display_score">--</div>
                            <div class="score-details">
                                <div style="font-size: 0.875rem; color: var(--on-surface-variant); font-weight: 500;">Composite Risk Score</div>
                                <div id="display_decision" class="decision-badge">PENDING</div>
                                <div id="display_reinsurance" class="warning-flag">⚠️ Reinsurance Flag</div>
                            </div>
                        </div>

                        <!-- 7 UI Progress Bars -->
                        <div class="progress-section">
                            <div class="progress-container">
                                <div class="progress-header">
                                    <span>Driver Profile</span>
                                    <span id="driver-risk-text" class="data-mono">0 / 22</span>
                                </div>
                                <div class="progress-track" style="width: 100%; height: 8px; background: #E5E7EB; border-radius: 4px; overflow: hidden; margin-top: 4px;">
                                    <div id="driver-risk-fill" class="progress-fill" style="width: 0%; height: 100%; background: #1D4ED8; transition: width 0.5s ease-in-out;"></div>
                                </div>
                            </div>
                            
                            <div class="progress-container">
                                <div class="progress-header">
                                    <span>Vehicle Traits</span>
                                    <span id="vehicle-risk-text" class="data-mono">0 / 19</span>
                                </div>
                                <div class="progress-track" style="width: 100%; height: 8px; background: #E5E7EB; border-radius: 4px; overflow: hidden; margin-top: 4px;">
                                    <div id="vehicle-risk-fill" class="progress-fill" style="width: 0%; height: 100%; background: #1D4ED8; transition: width 0.5s ease-in-out;"></div>
                                </div>
                            </div>

                            <div class="progress-container">
                                <div class="progress-header">
                                    <span>Usage Profile</span>
                                    <span id="usage-risk-text" class="data-mono">0 / 9</span>
                                </div>
                                <div class="progress-track" style="width: 100%; height: 8px; background: #E5E7EB; border-radius: 4px; overflow: hidden; margin-top: 4px;">
                                    <div id="usage-risk-fill" class="progress-fill" style="width: 0%; height: 100%; background: #1D4ED8; transition: width 0.5s ease-in-out;"></div>
                                </div>
                            </div>

                            <div class="progress-container">
                                <div class="progress-header">
                                    <span>Claims History</span>
                                    <span id="claims-risk-text" class="data-mono">0 / 18</span>
                                </div>
                                <div class="progress-track" style="width: 100%; height: 8px; background: #E5E7EB; border-radius: 4px; overflow: hidden; margin-top: 4px;">
                                    <div id="claims-risk-fill" class="progress-fill" style="width: 0%; height: 100%; background: #1D4ED8; transition: width 0.5s ease-in-out;"></div>
                                </div>
                            </div>

                            <div class="progress-container">
                                <div class="progress-header">
                                    <span>Environmental Risk</span>
                                    <span id="geo-risk-text" class="data-mono">0 / 13</span>
                                </div>
                                <div class="progress-track" style="width: 100%; height: 8px; background: #E5E7EB; border-radius: 4px; overflow: hidden; margin-top: 4px;">
                                    <div id="geo-risk-fill" class="progress-fill" style="width: 0%; height: 100%; background: #1D4ED8; transition: width 0.5s ease-in-out;"></div>
                                </div>
                            </div>

                            <div class="progress-container">
                                <div class="progress-header">
                                    <span>Security Profile</span>
                                    <span id="security-risk-text" class="data-mono">0 / 6</span>
                                </div>
                                <div class="progress-track" style="width: 100%; height: 8px; background: #E5E7EB; border-radius: 4px; overflow: hidden; margin-top: 4px;">
                                    <div id="security-risk-fill" class="progress-fill" style="width: 0%; height: 100%; background: #1D4ED8; transition: width 0.5s ease-in-out;"></div>
                                </div>
                            </div>

                            <div class="progress-container">
                                <div class="progress-header">
                                    <span>Policy Setup</span>
                                    <span id="policy-risk-text" class="data-mono">0 / 11</span>
                                </div>
                                <div class="progress-track" style="width: 100%; height: 8px; background: #E5E7EB; border-radius: 4px; overflow: hidden; margin-top: 4px;">
                                    <div id="policy-risk-fill" class="progress-fill" style="width: 0%; height: 100%; background: #1D4ED8; transition: width 0.5s ease-in-out;"></div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="panel">
                        <h3>Premium Breakdown</h3>
                        <div class="premium-breakdown">
                            <div class="breakdown-item">
                                <span>Base Premium</span>
                                <span id="bk_base" class="data-mono">RM 0.00</span>
                            </div>
                            <div class="breakdown-item">
                                <span>Risk Loading</span>
                                <span id="bk_loading" class="data-mono">RM 0.00</span>
                            </div>
                            <div class="breakdown-item">
                                <span>E-Hailing Surcharge</span>
                                <span id="bk_ehailing" class="data-mono">RM 0.00</span>
                            </div>
                            <div class="breakdown-item">
                                <span>NCD Discount</span>
                                <span id="bk_ncd" class="data-mono">- RM 0.00</span>
                            </div>
                            <div class="breakdown-item">
                                <span>Add-ons</span>
                                <span id="bk_addons" class="data-mono">RM 0.00</span>
                            </div>
                            <div class="breakdown-item">
                                <span>Premium (excl. Tax)</span>
                                <span id="bk_excl" class="data-mono">RM 0.00</span>
                            </div>
                            <div id="display_floor_warning" class="warning-flag" style="margin-bottom: 0.5rem; text-align: center;">🛡️ Minimum Premium Floor Activated</div>
                            <div id="display_mandatory_addon" class="warning-flag" style="display: none; background-color: #fee2e2; color: #b91c1c; margin-bottom: 0.5rem; text-align: center;">🚨 Mandatory Add-on Applied</div>
                            <div id="display_ncd_stepback" class="warning-flag" style="display: none; background-color: #fef3c7; color: #b45309; margin-bottom: 0.5rem; text-align: center;">⚠️ NCD Stepped Back to 0% (Prior Claim)</div>
                            <div class="breakdown-item">
                                <span>SST (8%)</span>
                                <span id="bk_sst" class="data-mono">RM 0.00</span>
                            </div>
                            <div class="breakdown-item">
                                <span>Stamp Duty</span>
                                <span id="bk_stamp_duty" class="data-mono">RM 10.00</span>
                            </div>
                            <div class="breakdown-item total">
                                <span>Total Payable</span>
                                <span id="bk_total" class="data-mono">RM 0.00</span>
                            </div>
                        </div>
                        <div id="display_metadata" style="font-size: 0.75rem; color: var(--on-surface-variant); margin-top: 1rem; text-align: center;"></div>
                    </div>
                </section>
            </div>
        </main>
    </div>

    <script src="js/app.js"></script>
</body>
</html>
"""

APP_JS_CONTENT = """const testProfiles = [
    {
        name: "1. The Baseline National Car",
        data: {
            driver_age: 40, gender: "M", years_licensed: "5+ years", occupation: "Professional/Exec", previous_claims_3yr: "0 claims", traffic_violations: 0, telematics_risk: "Low",
            engine_capacity: 1600, vehicle_age: 3, vehicle_value: 45000, vehicle_category: "Private Car", valuation_type: "Market Value", modification_status: "Stock/standard", safety_features: "ADAS, AEB, ESC", tyre_condition: "New/good",
            usage_type: "Private", parking_night: "Garaged", annual_trips: "<5,000", annual_mileage: 10000,
            prior_claims_count: 0, average_prior_severity: "Low", ncd_percentage: "55.0", fault_profile: "Not at fault", fraud_indicators: "None",
            territory: "Urban (KL, Selangor, Penang, Johor)", flood_zone: "Low", crime_rate: "Low", road_type: "Highway primary", seasonal_risk: "Year-round",
            immobiliser: "Factory fitted", gps_tracking: "Active tracking", alarm_system: "OEM alarm",
            excess_chosen: "High (>1,000)", named_drivers: "1 (owner only)", policy_lapse_history: "No lapse", sum_insured_accuracy: "Accurate", premium_payment: "Annual full",
            windscreen_cover: false, ncd_protector: false, special_perils_cover: false
        }
    },
    {
        name: "2. The Young High-Risk Speedster",
        data: {
            driver_age: 20, gender: "M", years_licensed: "2-4 years", occupation: "Manual/Delivery", previous_claims_3yr: "1 claim", traffic_violations: 2, telematics_risk: "High",
            engine_capacity: 1500, vehicle_age: 2, vehicle_value: 90000, vehicle_category: "Private Car", valuation_type: "Market Value", modification_status: "Major mods", safety_features: "Minimal", tyre_condition: "Worn/illegal",
            usage_type: "Private", parking_night: "Street parking", annual_trips: ">10,000", annual_mileage: 15000,
            prior_claims_count: 1, average_prior_severity: "Low", ncd_percentage: "0.0", fault_profile: "At fault", fraud_indicators: "Suspicious",
            territory: "Urban (Other)", flood_zone: "Low", crime_rate: "High", road_type: "Urban mixed", seasonal_risk: "Year-round",
            immobiliser: "None", gps_tracking: "None", alarm_system: "None",
            excess_chosen: "Minimum", named_drivers: "4+", policy_lapse_history: "2+ lapses", sum_insured_accuracy: "Underinsured >10%", premium_payment: "Monthly",
            windscreen_cover: false, ncd_protector: false, special_perils_cover: false
        }
    }
];

const testSelect = document.getElementById('test-cases');
testProfiles.forEach((profile, index) => {
    const opt = document.createElement('option');
    opt.value = index;
    opt.textContent = profile.name;
    testSelect.appendChild(opt);
});

testSelect.addEventListener('change', (e) => {
    const index = e.target.value;
    if (index === "") return;
    const data = testProfiles[index].data;
    
    for (const key in data) {
        const el = document.getElementById(key);
        if (el) {
            if (el.type === 'checkbox') {
                el.checked = data[key];
            } else {
                el.value = data[key];
            }
        }
    }
});

const form = document.getElementById('quote-form');
const errorMsg = document.getElementById('error-msg');

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    errorMsg.style.display = 'none';
    
    // Check if sum_insured_accuracy is weirdly encoded due to Windows CP-1252 / UTF-8
    let siaValue = document.getElementById('sum_insured_accuracy').value;
    if (siaValue.includes('10%') && !siaValue.includes('Under')) {
        siaValue = 'A\ufffd10%';
    }

    const payload = {
        driver_age: parseInt(document.getElementById('driver_age').value),
        gender: document.getElementById('gender').value,
        years_licensed: document.getElementById('years_licensed').value,
        occupation: document.getElementById('occupation').value,
        previous_claims_3yr: document.getElementById('previous_claims_3yr').value,
        traffic_violations: parseInt(document.getElementById('traffic_violations').value),
        telematics_risk: document.getElementById('telematics_risk').value,

        engine_capacity: parseInt(document.getElementById('engine_capacity').value),
        vehicle_age: parseInt(document.getElementById('vehicle_age').value),
        vehicle_value: parseFloat(document.getElementById('vehicle_value').value),
        vehicle_category: document.getElementById('vehicle_category').value,
        valuation_type: document.getElementById('valuation_type').value,
        modification_status: document.getElementById('modification_status').value,
        safety_features: document.getElementById('safety_features').value,
        tyre_condition: document.getElementById('tyre_condition').value,

        usage_type: document.getElementById('usage_type').value,
        parking_night: document.getElementById('parking_night').value,
        annual_trips: document.getElementById('annual_trips').value,
        annual_mileage: parseInt(document.getElementById('annual_mileage').value),

        prior_claims_count: parseInt(document.getElementById('prior_claims_count').value),
        average_prior_severity: document.getElementById('average_prior_severity').value,
        ncd_percentage: parseFloat(document.getElementById('ncd_percentage').value),
        fault_profile: document.getElementById('fault_profile').value,
        fraud_indicators: document.getElementById('fraud_indicators').value,

        territory: document.getElementById('territory').value,
        flood_zone: document.getElementById('flood_zone').value,
        crime_rate: document.getElementById('crime_rate').value,
        road_type: document.getElementById('road_type').value,
        seasonal_risk: document.getElementById('seasonal_risk').value,

        immobiliser: document.getElementById('immobiliser').value,
        gps_tracking: document.getElementById('gps_tracking').value,
        alarm_system: document.getElementById('alarm_system').value,

        excess_chosen: document.getElementById('excess_chosen').value,
        named_drivers: document.getElementById('named_drivers').value,
        policy_lapse_history: document.getElementById('policy_lapse_history').value,
        sum_insured_accuracy: siaValue,
        premium_payment: document.getElementById('premium_payment').value,

        windscreen_cover: document.getElementById('windscreen_cover').checked,
        ncd_protector: document.getElementById('ncd_protector').checked,
        special_perils_cover: document.getElementById('special_perils_cover').checked
    };

    try {
        const res = await fetch('http://localhost:8015/quote', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        const data = await res.json();
        
        if (!res.ok) {
            errorMsg.textContent = `${data.error_code}: ${data.message} (Field: ${data.field})`;
            errorMsg.style.display = 'block';
            resetDashboard();
            return;
        }

        updateDashboard(data);

    } catch (err) {
        errorMsg.textContent = "Error: " + err.message;
        errorMsg.style.display = 'block';
        resetDashboard();
    }
});

function resetDashboard() {
    document.getElementById('display_score').textContent = '--';
    const badge = document.getElementById('display_decision');
    badge.textContent = 'PENDING';
    badge.className = 'decision-badge';
    document.getElementById('display_reinsurance').style.display = 'none';
    
    const resetProgressBar = (idPrefix, maxVal) => {
        const pb = document.getElementById(`${idPrefix}-risk-fill`);
        const txt = document.getElementById(`${idPrefix}-risk-text`);
        if (pb) {
            pb.style.width = '0%';
            pb.style.backgroundColor = '#1D4ED8';
        }
        if (txt) txt.innerText = `0 / ${maxVal}`;
    };
    resetProgressBar('driver', 22);
    resetProgressBar('vehicle', 19);
    resetProgressBar('usage', 9);
    resetProgressBar('claims', 18);
    resetProgressBar('geo', 13);
    resetProgressBar('security', 6);
    resetProgressBar('policy', 11);

    document.getElementById('bk_base').textContent = 'RM 0.00';
    document.getElementById('bk_loading').textContent = 'RM 0.00';
    document.getElementById('bk_ehailing').textContent = 'RM 0.00';
    document.getElementById('bk_ncd').textContent = '- RM 0.00';
    document.getElementById('bk_addons').textContent = 'RM 0.00';
    document.getElementById('bk_excl').textContent = 'RM 0.00';
    document.getElementById('display_floor_warning').style.display = 'none';
    document.getElementById('display_mandatory_addon').style.display = 'none';
    document.getElementById('display_ncd_stepback').style.display = 'none';
    document.getElementById('bk_sst').textContent = 'RM 0.00';
    document.getElementById('bk_stamp_duty').textContent = 'RM 10.00';
    document.getElementById('bk_total').textContent = 'RM 0.00';
    document.getElementById('display_metadata').textContent = '';
}

function updateDashboard(data) {
    document.getElementById('display_score').textContent = data.composite_score || '--';
    
    const badge = document.getElementById('display_decision');
    badge.textContent = data.decision.replace(/_/g, ' ');
    if (data.decision === 'AUTO_APPROVED') {
        badge.className = 'decision-badge approved';
    } else {
        badge.className = 'decision-badge referral';
    }

    document.getElementById('display_reinsurance').style.display = 
        data.reinsurance_referral ? 'block' : 'none';

    if (data.score_breakdown) {
        const setProgressBar = (idPrefix, currentVal, maxVal) => {
            const pb = document.getElementById(`${idPrefix}-risk-fill`);
            const txt = document.getElementById(`${idPrefix}-risk-text`);
            if (!pb || !txt) return;

            const percentage = Math.min((currentVal / maxVal) * 100, 100);
            pb.style.width = `${percentage}%`;
            txt.innerText = `${currentVal} / ${maxVal}`;

            if (percentage > 70) {
                pb.style.backgroundColor = 'var(--crimson)';
            } else if (percentage > 40) {
                pb.style.backgroundColor = '#fbbf24'; 
            } else {
                pb.style.backgroundColor = '#1D4ED8'; 
            }
        };

        const getScore = (obj) => {
            if (!obj) return 0;
            return Object.values(obj).reduce((a, b) => a + b, 0);
        };

        setProgressBar('driver', getScore(data.score_breakdown.driver), 22);
        setProgressBar('vehicle', getScore(data.score_breakdown.vehicle), 19);
        setProgressBar('usage', getScore(data.score_breakdown.usage), 9);
        setProgressBar('claims', getScore(data.score_breakdown.claims), 18);
        setProgressBar('geo', getScore(data.score_breakdown.environmental), 13);
        setProgressBar('security', getScore(data.score_breakdown.security), 6);
        setProgressBar('policy', getScore(data.score_breakdown.policy), 11);
    }

    if (data.premium_breakdown) {
        const fmt = (val) => `RM ${val.toFixed(2)}`;
        document.getElementById('bk_base').textContent = fmt(data.premium_breakdown.base_premium);
        document.getElementById('bk_loading').textContent = fmt(data.premium_breakdown.risk_loading_amount);
        document.getElementById('bk_ehailing').textContent = fmt(data.premium_breakdown.ehailing_surcharge);
        document.getElementById('bk_ncd').textContent = `- ${fmt(data.premium_breakdown.ncd_discount_amount)}`;
        document.getElementById('bk_addons').textContent = fmt(data.premium_breakdown.total_add_ons);
        document.getElementById('bk_excl').textContent = fmt(data.premium_breakdown.premium_excl_tax);
        document.getElementById('bk_sst').textContent = fmt(data.premium_breakdown.sst_amount);
        document.getElementById('bk_stamp_duty').textContent = fmt(data.premium_breakdown.stamp_duty);
        document.getElementById('bk_total').textContent = fmt(data.premium_breakdown.total_payable);
    }

    if (data.metadata) {
        const metaKeys = Object.keys(data.metadata);
        const terms = metaKeys.join(" | ");
        document.getElementById('display_metadata').textContent = terms;
        
        document.getElementById('display_floor_warning').style.display = 
            metaKeys.includes("PREMIUM_FLOOR_APPLIED") ? 'block' : 'none';
            
        const isMandatory = metaKeys.includes("MANDATORY FLOOD COVER APPLIED");
        document.getElementById('display_mandatory_addon').style.display = isMandatory ? 'block' : 'none';
        
        const isNcdSteppedBack = metaKeys.includes("NCD STEP-BACK APPLIED DUE TO PRIOR CLAIMS");
        document.getElementById('display_ncd_stepback').style.display = isNcdSteppedBack ? 'block' : 'none';
        
    } else {
        document.getElementById('display_floor_warning').style.display = 'none';
        document.getElementById('display_mandatory_addon').style.display = 'none';
        document.getElementById('display_ncd_stepback').style.display = 'none';
    }
}
"""

with open('frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(INDEX_HTML_CONTENT)

with open('frontend/js/app.js', 'w', encoding='utf-8') as f:
    f.write(APP_JS_CONTENT)

print("Successfully updated frontend/index.html and frontend/js/app.js")
