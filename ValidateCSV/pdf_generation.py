from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import ast
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
    elements.append(Paragraph("NOT VALID", styles['Title']))
    elements.append(Spacer(1, 12))

    current_file = ""
    for error in errors:
        error_dict = ast.literal_eval(error)
        file_name = error_dict["file"]
        row_num = error_dict["row"]
        error_message = error_dict["error"]

        if current_file != file_name:
            if current_file:
                elements.append(Table(error_table_data, hAlign='LEFT'))
                elements.append(Spacer(1, 12))
            current_file = file_name
            elements.append(Paragraph(file_name, styles['Heading2']))
            elements.append(Spacer(1, 12))
            error_table_data = [["Row", "Error"]]
        
        error_table_data.append([row_num, error_message])

    if current_file:
        error_table = Table(error_table_data, hAlign='LEFT')
        error_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(error_table)

    doc.build(elements)

if __name__ == "__main__":
    from csv_validation import results, validated_files, total_rows
    if validated_files:
        generate_pdf(results, validated_files, total_rows)
        print("PDF report saved to the 'Results' folder.")
