Ushur CSV Validation

The purpose of this tool is to validate and process CSV files, ensuring that they follow a specific format and structure before being used in further processing or analysis.



Features

Validation of CSV files against a predefined set of rules.
Generation of a validation report in PDF format.
Generation of an error report in PDF format (if errors are found).




Requirements

Python 3.x
ReportLab library (for PDF generation)





Installation

-Clone the repository:

git clone https://github.com/BeepBoopImChris/DocumentVerfication

-Navigate to the project directory:

cd DocumentVerfication

-Install the required Python packages:

pip install -r requirements.txt





Usage


-Place the CSV files you want to validate inside the Validate folder.

-Run the csv_validation.py script:

python csv_validation.py



The script will validate each CSV file in the Validate folder and generate a report in the Results folder:


If all files are validated successfully, a validation_results.pdf file will be generated containing a summary of the validation process and the list of validated files.

If there are errors in any file, an error_report.pdf file will be generated containing a list of errors with their respective file names and row numbers.





Validators

The validation rules implemented are:

Check for the correct header row structure.
Validate the triggersend column values ('Yes' or 'No').
Ensure the ushurname value is consistent across all rows in a file.
Validate the sendPhoneNo column, ensuring it starts with '+1' and has the correct number of digits.
Validate the senddate column, ensuring it follows the format: MM/DD/YYYY hh:mm AM/PM.
Check for the uniqueness of the sendPrimaryKeyId column.
Validate the sendEmailId column, ensuring it has a valid email format.
