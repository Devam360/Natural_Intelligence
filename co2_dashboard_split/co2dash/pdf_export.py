
from fpdf import FPDF
from datetime import datetime
from io import BytesIO
from PIL import Image
from .i18n import LANGS
def export_pdf(filename_base, baseline, post_total, reduction, selected_actions, logo_image, fig1, fig2, lang_code):
    buf1 = BytesIO(); fig1.write_image(buf1, format="png", scale=2); buf1.seek(0)
    buf2 = BytesIO(); fig2.write_image(buf2, format="png", scale=2); buf2.seek(0)
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"{filename_base}_{ts}.pdf"
    img1 = Image.open(buf1); img1_path = "before_after.png"; img1.save(img1_path)
    img2 = Image.open(buf2); img2_path = "breakdown.png"; img2.save(img2_path)
    T = LANGS[lang_code]
    pdf = FPDF(); pdf.add_page()
    if logo_image is not None: pdf.image(logo_image, x=160, y=8, w=40)
    pdf.set_font("Arial", "B", 16); pdf.cell(0, 10, T["title"].encode('latin-1','ignore').decode('latin-1'), ln=True, align="C")
    pdf.set_font("Arial", "", 11); pdf.cell(0, 8, f"{T['pdf_generated']}: {ts.replace('_', ' ')}", ln=True); pdf.ln(4)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"{T['pdf_baseline']}: {baseline['Total CO2 (tons)']:.1f} t/yr", ln=True)
    pdf.cell(0, 8, f"{T['pdf_post']}: {post_total:.1f} t/yr", ln=True)
    pdf.cell(0, 8, f"{T['pdf_reduction']}: {reduction:.1f} t/yr", ln=True)
    pdf.ln(4)
    pdf.set_font("Arial", "B", 12); pdf.cell(0, 8, f"{T['pdf_selected_actions']}:", ln=True)
    pdf.set_font("Arial", "", 12)
    if selected_actions:
        for i, a in enumerate(selected_actions, 1):
            pdf.cell(0, 8, f"{i}. {a.encode('latin-1','ignore').decode('latin-1')}", ln=True)
    else:
        pdf.cell(0, 8, "None", ln=True)
    pdf.ln(6)
    pdf.set_font("Arial", "B", 12); pdf.cell(0, 8, f"{T['pdf_before_after']}:", ln=True)
    pdf.image(img1_path, x=10, y=None, w=180); pdf.ln(2)
    pdf.set_font("Arial", "B", 12); pdf.cell(0, 8, f"{T['pdf_baseline_breakdown']}:", ln=True)
    pdf.image(img2_path, x=10, y=None, w=180)
    pdf.output(filename)
    return filename
