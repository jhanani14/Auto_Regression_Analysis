from fpdf import FPDF

def generate_pdf(coef, intercept, r2, model_type, filename="report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # ❌ Removed emojis to avoid encoding errors
    pdf.cell(200, 10, txt="Regression Report", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Model: {model_type}", ln=True)
    pdf.cell(200, 10, txt=f"Intercept: {intercept:.3f}", ln=True)
    pdf.cell(200, 10, txt=f"R² Score: {r2:.3f}", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, txt="Coefficients:", ln=True)
    for col, val in coef.items():
        pdf.cell(200, 10, txt=f"{col}: {val:.4f}", ln=True)

    pdf.output(filename)
    return filename
