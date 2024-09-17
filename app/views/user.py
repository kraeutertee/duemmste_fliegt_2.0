import csv
import os
import bcrypt
from flask import Blueprint, current_app, render_template, request, session, redirect, flash, url_for

user_bp = Blueprint('user', __name__)

def check_user_exists(username): #if username in data/user.csv, return True else False
    try:
        with open(os.path.join('data', 'user.csv'), mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get('username') == username:
                    return True
        current_app.logger.error(f"user {username} was not found")
        return False
    except FileNotFoundError:
        current_app.logger.error(f"The file data/user.csv was not found.")
        return False
    except Exception as e:
        current_app.logger.error(f"An error occurred: {str(e)}")
        return False
    
# def check_user_password(username, password): #if user in data/user.csv has same hashed password as provided, return True else False

#     print('check_user_password() accessed')

#     try:
#         with open(os.path.join('data', 'user.csv'), mode='r', newline='') as file:
#             reader = csv.DictReader(file)
#             for row in reader:
#                 if row.get('username') == username and row.get('password') == password:
#                     return True
#         current_app.logger.error(f"password for {username} was wrong")
#         return False
#     except FileNotFoundError:
#         current_app.logger.error(f"The file data/user.csv was not found.")
#         return False
#     except Exception as e:
#         current_app.logger.error(f"An error occurred: {str(e)}")
#         return False
    
def check_user_password(username, password):
    with open('data/user.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            csv_username, csv_hashed_password = row
            if csv_username == username:
                # Verify the password using the stored hash (salt is part of the hash)
                if bcrypt.checkpw(password.encode('utf-8'), csv_hashed_password.encode('utf-8')):
                    return True
                else:
                    return False
    return False  # If username not found or password doesn't match
    
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')  # Store as a string

