"""Construction Engineering Multi-Turn Assistant Chatbot (Epic 5).

Provides conversational domain knowledge on IS 456, IS 10262, IS 13920, OSHA 1926,
concrete technology, real estate budgeting, and site execution.
Operates via Gemini 1.5 with full demonstration mode fallback.
"""

from typing import List, Dict, Tuple
from modules.gemini_client import GeminiMultimodalClient

CHATBOT_SYSTEM_INSTRUCTION = """You are 'SiteVision AI', a Senior Principal Construction & Structural Engineering Consultant.
You possess deep expertise in:
1. Bureau of Indian Standards (BIS):
   - IS 456:2000 (Plain and Reinforced Concrete - Code of Practice)
   - IS 10262:2019 (Concrete Mix Design Guidelines for M20 to M80)
   - IS 13920:2016 (Ductile Detailing of RC Structures for Seismic Forces)
   - IS 383:2016 (Coarse and Fine Aggregates)
   - IS 1199 (Methods of Sampling and Analysis of Concrete / Slump)
   - IS 7861 (Hot Weather and Cold Weather Concreting)
2. International Safety Codes:
   - OSHA 1926 (Safety and Health Regulations for Construction)
   - Fall Protection (1926.501/502), Cranes (1926.1431), Excavations (Subpart P)
3. Site Execution & Project Controls:
   - Formwork stripping time schedules (IS 456 Table 11)
   - Rebar cover standards (Footings 50mm, Columns 40mm, Beams 25mm, Slabs 20mm)
   - Curing periods (Minimum 7 days for OPC, 10-14 days for mineral admixtures/dry climates)
   - Real estate planning, CapEx forecasting, and RERA compliance.

Give concise, authoritative, practical civil engineering responses. Cite specific code clauses wherever relevant.
Format key steps with bullet points and bold technical terms.
"""

# Rich engineering knowledgebase for offline/demo queries
CIVIL_KNOWLEDGEBASE = {
    "stripping": """### Formwork Stripping Times (IS 456:2000, Table 11)
Under standard temperatures (> 16°C) using Ordinary Portland Cement (OPC):
1. **Vertical formwork to columns, walls, and beams**: **16 – 24 hours** (ensure concrete has achieved sufficient strength to resist self-weight).
2. **Soffit formwork to slabs (props left under)**: **3 days**
3. **Soffit formwork to beams (props left under)**: **7 days**
4. **Removal of props under slabs**:
   - Spanning up to 4.5 m: **7 days**
   - Spanning over 4.5 m: **14 days**
5. **Removal of props under beams and arches**:
   - Spanning up to 6 m: **14 days**
   - Spanning over 6 m: **21 days**

*Note: If using Portland Pozzolana Cement (PPC) or Fly Ash blends, stripping times should be suitably prolonged based on cube test results (IS 456 Clause 11.3).*""",

    "cover": """### Minimum Nominal Concrete Cover Requirements (IS 456:2000, Clause 26.4 & Table 16)
To satisfy durability under **Moderate** exposure conditions:
- **Footings / Foundations**: **50 mm** (increases to 75 mm if cast against unformed soil)
- **RCC Columns**: **40 mm** (or diameter of longitudinal bar if > 40mm; can be 25mm for columns <= 200mm with bars <= 12mm)
- **Beams**: **25 mm** (or bar diameter)
- **Slabs**: **20 mm** (or bar diameter; 15mm permitted in mild exposure for bars <= 12mm)
- **Shear Walls**: **25 mm**

*Note: For severe coastal environments (e.g. Mumbai, Chennai), increase cover by 15-20 mm or apply anti-carbonation coatings (IS 456 Clause 26.4.2).*""",

    "curing": """### Concrete Curing Protocol (IS 456:2000, Clause 13.5)
- **Minimum Curing Period**:
  - Ordinary Portland Cement (OPC): **Minimum 7 days**
  - Blended Cements (PPC, GGBS, Slag, Fly Ash): **Minimum 10 to 14 days**
  - Dry and hot weather conditions: Minimum **14 days**
- **Permissible Methods**:
  1. **Ponding**: Ideal for horizontal slabs (creating 25mm water dykes).
  2. **Wet Hessian / Burlap Cloth**: Kept continuously moist for vertical columns and beam soffits.
  3. **Liquid Membrane-Forming Curing Compounds**: Conforming to ASTM C309 (applied as soon as surface sheen vanishes).
  
*Early cessation of curing leads to plastic shrinkage micro-cracking and up to 30% reduction in ultimate compressive strength.*""",

    "shear": """### Diagnostic & Repair Protocol: Diagonal Shear Crack in RCC Beam
1. **Root Cause Analysis (IS 456 Clause 40)**:
   - A 45° diagonal crack originating near the support indicates that principal tensile stress has exceeded the diagonal tensile strength ($\tau_c$).
   - Common causes: Stirrup spacing too wide, unanticipated point load, or rebar yield.
2. **Immediate Site Action**:
   - **Erect Temporary Shoring**: Place adjustable steel Acro-props under the beam span within 24 hours to relieve live and dead load.
3. **Engineering Repair Procedure**:
   - **Epoxy Pressure Injection**: For crack widths > 0.3 mm, install injection nipples at 150mm c/c along the crack, seal surface with epoxy putty, and inject low-viscosity epoxy resin (e.g., Sikadur-52) at 2 to 4 bar pressure until refusal.
   - **CFRP Strengthening**: For critical shear deficiency, bond unidirectional Carbon Fiber Reinforced Polymer (CFRP) fabric wraps (e.g., SikaWrap-300C) in a U-jacket configuration perpendicular to the crack axis to restore ultimate shear capacity."""
}

