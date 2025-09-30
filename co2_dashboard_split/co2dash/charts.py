
import pandas as pd
import plotly.express as px

def fig_before_after(baseline_total, post_total):
    df = pd.DataFrame({
        "Scenario": ["Before 🔴", "After 🟢"],
        "CO2 Emissions (tons)": [baseline_total, post_total]
    })
    return px.bar(df, x="Scenario", y="CO2 Emissions (tons)", text="CO2 Emissions (tons)")

def fig_breakdown(breakdown_dict, title):
    df = pd.DataFrame({"Source": list(breakdown_dict.keys()),
                       "CO2 Emissions": list(breakdown_dict.values())})
    return px.pie(df, names="Source", values="CO2 Emissions", title=title)

def fig_sensitivity(sweep_vals, totals):
    import plotly.express as px
    import pandas as pd
    df = pd.DataFrame({"Change (%)": sweep_vals, "Total CO2 (tons)": totals})
    fig = px.line(df, x="Change (%)", y="Total CO2 (tons)")
    fig.update_traces(mode="lines+markers")
    return fig
