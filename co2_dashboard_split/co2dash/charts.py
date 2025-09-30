
import pandas as pd
import plotly.express as px
SAFE_SEQ = px.colors.qualitative.Safe

def fig_before_after(baseline_total, post_total):
    df = pd.DataFrame({
        "Scenario": ["Before 🔴", "After 🟢"],
        "CO2 Emissions (tons)": [baseline_total, post_total]
    })
    fig = px.bar(df, x="Scenario", y="CO2 Emissions (tons)", text="CO2 Emissions (tons)")
    fig.update_traces(hovertemplate="<b>%{x}</b><br>Total: %{y:.1f} t CO₂<extra></extra>")
    return fig

def fig_breakdown(breakdown_dict, title):
    df = pd.DataFrame({"Source": list(breakdown_dict.keys()),
                       "CO2 Emissions": list(breakdown_dict.values())})
    fig = px.pie(df, names="Source", values="CO2 Emissions", title=title, color_discrete_sequence=SAFE_SEQ)
    fig.update_traces(hovertemplate="%{label}: %{value:.1f} t CO₂ (%{percent})<extra></extra>")
    return fig

def fig_sensitivity(sweep_vals, totals):
    df = pd.DataFrame({"Change (%)": sweep_vals, "Total CO2 (tons)": totals})
    fig = px.line(df, x="Change (%)", y="Total CO2 (tons)")
    fig.update_traces(mode="lines+markers", hovertemplate="Δ Electricity: %{x}%<br>Total: %{y:.1f} t CO₂<extra></extra>")
    return fig
