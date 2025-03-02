import requests

BASE_URL = "http://localhost:8000"

def health_check():
    response = requests.get(f"{BASE_URL}/health/")
    return response.json()

def create_user(name, email, password):
    try:
        response = requests.post(f"{BASE_URL}/users/", json={"name": name, "email": email, "password": password})
        return response.json()
    except Exception as ex:
        print(ex)


def get_user(user_id):
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    return response.json()


def login(email: str, password: str):
    response = requests.post(f"{BASE_URL}/auth/token/", json={"email": email, "password": password})
    return response.json()
