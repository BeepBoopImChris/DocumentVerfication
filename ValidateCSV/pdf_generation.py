from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import csv
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, TableStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.platypus import ListFlowable, ListItem
from reportlab.platypus import PageBreak
import os

def generate_pdf(results, validated_files, total_rows):
    os.makedirs("Results", exist_ok=True)
    pdf_file = "Results/validation_results.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)

    elements = []
    styles = getSampleStyleSheet()

    styles['Title'].fontName = 'Helvetica-Bold'
    styles['Title'].fontSize = 24
    styles['Heading1'].fontName = 'Helvetica-Bold'
    styles['Heading1'].fontSize = 18
    styles['Heading2'].fontName = 'Helvetica-Bold'
    styles['Heading2'].fontSize = 14
    styles['Normal'].fontName = 'Helvetica'
    styles['Normal'].fontSize = 12

    elements.append(Paragraph("CSV Validation Results", styles['Title']))
    elements.append(Spacer(1, 24))

    elements.append(Paragraph("Results Summary", styles['Heading1']))
    elements.append(Spacer(1, 12))

    data = [['Key', 'Value']]
    for key, value in results.items():
        if key == "triggersend":
            text = f"Yes: {value['Yes']}, No: {value['No']}"
        elif key == "ushurname":
            text = value
        else:
            text = "Format Validated"
        data.append([key, text])

    summary_table = Table(data)
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(summary_table)
    elements.append(Spacer(1, 24))

    elements.append(Paragraph(f"<b>Total Rows:</b> {total_rows}", styles['Normal']))
    elements.append(Spacer(1, 24))

    elements.append(Paragraph("Validated Files", styles['Heading1']))
    elements.append(Spacer(1, 12))

    file_list = ListFlowable(
        [ListItem(Paragraph(file_name, styles['Normal'])) for file_name in validated_files],
        bulletType='bullet',
        start='circle',
        leftIndent=20
    )
    elements.append(file_list)
    elements.append(Spacer(1, 24))

    ushurname = results["ushurname"]

    if validated_files:
        with open(validated_files[0], 'r') as csvfile:
            reader = csv.reader(csvfile)
            header_row = next(reader)
            first_data_row = next(reader)
            senddate_index = header_row.index('senddate')
            senddate = first_data_row[senddate_index]
    else:
        senddate = "N/A"

    elements.append(Paragraph(f"<i>Dropping this CSV file will trigger {total_rows} campaigns on the workflow {ushurname} at {senddate}.</i>", styles['Normal']))

    doc.build(elements)

def generate_error_pdf(errors):
    os.makedirs("Results", exist_ok=True)
    pdf_file = "Results/error_report.pdf"
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)

    elements = []
    styles = getSampleStyleSheet()

    styles['Title'].fontName = 'Helvetica-Bold'
    styles['Title'].fontSize = 24
    styles['Heading1'].fontName = 'Helvetica-Bold'
    styles['Heading1'].fontSize = 18
    styles['Heading2'].fontName = 'Helvetica-Bold'
    styles['Heading2'].fontSize = 14
    styles['Normal'].fontName = 'Helvetica'
    styles['Normal'].fontSize = 12

    elements.append(Paragraph("NOT VALID", styles['Title']))
    elements.append(Spacer(1, 12))

    current_file = ""
    error_table_data = []

    for error in errors:
        error_dict = error
        file_name = error_dict["file"]
        row_num = error_dict["row"]
        error_message = error_dict["error"]

        if current_file != file_name:
            if current_file and error_table_data:
                t = Table(error_table_data, hAlign='LEFT', colWidths=[50, 400])
                t.setStyle(TableStyle([
                    ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                    ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.beige]),
                ]))
                elements.append(t)
                elements.append(Spacer(1, 12))
                elements.append(PageBreak())  # Add this line
                error_table_data = []

            current_file = file_name
            elements.append(Paragraph(file_name, styles['Heading2']))
            elements.append(Spacer(1, 12))
            error_table_data.append(["Row", "Error"])

        error_table_data.append([row_num, error_message])

    if error_table_data:
        t = Table(error_table_data, hAlign='LEFT', colWidths=[50, 400])
        t.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.beige]),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 12))

    doc.build(elements)



if __name__ == "__main__":
    from csv_validation import results, validated_files, total_rows, errors, fixes
    if validated_files:
        generate_pdf(results, validated_files, total_rows)
        print("PDF report saved to the 'Results' folder.")
    if errors:
        generate_error_pdf(errors)
        print("Error report saved to the 'Results' folder.")
