import requests
import json

file_path = r"./utils/rpc.json"

def read_variable_json(variable_name: str):
    """
    Helper function that will return the value of the given variable name.
    """
    global file_path
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            if variable_name in data:
                return data[variable_name]
    except Exception as e:
        print(f"Error while trying to read the rpc.json: {e}")

def edit_variable_json(variable_name: str, new_value):
    """
    Helper function that will edit the value of the given variable name to the given value.
    """
    global file_path
    with open(file_path, "r") as file:
        data = json.load(file)
    
    if variable_name in data:
        data[variable_name] = new_value
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

def get_raw_json(repo_owner: str, repo_name: str, file_path: str):
    """
    Helper function to get assets url from the `assets.json` of the repository.
    Returns None if GitHub is unreachable (graceful fallback).
    """
    try:
        url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/{file_path}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch {file_path} from GitHub (Status {response.status_code}). Using fallback.")
            return None
    except Exception as e:
        print(f"Warning: Could not reach GitHub ({e}). Using local fallback.")
        return None
