import requests
import random
import string
from bs4 import BeautifulSoup

follow_url = "https://www.roblox.com/users/userID/profile"

def generate_username():
    # Generate a random username consisting of letters and numbers
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def generate_password():
    # Generate a random password consisting of letters, numbers, and symbols
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=12))

def create_account():
    # Create a new Roblox account with a random username and password
    username = generate_username()
    password = generate_password()

    register_url = "https://www.roblox.com/account/signupredir"
    session = requests.Session()
    register_page = session.get(register_url)
    soup = BeautifulSoup(register_page.text, 'html.parser')
    csrf_token = soup.find("input", {"name": "__RequestVerificationToken"})["value"]

    payload = {
        "__RequestVerificationToken": csrf_token,
        "username": username,
        "password": password,
        "birthday": "2005-01-01",
        "gender": "2",
        "email": "",
        "emailOptIn": "false",
        "birthYear": "2005",
        "captchaToken": "",
        "captchaProvider": "",
        "isTcAgreementBoxChecked": "true",
        "submitBtn": "Sign Up"
    }

    register_request = session.post(register_url, data=payload)

    if "Thanks for signing up" in register_request.text:
        return (username, password)
    else:
        return None

def follow_user(username, password, user_id):
    # Log in to the Roblox account and follow the specified user
    login_url = "https://www.roblox.com/login"
    session = requests.Session()
    login_page = session.get(login_url)
    soup = BeautifulSoup(login_page.text, 'html.parser')
    csrf_token = soup.find("input", {"name": "__RequestVerificationToken"})["value"]

    payload = {
        "__RequestVerificationToken": csrf_token,
        "username": username,
        "password": password
    }

    login_request = session.post(login_url, data=payload)

    follow_page = session.get(follow_url.replace("userID", user_id))
    soup = BeautifulSoup(follow_page.text, 'html.parser')
    csrf_token = soup.find("input", {"name": "__RequestVerificationToken"})["value"]

    payload = {
        "__RequestVerificationToken": csrf_token,
        "targetUserId": user_id,
        "actionType": "Follow"
    }

    follow_request = session.post(follow_url.replace("userID", user_id), data=payload)

    if "Unfollow" in follow_request.text:
        print("Successfully followed user with ID " + user_id + " using account " + username)
    else:
        print("Failed to follow user with ID " + user_id + " using account " + username)

# Main program
user_id = "youruseridhere" # Replace with the user ID of the user you want to follow
num_accounts = 5 # Set the number of accounts to create

for i in range(num_accounts):
    account = create_account()
    if account is not None:
        follow_user(account[0], account[1], user_id)
    else:
        print("Failed to create account")        
