"""Crack Diagnostics & Structural Integrity Module (Epic 2).

Analyzes concrete, beam, slab, and wall surface imagery.
Classifies defect types (Hairline, Settlement, Structural Shear, Thermal Expansion, Spalling).
Estimates crack width in mm, determines root causes, engineering repair procedures (epoxy injection, re-grouting),
and assesses urgency according to IS 456:2000 and ACI standards.
"""

from datetime import datetime
from typing import Dict, Any, Tuple
from PIL import Image
from modules.gemini_client import GeminiMultimodalClient

CRACK_SYSTEM_PROMPT = """You are a Senior Forensic Structural Engineer specialized in concrete pathology and IS 456 / ACI structural failure analysis.
Analyze the provided photograph of a concrete or masonry building surface for cracks, spalling, and structural defects.

Classify the defect strictly into one of:
- "Structural Shear" (Diagonal ~45° cracks across beams, columns, or shear walls)
- "Hairline" (Fine surface shrinkage cracks < 1mm in plaster or non-structural screed)
- "Settlement" (Stepped or vertical diagonal cracks due to differential soil movement)
- "Thermal Expansion" (Cyclic expansion/contraction cracks near joints or parapets)
- "Spalling & Rebar Corrosion" (Delamination of concrete cover exposing oxidized reinforcement)

Return STRICT JSON with this schema:
{
  "defect_type": "<Structural Shear | Hairline | Settlement | Thermal Expansion | Spalling & Rebar Corrosion>",
  "severity_level": "<Minor | Moderate | Severe | Critical>",
  "estimated_crack_width_mm": <number representing estimated aperture width in mm>,
  "crack_depth_classification": "<Surface / Plaster | Medium Concrete Cover | Deep Structural Concrete | Through-Wall>",
  "structural_integrity_risk": "<Low | Moderate | High | Imminent Hazard>",
  "root_causes": [
    "<engineering root cause 1>",
    "<engineering root cause 2>"
  ],
  "recommended_engineering_repairs": [
    {
      "method": "<e.g., Low-Viscosity Epoxy Pressure Injection | Structural Polymer Micro-Concrete Re-Grouting | Polyurethane Grouting | Carbon Fiber Wrapping>",
      "material": "<specification and proprietary/chemical grade>",
      "procedure": "<step-by-step engineering execution steps>",
      "estimated_unit_cost_inr": "<estimated price range in INR>"
    }
  ],
  "urgency": "<Immediate (24-48 Hours) | High (7 Days) | Routine Maintenance (30 Days) | Periodic Monitoring>",
  "compliance_codes": ["IS 456:2000 (Clause 35 & 40)", "IS 13920:2016", "ACI 224R-01"],
  "engineering_notes": "<concise forensic assessment>"
}
"""

