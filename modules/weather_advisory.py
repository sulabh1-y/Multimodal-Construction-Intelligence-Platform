"""Weather-Aware Site Advisory Module (Epic 5).

Provides dynamic safety alerts and operational directives based on meteorological conditions,
enforcing OSHA 1926 standards and Indian Standard IS 456 / IS 7861 protocols.
"""

from typing import Dict, Any
from config import WEATHER_PROTOCOLS

def get_weather_protocol(condition: str) -> Dict[str, Any]:
    """Retrieve full safety directives and operational protocols for a given weather condition."""
    return WEATHER_PROTOCOLS.get(condition, WEATHER_PROTOCOLS["Normal / Favorable Site Weather"])

def get_weather_impact_summary(condition: str) -> Dict[str, Any]:
    """Generates high-level impact score and operational flags."""
    proto = get_weather_protocol(condition)
    
    risk_mapping = {
        "High Wind (> 35 km/h / Gale)": {
            "risk_index": 85,
            "crane_status": "PROHIBITED / HALTED",
            "concreting_status": "RESTRICTED (Windbreaks & Curing Mats Required)",
            "external_scaffold_status": "EVACUATION ORDER"
        },
        "Heavy Rain / Monsoon Inundation": {
            "risk_index": 92,
            "crane_status": "RESTRICTED (Ground Bearing Checks)",
            "concreting_status": "HALT FRESH POURS (Tarpaulin Covers On)",
            "external_scaffold_status": "RESTRICTED (Slip Hazards)"
        },
        "Extreme Heat (> 40°C / Heatwave)": {
            "risk_index": 68,
            "crane_status": "OPERATIONAL (Cabin AC & Vigilance)",
            "concreting_status": "NIGHT/EARLY POURS ONLY (Ice Water / Retarders)",
            "external_scaffold_status": "RESTRICTED (Shift Rotations)"
        },
        "Normal / Favorable Site Weather": {
            "risk_index": 15,
            "crane_status": "NORMAL OPERATIONS",
            "concreting_status": "STANDARD CURING PROTOCOL (7-Day Wet Burlap)",
            "external_scaffold_status": "STANDARD 100% TIE-OFF"
        }
    }
    
    impact = risk_mapping.get(condition, risk_mapping["Normal / Favorable Site Weather"])
    return {
        **proto,
        **impact
    }
