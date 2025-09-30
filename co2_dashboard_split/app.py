
# streamlit run app.py
import streamlit as st
import numpy as np
import pandas as pd
from io import BytesIO
from PIL import Image

from co2dash.i18n import LANGS
from co2dash.regions import REGIONAL_GRID
from co2dash.emissions import calculate_emissions, apply_interventions
from co2dash.recommendations import make_recommendations
from co2dash.charts import fig_before_after, fig_breakdown, fig_sensitivity
from co2dash.pdf_export import export_pdf

st.set_page_config(page_title="🌱 SME CO₂ Dashboard", layout="wide")

# Language selector
lang = st.sidebar.selectbox("Language / भाषा", ["en", "hi"], index=0)
T = LANGS[lang]

st.title(T["title"])
st.caption(T["intro"])
st.sidebar.markdown(f"**{T['lang']}**: {lang.upper()}")

# Region selection for electricity factor
region = st.selectbox(T["region"], list(REGIONAL_GRID.keys()), index=0)
default_elec_factor = REGIONAL_GRID[region]

# Custom factors
with st.expander(T["override_factors"]):
    colf1, colf2, colf3 = st.columns(3)
    coal_factor = colf1.number_input(T["coal_factor"], min_value=0.0, value=2.5, step=0.1, help="tCO₂ per ton of coal")
    elec_factor = colf2.number_input(T["elec_factor"], min_value=0.0, value=float(default_elec_factor), step=0.00001, format="%.5f", help="tCO₂ per kWh")
    proc_factor = colf3.number_input(T["proc_factor"], min_value=0.0, value=1.8, step=0.1, help="tCO₂ per ton of steel")

factors = {"coal_factor": coal_factor, "electricity_factor": elec_factor, "process_factor": proc_factor}

# Plant inputs (number inputs instead of sliders)
st.header(T["plant_data"])
c1, c2 = st.columns(2)
with c1:
    production = st.number_input(T["prod"], min_value=0.0, value=500.0, step=1.0, help="Monthly tons of finished steel")
    coal = st.number_input(T["coal"], min_value=0.0, value=200.0, step=1.0, help="Monthly tons of coal")
with c2:
    electricity = st.number_input(T["elec"], min_value=0.0, value=100000.0, step=100.0, help="Monthly kWh")
    scrap_percent = st.number_input(T["scrap"], min_value=0.0, max_value=100.0, value=20.0, step=1.0, help="Percent of scrap in charge mix")

annual_production = production * 12
annual_coal = coal * 12
annual_electricity = electricity * 12

baseline = calculate_emissions(annual_production, annual_coal, annual_electricity, scrap_percent, factors)

# Actions
st.header(T["actions"])
actions_desc = {
    T["action_scrap"]: T["desc_scrap"],
    T["action_heat"]: T["desc_heat"],
    T["action_re"]: T["desc_re"],
    T["action_eff"]: T["desc_eff"],
}
flags = {"scrap":0,"heat":0,"re":0,"eff":0}
selected_actions = []
for lbl, desc in actions_desc.items():
    if st.checkbox(f"{lbl} — {desc}"):
        selected_actions.append(lbl)
        if lbl == T["action_scrap"]: flags["scrap"]=1
        if lbl == T["action_heat"]: flags["heat"]=1
        if lbl == T["action_re"]: flags["re"]=1
        if lbl == T["action_eff"]: flags["eff"]=1

post_total, reduction = apply_interventions(baseline["Total CO2 (tons)"], flags)

# Summary
st.header(T["summary"])
m1, m2, m3 = st.columns(3)
m1.metric(T["baseline"], f"{baseline['Total CO2 (tons)']:.1f}")
m2.metric(T["post"], f"{post_total:.1f}")
m3.metric(T["reduction"], f"{reduction:.1f}")

# Charts
st.subheader(T["charts"])
fig_bar = fig_before_after(baseline["Total CO2 (tons)"], post_total)
st.plotly_chart(fig_bar, use_container_width=True)

fig_pie = fig_breakdown(baseline["Breakdown"], T["breakdown"])
st.plotly_chart(fig_pie, use_container_width=True)

# Sensitivity Analysis (kept as sliders to explore dynamics quickly)
st.header(T["sensitivity"])
st.caption(T["sens_note"])
s1, s2, s3, s4 = st.columns(4)
d_prod = s1.slider(T["sens_prod"], -50, 50, 0)
d_coal = s2.slider(T["sens_coal"], -50, 50, 0)
d_elec = s3.slider(T["sens_elec"], -50, 50, 0)
d_scrap = s4.slider(T["sens_scrap"], -20, 20, 0)

sens_production = annual_production * (1 + d_prod/100)
sens_coal = annual_coal * (1 + d_coal/100)
sens_elec = annual_electricity * (1 + d_elec/100)
sens_scrap = min(max(scrap_percent + d_scrap, 0), 100)

sens_base = calculate_emissions(sens_production, sens_coal, sens_elec, sens_scrap, factors)
st.plotly_chart(
    fig_breakdown(sens_base["Breakdown"], f"{T['breakdown']} (Sensitivity)"),
    use_container_width=True
)

# Sweep electricity to show curve
sweep = np.arange(-50, 51, 5)
totals = []
for v in sweep:
    _elec = annual_electricity * (1 + v/100)
    totals.append(calculate_emissions(annual_production, annual_coal, _elec, scrap_percent, factors)["Total CO2 (tons)"])
st.plotly_chart(fig_sensitivity(sweep, totals), use_container_width=True)

# Smart Recommendations
st.header(T["smart_recs"])
for tip in make_recommendations(baseline["Breakdown"]):
    st.write("• " + tip)

# Multi-Plant Comparison (in-memory)
st.header(T["compare"])
if "plants" not in st.session_state:
    st.session_state.plants = {}

pc1, pc2, pc3 = st.columns([2,1,1])
with pc1:
    plant_name = st.text_input(T["plant_name"], "Plant A")
if pc2.button(T["add_plant"]):
    st.session_state.plants[plant_name] = {
        "Baseline": baseline["Total CO2 (tons)"],
        "Post": post_total
    }
if pc3.button(T["clear_plants"]):
    st.session_state.plants = {}

if st.session_state.plants:
    df_plants = pd.DataFrame(st.session_state.plants).T
    st.subheader(T["plants_table"])
    st.dataframe(df_plants, use_container_width=True)

    df_long = df_plants.reset_index().melt(id_vars="index", var_name="Scenario", value_name="tCO2")
    df_long.rename(columns={"index":"Plant"}, inplace=True)
    import plotly.express as px
    fig_cmp = px.bar(df_long, x="Plant", y="tCO2", color="Scenario", barmode="group", text="tCO2")
    st.plotly_chart(fig_cmp, use_container_width=True)

# Branded PDF Export with charts & logo
st.header(T["export"])
logo_file = st.file_uploader(T["logo"], type=["png","jpg","jpeg"])
logo_path = None
if logo_file:
    logo_img = Image.open(logo_file).convert("RGBA")
    tmp = BytesIO()
    logo_img.save(tmp, format="PNG")
    tmp.seek(0)
    logo_path = "company_logo.png"
    Image.open(tmp).save(logo_path)

if st.button(T["download_pdf"]):
    export_pdf(
        filename="CO2_Summary.pdf",
        baseline=baseline,
        post_total=post_total,
        reduction=reduction,
        selected_actions=selected_actions,
        logo_image=logo_path,
        fig1=fig_bar,
        fig2=fig_pie,
        lang_code=lang
    )
    st.success(T["saved_msg"])