def get_demo_shear_data() -> Dict[str, Any]:
    """Realistic forensic analysis for structural shear crack."""
    return {
        "defect_type": "Structural Shear",
        "severity_level": "Critical",
        "estimated_crack_width_mm": 6.5,
        "crack_depth_classification": "Deep Structural Concrete",
        "structural_integrity_risk": "High - Immediate Shoring Recommended",
        "root_causes": [
            "Excess diagonal tension exceeding the principal tensile capacity of concrete (IS 456 Clause 40).",
            "Inadequate shear reinforcement spacing (stirrup pitch exceeded permissible limit under design shear force V_u).",
            "Localized stress concentration at the beam-column beam interface exacerbated by seismic/lateral vibration."
        ],
        "recommended_engineering_repairs": [
            {
                "method": "Structural Shoring & Relief Propping",
                "material": "Acro-jack steel props (Heavy duty 4-ton capacity)",
                "procedure": "Install adjustable mechanical steel props beneath beam span within 24 hours to redistribute dead and live loads before executing chemical repairs.",
                "estimated_unit_cost_inr": "₹8,000 - ₹12,000 for temporary shoring grid"
            },
            {
                "method": "Low-Viscosity Epoxy Resin Pressure Injection",
                "material": "Sikadur-52 / Fosroc Nitokit LV (Viscosity < 250 mPa.s)",
                "procedure": "V-groove crack surface, install copper/nylon injection ports at 150mm intervals, seal perimeter with epoxy putty, pump resin at 2-4 bar until refusal.",
                "estimated_unit_cost_inr": "₹1,400 - ₹1,900 per linear meter"
            },
            {
                "method": "CFRP (Carbon Fiber Reinforced Polymer) Shear Strengthening",
                "material": "Unidirectional Carbon Fiber Fabric (300 gsm) + epoxy saturant resin",
                "procedure": "Grind concrete substrate to CSP-3 profile, apply primer, wrap U-jacket carbon fiber bands perpendicular to crack to permanently restore shear capacity.",
                "estimated_unit_cost_inr": "₹5,000 - ₹7,200 per sq. meter"
            }
        ],
        "urgency": "Immediate (24-48 Hours)",
        "compliance_codes": ["IS 456:2000 Clause 40 & Annex D", "IS 13920:2016", "ACI 224.1R-07"],
        "engineering_notes": "Severe diagonal fracture (estimated 6.5 mm aperture) passing through the primary shear zone. This exceeds the maximum allowable crack width of 0.3 mm specified under IS 456 Clause 35.3.2 by over 20x. Structural capacity is significantly compromised."
    }

def get_demo_hairline_data() -> Dict[str, Any]:
    """Realistic forensic analysis for hairline shrinkage crack."""
    return {
        "defect_type": "Hairline",
        "severity_level": "Minor",
        "estimated_crack_width_mm": 0.3,
        "crack_depth_classification": "Surface / Plaster",
        "structural_integrity_risk": "Low - Non-Structural Superficial Defect",
        "root_causes": [
            "Plastic and drying shrinkage of surface cement-sand plaster (rich 1:3 mix ratio).",
            "Rapid moisture loss during initial curing phase due to ambient wind or thermal drying.",
            "Differential thermal coefficients between masonry brickwork and concrete lintel backing."
        ],
        "recommended_engineering_repairs": [
            {
                "method": "Elastomeric Micro-Filler Coating",
                "material": "Dr. Fixit Crack-X Paste / Asian Paints SmartCare Crack Seal",
                "procedure": "Widen crack to 2mm with triangular scraper, clean dust, apply flexible synthetic resin crack filler using putty blade, sand smooth after 6 hours.",
                "estimated_unit_cost_inr": "₹80 - ₹140 per linear meter"
            },
            {
                "method": "Waterproof Exterior Acrylic Emulsion",
                "material": "Elastomeric 100% acrylic waterproofing paint (anti-carbonation)",
                "procedure": "Apply 2 coats of elastomeric exterior coating capable of bridging micro-cracks up to 0.5 mm during thermal cycling.",
                "estimated_unit_cost_inr": "₹35 - ₹55 per sq. foot"
            }
        ],
        "urgency": "Routine Maintenance (30 Days)",
        "compliance_codes": ["IS 456:2000 Clause 35.3.2", "IS 2402 (Code of practice for external renderings)"],
        "engineering_notes": "Defect is within permissible IS 456 crack width limits (0.3 mm) for non-aggressive environments. No structural distress or rebar corrosion observed. Routine cosmetic sealing recommended to prevent water ingress."
    }

def run_crack_diagnostics(
    image: Image.Image,
    client: GeminiMultimodalClient,
    sample_type: str = "custom"
) -> Tuple[Dict[str, Any], bool, str]:
    """Execute multimodal crack diagnostics analysis."""
    if sample_type == "shear":
        demo_data = get_demo_shear_data()
    elif sample_type == "hairline":
        demo_data = get_demo_hairline_data()
    else:
        demo_data = get_demo_shear_data()

    user_prompt = "Perform forensic concrete crack classification, width estimation, root cause identification, and repair protocol generation."
    return client.analyze_image_with_json_contract(
        image=image,
        system_prompt=CRACK_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        demo_fallback_data=demo_data
    )
