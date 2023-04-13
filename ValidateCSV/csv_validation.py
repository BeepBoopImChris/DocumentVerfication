import csv
import os
import glob
from pdf_generation import generate_pdf, generate_error_pdf
from validators import (
    check_headers,
    check_triggersend,
    check_ushurname,
    check_sendPhoneNo,
    check_senddate,
    check_sendPrimaryKeyID,
    check_sendEmailID,
)

def validate_csv(file_path, results):
    print(f"Validating file: {file_path}")
    
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header_row = next(reader)
        
        if not check_headers(header_row):
            print(f"Error in {file_path}: Missing or incorrect headers")
            return
        
        unique_ids = set()
        ushurname_value = None
        errors = []
        
        for row_num, row in enumerate(reader, start=1):
            if not check_triggersend(row[0]):
                errors.append(f"Error in {file_path} row {row_num}: Invalid triggersend")
            else:
                results["triggersend"][row[0]] += 1
                
            if ushurname_value is None:
                ushurname_value = row[1]
                results["ushurname"] = ushurname_value
            elif not check_ushurname(row[1], ushurname_value):
                errors.append(f"Error in {file_path} row {row_num}: Invalid ushurname")
                
            if not check_sendPhoneNo(row[2]):
                errors.append(f"Error in {file_path} row {row_num}: Invalid sendPhoneNo")
                
            if not check_senddate(row[3]):
                errors.append(f"Error in {file_path} row {row_num}: Invalid senddate")
                
            if not check_sendPrimaryKeyID(row[4], unique_ids):
                errors.append(f"Error in {file_path} row {row_num}: Duplicate sendPrimaryKeyID")
                
            if not check_sendEmailID(row[5]):
                errors.append(f"Error in {file_path} row {row_num}: Invalid sendEmailID")
                
    if errors:
        for error in errors:
            print(error)
        return 0, errors
    else:
        print(f"File {file_path} is ready to go")
        return row_num, []

validate_folder = 'Validate'
os.makedirs(validate_folder, exist_ok=True)

csv_files = glob.glob(f"{validate_folder}/*.csv")

if not csv_files:
    print("No CSV files found in the 'Validate' folder.")
else:
    results = {
        "triggersend": {"Yes": 0, "No": 0},
        "ushurname": None,
        "sendPhoneNo": "Format Validated",
        "senddate": "Format Validated",
        "sendPrimaryKeyId": "Format Validated",
        "sendEmailId": "Format Validated",
    }
    validated_files = []
    all_errors = []
    

    total_rows = 0
    for file_path in csv_files:
        row_count, file_errors = validate_csv(file_path, results)
        if row_count:
            validated_files.append(file_path)
            total_rows += row_count
        if file_errors:
            all_errors.extend(file_errors)

    if all_errors:
        generate_error_pdf(all_errors)
        print("Error report saved to the 'Results' folder.")
    else:
        if validated_files:
            generate_pdf(results, validated_files, total_rows)
            print("PDF report saved to the 'Results' folder.")