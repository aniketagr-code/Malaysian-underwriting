const testProfiles = [
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
        siaValue = 'A�10%';
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
