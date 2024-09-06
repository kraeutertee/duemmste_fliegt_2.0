import os
from flask import Blueprint, app, flash, render_template, request, redirect, session, url_for

data_access_bp = Blueprint('data_access', __name__)

def get_questions_folder():
    return os.path.join('data','questions', session.get('username'))

def check_for_question_folder(): 
    QuestionsFolder = get_questions_folder()
    try:
        if os.path.exists(QuestionsFolder):
            app.logger.info(f"Directory {QuestionsFolder} was found")
            return True
        else:
            app.logger.info(f"Directory {QuestionsFolder} was not found and has to be created")
            return create_question_folder()
    except Exception as e:
        app.logger.error(f"Error checking directory {QuestionsFolder}: {str(e)}")
        return False

def create_question_folder():
    QuestionsFolder = get_questions_folder()
    try:
        os.makedirs(QuestionsFolder)
        app.logger.info(f"Directory created: {QuestionsFolder}")
        return True
    except Exception as e:
        app.logger.error(f"Error creating directory {QuestionsFolder}: {str(e)}")
        return False