def generate_assistant_response(
    client: GeminiMultimodalClient,
    chat_history: List[Dict[str, str]]
) -> Tuple[str, bool]:
    """Generates an answer using either live Gemini 1.5 or offline engineering knowledgebase."""
    if not chat_history:
        return "How can I assist you with site engineering, IS 456 compliance, or safety today?", True

    latest_user_query = chat_history[-1]["content"].lower()

    # Determine fallback text based on keyword match
    fallback_text = None
    if "stripping" in latest_user_query or "shuttering" in latest_user_query or "formwork" in latest_user_query or "props" in latest_user_query:
        fallback_text = CIVIL_KNOWLEDGEBASE["stripping"]
    elif "cover" in latest_user_query or "clear cover" in latest_user_query or "rebar spacing" in latest_user_query:
        fallback_text = CIVIL_KNOWLEDGEBASE["cover"]
    elif "curing" in latest_user_query or "hydration" in latest_user_query:
        fallback_text = CIVIL_KNOWLEDGEBASE["curing"]
    elif "shear" in latest_user_query or "crack" in latest_user_query or "epoxy" in latest_user_query:
        fallback_text = CIVIL_KNOWLEDGEBASE["shear"]
    else:
        fallback_text = (
            "### Civil Engineering Advisory\n"
            f"Regarding your query on: **{chat_history[-1]['content']}**\n\n"
            "Under Indian Standard **IS 456:2000** and **OSHA 1926** construction guidelines:\n"
            "- Ensure all structural actions comply with limit state design parameters (partial safety factor $\\gamma_m = 1.5$ for concrete, $1.15$ for steel).\n"
            "- Material test certificates for TMT Fe500D rebar and 53-grade OPC cement must be verified against IS 1786 and IS 12269 respectively.\n"
            "- For specialized guidance on concrete mix design, crack repair injection, or weather-specific site shutdowns, please select the relevant preset query or input your project parameters in Tabs 1–3."
        )

    return client.generate_chat_response(
        chat_history=chat_history,
        system_instruction=CHATBOT_SYSTEM_INSTRUCTION,
        demo_fallback_text=fallback_text
    )
