import requests
import json
from tqdm import tqdm
from datetime import datetime
import click

# Define the API URL to fetch random user data
RANDOMUSER_API_URL = "https://randomuser.me/api/"

# Function that parses the JSON data and extracts relevant fields
def parse_json(user_json: dict) -> dict:
    # Extract user ID by combining name and ID value
    id = user_json["results"][0]["id"]["name"] + " " + str(user_json["results"][0]["id"]["value"])
    
    # Extract user's first and last name
    first_name = user_json["results"][0]["name"]["first"]
    last_name = user_json["results"][0]["name"]["last"]
    
    # Extract user's location details
    location_city = user_json["results"][0]["location"]["city"]
    location_country = user_json["results"][0]["location"]["country"]
    location_latitude = user_json["results"][0]["location"]["coordinates"]["latitude"]
    location_longitude = user_json["results"][0]["location"]["coordinates"]["longitude"]
    location_postcode = user_json["results"][0]["location"]["postcode"]
    location_state = user_json["results"][0]["location"]["state"]
    location_street_info = f"{user_json['results'][0]['location']['street']['name']}, {user_json['results'][0]['location']['street']['number']}"
    
    # Extract other fields such as email and gender
    email = user_json["results"][0].get("email")
    gender = user_json["results"][0].get("gender")
    
    # Extract user's login details including UUID, username, and password
    login_uuid = user_json["results"][0]["login"].get("uuid")
    login_username = user_json["results"][0]["login"].get("username")
    login_password = user_json["results"][0]["login"].get("password")
    
    # Extract user's phone and cell numbers
    phone = user_json["results"][0].get("phone")
    cell = user_json["results"][0].get("cell")
    
    # Extract user's date of birth and registration details
    date_of_birth = user_json["results"][0]["dob"].get("date")
    age = user_json["results"][0]["dob"].get("age")
    date_of_registration = user_json["results"][0]["registered"].get("date")
    
    # Extract the link to the user's profile picture
    photo_link = user_json["results"][0]["picture"].get("large")
    
    # Capture the date and time of data extraction
    extract_time = str(datetime.now())
    
    return {
        "id": id,
        "firstname": first_name,
        "lastname": last_name,
        "location_city": location_city,
        "location_country": location_country,
        "location_state": location_state,
        "location_latitude": location_latitude,
        "location_longitude": location_longitude,
        "location_postcode": location_postcode,
        "location_street_info": location_street_info,
        "email": email,
        "gender": gender,
        "login_uuid": login_uuid,
        "login_username": login_username,
        "login_password": login_password,
        "phone": phone,
        "cell": cell,
        "date_of_birth": date_of_birth,
        "age": age,
        "date_of_registration": date_of_registration,
        "photo_link": photo_link,
        "extract_time" : extract_time
    }

# Define function to fetch user data from the API
def fetch_user_from_api(url: str):
    # Send GET request to the specified URL
    r = requests.get(url=url)
    # Parse the response as JSON
    user_json = r.json()
    # Process the JSON data into a structured format
    parsed_user = parse_json(user_json)
    # Return the parsed user data
    return parsed_user

# Define function to load batch user data from the API and save to file
def load_batch_data(result_path: str, n_users: int):
    #Print start info
    print(f"Collecting data from {RANDOMUSER_API_URL}; n_users = {n_users}")
    # Initialize empty list to store user data
    users = []
    # Loop to fetch specified number of users, with progress bar display
    for _ in tqdm(range(n_users), desc="Fetching users from API..."):
        # Fetch individual user data from API and append to users list
        user = fetch_user_from_api(url=RANDOMUSER_API_URL)
        users.append(user)
    # Save the collected user data to a JSON file
    batch_data = {"n_users": n_users, "users": users}

    print("Saving users to file ", result_path)
    with open(result_path, "w") as file:
        json.dump(batch_data, file, indent=2, ensure_ascii=False)

    # Confirm job completion
    print("JOB IS DONE")

# Define command-line interface for loading batch user data
@click.command()
@click.option('--result_path', type=str, help='Path to save loaded batch of users')
@click.option('--n_users', type=int, help='How many users to fetch from API')
def load_batch_cli(result_path: str, n_users: int):
    # Call the function to load batch data with provided CLI arguments
    load_batch_data(result_path=result_path, n_users=n_users)

# Run the CLI command when this script is executed
load_batch_cli()

# How to use
# python3 extract.py --result_path batch15users.json --n_users 15
# python3 extract.py --result_path batch100users.json --n_users 100
# python3 extract.py --result_path batch1000users.json --n_users 1000
