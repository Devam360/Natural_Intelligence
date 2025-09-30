
from typing import Dict

def calculate_emissions(production_tpy: float, coal_tpy: float, electricity_kwh_py: float, scrap_percent: float,
                        factors: Dict[str, float]) -> Dict:
    COAL_FACTOR = factors["coal_factor"]
    ELECTRICITY_FACTOR = factors["electricity_factor"]
    PROCESS_FACTOR = factors["process_factor"]

    process_emissions = production_tpy * PROCESS_FACTOR * (1 - scrap_percent/100)
    coal_emissions = coal_tpy * COAL_FACTOR
    electricity_emissions = electricity_kwh_py * ELECTRICITY_FACTOR
    total = coal_emissions + electricity_emissions + process_emissions

    return {
        "Total CO2 (tons)": float(total),
        "Breakdown": {
            "Coal 🔥": float(coal_emissions),
            "Electricity ⚡": float(electricity_emissions),
            "Steel-making ♻️": float(process_emissions)
        }
    }

def apply_interventions(baseline_total: float, interventions_flags: Dict[str, int]):
    reduction_frac = (
        0.10 * interventions_flags.get("scrap", 0) +
        0.07 * interventions_flags.get("heat", 0) +
        0.05 * interventions_flags.get("re", 0) +
        0.08 * interventions_flags.get("eff", 0)
    )
    reduction = baseline_total * reduction_frac
    return max(baseline_total - reduction, 0.0), reduction
