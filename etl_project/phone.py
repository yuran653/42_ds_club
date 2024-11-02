import json
import phonenumbers # https://github.com/daviddrysdale/python-phonenumbers
from tqdm import tqdm

input_file = 'country_batch15users.json'

with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

def convert_alpha(phone_number):
    letters_to_digit = {
        'A': '2', 'B': '2', 'C': '2',
        'D': '3', 'E': '3', 'F': '3',
        'G': '4', 'H': '4', 'I': '4',
        'J': '5', 'K': '5', 'L': '5',
        'M': '6', 'N': '6', 'O': '6',
        'P': '7', 'Q': '7', 'R': '7', 'S': '7',
        'T': '8', 'U': '8', 'V': '8',
        'W': '9', 'X': '9', 'Y': '9', 'Z': '9'
    }
    return ''.join(letters_to_digit.get(c, c) for c in phone_number.upper()
                   if letters_to_digit.get(c, c).isdigit())

# Function to clean and normalize phone numbers
def normalize_phone_number(phone_number, country_code):
    # Convert alphanumeric parts to digits
    phone_numbers = convert_alpha(phone_number)

    try:
        # Parse and validate number with the provided Alpha-2 country code
        parsed_number = phonenumbers.parse(phone_numbers, country_code)
        if phonenumbers.is_valid_number(parsed_number):
            normalized = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
            return normalized
        else:
            print(f"Invalid number for country code {country_code}: {phone_numbers}")
    except phonenumbers.NumberParseException as e:
        print(f"Failed to parse with country code {country_code}: {e}")

    return phone_number

# Process each user to normalize phone and cell numbers
for user in tqdm(data['users'], desc='Processing and verifying phones and cells'):
    country_code = user.get('location_country')
    user['phone'] = normalize_phone_number(user.get('phone', ''), country_code)
    user['cell'] = normalize_phone_number(user.get('cell', ''), country_code)

# Print all normalized phone and cell values, including country code
for user in data['users']:
    if not user['phone'].startswith('+') or not user['cell'].startswith('+'):
        print(f"Name: {user['firstname']} {user['lastname']}, Country: {user['location_country']}, Phone: {user['phone']}, Cell: {user['cell']}")
