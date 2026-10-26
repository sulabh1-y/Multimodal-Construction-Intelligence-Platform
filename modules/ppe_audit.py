"""Site Safety & PPE Audit Module (Epic 2).

Analyzes site imagery for PPE compliance and site hazards under OSHA and Indian IS 456 / IS standards.
Outputs structured JSON contracts and interactive UI metric visualizers.
"""

from datetime import datetime
from typing import Dict, Any, Tuple
from PIL import Image
from modules.gemini_client import GeminiMultimodalClient

PPE_SYSTEM_PROMPT = """You are a Principal Civil Safety Engineer and OSHA/IS 456 Site Compliance Auditor.
Analyze the provided construction site photo for worker Personal Protective Equipment (PPE) compliance and occupational hazards.

You must reference:
- Indian Standard IS 2925 / OSHA 1926.100 (Industrial Safety Helmets)
- Indian Standard IS 15809 / OSHA 1926.201 (High-Visibility Warning Garments)
- Indian Standard IS 15298 / OSHA 1926.96 (Protective Safety Footwear with Steel Toes)
- Indian Standard IS 3521 / OSHA 1926.502 (Fall Arrest Safety Harnesses and Lifelines)
- Indian Standard IS 456:2000 & IS 4014 (Scaffolding and Concrete Shuttering Safety)

Return STRICT JSON with this schema:
{
  "safety_score": <number between 0 and 100>,
  "overall_status": "<COMPLIANT | NEEDS_ATTENTION | CRITICAL_HAZARD>",
  "audit_timestamp": "<ISO timestamp>",
  "workers_detected_count": <integer>,
  "standards_referenced": ["OSHA 1926.100", "IS 2925", "IS 15809", "IS 15298", "IS 3521", "IS 456"],
  "ppe_detection": [
    {
      "item": "Industrial Safety Helmets / Hard Hats",
      "required_by": "IS 2925 / OSHA 1926.100",
      "detected": <true/false>,
      "compliant": <true/false>,
      "compliance_rate_pct": <number 0-100>,
      "notes": "<observation>"
    },
    {
      "item": "High-Visibility Reflective Vests",
      "required_by": "IS 15809 / OSHA 1926.201",
      "detected": <true/false>,
      "compliant": <true/false>,
      "compliance_rate_pct": <number 0-100>,
      "notes": "<observation>"
    },
    {
      "item": "Steel-Toe Safety Footwear",
      "required_by": "IS 15298 / OSHA 1926.96",
      "detected": <true/false>,
      "compliant": <true/false>,
      "compliance_rate_pct": <number 0-100>,
      "notes": "<observation>"
    },
    {
      "item": "Full-Body Safety Harness & Lanyards",
      "required_by": "IS 3521 / OSHA 1926.502",
      "detected": <true/false>,
      "compliant": <true/false>,
      "compliance_rate_pct": <number 0-100>,
      "notes": "<observation>"
    }
  ],
  "identified_site_hazards": [
    {
      "hazard": "<hazard description>",
      "severity": "<Low | Medium | High | Critical>",
      "location": "<site area or worker description>",
      "regulatory_standard": "<OSHA or IS code>",
      "corrective_remedy": "<exact corrective engineering or safety action>"
    }
  ],
  "executive_summary": "<summary paragraph>"
}
"""

def get_demo_compliant_data() -> Dict[str, Any]:
    """Pre-computed realistic compliant site audit."""
    return {
        "safety_score": 94,
        "overall_status": "COMPLIANT",
        "audit_timestamp": datetime.now().isoformat(),
        "workers_detected_count": 2,
        "standards_referenced": ["OSHA 1926.100", "IS 2925", "IS 15809", "IS 15298", "IS 3521", "IS 456:2000"],
        "ppe_detection": [
            {
                "item": "Industrial Safety Helmets / Hard Hats",
                "required_by": "IS 2925 / OSHA 1926.100",
                "detected": True,
                "compliant": True,
                "compliance_rate_pct": 100,
                "notes": "Both workers equipped with undamaged Type I Class E safety helmets fastened with chinstraps."
            },
            {
                "item": "High-Visibility Reflective Vests",
                "required_by": "IS 15809 / OSHA 1926.201",
                "detected": True,
                "compliant": True,
                "compliance_rate_pct": 100,
                "notes": "Fluorescent orange Class 2 vests with 360-degree retroreflective bands visible."
            },
            {
                "item": "Steel-Toe Safety Footwear",
                "required_by": "IS 15298 / OSHA 1926.96",
                "detected": True,
                "compliant": True,
                "compliance_rate_pct": 100,
                "notes": "Heavy-duty puncture-resistant steel toe safety boots observed on all personnel."
            },
            {
                "item": "Full-Body Safety Harness & Lanyards",
                "required_by": "IS 3521 / OSHA 1926.502",
                "detected": True,
                "compliant": True,
                "compliance_rate_pct": 95,
                "notes": "Elevated crew members wearing EN 361 / IS 3521 certified dual-lanyard full body harnesses."
            }
        ],
        "identified_site_hazards": [
            {
                "hazard": "Scaffold working platform requires additional cross-bracing inspection",
                "severity": "Low",
                "location": "Upper staging level grid line C-2",
                "regulatory_standard": "IS 4014 Part 2 / OSHA 1926.451",
                "corrective_remedy": "Re-torque coupler bolts to 40 Nm and verify diagonal tubular braces are locked before shift extension."
            }
        ],
        "executive_summary": "Superb site safety adherence. All personnel are strictly observing mandatory PPE protocols under IS 456 and OSHA 1926. The staging area demonstrates proper housekeeping and zero imminent danger."
    }

