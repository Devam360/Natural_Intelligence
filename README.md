SME CO₂ Emission Reduction Dashboard

This is a web-based tool designed to help small and medium-sized steel manufacturers estimate and reduce their carbon dioxide (CO₂) emissions. It allows you to enter your plant data, simulate reduction actions, compare multiple plants, and export a PDF summary.

Features

Input your steel production, coal and electricity use, and scrap percentage.

Estimate your baseline CO₂ emissions using standard or custom emission factors.

Simulate different emission reduction actions and see the potential savings.

Get automatic suggestions based on your emission profile.

Run sensitivity analysis to see how input changes affect total CO₂.

Compare multiple plants side by side.

Export a branded summary PDF with charts.

How to Use

Select Language
Choose between English or Hindi from the sidebar.

Enter Plant Data
Input your plant’s monthly production, coal consumption, electricity usage, and scrap percentage.

Adjust Emission Factors (Optional)
If you have more accurate emission data, you can override the default coal, electricity, and process emission factors.

View Baseline Emissions
The app calculates and displays your annual CO₂ emissions and shows the breakdown by source.

Choose Recommended Actions
Tick the actions you plan to implement, such as improving efficiency or using more scrap. The app shows the new CO₂ emissions after applying these changes.

Understand Recommendations
Based on your baseline emissions, the app provides automatic insights on which sources dominate your emissions and where you should focus.

Test Sensitivity
Adjust sliders to simulate changes in inputs (e.g. +10% electricity or -5% coal) and see how it affects emissions.

Compare Plants
You can add and save multiple plants to compare their emissions before and after actions.

Export Report
Upload your company logo (optional), and download a PDF summary of your data, actions, and emissions profile.

Requirements

Python 3.8+

Streamlit

pandas, numpy, plotly, pillow, kaleido, fpdf

Install requirements:

pip install -r requirements.txt


Run the app:

streamlit run app.py

Notes

No internet connection is required once set up.

All data remains on your device.

Designed to support both English and Hindi interfaces.

Works on desktop and mobile browsers.