import re
from datetime import datetime

def check_headers(header_row):
    """Check if the trigger header rows are present"""
    expected_headers = {
        'triggersend',
        'ushurname',
        'sendPhoneNo',
        'senddate',
        'sendPrimaryKeyId',
        'sendEmailId'
    }
    return expected_headers == set(header_row)

def check_triggersend(value):
    """Check if the triggersend value is either 'Yes' or 'No'."""
    return value in ('Yes', 'No')

def check_ushurname(value, previous_value):
    """Check if the ushurname value matches the previous value."""
    return value == previous_value

def check_sendPhoneNo(value):
    """Check if the phone number starts with '+1' and has the correct number of digits."""
    return re.match(r"^\+1\d{10}$", value) is not None

def check_senddate(value):
    """Check if the senddate value follows the format: MM/DD/YYYY hh:mm AM/PM."""
    try:
        datetime.strptime(value, "%m/%d/%Y %I:%M %p")
        return True
    except ValueError:
        return False

def check_sendPrimaryKeyID(value, unique_ids):
    """Check if the sendPrimaryKeyID value is unique."""
    if value not in unique_ids:
        unique_ids.add(value)
        return True
    return False

def check_sendEmailID(value):
    """Check if the sendEmailID value has a valid email format."""
    return re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", value) is not None
