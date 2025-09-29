import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF

# ---- Helper Functions ----
def calculate_emissions(production, coal, electricity, scrap_percent):
    COAL_FACTOR = 2.5
    ELECTRICITY_FACTOR = 0.0009
    PROCESS_FACTOR = 1.8

    process_emissions = production * PROCESS_FACTOR * (1 - scrap_percent/100)
    coal_emissions = coal * COAL_FACTOR
    electricity_emissions = electricity * ELECTRICITY_FACTOR
    total = coal_emissions + electricity_emissions + process_emissions

    return {
        "Total CO2 (tons)": total,
        "Breakdown": {
            "Coal 🔥": coal_emissions,
            "Electricity ⚡": electricity_emissions,
            "Steel-making ♻️": process_emissions
        }
    }

def apply_interventions(baseline_emissions, interventions):
    reduction = 0
    if interventions.get("Use more scrap steel ♻️"):
        reduction += 0.10 * baseline_emissions["Total CO2 (tons)"]
    if interventions.get("Recover wasted heat 🔥"):
        reduction += 0.07 * baseline_emissions["Total CO2 (tons)"]
    if interventions.get("Add small renewable energy ⚡"):
        reduction += 0.05 * baseline_emissions["Total CO2 (tons)"]
    if interventions.get("Improve energy efficiency 💡"):
        reduction += 0.08 * baseline_emissions["Total CO2 (tons)"]
    
    total_after = baseline_emissions["Total CO2 (tons)"] - reduction
    return total_after, reduction

def generate_pdf(baseline, post_total, reduction, selected_actions):
    clean_actions = [action.encode('latin-1', 'ignore').decode('latin-1') for action in selected_actions]
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "SME CO2 Reduction Summary", ln=True, align="C")
    pdf.ln(10)
    
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"Baseline CO2: {baseline['Total CO2 (tons)']:.1f} tons/year", ln=True)
    pdf.cell(0, 8, f"Post-action CO2: {post_total:.1f} tons/year", ln=True)
    pdf.cell(0, 8, f"Potential Reduction: {reduction:.1f} tons/year", ln=True)
    pdf.ln(10)
    
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, "Selected Actions:", ln=True)
    pdf.set_font("Arial", "", 12)
    for i, action in enumerate(clean_actions, 1):
        pdf.cell(0, 8, f"{i}. {action}", ln=True)
    
    pdf.output("CO2_Summary.pdf")

# ---- Streamlit App ----
st.set_page_config(page_title="🌱 SME CO₂ Dashboard", layout="wide")
st.title("🌱 SME CO₂ Emission Reduction Dashboard")
st.markdown("Select recommended actions to see CO₂ reduction and generate a PDF summary!")

# ---- 1️⃣ Plant Data Inputs ----
st.header("🛠 Enter Your Plant Data")
col1, col2 = st.columns(2)
with col1:
    production = st.slider("Monthly Steel Production (tons)", 0, 1000, 500)
    coal = st.slider("Monthly Coal Consumption (tons)", 0, 500, 200)
with col2:
    electricity = st.slider("Monthly Electricity Usage (kWh)", 0, 200000, 100000)
    scrap_percent = st.slider("Scrap Steel Usage (%)", 0, 50, 20)

annual_production = production * 12
annual_coal = coal * 12
annual_electricity = electricity * 12

baseline = calculate_emissions(annual_production, annual_coal, annual_electricity, scrap_percent)

# ---- 2️⃣ Recommended Actions ----
st.header("💡 Recommended Actions")
actions = {
    "Use more scrap steel ♻️": "Increase scrap usage to reduce steel-making emissions.",
    "Recover wasted heat 🔥": "Implement heat recovery to save energy and CO₂.",
    "Add small renewable energy ⚡": "Add solar/wind to partially replace grid electricity.",
    "Improve energy efficiency 💡": "Minor upgrades to reduce energy consumption."
}

selected_actions = []
for action, desc in actions.items():
    if st.checkbox(f"{action} — {desc}"):
        selected_actions.append(action)

# ---- 3️⃣ Apply Interventions ----
post_total, reduction = apply_interventions(baseline, {k: k in selected_actions for k in actions.keys()})

# ---- 4️⃣ Dashboard Summary ----
st.header("📊 Your CO₂ Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Baseline CO₂ 🔴", f"{baseline['Total CO2 (tons)']:.1f}")
col2.metric("Post-action CO₂ 🟢", f"{post_total:.1f}")
col3.metric("Potential Reduction ⚡", f"{reduction:.1f}")

# ---- 5️⃣ Charts ----
st.subheader("📈 Emissions Charts")
bar_df = pd.DataFrame({
    "Scenario": ["Before 🔴", "After 🟢"],
    "CO2 Emissions (tons)": [baseline["Total CO2 (tons)"], post_total]
})
fig_bar = px.bar(bar_df, x="Scenario", y="CO2 Emissions (tons)",
                 color="Scenario", text="CO2 Emissions (tons)",
                 color_discrete_map={"Before 🔴":"red", "After 🟢":"green"})
st.plotly_chart(fig_bar, use_container_width=True)

pie_df = pd.DataFrame({
    "Source": list(baseline["Breakdown"].keys()),
    "CO2 Emissions": list(baseline["Breakdown"].values())
})
fig_pie = px.pie(pie_df, names="Source", values="CO2 Emissions",
                 title="Baseline CO₂ Breakdown", color_discrete_sequence=px.colors.qualitative.Set3)
st.plotly_chart(fig_pie, use_container_width=True)

# ---- 6️⃣ PDF Export ----
st.header("📄 Export Summary")
if st.button("Download PDF Summary"):
    generate_pdf(baseline, post_total, reduction, selected_actions)
    st.success("PDF saved as CO2_Summary.pdf in current folder.")
