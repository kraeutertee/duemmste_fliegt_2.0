import os
from flask import Blueprint, render_template, request, session, redirect, flash, current_app
from app.views import game, user
from app import data_access

nav_bp = Blueprint('nav', __name__)

@nav_bp.route('/')
def show_index():
    try:
        current_app.logger.info('Index page accessed.')
        return render_template('index.html')
    except Exception as e:
        current_app.logger.error(f"Error loading the index page: {str(e)}")
        flash(f"Error loading the index page: {str(e)}", "danger")
        return redirect('/error')

@nav_bp.route('/login', methods=['POST'])
def login():
    try:
        username = request.form['username']
        password = request.form['password']

        print(username, password)

        session['username'] = username
        session['password'] = password
        session['current_question_index'] = 0
        session['current_player_index'] = 0
        session['editor_set'] = ''
        session['game_set'] = ''
        session['players'] = []

        return redirect('/menu')

        # if user.check_user_exists(username):
        #     print('user True')
        #     if user.check_user_password(username, password):
        #         print('pw True')
        #         session['username'] = username
        #         session['password'] = password
        #         session['current_question_index'] = 0
        #         session['current_player_index'] = 0
        #         session['editor_set'] = ''
        #         session['game_set'] = ''

        #         if 'username' in session:
        #             current_app.logger.info(f"User '{session['username']}' started a new session.")
        #         else:
        #             current_app.logger.warning("Session username is not set.")

        #         current_app.logger.info(f"User '{session['username']}' started a new session.")
        #         return redirect('/menu')
        # return redirect('/')
    except Exception as e:
        current_app.logger.error(f"Error processing check_user_* : {str(e)}")
        flash(f"Error processing menu request: {str(e)}", "danger")
        return redirect('/')

@nav_bp.route('/menu')
def show_menu_page():
    try:
        username = session.get('username', None)
        current_app.logger.info(f"Menu page accessed by user: {username}")
        return render_template('menu.html', username=username)
    except Exception as e:
        current_app.logger.error(f"Error loading the menu page: {str(e)}")
        flash(f"Error rendering the menu page: {str(e)}", "danger")
        return redirect('/')

@nav_bp.route('/editor_select')
def show_editor_select():
    try:
        # Attempt to render the template and pass the file list
        return render_template('editor_select.html', files=data_access.get_files_list())
    except Exception as e:
        # Log the error and notify the user
        current_app.logger.error(f"Error loading editor_select: {str(e)}")
        flash(f"Error rendering editor_select page: {str(e)}", "danger")
        return redirect('/')

@nav_bp.route('/game_opt')
def show_game_opt():
    try:
        # Attempt to render the template with user files
        return render_template('game_opt.html', userfiles=data_access.get_files_list())
    except Exception as e:
        # Log the error and notify the user
        current_app.logger.error(f"Error loading show_game_opt: {str(e)}")
        flash(f"Error rendering show_game_opt page: {str(e)}", "danger")
        return redirect('/')

@nav_bp.route('/game', methods=['POST'])
def show_game():
    try:
        if session.get('game_set') != request.form['selected_game_set']:
            # if selected set is the same as before played, keep the same index to keep playing
            session['current_question_index'] = 0
        session['game_set'] = request.form['selected_game_set']

        current_app.logger.info(f"Question set '{session.get('game_set')}' loaded for user: {session.get('username')}")
        
        # Attempt to render the game page
        return render_template('game.html', question = game.load_next_question(), players = session.get('players', []), current_player_index = session.get('current_player_index', 0))
    except Exception as e:
        # Log the error and notify the user
        current_app.logger.error(f"Error loading show_game: {str(e)}")
        flash(f"Error rendering game page: {str(e)}", "danger")
        return redirect('/')
    
@nav_bp.route('/player')
def show_player():
    try:
        players = session.get('players', [])
        current_app.logger.info("Player management page accessed.")
        return render_template('player.html', players=players)
    except Exception as e:
        current_app.logger.error(f"Error loading player page: {str(e)}")
        flash(f"Error loading player page: {str(e)}", "danger")
        return redirect('/menu')