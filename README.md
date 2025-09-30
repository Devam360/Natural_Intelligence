SME CO₂ Emission Reduction Dashboard

This is a web-based tool designed to help small and medium-sized steel manufacturers estimate and reduce their carbon dioxide (CO₂) emissions. It allows you to enter your plant data, simulate reduction actions, compare multiple plants, and export a PDF summary.

Features:

1. Input your steel production, coal and electricity use, and scrap percentage.

2. Estimate your baseline CO₂ emissions using standard or custom emission factors.

3. Simulate different emission reduction actions and see the potential savings.

4. Get automatic suggestions based on your emission profile.

5. Run sensitivity analysis to see how input changes affect total CO₂.

6. Compare multiple plants side by side.

7. Export a branded summary PDF with charts.

How to Use:

1. Select Language - 
Choose between English or Hindi from the sidebar.

2. Enter Plant Data - 
Input your plant’s monthly production, coal consumption, electricity usage, and scrap percentage.

3. Adjust Emission Factors (Optional) - 
If you have more accurate emission data, you can override the default coal, electricity, and process emission factors.

4. View Baseline Emissions - 
The app calculates and displays your annual CO₂ emissions and shows the breakdown by source.

5. Choose Recommended Actions - 
Tick the actions you plan to implement, such as improving efficiency or using more scrap. The app shows the new CO₂ emissions after applying these changes.

6. Understand Recommendations - 
Based on your baseline emissions, the app provides automatic insights on which sources dominate your emissions and where you should focus.

7. Test Sensitivity - 
Adjust sliders to simulate changes in inputs (e.g. +10% electricity or -5% coal) and see how it affects emissions.

8. Compare Plants - 
You can add and save multiple plants to compare their emissions before and after actions.

9. Export Report - 
Upload your company logo (optional), and download a PDF summary of your data, actions, and emissions profile.

Requirements:

- Python 3.8+

- Streamlit

- pandas, numpy, plotly, pillow, kaleido, fpdf

Install requirements:
- pip install -r requirements.txt

Run the app:

- streamlit run app.py

Notes:

- No internet connection is required once set up.

- All data remains on your device.

- Designed to support both English and Hindi interfaces.

- Works on desktop and mobile browsers.