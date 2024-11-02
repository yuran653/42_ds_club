import requests
from pprint import pprint
import json
from tqdm import tqdm
import time
import click

FOOTBALL_API_URL = "https://v3.football.api-sports.io/"



def parse_json(user_json: dict) -> dict:
    pass

def fetch_user_from_api(url : str):
    
    r = requests.get(url=url)
    user_json = r.json()
    
    parsed_user = parse_json(user_json)
    
    return parsed_user


def load_batch_data(result_path : str, n_users : int):
    
    print(f"Collecting data from {FOOTBALL_API_URL}")
    
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
