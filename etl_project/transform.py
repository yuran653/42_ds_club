import pandas as pd
from tqdm import tqdm
import country_converter
import phonenumbers as ph
from phonenumbers.phonenumberutil import NumberParseException
from datetime import datetime
import json
import click

# Define a function to load user data from a JSON file into a DataFrame
def load_batch_to_df(path : str):
    with open(path, 'r') as file:
        # Load JSON data from file
        batch_json = json.load(file)
    # Convert user data to DataFrame
    df = pd.DataFrame(batch_json['users'])
    return df

# Define a function to convert a country name to ISO2 code
def convert_country_code(country_name: str) -> str:
    # Convert country name to ISO2 code
    iso_code = country_converter.convert(country_name, to='ISO2')
    return iso_code

# Define a function to convert alpha characters to their corresponding digits
def convert_alpha(phone_number : str) -> str:
    # Mapping of alpha characters to their respective digits on a phone keypad
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
    # Skips any character that is not a number or in the map
    # Convert the character to its corresponding digit if it is in the map
    return ''.join(letters_to_digit.get(c, c) for c in phone_number.upper()
                   if letters_to_digit.get(c, c).isdigit())

# Define a function to normalize a phone number
def normalize_number(number: str, cc_iso2: str) -> str:
    try:
        # Parse the phone number after converting alphabetic characters using the ISO2 code
        number_obj = ph.parse(convert_alpha(number), region=cc_iso2)
    except NumberParseException as e:
        return 'number_not_parsed'
    # Check if the parsed number is valid
    if not ph.is_valid_number(number_obj):
        return 'number_not_valid'
    # Format the valid number to E.164 format
    normalized = ph.format_number(number_obj, ph.PhoneNumberFormat.E164)
    return normalized

# Define a function to transform the batch data in a DataFrame
def transform_data_batch(df : pd.DataFrame):
    
    # Convert latitude and longitude to float for accurate geographic data
    df['location_longitude'] = df['location_longitude'].astype(float)
    df['location_latitude'] = df['location_latitude'].astype(float)
    
    # Convert country names to ISO2 country codes
    tqdm.pandas(desc='Converting country names to ISO2 country codes')
    df['country_iso2'] = df['location_country'].progress_apply(convert_country_code)
    # df['country_iso2'] = df['location_country'].apply(convert_country_code)
    
    # Normalize phone and cell numbers by applying the country ISO2 code
    tqdm.pandas(desc='Normalizing phone numbers by applying the country ISO2 code')
    df['normalized_phone'] = df.progress_apply(lambda row: normalize_number(row['phone'], row['country_iso2']), axis=1)
    tqdm.pandas(desc='Normalizing cell numbers by applying the country ISO2 code')
    df['normalized_cell'] = df.progress_apply(lambda row: normalize_number(row['cell'], row['country_iso2']), axis=1)
    # df['normalized_phone'] = df.apply(lambda row: normalize_number(row['phone'], row['country_iso2']), axis=1)
    # df['normalized_cell'] = df.apply(lambda row: normalize_number(row['cell'], row['country_iso2']), axis=1)
    
    # Convert date fields to datetime objects for accurate date manipulations
    tqdm.pandas(desc="Convert 'date_of_registration' fields to datetime objects")
    df['date_of_registration'] = df['date_of_registration'].progress_apply(pd.to_datetime)
    tqdm.pandas(desc="Convert 'date_of_birth' fields to datetime objects")
    df['date_of_birth'] = df['date_of_birth'].progress_apply(pd.to_datetime)
    tqdm.pandas(desc="Convert 'extract_time' fields to datetime objects")
    df['extract_time'] = df['extract_time'].progress_apply(pd.to_datetime)
    # df['date_of_registration'] = pd.to_datetime(df['date_of_registration'])
    # df['date_of_birth'] = pd.to_datetime(df['date_of_birth'])
    # df['extract_time'] = pd.to_datetime(df['extract_time'])

    # Extract year, month, and day from registration date for analysis
    df['year_of_registration'] = df['date_of_registration'].dt.year
    df['month_of_registration'] = df['date_of_registration'].dt.month
    df['day_of_registration'] = df['date_of_registration'].dt.day

    # Standardize gender values to 'M' and 'F'
    df['gender'] = df['gender'].replace({'male' : 'M', 'female' : 'F'})

    # Calculate and store lengths of login password and username fields
    tqdm.pandas(desc='Calculate lengths of login fields')
    df['password_length'] = df['login_password'].progress_apply(len)
    tqdm.pandas(desc='Calculate lengths of password fields')
    df['login_length'] = df['login_username'].progress_apply(len)
    # df['password_length'] = df['login_password'].apply(len)
    # df['login_length'] = df['login_username'].apply(len)

    # Record the timestamp for the transformation process
    df['transform_timestamp'] = datetime.now()
    
    return df

# Define command-line interface for transforming batch data
@click.command()
@click.option('--batch_path', type=str, help='Path to saved json batch')
@click.option('--result_path', type=str, help='Path to save transformed data (CSV)')
def transform_step(batch_path, result_path):
    # Load batch data from JSON file into DataFrame
    df  = load_batch_to_df(batch_path)
    # Transform the loaded data
    transformed_df = transform_data_batch(df)
    # Save the transformed data to a CSV file at the specified path
    transformed_df.to_csv(result_path)

# Run the CLI command when this script is executed
transform_step()

# How to Use
# python3 transform.py --batch_path batch15users.json --result_path batch15users.csv
# python3 transform.py --batch_path batch100users.json --result_path batch100users.csv
# python3 transform.py --batch_path batch1000users.json --result_path batch1000users.csv
