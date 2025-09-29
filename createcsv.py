import pandas as pd

# Sample SME steel plant data
data = {
    "Plant": ["Alpha Steel", "Beta Steel", "Gamma Steel"],
    "Monthly Production (tons)": [500, 750, 300],
    "Coal Consumption (tons)": [200, 300, 120],
    "Electricity Usage (kWh)": [100000, 150000, 60000],
    "Scrap Steel (%)": [20, 15, 25]
}

df = pd.DataFrame(data)
df.to_csv("sample_steel_sme_data.csv", index=False)
