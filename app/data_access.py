import os
from flask import Blueprint, current_app, flash, jsonify, render_template, request, redirect, session, url_for

data_access_bp = Blueprint('data_access', __name__)

def check_for_question_folder(): 
    QuestionsFolder = get_questions_folder()
    try:
        if os.path.exists(QuestionsFolder):
            current_app.logger.info(f"Directory {QuestionsFolder} was found")
            return True
        else:
            current_app.logger.info(f"Directory {QuestionsFolder} was not found and has to be created")
            return create_question_folder()
    except Exception as e:
        current_app.logger.error(f"Error checking directory {QuestionsFolder}: {str(e)}")
        return False

def create_question_folder():
    QuestionsFolder = get_questions_folder()
    try:
        os.makedirs(QuestionsFolder)
        current_app.logger.info(f"Directory created: {QuestionsFolder}")
        return True
    except Exception as e:
        current_app.logger.error(f"Error creating directory {QuestionsFolder}: {str(e)}")
        return False
    
def get_questions_folder():
    try:
        # Retrieve username from session
        username = session.get('username')

        # Check if username is available in the session
        if not username:
            current_app.logger.error("Username not found in session.")
            raise ValueError("Username is not set in the session.")

        # Construct the path using username
        questions_folder = os.path.join('data', 'questions', username)
        
        # Log the folder being accessed
        current_app.logger.info(f"Questions folder path generated: {questions_folder}")

        return questions_folder

    except Exception as e:
        # Log any error that occurs
        current_app.logger.error(f"Error in get_questions_folder: {str(e)}")
        # Optionally, you could re-raise the exception or handle it as needed
        raise e

def get_files_list():
    try:
        # Get the directory path from data_access
        directory = get_questions_folder()

        # Log the directory being accessed
        current_app.logger.info(f"Accessing directory: {directory}")

        # List to store file names
        files_list = []

        # Check if the directory exists
        if os.path.isdir(directory):
            # Loop through the directory and append files to the list
            for file_name in os.listdir(directory):
                file_path = os.path.join(directory, file_name)
                # Check if it's a file (and not a directory or something else)
                if os.path.isfile(file_path):
                    files_list.append(file_name)
            current_app.logger.info(f"Found {len(files_list)} files in the directory.")
        else:
            # Log and raise an error if the directory does not exist
            current_app.logger.error(f"Directory {directory} does not exist.")
            raise FileNotFoundError(f"The directory {directory} does not exist.")

        return files_list

    except Exception as e:
        # Log any exception that occurs
        current_app.logger.error(f"An error occurred: {str(e)}")
        # Raise the error again if necessary or return a blank list
        return []