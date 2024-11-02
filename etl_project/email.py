import json
from email_validator import validate_email # https://github.com/JoshData/python-email-validator
from tqdm import tqdm

input_file = 'batch15users.json'
output_file = 'email_batch15users.json'

with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

def normalize_email(email):
    try:
        email_info = validate_email(email, check_deliverability=False)
        return email_info.normalized
    except EmailNotValidError as e:
        print(f"Invalid email '{email}'")
        return None
    
for user in tqdm(data['users'], desc='Processing and verifying emails'):
    user['email'] = user.get('email')
    
with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    
print('Emails validation is completed')

errors = sum(1 for user in data['users'] if user['email'] is None)
print(f'Invalid emails: {errors}')
