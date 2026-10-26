"""Configuration constants, Indian engineering standards, and cost benchmarks for the Multimodal Construction Intelligence Platform."""

PLATFORM_NAME = "Multimodal Construction Intelligence Platform"
CAPSTONE_ID = "6ac4c98d1dcde6d7857c1642"
APP_VERSION = "2.4.0 (Enterprise Capstone Edition)"

# Indian City Tiers & Real Estate Multipliers
CITY_TIERS = {
    "Tier 1 (Metro)": {
        "cities": ["Mumbai (MMR)", "Delhi-NCR", "Bengaluru", "Hyderabad", "Chennai"],
        "base_cost_multiplier": 1.25,
        "market_val_multiplier": 2.80, # Ready asset market valuation multiple over construction cost
        "land_share_pct": 55, # Land accounts for ~55% of ready asset value in Tier 1
        "tier_label": "Tier 1 High-Density Metros"
    },
    "Tier 2 (Emerging Urban)": {
        "cities": ["Pune", "Ahmedabad", "Kolkata", "Jaipur", "Surat", "Kochi", "Chandigarh"],
        "base_cost_multiplier": 1.05,
        "market_val_multiplier": 1.95,
        "land_share_pct": 40,
        "tier_label": "Tier 2 Major Economic Hubs"
    },
    "Tier 3 (Developing Districts)": {
        "cities": ["Bhopal", "Indore", "Coimbatore", "Vadodara", "Visakhapatnam", "Nagpur", "Lucknow"],
        "base_cost_multiplier": 0.90,
        "market_val_multiplier": 1.50,
        "land_share_pct": 28,
        "tier_label": "Tier 3 Fast-Growing Cities"
    }
}

# Structure Types & Base Construction Cost (INR / sqft)
STRUCTURE_TYPES = {
    "Residential Apartment (G+14 RCC Frame)": {
        "base_rate_per_sqft": 2400,
        "steel_kg_per_sqft": 3.8,
        "cement_bags_per_sqft": 0.42,
        "sand_cft_per_sqft": 1.85,
        "aggregate_cft_per_sqft": 2.30,
        "typical_duration_months": 24,
        "style_tag": "modern residential multi-story residential towers with landscaped balconies"
    },
    "Commercial Office Park (Grade-A Glass Facade)": {
        "base_rate_per_sqft": 3500,
        "steel_kg_per_sqft": 4.5,
        "cement_bags_per_sqft": 0.48,
        "sand_cft_per_sqft": 2.05,
        "aggregate_cft_per_sqft": 2.60,
        "typical_duration_months": 30,
        "style_tag": "futuristic corporate commercial tower with double-glazed curtain wall, podium parking"
    },
    "Industrial Pre-Engineered Building (PEB / Warehouse)": {
        "base_rate_per_sqft": 1750,
        "steel_kg_per_sqft": 5.2, # Higher steel for portal frames/trusses
        "cement_bags_per_sqft": 0.28,
        "sand_cft_per_sqft": 1.20,
        "aggregate_cft_per_sqft": 1.70,
        "typical_duration_months": 12,
        "style_tag": "heavy industrial logistics warehouse, steel portal frame, insulated puff panels, loading bays"
    },
    "Luxury Independent Villa (G+2 Modern Tropical)": {
        "base_rate_per_sqft": 4200,
        "steel_kg_per_sqft": 4.0,
        "cement_bags_per_sqft": 0.45,
        "sand_cft_per_sqft": 2.10,
        "aggregate_cft_per_sqft": 2.45,
        "typical_duration_months": 18,
        "style_tag": "luxury contemporary biophilic villa with cantilevered decks, plunge pool, teak louvers"
    },
    "Mixed-Use Urban Complex (Retail Podium + SOHO)": {
        "base_rate_per_sqft": 3100,
        "steel_kg_per_sqft": 4.2,
        "cement_bags_per_sqft": 0.44,
        "sand_cft_per_sqft": 1.95,
        "aggregate_cft_per_sqft": 2.40,
        "typical_duration_months": 28,
        "style_tag": "mixed-use retail plaza with bustling pedestrian walkways and integrated residential tower"
    }
}

# Project Milestones Breakdown (% of construction cost)
CONSTRUCTION_MILESTONES = [
    {"stage": "Mobilization, Excavation & Footings", "weight": 15, "cumulative": 15},
    {"stage": "Substructure & Basement RCC Retaining Walls", "weight": 15, "cumulative": 30},
    {"stage": "Superstructure RCC Columns, Beams & Slabs", "weight": 30, "cumulative": 60},
    {"stage": "Masonry, External & Internal Plastering", "weight": 15, "cumulative": 75},
    {"stage": "MEP (Mechanical, Electrical, Plumbing) Rough-in", "weight": 10, "cumulative": 85},
    {"stage": "Finishing, Glazing, Flooring & Painting", "weight": 10, "cumulative": 95},
    {"stage": "Commissioning, Snagging & Occupancy Certificate", "weight": 5, "cumulative": 100}
]

