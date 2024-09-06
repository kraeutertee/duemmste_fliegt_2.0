import csv
import os
from flask import Blueprint, app, render_template, request, redirect, url_for

user_bp = Blueprint('user', __name__)

def check_user_exists(username): #if username in data/user.csv, return True else False
    try:
        with open(os.path.join('data', 'user.csv'), mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get('username') == username:
                    return True
        app.logger.error(f"user {username} was not found")
        return False
    except FileNotFoundError:
        app.logger.error(f"The file data/user.csv was not found.")
        return False
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return False
    
def check_user_password(username, password): #if user in data/user.csv has same hashed password as provided, return True else False
    try:
        with open(os.path.join('data', 'user.csv'), mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get('username') == username and row.get('password') == password:
                    return True
        app.logger.error(f"password for {username} was wrong")
        return False
    except FileNotFoundError:
        app.logger.error(f"The file data/user.csv was not found.")
        return False
    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return False