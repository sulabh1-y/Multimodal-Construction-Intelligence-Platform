"""End-to-End Verification Test Suite for Multimodal Construction Intelligence Platform."""

import os
import sys
from PIL import Image

def test_imports():
    print("[1/7] Testing module imports...")
    import config
    from modules.gemini_client import GeminiMultimodalClient
    from modules.ppe_audit import run_ppe_audit
    from modules.crack_diagnostics import run_crack_diagnostics
    from modules.valuation import calculate_project_financials
    from modules.pollinations_client import generate_architectural_prompt, build_pollinations_image_url
    from modules.weather_advisory import get_weather_impact_summary
    from modules.chatbot import generate_assistant_response
    print("  -> All modules imported successfully!")

def test_ppe_audit():
    print("[2/7] Testing PPE Audit Engine...")
    from modules.gemini_client import GeminiMultimodalClient
    from modules.ppe_audit import run_ppe_audit
    
    client = GeminiMultimodalClient(api_key="")
    assert client.is_demo_mode == True
    
    img = Image.open("assets/sample_ppe_violation.jpg")
    res, is_sim, note = run_ppe_audit(img, client, sample_type="violation")
    
    assert "safety_score" in res, "Missing safety_score"
    assert "overall_status" in res, "Missing overall_status"
    assert "ppe_detection" in res, "Missing ppe_detection checklist"
    assert "identified_site_hazards" in res, "Missing hazards list"
    assert len(res["ppe_detection"]) >= 4, "Must have 4 PPE categories"
    print(f"  -> PPE Audit OK: Score={res['safety_score']}, Status={res['overall_status']}, Hazards={len(res['identified_site_hazards'])}")

def test_crack_diagnostics():
    print("[3/7] Testing Crack Diagnostics Engine...")
    from modules.gemini_client import GeminiMultimodalClient
    from modules.crack_diagnostics import run_crack_diagnostics
    
    client = GeminiMultimodalClient(api_key="")
    img = Image.open("assets/sample_crack_shear.jpg")
    res, is_sim, note = run_crack_diagnostics(img, client, sample_type="shear")
    
    assert res["defect_type"] == "Structural Shear"
    assert res["estimated_crack_width_mm"] > 0
    assert len(res["recommended_engineering_repairs"]) >= 2
    assert "IS 456" in res["engineering_notes"] or "IS 456" in str(res["compliance_codes"])
    print(f"  -> Crack Diagnostics OK: Defect={res['defect_type']}, Width={res['estimated_crack_width_mm']}mm, Urgency={res['urgency']}")

def test_valuation_engine():
    print("[4/7] Testing Planning & Real Estate Valuation...")
    from modules.valuation import calculate_project_financials
    
    fin = calculate_project_financials(
        structure_type="Residential Apartment (G+14 RCC Frame)",
        built_up_sqft=50_000,
        location_tier="Tier 1 (Metro)",
        completion_pct=60.0
    )
    
    assert fin["total_budget_inr"] > 0
    assert fin["capex_incurred_inr"] > 0
    assert fin["current_asset_valuation_inr"] > fin["capex_incurred_inr"]
    assert "Cr" in fin["total_budget_formatted"] or "L" in fin["total_budget_formatted"]
    assert fin["materials"]["cement"]["total_bags"] > 0
    assert fin["materials"]["steel"]["total_mt"] > 0
    assert len(fin["milestones"]) == 7
    print(f"  -> Valuation OK: Budget={fin['total_budget_formatted']}, CapEx={fin['capex_incurred_formatted']}, WIP Value={fin['current_asset_valuation_formatted']}, Steel={fin['materials']['steel']['total_mt']} MT")

def test_weather_advisory():
    print("[5/7] Testing Weather Advisory Matrix...")
    from modules.weather_advisory import get_weather_impact_summary
    
    wind = get_weather_impact_summary("High Wind (> 35 km/h / Gale)")
    assert "HALT" in wind["crane_operations"].upper()
    
    rain = get_weather_impact_summary("Heavy Rain / Monsoon Inundation")
    assert "RESTRICTED" in rain["crane_operations"].upper()
    assert "ELECTROCUTION" in rain["electrical"].upper() or "ELCB" in rain["electrical"].upper()
    print(f"  -> Weather Advisory OK: High Wind Risk={wind['risk_index']}, Monsoon Risk={rain['risk_index']}")

def test_chatbot():
    print("[6/7] Testing SiteVision AI Assistant Chatbot...")
    from modules.gemini_client import GeminiMultimodalClient
    from modules.chatbot import generate_assistant_response
    
    client = GeminiMultimodalClient(api_key="")
    history = [{"role": "user", "content": "What is the formwork stripping time for beam props under IS 456 Table 11?"}]
    reply, is_sim = generate_assistant_response(client, history)
    
    assert "IS 456" in reply or "Table 11" in reply or "props" in reply.lower()
    print("  -> Chatbot OK: Successfully answered stripping time query based on IS 456 Table 11")

def test_pollinations():
    print("[7/7] Testing Pollinations AI 3D Render URL Builder...")
    from modules.pollinations_client import generate_architectural_prompt, build_pollinations_image_url
    
    prompt = generate_architectural_prompt("Commercial Office Park", "Sustainable Biophilic", "Golden Hour Sunset")
    url = build_pollinations_image_url(prompt, seed=123)
    assert url.startswith("https://image.pollinations.ai/prompt/")
    assert "width=1024" in url
    print(f"  -> Pollinations OK: Generated prompt and valid URL: {url[:60]}...")

if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING VERIFICATION SUITE: MULTIMODAL CONSTRUCTION PLATFORM")
    print("=" * 60)
    test_imports()
    test_ppe_audit()
    test_crack_diagnostics()
    test_valuation_engine()
    test_weather_advisory()
    test_chatbot()
    test_pollinations()
    print("=" * 60)
    print("🎉 ALL 7 TEST SUITES PASSED PERFECTLY!")
    print("=" * 60)
