
def make_recommendations(breakdown: dict):
    parts = sorted(breakdown.items(), key=lambda x: x[1], reverse=True)
    tips = []
    if parts and parts[0][0].startswith("Electricity"):
        tips.append("High electricity emissions → prioritize on-site solar/PPA and efficiency.")
    if parts and parts[0][0].startswith("Coal"):
        tips.append("Coal dominates → fuel switch, heat recovery, and combustion optimization.")
    if parts and parts[0][0].startswith("Steel-making"):
        tips.append("Process heavy → increase scrap charge and explore alternative feedstocks.")
    return tips
