import os
from flask import Blueprint, render_template, request, session, redirect, flash, current_app as fapp
from app.views import user
from app import data_access

nav_bp = Blueprint('nav', __name__)

@nav_bp.route('/')
def index():
    try:
        fapp.logger.info('Index page accessed.')
        return render_template('index.html')
    except Exception as e:
        fapp.logger.error(f"Error loading the index page: {str(e)}")
        flash(f"Error loading the index page: {str(e)}", "danger")
        return redirect('/error')

@nav_bp.route('/login', methods=['POST'])
def login():
    try:
        username = request.form['username']
        password = request.form['password']
        if user.check_user_exists(username):
            if user.check_user_password(username, password):
                session['username'] = username
                session['password'] = password
                session['current_question_index'] = 0
                session['current_player_index'] = 0
                session['editor_set'] = ''
                session['game_set'] = ''
                fapp.logger.info(f"User '{session['username']}' started a new session.")
                return redirect('/menu')
        return redirect('/')
    except Exception as e:
        fapp.logger.error(f"Error processing check_user_* : {str(e)}")
        flash(f"Error processing menu request: {str(e)}", "danger")
        return redirect('/')

@nav_bp.route('/menu')
def show_menu_page():
    try:
        username = session.get('username', None)
        fapp.logger.info(f"Menu page accessed by user: {username}")
        return render_template('menu.html', username=username)
    except Exception as e:
        fapp.logger.error(f"Error loading the menu page: {str(e)}")
        flash(f"Error loading the menu page: {str(e)}", "danger")
        return redirect('/')

@nav_bp.route('/editor_select')
def editor_select():
    try:
        QuestionsFolder = data_access.get_questions_folder()
        userfiles = os.listdir(QuestionsFolder)
        return render_template('editor_select.html', userfiles=userfiles)
    except Exception as e:
        fapp.logger.error(f"Error accessing questions folder: {str(e)}")
        flash(f"Error accessing questions folder: {str(e)}", "danger")
        return redirect('/')