def get_demo_violation_data() -> Dict[str, Any]:
    """Pre-computed realistic hazard violation site audit."""
    return {
        "safety_score": 42,
        "overall_status": "CRITICAL_HAZARD",
        "audit_timestamp": datetime.now().isoformat(),
        "workers_detected_count": 2,
        "standards_referenced": ["OSHA 1926.100", "OSHA 1926.502", "IS 2925", "IS 15809", "IS 15298", "IS 3764 (Trench Safety)"],
        "ppe_detection": [
            {
                "item": "Industrial Safety Helmets / Hard Hats",
                "required_by": "IS 2925 / OSHA 1926.100",
                "detected": True,
                "compliant": False,
                "compliance_rate_pct": 50,
                "notes": "Worker in trench excavation completely missing safety hard hat under overhead load zone."
            },
            {
                "item": "High-Visibility Reflective Vests",
                "required_by": "IS 15809 / OSHA 1926.201",
                "detected": True,
                "compliant": False,
                "compliance_rate_pct": 50,
                "notes": "Excavation worker wearing non-compliant blue civilian clothing; not visible to mobile equipment operators."
            },
            {
                "item": "Steel-Toe Safety Footwear",
                "required_by": "IS 15298 / OSHA 1926.96",
                "detected": True,
                "compliant": False,
                "compliance_rate_pct": 50,
                "notes": "Open sandals / soft footwear detected near heavy structural trench. Severe crush risk."
            },
            {
                "item": "Full-Body Safety Harness & Lanyards",
                "required_by": "IS 3521 / OSHA 1926.502",
                "detected": False,
                "compliant": False,
                "compliance_rate_pct": 0,
                "notes": "Elevated worker on steel beam (> 5m height) working without tied-off fall arrest lanyard."
            }
        ],
        "identified_site_hazards": [
            {
                "hazard": "Fall from Heights (> 5 meters) without Fall Arrest System",
                "severity": "Critical",
                "location": "Transverse steel girder above excavation bay",
                "regulatory_standard": "OSHA 1926.501(b)(1) / IS 3521",
                "corrective_remedy": "Issue immediate STOP-WORK order. Anchor worker to certified horizontal lifeline using shock-absorbing lanyard immediately."
            },
            {
                "hazard": "Unshored Deep Trench with worker inside (> 1.5m depth)",
                "severity": "Critical",
                "location": "Foundation bay trench pit",
                "regulatory_standard": "IS 3764:1992 / OSHA 1926 Subpart P",
                "corrective_remedy": "Evacuate trench immediately. Install trench shielding boxes or cut benching at 1:1 slope before permitting re-entry."
            },
            {
                "hazard": "Footwear Puncture and Crush Vulnerability",
                "severity": "High",
                "location": "Excavation floor / rebar staging zone",
                "regulatory_standard": "IS 15298 Part 2",
                "corrective_remedy": "Mandate S3-rated steel-toe boots with puncture-resistant steel midsole before permitting site access."
            }
        ],
        "executive_summary": "CRITICAL NON-COMPLIANCE DETECTED. Immediate supervisory intervention required. Two life-threatening safety violations identified: untethered work at height and un-helmeted labor in an unshored trench. Total safety score: 42/100."
    }

def run_ppe_audit(
    image: Image.Image,
    client: GeminiMultimodalClient,
    sample_type: str = "custom"
) -> Tuple[Dict[str, Any], bool, str]:
    """Execute multimodal PPE compliance analysis."""
    if sample_type == "compliant":
        demo_data = get_demo_compliant_data()
    elif sample_type == "violation":
        demo_data = get_demo_violation_data()
    else:
        demo_data = get_demo_violation_data()

    user_prompt = "Perform complete PPE detection and site hazard assessment as specified in the system instructions."
    return client.analyze_image_with_json_contract(
        image=image,
        system_prompt=PPE_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        demo_fallback_data=demo_data
    )
