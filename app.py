"""Multimodal Construction Intelligence Platform.

Capstone Project 1: Generative AI | Real Estate Decision Support
Platform ID: 6ac4c98d1dcde6d7857c1642

Streamlit Web Application featuring:
- Multimodal PPE Site Safety Compliance Audit (OSHA & IS 456)
- Forensic Concrete Crack Diagnostics & Structural Integrity
- Planning & Real Estate Valuation Engine (INR Lakhs/Crores, CapEx, Materials)
- Conceptual 3D Architectural Rendering via Pollinations AI
- Weather-Aware Daily Safety Advisory & Interactive Civil Engineering Chatbot
"""

import os
import json
import streamlit as st
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

# Import modular components
from config import (
    PLATFORM_NAME,
    CAPSTONE_ID,
    APP_VERSION,
    CITY_TIERS,
    STRUCTURE_TYPES,
    WEATHER_PROTOCOLS,
)
from modules.gemini_client import GeminiMultimodalClient
from modules.ppe_audit import run_ppe_audit
from modules.crack_diagnostics import run_crack_diagnostics
from modules.valuation import calculate_project_financials, format_inr
from modules.pollinations_client import (
    generate_architectural_prompt,
    build_pollinations_image_url,
    STYLE_PRESETS,
    LIGHTING_PRESETS,
    CAMERA_ANGLES,
)
from modules.weather_advisory import get_weather_impact_summary
from modules.chatbot import generate_assistant_response

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Multimodal Construction Intelligence Platform",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# CUSTOM CSS STYLING
# -----------------------------------------------------------------------------
st.markdown(
    """
<style>
    /* Global Styling */
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
        padding: 24px;
        border-radius: 12px;
        color: white;
        margin-bottom: 24px;
        border-left: 6px solid #f59e0b;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .platform-badge {
        display: inline-block;
        background-color: #f59e0b;
        color: #0f172a;
        font-weight: 700;
        font-size: 11px;
        padding: 3px 8px;
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-right: 8px;
    }
    .status-pill {
        display: inline-block;
        font-size: 12px;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 16px;
        margin-bottom: 8px;
    }
    .pill-compliant {
        background-color: #dcfce7;
        color: #15803d;
        border: 1px solid #86efac;
    }
    .pill-warning {
        background-color: #fef3c7;
        color: #b45309;
        border: 1px solid #fcd34d;
    }
    .pill-critical {
        background-color: #fee2e2;
        color: #b91c1c;
        border: 1px solid #fca5a5;
    }
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .hazard-box {
        background-color: #ffffff;
        border-left: 4px solid #ef4444;
        border-radius: 6px;
        padding: 14px 18px;
        margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    .repair-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-top: 4px solid #0284c7;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f1f5f9;
        border-radius: 8px 8px 0px 0px;
        gap: 8px;
        padding-top: 10px;
        padding-bottom: 10px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0f172a !important;
        color: #f8fafc !important;
        border-bottom: 3px solid #f59e0b !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {
            "role": "model",
            "content": "Hello Engineer! I am **SiteVision AI**, your construction and structural advisory assistant. Ask me anything about **IS 456:2000**, **OSHA 1926**, concrete mix proportions, formwork stripping schedules, or crack remediation.",
        }
    ]

if "pollinations_seed" not in st.session_state:
    st.session_state.pollinations_seed = 42

# -----------------------------------------------------------------------------
# SIDEBAR CONTROLS & ARCHITECTURE OVERVIEW
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        f"""
    <div style="text-align: center; padding-bottom: 12px;">
        <span class="platform-badge">CAPSTONE PROJECT 1</span>
        <h3 style="margin-top: 6px; margin-bottom: 2px; color: #0f172a;">🏗️ Construction AI</h3>
        <p style="font-size: 11px; color: #64748b; margin: 0;">Platform ID: <code>{CAPSTONE_ID}</code></p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("### 🔑 API & Model Configuration")

    # API Key Input
    env_gemini_key = os.environ.get("GEMINI_API_KEY", "")
    api_key_input = st.text_input(
        "Google Gemini API Key",
        value=env_gemini_key,
        type="password",
        placeholder="Enter AIzaSy... or leave empty for Demo Mode",
        help="Optional. If not provided, application automatically runs high-fidelity engineering simulations.",
    )

    selected_model = st.selectbox(
        "Gemini Multimodal Model",
        options=["gemini-1.5-flash", "gemini-1.5-pro"],
        index=0,
        help="Gemini 1.5 Flash provides ultra-fast multimodal inference; 1.5 Pro provides deep reasoning.",
    )

    # Initialize Gemini client
    client = GeminiMultimodalClient(api_key=api_key_input, model=selected_model)

    if client.is_demo_mode:
        st.info(
            "🎮 **Demonstration Mode Active**\n\nNo API key detected. Running high-precision benchmark simulations conforming to IS 456 & OSHA standards."
        )
    else:
        st.success("🟢 **Live Gemini API Connected**")

    st.markdown("---")
    st.markdown("### 🏛️ Architecture & Epics")
    with st.expander("System Specs & Kanban Coverage", expanded=False):
        st.markdown(
            """
        - **Epic 1**: Requirements & Environment Setup
        - **Epic 2**: PPE Vision Audit & Forensic Crack Diagnostics
        - **Epic 3**: Real Estate Valuation & Material Engine (INR)
        - **Epic 4**: Structured JSON Contracts & Schema Validation
        - **Epic 5**: Weather Advisory & Construction Engineering Chatbot
        - **Epic 6**: Testing & 1-Click Cloud Deployment
        
        **Governing Codes**:
        - Bureau of Indian Standards: `IS 456:2000`, `IS 10262`, `IS 13920`, `IS 2925`, `IS 15809`
        - International: `OSHA 1926`, `ACI 224R-01`
        """
        )

    st.markdown(
        f"<div style='font-size: 11px; color: #94a3b8; text-align: center;'>Version {APP_VERSION}</div>",
        unsafe_allow_html=True,
    )

# -----------------------------------------------------------------------------
# MAIN APP HEADER
# -----------------------------------------------------------------------------
st.markdown(
    f"""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
        <div>
            <span class="platform-badge">Generative AI • Real Estate Decision Support</span>
            <h1 style="margin: 8px 0 4px 0; font-size: 26px; color: white;">{PLATFORM_NAME}</h1>
            <p style="margin: 0; font-size: 14px; color: #cbd5e1;">
                Intelligent multimodal computer vision auditing, forensic structural integrity diagnostics, 
                INR cost & CapEx valuation, and weather-aware site safety protocols.
            </p>
        </div>
        <div style="text-align: right; background: rgba(255,255,255,0.08); padding: 8px 14px; border-radius: 8px;">
            <div style="font-size: 11px; color: #94a3b8;">DEPLOYMENT STATUS</div>
            <div style="font-size: 13px; font-weight: 700; color: #38bdf8;">Streamlit Cloud Ready</div>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# TABS NAVIGATION
# -----------------------------------------------------------------------------
tab_ppe, tab_crack, tab_valuation, tab_weather_chat = st.tabs(
    [
        "🦺 1. Site Safety & PPE Audit",
        "🔍 2. Crack Diagnostics & Integrity",
        "📊 3. Planning & Real Estate Valuation",
        "🌦️ 4. Daily Advisory & Engineering Assistant",
    ]
)

# =============================================================================
# TAB 1: SITE SAFETY & PPE AUDIT (EPIC 2)
# =============================================================================
with tab_ppe:
    st.markdown("### 🦺 Multimodal Site Safety & Worker PPE Compliance Audit")
    st.caption(
        "Analyzes site imagery for mandatory worker protective gear under **OSHA 1926** and Indian **IS 456 / IS 2925** standards. Emits structured JSON compliance contracts."
    )

    col_ppe_left, col_ppe_right = st.columns([1, 1.25], gap="large")

    with col_ppe_left:
        st.markdown("#### 📸 Input Site Imagery")

        # Sample selector buttons
        sample_ppe_choice = st.radio(
            "Select Inspection Image Source:",
            [
                "Upload Custom Photo",
                "Pre-loaded Benchmark: 100% Compliant Crew",
                "Pre-loaded Benchmark: Critical Site Hazards & Violations",
            ],
            index=1,
            horizontal=False,
        )

        ppe_image = None
        sample_tag = "custom"

        if sample_ppe_choice == "Upload Custom Photo":
            uploaded_file = st.file_uploader(
                "Upload Construction Site Photo",
                type=["jpg", "jpeg", "png"],
                key="ppe_uploader",
                help="Supported formats: JPG, PNG",
            )
            if uploaded_file:
                ppe_image = Image.open(uploaded_file)
                st.image(
                    ppe_image,
                    caption="Uploaded Site Inspection Photo",
                    use_container_width=True,
                )
        elif (
            sample_ppe_choice == "Pre-loaded Benchmark: 100% Compliant Crew"
        ):
            sample_path = "assets/sample_ppe_compliant.jpg"
            if os.path.exists(sample_path):
                ppe_image = Image.open(sample_path)
                sample_tag = "compliant"
                st.image(
                    ppe_image,
                    caption="Benchmark Sample: Fully Compliant Scaffolding Crew (IS 2925 / IS 15809)",
                    use_container_width=True,
                )
        else:
            sample_path = "assets/sample_ppe_violation.jpg"
            if os.path.exists(sample_path):
                ppe_image = Image.open(sample_path)
                sample_tag = "violation"
                st.image(
                    ppe_image,
                    caption="Benchmark Sample: Unprotected Trench & Missing Hard Hats (High Risk)",
                    use_container_width=True,
                )

        run_ppe_btn = st.button(
            "⚡ Run Site Safety & PPE Audit",
            type="primary",
            use_container_width=True,
            disabled=(ppe_image is None),
        )

    with col_ppe_right:
        st.markdown("#### 📋 Inspection Report & Findings")

        if run_ppe_btn and ppe_image is not None:
            with st.spinner("Analyzing worker PPE and scanning site hazards..."):
                audit_result, is_sim, status_note = run_ppe_audit(
                    image=ppe_image, client=client, sample_type=sample_tag
                )

            # Store in session state for persistence
            st.session_state.last_ppe_audit = audit_result
            st.session_state.last_ppe_sim = is_sim
            st.session_state.last_ppe_status_note = status_note

        if "last_ppe_audit" in st.session_state:
            res = st.session_state.last_ppe_audit
            score = res.get("safety_score", 0)
            overall_status = res.get("overall_status", "UNKNOWN")

            # Status styling
            if score >= 80:
                badge_class = "pill-compliant"
                score_color = "#15803d"
            elif score >= 50:
                badge_class = "pill-warning"
                score_color = "#b45309"
            else:
                badge_class = "pill-critical"
                score_color = "#b91c1c"

            # Top Metrics Row
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(
                    f"""
                <div class="metric-card">
                    <div style="font-size: 11px; color: #64748b;">SAFETY SCORE</div>
                    <div style="font-size: 28px; font-weight: 800; color: {score_color};">{score}/100</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )
            with m2:
                st.markdown(
                    f"""
                <div class="metric-card">
                    <div style="font-size: 11px; color: #64748b;">OVERALL STATUS</div>
                    <div style="margin-top: 6px;"><span class="status-pill {badge_class}">{overall_status}</span></div>
                </div>
                """,
                    unsafe_allow_html=True,
                )
            with m3:
                st.markdown(
                    f"""
                <div class="metric-card">
                    <div style="font-size: 11px; color: #64748b;">WORKERS DETECTED</div>
                    <div style="font-size: 26px; font-weight: 700; color: #0f172a;">{res.get('workers_detected_count', 'N/A')}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )
            with m4:
                hazards_count = len(res.get("identified_site_hazards", []))
                st.markdown(
                    f"""
                <div class="metric-card">
                    <div style="font-size: 11px; color: #64748b;">HAZARDS FLAGGED</div>
                    <div style="font-size: 26px; font-weight: 700; color: {'#b91c1c' if hazards_count > 0 else '#15803d'};">{hazards_count}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            st.markdown(f"**Executive Summary:** {res.get('executive_summary', '')}")

            # PPE Detection Checklist Table
            st.markdown("##### 🔍 PPE Gear Compliance Checklist")
            checklist = res.get("ppe_detection", [])
            for item in checklist:
                is_comp = item.get("compliant", False)
                icon = "✅" if is_comp else "❌"
                rate = item.get("compliance_rate_pct", 0)
                st.markdown(
                    f"- **{icon} {item.get('item', '')}** (`{item.get('required_by', '')}`): "
                    f"Compliance **{rate}%** — {item.get('notes', '')}"
                )

            # Hazards & Corrective Remedies
            hazards = res.get("identified_site_hazards", [])
            if hazards:
                st.markdown("##### ⚠️ Identified Hazards & Mandated Remedies")
                for h in hazards:
                    sev = h.get("severity", "Medium")
                    st.markdown(
                        f"""
                    <div class="hazard-box">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <strong style="color: #0f172a; font-size: 15px;">🚨 {h.get('hazard')}</strong>
                            <span style="font-size: 11px; font-weight: 700; background: #fee2e2; color: #b91c1c; padding: 2px 8px; border-radius: 4px;">{sev.upper()} SEVERITY</span>
                        </div>
                        <div style="font-size: 13px; color: #475569; margin-top: 4px;">
                            <strong>Location:</strong> {h.get('location')} | <strong>Standard:</strong> <code>{h.get('regulatory_standard')}</code>
                        </div>
                        <div style="font-size: 13px; color: #1e293b; margin-top: 6px; background: #f8fafc; padding: 8px; border-radius: 4px;">
                            <strong>🛠️ Corrective Remedy:</strong> {h.get('corrective_remedy')}
                        </div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )
            else:
                st.success("🎉 No active safety hazards detected on site. Zero imminent dangers observed.")

            # Downloadable JSON Report
            json_report = json.dumps(res, indent=2)
            st.download_button(
                label="📥 Download Structured JSON Safety Report",
                data=json_report,
                file_name="site_safety_audit_report.json",
                mime="application/json",
                use_container_width=True,
            )
        else:
            st.info(
                "👈 Select an inspection photo on the left and click **'Run Site Safety & PPE Audit'** to generate findings."
            )


# =============================================================================
# TAB 2: CRACK DIAGNOSTICS & STRUCTURAL INTEGRITY (EPIC 2)
# =============================================================================
with tab_crack:
    st.markdown("### 🔍 Forensic Concrete Crack Diagnostics & Structural Integrity")
    st.caption(
        "Multimodal defect classification, aperture width estimation, root cause forensics, and engineering repair specifications according to **IS 456:2000** and **ACI 224R**."
    )

    col_crk_left, col_crk_right = st.columns([1, 1.25], gap="large")

    with col_crk_left:
        st.markdown("#### 📸 Concrete Surface Inspection")

        sample_crack_choice = st.radio(
            "Select Crack Surface Photo Source:",
            [
                "Upload Custom Photo",
                "Pre-loaded Benchmark: 45° Diagonal Shear Fracture (Beam)",
                "Pre-loaded Benchmark: Hairline Surface Plaster Shrinkage",
            ],
            index=1,
            horizontal=False,
        )

        crack_image = None
        crack_sample_tag = "custom"

        if sample_crack_choice == "Upload Custom Photo":
            uploaded_crack = st.file_uploader(
                "Upload Concrete / Wall Surface Photo",
                type=["jpg", "jpeg", "png"],
                key="crack_uploader",
            )
            if uploaded_crack:
                crack_image = Image.open(uploaded_crack)
                st.image(
                    crack_image,
                    caption="Uploaded Concrete Surface",
                    use_container_width=True,
                )
        elif (
            sample_crack_choice
            == "Pre-loaded Benchmark: 45° Diagonal Shear Fracture (Beam)"
        ):
            sample_path = "assets/sample_crack_shear.jpg"
            if os.path.exists(sample_path):
                crack_image = Image.open(sample_path)
                crack_sample_tag = "shear"
                st.image(
                    crack_image,
                    caption="Benchmark Sample: Diagonal Shear Fracture (IS 456 Clause 40)",
                    use_container_width=True,
                )
        else:
            sample_path = "assets/sample_crack_hairline.jpg"
            if os.path.exists(sample_path):
                crack_image = Image.open(sample_path)
                crack_sample_tag = "hairline"
                st.image(
                    crack_image,
                    caption="Benchmark Sample: Hairline Shrinkage (<0.4 mm Non-Structural)",
                    use_container_width=True,
                )

        run_crack_btn = st.button(
            "⚡ Diagnose Concrete Defect",
            type="primary",
            use_container_width=True,
            disabled=(crack_image is None),
        )

    with col_crk_right:
        st.markdown("#### 🔬 Structural Forensic Diagnostics")

        if run_crack_btn and crack_image is not None:
            with st.spinner("Classifying fracture patterns and calculating shear/settlement stress..."):
                diag_result, is_sim_crk, status_note_crk = run_crack_diagnostics(
                    image=crack_image, client=client, sample_type=crack_sample_tag
                )
            st.session_state.last_crack_diag = diag_result

        if "last_crack_diag" in st.session_state:
            c_res = st.session_state.last_crack_diag
            defect = c_res.get("defect_type", "Unknown")
            severity = c_res.get("severity_level", "Moderate")
            width_mm = c_res.get("estimated_crack_width_mm", 0.0)
            urgency = c_res.get("urgency", "Monitor")

            # Metrics row
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown(
                    f"""
                <div class="metric-card">
                    <div style="font-size: 11px; color: #64748b;">DEFECT TYPE</div>
                    <div style="font-size: 16px; font-weight: 800; color: #0369a1; margin-top: 4px;">{defect}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )
            with c2:
                st.markdown(
                    f"""
                <div class="metric-card">
                    <div style="font-size: 11px; color: #64748b;">ESTIMATED WIDTH</div>
                    <div style="font-size: 24px; font-weight: 800; color: {'#b91c1c' if width_mm > 0.3 else '#15803d'};">{width_mm} mm</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )
            with c3:
                st.markdown(
                    f"""
                <div class="metric-card">
                    <div style="font-size: 11px; color: #64748b;">SEVERITY</div>
                    <div style="font-size: 18px; font-weight: 700; color: {'#b91c1c' if severity in ['Critical', 'Severe'] else '#0f172a'}; margin-top: 4px;">{severity}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )
            with c4:
                st.markdown(
                    f"""
                <div class="metric-card">
                    <div style="font-size: 11px; color: #64748b;">URGENCY</div>
                    <div style="font-size: 13px; font-weight: 700; color: #b45309; margin-top: 6px;">{urgency}</div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            st.markdown(
                f"**Integrity Risk:** `{c_res.get('structural_integrity_risk', '')}` | **Crack Depth:** `{c_res.get('crack_depth_classification', '')}`"
            )
            st.info(f"📋 **Forensic Assessment:** {c_res.get('engineering_notes', '')}")

            # Root Causes
            st.markdown("##### 🔬 Root Cause Forensics")
            for cause in c_res.get("root_causes", []):
                st.markdown(f"- ⚠️ {cause}")

            # Recommended Engineering Repairs
            st.markdown("##### 🛠️ Recommended Engineering Repair Protocols")
            for rep in c_res.get("recommended_engineering_repairs", []):
                st.markdown(
                    f"""
                <div class="repair-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <strong style="color: #0369a1; font-size: 15px;">🔧 {rep.get('method')}</strong>
                        <span style="font-size: 12px; font-weight: 700; color: #047857; background: #ecfdf5; padding: 2px 8px; border-radius: 4px;">{rep.get('estimated_unit_cost_inr')}</span>
                    </div>
                    <div style="font-size: 13px; color: #475569; margin-top: 4px;">
                        <strong>Material Specification:</strong> <code>{rep.get('material')}</code>
                    </div>
                    <div style="font-size: 13px; color: #1e293b; margin-top: 6px;">
                        <strong>Procedure:</strong> {rep.get('procedure')}
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            # Standards Cited & Download
            codes = ", ".join(c_res.get("compliance_codes", []))
            st.caption(f"Referenced Civil Design Codes: `{codes}`")

            crack_json = json.dumps(c_res, indent=2)
            st.download_button(
                label="📥 Download Crack Diagnostics JSON Contract",
                data=crack_json,
                file_name="crack_diagnostics_report.json",
                mime="application/json",
                use_container_width=True,
            )
        else:
            st.info(
                "👈 Select a concrete surface image on the left and click **'Diagnose Concrete Defect'**."
            )


# =============================================================================
# TAB 3: PLANNING & REAL ESTATE VALUATION (EPIC 3)
# =============================================================================
with tab_weather_chat:
    pass  # Defined later

with tab_valuation:
    st.markdown("### 📊 Planning, Cost Estimation & Real Estate Asset Valuation (INR)")
    st.caption(
        "Interactive econometric model computing construction budgets, CapEx incurred, current WIP asset valuation in **INR (Lakhs/Crores)**, and IS 456 material forecasting."
    )

    col_val_inputs, col_val_outputs = st.columns([1, 1.25], gap="large")

    with col_val_inputs:
        st.markdown("#### 📐 Project Parameters")

        selected_structure = st.selectbox(
            "Structure Type",
            options=list(STRUCTURE_TYPES.keys()),
            index=0,
        )

        built_up_area = st.number_input(
            "Built-Up Area (sq. ft.)",
            min_value=1000,
            max_value=1_000_000,
            value=35_000,
            step=1000,
            help="Total gross construction area across all slabs/floors.",
        )

        selected_tier = st.selectbox(
            "Location City Tier",
            options=list(CITY_TIERS.keys()),
            index=0,
            help="Tier 1 Metros command higher land shares and labor costs.",
        )

        tier_details = CITY_TIERS[selected_tier]
        st.caption(f"Representative Cities: {', '.join(tier_details['cities'][:4])}")

        quality_choice = st.selectbox(
            "Construction Specification / Finishes",
            options=[
                "Standard Quality (CPWD Specs)",
                "Premium Specification (Imported Finishes)",
                "Ultra-Luxury Specification (High-End Automation)",
            ],
            index=0,
        )

        completion_slider = st.slider(
            "Current Project Completion Percentage (%)",
            min_value=0,
            max_value=100,
            value=45,
            step=1,
            help="Drag to dynamically recompute CapEx incurred and milestone progress.",
        )

        # Architectural Rendering Prompt Generator
        st.markdown("---")
        st.markdown("#### 🎨 Conceptual 3D Architectural Rendering")
        st.caption("Powered by Pollinations AI / Flux Generative Engine")

        style_choice = st.selectbox("Architectural Preset", list(STYLE_PRESETS.keys()))
        lighting_choice = st.selectbox("Lighting & Ambience", list(LIGHTING_PRESETS.keys()))
        camera_choice = st.selectbox("Perspective", list(CAMERA_ANGLES.keys()))

        extra_prompt_details = st.text_input(
            "Custom Design Details (Optional)",
            value="ultra-modern clubhouse with cantilevered infinity pool, lush greenery",
        )

        gen_render_btn = st.button("✨ Generate Conceptual 3D Render", use_container_width=True)

    # Compute financial calculations
    fin = calculate_project_financials(
        structure_type=selected_structure,
        built_up_sqft=built_up_area,
        location_tier=selected_tier,
        completion_pct=completion_slider,
        quality_spec=quality_choice,
    )

    with col_val_outputs:
        st.markdown("#### 💰 Financial Ledger & Asset Valuation")

        # Top Financial Metric Cards
        f1, f2, f3 = st.columns(3)
        with f1:
            st.markdown(
                f"""
            <div class="metric-card" style="border-top: 4px solid #0284c7;">
                <div style="font-size: 11px; color: #64748b;">TOTAL PROJECT BUDGET</div>
                <div style="font-size: 24px; font-weight: 800; color: #0f172a; margin-top: 4px;">{fin['total_budget_formatted']}</div>
                <div style="font-size: 11px; color: #64748b;">@ ₹{fin['effective_rate_per_sqft']:,.0f} / sqft</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        with f2:
            st.markdown(
                f"""
            <div class="metric-card" style="border-top: 4px solid #f59e0b;">
                <div style="font-size: 11px; color: #64748b;">CAPEX INCURRED ({completion_slider}%)</div>
                <div style="font-size: 24px; font-weight: 800; color: #b45309; margin-top: 4px;">{fin['capex_incurred_formatted']}</div>
                <div style="font-size: 11px; color: #64748b;">Bal: {fin['capex_remaining_formatted']}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        with f3:
            st.markdown(
                f"""
            <div class="metric-card" style="border-top: 4px solid #10b981;">
                <div style="font-size: 11px; color: #64748b;">CURRENT ASSET VALUE (WIP)</div>
                <div style="font-size: 24px; font-weight: 800; color: #15803d; margin-top: 4px;">{fin['current_asset_valuation_formatted']}</div>
                <div style="font-size: 11px; color: #15803d; font-weight: 600;">Ready: {fin['projected_ready_market_value_formatted']}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

        # Milestone Progress Breakdown
        st.markdown("##### 📌 Milestone Schedule & Status")
        st.progress(completion_slider / 100.0)

        milestone_cols = st.columns(len(fin["milestones"]))
        for idx, m in enumerate(fin["milestones"]):
            status = m["status"]
            color = (
                "#15803d"
                if status == "Completed"
                else ("#b45309" if status == "In Progress" else "#94a3b8")
            )
            with milestone_cols[idx]:
                st.markdown(
                    f"""
                <div style="text-align: center; font-size: 10px; border-top: 2px solid {color}; padding-top: 4px;">
                    <strong>Stage {idx+1}</strong><br/>
                    <span style="color: {color}; font-weight: 700;">{m['status']}</span>
                </div>
                """,
                    unsafe_allow_html=True,
                )

        # Materials Forecast Table
        st.markdown("##### 🧱 Material Requirement Metrics (IS 456 Thumb Rules)")
        mats = fin["materials"]
        mat_col1, mat_col2 = st.columns(2)
        with mat_col1:
            st.markdown(
                f"- **Cement Requirements:** Total **{mats['cement']['total_bags']:,} bags** ({mats['cement']['total_mt']} MT)\n"
                f"  - Consumed: `{mats['cement']['consumed_bags']:,} bags` | Remaining: `{mats['cement']['remaining_bags']:,} bags`"
            )
            st.markdown(
                f"- **TMT Steel (Fe500D):** Total **{mats['steel']['total_mt']} MT**\n"
                f"  - Consumed: `{mats['steel']['consumed_mt']} MT` | Remaining: `{mats['steel']['remaining_mt']} MT`"
            )
        with mat_col2:
            st.markdown(
                f"- **Coarse Sand / M-Sand:** Total **{mats['sand']['total_brass']} Brass** ({mats['sand']['total_brass']*100:,.0f} cu.ft)\n"
                f"  - Consumed: `{mats['sand']['consumed_brass']} Brass`"
            )
            st.markdown(
                f"- **Coarse Aggregate (10/20mm):** Total **{mats['aggregate']['total_brass']} Brass** ({mats['aggregate']['total_brass']*100:,.0f} cu.ft)\n"
                f"  - Consumed: `{mats['aggregate']['consumed_brass']} Brass`"
            )

        # Interactive Chart: Budget vs Expenditure
        fig_financials = go.Figure(
            data=[
                go.Bar(
                    name="CapEx Incurred",
                    x=["Project Financials"],
                    y=[fin["capex_incurred_inr"] / 10_000_000],
                    marker_color="#f59e0b",
                ),
                go.Bar(
                    name="Balance CapEx",
                    x=["Project Financials"],
                    y=[fin["capex_remaining_inr"] / 10_000_000],
                    marker_color="#cbd5e1",
                ),
                go.Bar(
                    name="Current Asset Valuation",
                    x=["Real Estate Asset Valuation"],
                    y=[fin["current_asset_valuation_inr"] / 10_000_000],
                    marker_color="#10b981",
                ),
                go.Bar(
                    name="Ready Possession Valuation",
                    x=["Real Estate Asset Valuation"],
                    y=[fin["projected_ready_market_value_inr"] / 10_000_000],
                    marker_color="#0284c7",
                ),
            ]
        )
        fig_financials.update_layout(
            barmode="group",
            height=280,
            margin=dict(l=20, r=20, t=30, b=20),
            yaxis_title="INR (Crores ₹ Cr)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig_financials, use_container_width=True)

        # Conceptual 3D Architectural Render Showcase
        if gen_render_btn:
            render_prompt = generate_architectural_prompt(
                structure_type=selected_structure,
                style_choice=style_choice,
                lighting_choice=lighting_choice,
                camera_choice=camera_choice,
                extra_keywords=extra_prompt_details,
            )
            st.session_state.pollinations_seed += 1
            render_url = build_pollinations_image_url(
                prompt=render_prompt,
                seed=st.session_state.pollinations_seed,
                width=1024,
                height=640,
            )
            st.session_state.last_render_url = render_url
            st.session_state.last_render_prompt = render_prompt

        if "last_render_url" in st.session_state:
            st.markdown("##### 🏛️ Conceptual 3D Architectural Rendering")
            st.image(
                st.session_state.last_render_url,
                caption=f"Conceptual 3D Visualization: {selected_structure}",
                use_container_width=True,
            )
            st.caption(f"**Render Prompt:** `{st.session_state.last_render_prompt}`")
            st.markdown(
                f"[🔗 Open Full-Resolution Image in New Tab]({st.session_state.last_render_url})"
            )


# =============================================================================
# TAB 4: DAILY SITE ASSISTANT & WEATHER-AWARE ADVISORY (EPIC 5)
# =============================================================================
with tab_weather_chat:
    st.markdown("### 🌦️ Daily Site Assistant & Weather-Aware Advisory")
    st.caption(
        "Dynamic meteorological hazard mitigation rules under **OSHA 1926** and **IS 456 / IS 7861**, coupled with a multi-turn structural engineering assistant chatbot."
    )

    col_weather_left, col_chat_right = st.columns([1, 1.25], gap="large")

    with col_weather_left:
        st.markdown("#### 🌤️ Daily Weather Condition Selector")

        selected_weather = st.selectbox(
            "Select Site Meteorological Condition",
            options=list(WEATHER_PROTOCOLS.keys()),
            index=0,
            help="Updates crane operation alerts, concreting curing protocols, and electrical safety advisories dynamically.",
        )

        weather_info = get_weather_impact_summary(selected_weather)

        # Dynamic Weather Banner
        st.markdown(
            f"""
        <div style="background-color: {weather_info['badge_color']}; color: white; padding: 14px 18px; border-radius: 8px; margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin: 0; color: white;">⚠️ {selected_weather}</h4>
                <span style="background: rgba(255,255,255,0.25); padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 12px;">{weather_info['severity']}</span>
            </div>
            <div style="font-size: 13px; margin-top: 6px; opacity: 0.95;">
                Risk Impact Index: <strong>{weather_info['risk_index']}/100</strong>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Protocol Details
        st.markdown("##### 🚨 Dynamic Safety Alerts & Directives")
        st.error(f"🏗️ **Tower Crane & Hoists:** {weather_info['crane_operations']}")
        st.warning(f"🧗 **Scaffolding & Heights:** {weather_info['height_work']}")
        st.info(f"⚡ **Electrical & Dewatering:** {weather_info['electrical']}")
        st.success(f"🧪 **Concrete Curing & Pouring (IS 456):** {weather_info['concrete_curing']}")

        # Today's Action Items Checkbox
        st.markdown("##### 📋 Today's Weather Action Checklist")
        for item in weather_info["action_items"]:
            st.checkbox(item, value=False, key=f"chk_{item[:20]}")

    with col_chat_right:
        st.markdown("#### 🤖 SiteVision AI Engineering Assistant")
        st.caption("Multi-turn advisory grounded in IS 456, IS 10262, IS 13920 & OSHA 1926.")

        # Preset query buttons for 1-click asking
        st.markdown("**Quick Preset Queries:**")
        preset_cols = st.columns(2)
        with preset_cols[0]:
            if st.button("⏱️ Formwork Stripping Times (Table 11)", use_container_width=True):
                st.session_state.chat_history.append(
                    {"role": "user", "content": "What are the formwork stripping times under IS 456 Table 11?"}
                )
                with st.spinner("Consulting IS 456:2000 knowledgebase..."):
                    reply, _ = generate_assistant_response(client, st.session_state.chat_history)
                st.session_state.chat_history.append({"role": "model", "content": reply})
                st.rerun()

            if st.button("📏 Minimum Clear Cover (IS 456 Cl. 26.4)", use_container_width=True):
                st.session_state.chat_history.append(
                    {"role": "user", "content": "What is the minimum nominal clear cover for footings, columns, and beams?"}
                )
                with st.spinner("Consulting IS 456:2000 knowledgebase..."):
                    reply, _ = generate_assistant_response(client, st.session_state.chat_history)
                st.session_state.chat_history.append({"role": "model", "content": reply})
                st.rerun()

        with preset_cols[1]:
            if st.button("🧪 Concrete Curing Protocols (>40°C)", use_container_width=True):
                st.session_state.chat_history.append(
                    {"role": "user", "content": "What are the hot weather concreting and curing rules under IS 7861 and IS 456?"}
                )
                with st.spinner("Consulting concrete technology knowledgebase..."):
                    reply, _ = generate_assistant_response(client, st.session_state.chat_history)
                st.session_state.chat_history.append({"role": "model", "content": reply})
                st.rerun()

            if st.button("🛠️ 45° Beam Shear Crack Repair", use_container_width=True):
                st.session_state.chat_history.append(
                    {"role": "user", "content": "Explain the forensic repair steps for a 45 degree diagonal shear crack in an RCC beam."}
                )
                with st.spinner("Consulting forensic repair protocols..."):
                    reply, _ = generate_assistant_response(client, st.session_state.chat_history)
                st.session_state.chat_history.append({"role": "model", "content": reply})
                st.rerun()

        # Chat message display container
        chat_container = st.container(height=360)
        with chat_container:
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "model" else "👷"):
                    st.markdown(msg["content"])

        # Chat Input Box
        user_query = st.chat_input("Ask a construction, IS 456 code, or safety question...")
        if user_query:
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            with st.spinner("SiteVision AI is analyzing structural codes..."):
                ans, _ = generate_assistant_response(client, st.session_state.chat_history)
            st.session_state.chat_history.append({"role": "model", "content": ans})
            st.rerun()

        if st.button("🗑️ Clear Conversation History"):
            st.session_state.chat_history = [
                {
                    "role": "model",
                    "content": "Conversation cleared. Ready for your next civil engineering question!",
                }
            ]
            st.rerun()

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown(
    f"""
<div style="display: flex; justify-content: space-between; align-items: center; font-size: 12px; color: #64748b;">
    <div><strong>{PLATFORM_NAME}</strong> • Skill Wallet Capstone Project 1</div>
    <div>Engineered for 1-Click Streamlit Cloud Deployment • Zero External DB Dependencies</div>
    <div>Platform ID: <code>{CAPSTONE_ID}</code></div>
</div>
""",
    unsafe_allow_html=True,
)