# Weather Advisory Rules & Protocols (OSHA & IS 456)
WEATHER_PROTOCOLS = {
    "High Wind (> 35 km/h / Gale)": {
        "severity": "High Alert",
        "badge_color": "#dc2626", # Red
        "crane_operations": "MANDATORY HALT: Suspend all tower crane lifts, mobile crane booms, and exterior hoists immediately (OSHA 1926.1431 / IS 13367). Weathercock crane jibs to free-slew.",
        "height_work": "PROHIBITED: Evacuate all suspended cradles, external mast climbers, and perimeter scaffolding above 3m.",
        "electrical": "Secure temporary distribution cables; inspect for snagging against swaying structural members.",
        "concrete_curing": "High evaporation risk: Apply aliphatic alcohol moisture retardant and heavy wet hessian cloth to prevent plastic shrinkage cracking (IS 456 Clause 13.5).",
        "action_items": [
            "Tie down loose corrugated sheets, formwork panels, and rebar bundles.",
            "Inspect perimeter safety catch netting and debris meshes.",
            "Verify crane boom angle locked and outriggers stable."
        ]
    },
    "Heavy Rain / Monsoon Inundation": {
        "severity": "Critical Risk",
        "badge_color": "#2563eb", # Blue
        "crane_operations": "RESTRICTED: Operating surface must have solid gravel mats; check ground bearing capacity around crane outriggers for washouts.",
        "height_work": "SLIP HAZARD: Cease work on wet rebar decks, steel girders, and open staging. Full harness attachment with trailing ropes mandatory.",
        "electrical": "ELECTROCUTION PROTOCOL: Disconnect non-weatherproof power boards; energize ONLY through 30mA Earth Leakage Circuit Breakers (ELCB / RCCB). Keep submersible dewatering pumps isolated.",
        "concrete_curing": "PROTECT FRESH POURS: Cover unhardened concrete surfaces immediately with waterproof tarpaulins to prevent cement paste washout and water-cement ratio dilution (IS 456 Clause 13.3).",
        "action_items": [
            "Activate dewatering pump systems in deep foundation pits.",
            "Shore up excavation slopes against mudslide or trench wall collapse (OSHA 1926 Subpart P).",
            "Store cement bags on raised timber pallets (minimum 200mm above ground) inside damp-proof sheds."
        ]
    },
    "Extreme Heat (> 40°C / Heatwave)": {
        "severity": "Moderate / Health Hazard",
        "badge_color": "#d97706", # Amber
        "crane_operations": "OPERATIONAL: Ensure crane cabin air conditioning is functioning; operator vigilance checks every 2 hours.",
        "height_work": "THERMAL STRESS: Schedule steel tying, welding, and high-altitude slab works for early morning (06:00 - 11:00) and late afternoon (16:00 - 19:00).",
        "electrical": "Prevent transformer and generator overheating; monitor cable derating under sustained thermal loads.",
        "concrete_curing": "HOT WEATHER CONCRETING PROTOCOL (IS 7861 Part 1): Concrete placing temperature must not exceed 32°C. Use chilled mixing water or flake ice. Continuous ponding/wet curing for minimum 14 days.",
        "action_items": [
            "Set up shaded rest canopies with cold potable water and oral rehydration salt (ORS) solutions.",
            "Buddy system monitoring for heat exhaustion, cramps, and sunstroke symptoms.",
            "Protect curing concrete with continuous water sprinklers."
        ]
    },
    "Normal / Favorable Site Weather": {
        "severity": "Normal Operations",
        "badge_color": "#059669", # Green
        "crane_operations": "NORMAL: Standard daily pre-lift safety inspection, load chart verification, and rigging checks.",
        "height_work": "NORMAL: 100% tie-off compliance above 1.8m (OSHA) / 2.0m (IS 3521). Daily toolbox safety briefing required.",
        "electrical": "Standard routine maintenance and lock-out/tag-out (LOTO) protocols.",
        "concrete_curing": "Standard 7-day wet burlap/ponding curing for OPC (10 days for PPC / fly-ash blended cements) per IS 456 Clause 13.5.",
        "action_items": [
            "Conduct routine morning site induction and PPE compliance sweep.",
            "Verify daily material logs for rebar delivery, cement batch test certificates, and slump test results.",
            "Review weekly target milestones with project managers and site subcontractors."
        ]
    }
}
