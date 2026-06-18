const testProfiles = [
    {
        name: "1. The Baseline National Car",
        data: {
            driver_age: 40, traffic_violations: 0, telematics_risk: "Low", ncd_percentage: "55.0", prior_claims_count: 0, average_prior_severity: "Low", territory: "Urban (KL, Selangor, Penang, Johor)", flood_zone: "Low", vehicle_value: 45000, engine_capacity: 1600, vehicle_category: "Private Car", valuation_type: "Market Value", vehicle_age: 3, annual_mileage: 10000, usage_type: "Private", windscreen_cover: false, ncd_protector: false, special_perils_cover: false
        }
    },
    {
        name: "2. The Young High-Risk Speedster",
        data: {
            driver_age: 20, traffic_violations: 2, telematics_risk: "High", ncd_percentage: "0.0", prior_claims_count: 0, average_prior_severity: "Low", territory: "Urban (Other)", flood_zone: "Low", vehicle_value: 90000, engine_capacity: 1500, vehicle_category: "Private Car", valuation_type: "Market Value", vehicle_age: 2, annual_mileage: 15000, usage_type: "Private", windscreen_cover: false, ncd_protector: false, special_perils_cover: false
        }
    },
    {
        name: "3. The Klang Valley Flood Risk",
        data: {
            driver_age: 35, traffic_violations: 0, telematics_risk: "Low", ncd_percentage: "30.0", prior_claims_count: 0, average_prior_severity: "Low", territory: "Urban (KL, Selangor, Penang, Johor)", flood_zone: "High", vehicle_value: 85000, engine_capacity: 1500, vehicle_category: "Private Car", valuation_type: "Market Value", vehicle_age: 5, annual_mileage: 12000, usage_type: "Private", windscreen_cover: false, ncd_protector: false, special_perils_cover: false
        }
    },
    {
        name: "4. The Reinsurance Trigger (Luxury Asset)",
        data: {
            driver_age: 50, traffic_violations: 0, telematics_risk: "Low", ncd_percentage: "55.0", prior_claims_count: 0, average_prior_severity: "Low", territory: "Urban (KL, Selangor, Penang, Johor)", flood_zone: "Low", vehicle_value: 280000, engine_capacity: 3000, vehicle_category: "Luxury Car", valuation_type: "Market Value", vehicle_age: 1, annual_mileage: 8000, usage_type: "Private", windscreen_cover: false, ncd_protector: false, special_perils_cover: false
        }
    },
    {
        name: "5. The Hard Underwriting Referral",
        data: {
            driver_age: 19, traffic_violations: 2, telematics_risk: "High", ncd_percentage: "0.0", prior_claims_count: 2, average_prior_severity: "High", territory: "Urban (KL, Selangor, Penang, Johor)", flood_zone: "High", vehicle_value: 130000, engine_capacity: 2400, vehicle_category: "Commercial Pickup", valuation_type: "Market Value", vehicle_age: 1, annual_mileage: 50000, usage_type: "E-hailing Commercial", windscreen_cover: false, ncd_protector: false, special_perils_cover: false
        }
    },
    {
        name: "6. The Premium Floor Boundary Case",
        data: {
            driver_age: 65, traffic_violations: 0, telematics_risk: "Low", ncd_percentage: "55.0", prior_claims_count: 0, average_prior_severity: "Low", territory: "Rural (East Malaysia)", flood_zone: "Low", vehicle_value: 5000, engine_capacity: 1300, vehicle_category: "Private Car", valuation_type: "Market Value", vehicle_age: 15, annual_mileage: 5000, usage_type: "Private", windscreen_cover: false, ncd_protector: false, special_perils_cover: false
        }
    },
    {
        name: "7. The Commercial E-Hailing Fleet Operator",
        data: {
            driver_age: 29, traffic_violations: 0, telematics_risk: "Low", ncd_percentage: "0.0", prior_claims_count: 0, average_prior_severity: "Low", territory: "Urban (KL, Selangor, Penang, Johor)", flood_zone: "Med", vehicle_value: 55000, engine_capacity: 1600, vehicle_category: "Private Car", valuation_type: "Market Value", vehicle_age: 4, annual_mileage: 50000, usage_type: "E-hailing Commercial", windscreen_cover: false, ncd_protector: false, special_perils_cover: false
        }
    },
    {
        name: "8. The NCD Protector Safe-Haven",
        data: {
            driver_age: 45, traffic_violations: 0, telematics_risk: "Low", ncd_percentage: "55.0", prior_claims_count: 1, average_prior_severity: "Med", territory: "Rural (West Malaysia)", flood_zone: "Low", vehicle_value: 120000, engine_capacity: 1500, vehicle_category: "Private Car", valuation_type: "Market Value", vehicle_age: 3, annual_mileage: 15000, usage_type: "Private", windscreen_cover: false, ncd_protector: true, special_perils_cover: false
        }
    },
    {
        name: "9. The East Malaysia Rural 4x4",
        data: {
            driver_age: 38, traffic_violations: 0, telematics_risk: "Low", ncd_percentage: "45.0", prior_claims_count: 0, average_prior_severity: "Low", territory: "Rural (East Malaysia)", flood_zone: "Low", vehicle_value: 140000, engine_capacity: 2800, vehicle_category: "Commercial Pickup", valuation_type: "Market Value", vehicle_age: 2, annual_mileage: 20000, usage_type: "Private", windscreen_cover: false, ncd_protector: false, special_perils_cover: false
        }
    },
    {
        name: "10. The Senior Citizen Driver Zone",
        data: {
            driver_age: 78, traffic_violations: 0, telematics_risk: "Med", ncd_percentage: "30.0", prior_claims_count: 0, average_prior_severity: "Low", territory: "Urban (Other)", flood_zone: "Low", vehicle_value: 65000, engine_capacity: 1500, vehicle_category: "Private Car", valuation_type: "Market Value", vehicle_age: 7, annual_mileage: 8000, usage_type: "Private", windscreen_cover: false, ncd_protector: false, special_perils_cover: false
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
    
    // Gather form data
    const payload = {
        driver_age: parseInt(document.getElementById('driver_age').value),
        traffic_violations: parseInt(document.getElementById('traffic_violations').value),
        telematics_risk: document.getElementById('telematics_risk').value,
        ncd_percentage: parseFloat(document.getElementById('ncd_percentage').value),
        prior_claims_count: parseInt(document.getElementById('prior_claims_count').value),
        average_prior_severity: document.getElementById('average_prior_severity').value,
        territory: document.getElementById('territory').value,
        flood_zone: document.getElementById('flood_zone').value,
        vehicle_value: parseFloat(document.getElementById('vehicle_value').value),
        engine_capacity: parseInt(document.getElementById('engine_capacity').value),
        vehicle_category: document.getElementById('vehicle_category').value,
        valuation_type: document.getElementById('valuation_type').value,
        vehicle_age: parseInt(document.getElementById('vehicle_age').value),
        annual_mileage: parseInt(document.getElementById('annual_mileage').value),
        usage_type: document.getElementById('usage_type').value,
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
    
    // Reset Progress Bars
    const resetProgressBar = (idPrefix, maxVal) => {
        const pb = document.getElementById(`${idPrefix}-risk-fill`);
        const txt = document.getElementById(`${idPrefix}-risk-text`);
        if (pb) {
            pb.style.width = '0%';
            pb.style.backgroundColor = '#1D4ED8';
        }
        if (txt) txt.innerText = `0 / ${maxVal}`;
    };
    resetProgressBar('driver', 30);
    resetProgressBar('claims', 25);
    resetProgressBar('geo', 20);
    resetProgressBar('vehicle', 15);

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
    
    // Market comparison no longer exists in index.html, handled gracefully if missing
    const mc = document.getElementById('market_comparison');
    if (mc) mc.style.display = 'none';
}

function updateDashboard(data) {
    // Score & Decision
    document.getElementById('display_score').textContent = data.composite_score || '--';
    
    const badge = document.getElementById('display_decision');
    badge.textContent = data.decision.replace(/_/g, ' ');
    if (data.decision === 'AUTO_APPROVED') {
        badge.className = 'decision-badge approved';
    } else {
        badge.className = 'decision-badge referral';
    }

    // Reinsurance
    document.getElementById('display_reinsurance').style.display = 
        data.reinsurance_referral ? 'block' : 'none';

    // Progress Bars based on score_breakdown
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
                pb.style.backgroundColor = '#fbbf24'; // amber
            } else {
                pb.style.backgroundColor = '#1D4ED8'; // default blue
            }
        };

        const getScore = (obj) => {
            if (!obj) return 0;
            return Object.values(obj).reduce((a, b) => a + b, 0);
        };

        setProgressBar('driver', getScore(data.score_breakdown.driver), 30);
        setProgressBar('claims', getScore(data.score_breakdown.claims), 25);
        setProgressBar('geo', getScore(data.score_breakdown.geographic), 20);
        setProgressBar('vehicle', getScore(data.score_breakdown.vehicle), 15);
    }

    // Premium Breakdown
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
        
        // Market Comparison (removed from UI, graceful fallback)
        const mc = document.getElementById('market_comparison');
        if (mc) {
            mc.style.display = 'block';
            document.getElementById('mc_ours').textContent = fmt(data.premium_breakdown.total_payable);
            document.getElementById('mc_allianz').textContent = fmt(data.premium_breakdown.total_payable * 1.10);
            document.getElementById('mc_etiqa').textContent = fmt(data.premium_breakdown.total_payable * 0.95);
        }
    } else {
        document.getElementById('bk_base').textContent = 'N/A';
        document.getElementById('bk_loading').textContent = 'N/A';
        document.getElementById('bk_ehailing').textContent = 'N/A';
        document.getElementById('bk_ncd').textContent = 'N/A';
        document.getElementById('bk_addons').textContent = 'N/A';
        document.getElementById('bk_excl').textContent = 'N/A';
        document.getElementById('display_floor_warning').style.display = 'none';
        document.getElementById('bk_sst').textContent = 'N/A';
        document.getElementById('bk_stamp_duty').textContent = 'N/A';
        document.getElementById('bk_total').textContent = 'N/A';
        const mc = document.getElementById('market_comparison');
        if (mc) mc.style.display = 'none';
    }

    // Metadata
    if (data.metadata) {
        const metaKeys = Object.keys(data.metadata);
        const terms = metaKeys.join(" | ");
        document.getElementById('display_metadata').textContent = terms;
        
        // Premium Floor Warning
        document.getElementById('display_floor_warning').style.display = 
            metaKeys.includes("PREMIUM_FLOOR_APPLIED") ? 'block' : 'none';
            
        // Mandatory Add-on Warning
        const isMandatory = metaKeys.includes("MANDATORY FLOOD COVER APPLIED");
        document.getElementById('display_mandatory_addon').style.display = isMandatory ? 'block' : 'none';
        
        // NCD Stepback Warning
        const isNcdSteppedBack = metaKeys.includes("NCD STEP-BACK APPLIED DUE TO PRIOR CLAIMS");
        document.getElementById('display_ncd_stepback').style.display = isNcdSteppedBack ? 'block' : 'none';
        
        if (isMandatory) {
            alert("Notice: An add-on (Flood Cover) was applied mandatorily because this vehicle resides in a High Flood Risk zone.");
        }
        
        if (isNcdSteppedBack) {
            alert("Notice: Due to a prior claim, your No Claim Discount (NCD) has stepped back to 0%.");
        }
    } else {
        document.getElementById('display_floor_warning').style.display = 'none';
        document.getElementById('display_mandatory_addon').style.display = 'none';
        document.getElementById('display_ncd_stepback').style.display = 'none';
    }
}
