#!/usr/bin/env python3

import requests
import getpass
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Fixed URLs
BASE_URL = "http://[ip]/dir"
LOGIN_URL = f"{BASE_URL}/lverify_new.php"
LOGOUT_URL = f"{BASE_URL}/logoffuser.php"

# Check argument
if len(sys.argv) != 2:
    print("Usage: python3 logoff.py <user_list.txt>")
    sys.exit(1)

input_file = sys.argv[1]
if not os.path.isfile(input_file):
    print(f"File not found: {input_file}")
    sys.exit(1)

# Prompt for credentials
username = input("Enter your username: ")
password = getpass.getpass("Enter your password: ")

# Start session
session = requests.Session()

def login():
    data = {
        "user": username,
        "pwd": password
    }
    try:
        response = session.post(LOGIN_URL, data=data, timeout=10)
        if "Login failed" in response.text:
            print("Login failed. Check credentials.")
            sys.exit(1)
        print("Login successful.")
    except Exception as e:
        print(f"Login request failed: {e}")
        sys.exit(1)

def logout_user(user):
    user = user.strip()
    if not user:
        return None

    data = {
        "u": user,
        "aa": "stl"
    }

    try:
        with session as s:
            response = s.post(LOGOUT_URL, data=data, timeout=10)
            if "SUCCESS" in response.text:
                return f"{user} - SUCCESS"
            else:
                return f"{user} - FAILED"
    except Exception as e:
        return f"{user} - ERROR: {e}"

def logout_users():
    with open(input_file, "r") as f:
        users = [line.strip() for line in f if line.strip()]

""" users = []

for line in f:
    stripped_line = line.strip()
    if stripped_line:
        users.append(stripped_line)
 """

    print(f"Logging out {len(users)} users...")

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(logout_user, user): user for user in users}
        for future in as_completed(futures):
            result = future.result()
            if result:
                print(result)

def main():
    login()
    logout_users()

if __name__ == "__main__":
    main()
