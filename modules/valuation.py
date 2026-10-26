"""Planning & Real Estate Valuation Module (Epic 3).

Calculates total project budgets, CapEx incurred, current asset market valuations in INR (Crores & Lakhs),
material requirement forecasting (Cement, TMT Steel, Sand, Aggregates), and milestone schedules.
"""

from typing import Dict, Any, List
from config import CITY_TIERS, STRUCTURE_TYPES, CONSTRUCTION_MILESTONES

def format_inr(amount_inr: float) -> str:
    """Format currency in Indian numbering system (Lakhs & Crores)."""
    if amount_inr >= 10_000_000: # >= 1 Crore
        crores = amount_inr / 10_000_000
        return f"₹{crores:,.2f} Cr"
    elif amount_inr >= 100_000: # >= 1 Lakh
        lakhs = amount_inr / 100_000
        return f"₹{lakhs:,.2f} L"
    else:
        return f"₹{amount_inr:,.0f}"

def calculate_project_financials(
    structure_type: str,
    built_up_sqft: float,
    location_tier: str,
    completion_pct: float,
    quality_spec: str = "Standard Quality"
) -> Dict[str, Any]:
    """Computes comprehensive project budget, CapEx incurred, ready market valuation, and materials."""
    
    tier_info = CITY_TIERS.get(location_tier, list(CITY_TIERS.values())[0])
    struct_info = STRUCTURE_TYPES.get(structure_type, list(STRUCTURE_TYPES.values())[0])
    
    quality_multipliers = {
        "Standard Quality (CPWD Specs)": 1.0,
        "Premium Specification (Imported Finishes)": 1.18,
        "Ultra-Luxury Specification (High-End Automation)": 1.38
    }
    q_mult = quality_multipliers.get(quality_spec, 1.0)
    
    # Unit rates
    base_rate = struct_info["base_rate_per_sqft"]
    tier_mult = tier_info["base_cost_multiplier"]
    effective_rate_per_sqft = base_rate * tier_mult * q_mult
    
    # Financial metrics
    total_budget = effective_rate_per_sqft * built_up_sqft
    capex_incurred = total_budget * (completion_pct / 100.0)
    capex_remaining = total_budget - capex_incurred
    
    # Real estate asset valuation
    market_val_multiplier = tier_info["market_val_multiplier"]
    land_share_pct = tier_info["land_share_pct"] / 100.0
    
    projected_ready_market_value = total_budget * market_val_multiplier
    base_land_value = projected_ready_market_value * land_share_pct
    
    # Current Work-in-Progress (WIP) Valuation = Land Value + Embedded CapEx value with contractor markup
    current_asset_valuation = base_land_value + (capex_incurred * 1.25)
    
    # Material consumption thumb rules (IS 456 / CPWD)
    total_cement_bags = built_up_sqft * struct_info["cement_bags_per_sqft"]
    total_cement_mt = total_cement_bags * 0.050 # 50kg bag
    
    total_steel_kg = built_up_sqft * struct_info["steel_kg_per_sqft"]
    total_steel_mt = total_steel_kg / 1000.0
    
    total_sand_cft = built_up_sqft * struct_info["sand_cft_per_sqft"]
    total_sand_brass = total_sand_cft / 100.0 # 1 Brass = 100 cu.ft
    
    total_aggregate_cft = built_up_sqft * struct_info["aggregate_cft_per_sqft"]
    total_aggregate_brass = total_aggregate_cft / 100.0
    
    # Consumed vs remaining
    cement_consumed_bags = total_cement_bags * (completion_pct / 100.0)
    steel_consumed_mt = total_steel_mt * (completion_pct / 100.0)
    sand_consumed_brass = total_sand_brass * (completion_pct / 100.0)
    aggregate_consumed_brass = total_aggregate_brass * (completion_pct / 100.0)
    
    # Milestone status calculation
    milestones_status = []
    for m in CONSTRUCTION_MILESTONES:
        cum = m["cumulative"]
        weight = m["weight"]
        start_pct = cum - weight
        
        if completion_pct >= cum:
            status = "Completed"
            stage_pct = 100
        elif completion_pct <= start_pct:
            status = "Pending"
            stage_pct = 0
        else:
            status = "In Progress"
            stage_pct = int(((completion_pct - start_pct) / weight) * 100)
            
        milestones_status.append({
            "stage": m["stage"],
            "weight": weight,
            "cumulative_threshold": cum,
            "status": status,
            "stage_progress_pct": stage_pct
        })
        
    return {
        "effective_rate_per_sqft": effective_rate_per_sqft,
        "total_budget_inr": total_budget,
        "total_budget_formatted": format_inr(total_budget),
        "capex_incurred_inr": capex_incurred,
        "capex_incurred_formatted": format_inr(capex_incurred),
        "capex_remaining_inr": capex_remaining,
        "capex_remaining_formatted": format_inr(capex_remaining),
        "current_asset_valuation_inr": current_asset_valuation,
        "current_asset_valuation_formatted": format_inr(current_asset_valuation),
        "projected_ready_market_value_inr": projected_ready_market_value,
        "projected_ready_market_value_formatted": format_inr(projected_ready_market_value),
        "base_land_value_inr": base_land_value,
        "base_land_value_formatted": format_inr(base_land_value),
        "completion_pct": completion_pct,
        "materials": {
            "cement": {
                "total_bags": int(total_cement_bags),
                "total_mt": round(total_cement_mt, 1),
                "consumed_bags": int(cement_consumed_bags),
                "remaining_bags": int(total_cement_bags - cement_consumed_bags)
            },
            "steel": {
                "total_mt": round(total_steel_mt, 2),
                "consumed_mt": round(steel_consumed_mt, 2),
                "remaining_mt": round(total_steel_mt - steel_consumed_mt, 2)
            },
            "sand": {
                "total_brass": round(total_sand_brass, 1),
                "consumed_brass": round(sand_consumed_brass, 1),
                "remaining_brass": round(total_sand_brass - sand_consumed_brass, 1)
            },
            "aggregate": {
                "total_brass": round(total_aggregate_brass, 1),
                "consumed_brass": round(aggregate_consumed_brass, 1),
                "remaining_brass": round(total_aggregate_brass - aggregate_consumed_brass, 1)
            }
        },
        "milestones": milestones_status
    }
