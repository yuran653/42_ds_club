import requests
from pprint import pprint
import json
from tqdm import tqdm
import time
import click

RANDOMUSER_API_URL = "https://randomuser.me/api/"



def parse_json(user_json: dict) -> dict:
    # Extract ID
    id = user_json["results"][0]["id"]["name"] + " " + str(user_json["results"][0]["id"]["value"])
    
    # Extract name details
    first_name = user_json["results"][0]["name"]["first"]
    last_name = user_json["results"][0]["name"]["last"]
    
    # Extract location details
    location_city = user_json["results"][0]["location"]["city"]
    location_country = user_json["results"][0]["location"]["country"]
    location_latitude = user_json["results"][0]["location"]["coordinates"]["latitude"]
    location_longitude = user_json["results"][0]["location"]["coordinates"]["longitude"]
    location_postcode = user_json["results"][0]["location"]["postcode"]
    location_state = user_json["results"][0]["location"]["state"]
    location_street_info = f"{user_json['results'][0]['location']['street']['name']}, {user_json['results'][0]['location']['street']['number']}"
    
    # Extract other fields
    email = user_json["results"][0].get("email")
    gender = user_json["results"][0].get("gender")
    
    # Extract login details
    login_uuid = user_json["results"][0]["login"].get("uuid")
    login_username = user_json["results"][0]["login"].get("username")
    login_password = user_json["results"][0]["login"].get("password")
    
    # Extract contact details
    phone = user_json["results"][0].get("phone")
    cell = user_json["results"][0].get("cell")
    
    # Extract date of birth and registration details
    date_of_birth = user_json["results"][0]["dob"].get("date")
    age = user_json["results"][0]["dob"].get("age")
    date_of_registration = user_json["results"][0]["registered"].get("date")
    
    # Extract picture link
    photo_link = user_json["results"][0]["picture"].get("large")
    
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
        "photo_link": photo_link
    }



def fetch_user_from_api(url : str):
    
    r = requests.get(url=url)
    user_json = r.json()
    
    parsed_user = parse_json(user_json)
    
    return parsed_user


def load_batch_data(result_path : str, n_users : int):
    
    print(f"Collecting data from {RANDOMUSER_API_URL}; n_users = {n_users}")
    
    users = []
    
    for i in tqdm(range(n_users), desc="Fetching users from API..."):
        
        user = fetch_user_from_api(url=RANDOMUSER_API_URL)
        users.append(user)
        
    
    #save users to file
    batch_data = {"n_users" : n_users,
                  "users" : users}
    
    print("Saving users to file ", result_path)
    with open(result_path, "w") as file:
        json.dump(batch_data, file, indent=2, ensure_ascii=False)
        
        
    print("JOB DONE")



@click.command()
@click.option('--result_path', type=str, help='Path to save loaded batch of users')
@click.option('--n_users', type=int, help='How many users to fetch from API')
def load_batch_cli(result_path: str, n_users: int):
    
    load_batch_data(result_path=result_path,
                    n_users=n_users)
    

load_batch_cli()

#How to use
#python3 extract.py --result_path batch100users.json --n_users 100
#python3 extract.py --result_path batch15users.json --n_users 15
