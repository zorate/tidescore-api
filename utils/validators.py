import re
from datetime import datetime

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email)) if email else False

def validate_phone(phone):
    """Validate Nigerian phone number format"""
    # Nigerian phone numbers: +234... or 0...
    pattern = r'^(\+234|0)[7-9][0-1]\d{8}$'
    return bool(re.match(pattern, phone)) if phone else False

def validate_bvn(bvn):
    """Validate Bank Verification Number (11 digits)"""
    return bvn.isdigit() and len(bvn) == 11 if bvn else False

def validate_dob(dob):
    """Validate date of birth (must be 18+ years)"""
    try:
        birth_date = datetime.strptime(dob, '%Y-%m-%d')
        age = (datetime.now() - birth_date).days // 365
        return age >= 18
    except (ValueError, TypeError):
        return False

def validate_amount(amount):
    """Validate monetary amount"""
    try:
        amount_float = float(amount)
        return amount_float >= 0
    except (ValueError, TypeError):
        return False
