from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

def generate_pdf(results, validated_files, total_rows):
    os.makedirs("Results", exist_ok=True)
    pdf_file = "Results/validation_results.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    
    elements = []
    styles = getSampleStyleSheet()
    
    for key, value in results.items():
        if key == "triggersend":
            text = f"{key}: Yes: {value['Yes']}, No: {value['No']}"
        elif key == "ushurname":
            text = f"{key}: {value}"
        else:
            text = f"{key}: Format Validated"
        elements.append(Paragraph(text, styles['Normal']))
        elements.append(Spacer(1, 12))

    elements.append(Paragraph(f"Total Rows: {total_rows}", styles['Normal']))
    elements.append(Spacer(1, 12))
    
    elements.append(Paragraph("Validated Files:", styles['Heading2']))
    elements.append(Spacer(1, 12))
    
    for file_name in validated_files:
        elements.append(Paragraph(file_name, styles['Normal']))
        elements.append(Spacer(1, 12))
    
    doc.build(elements)

def generate_error_pdf(errors):
    os.makedirs("Results", exist_ok=True)
    pdf_file = "Results/error_report.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)

    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("NOT VALID", styles['Heading1']))
    elements.append(Spacer(1, 24))

    for error in errors:
        elements.append(Paragraph(error, styles['Normal']))
        elements.append(Spacer(1, 12))

    doc.build(elements)

if __name__ == "__main__":
    from csv_validation import results, validated_files, total_rows
    if validated_files:
        generate_pdf(results, validated_files, total_rows)
        print("PDF report saved to the 'Results' folder.")
