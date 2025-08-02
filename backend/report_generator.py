from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def generate_pdf_report(results, reg_plot, residual_plot, filename):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("Regression Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"<b>{results['model_type'].capitalize()} Regression</b>", styles["Heading2"]))
    elements.append(Paragraph(f"R² Score: {results['r2']:.4f}", styles["Normal"]))
    elements.append(Paragraph(f"Intercept: {results['intercept']:.4f}", styles["Normal"]))
    elements.append(Paragraph(f"Y Column: {results['y_column']}", styles["Normal"]))
    elements.append(Paragraph(f"X Columns: {', '.join(results['x_columns'])}", styles["Normal"]))

    coef_str = "<br/>".join([f"{k}: {v:.4f}" for k, v in results['coef'].items()])
    elements.append(Paragraph("Coefficients:<br/>" + coef_str, styles["Normal"]))

    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Regression Plot", styles["Heading2"]))
    elements.append(Image(reg_plot, width=400, height=300))

    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Residual Plot", styles["Heading2"]))
    elements.append(Image(residual_plot, width=400, height=300))

    doc.build(elements)

    with open(filename, "wb") as f:
        f.write(buffer.getvalue())
