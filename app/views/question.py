import os
from flask import Blueprint, app, flash, render_template, request, redirect, session, url_for
from app import data_access

question_bp = Blueprint('question', __name__)

@question_bp.route('/question_editor_select')
def show_questionselect_page():
    try:
        username = session.get('username', None)
        userfiles = []
        for filename in os.listdir(data_access.get_questions_folder()) and os.path.isfile(os.path.join(data_access.get_questions_folder(), filename)):
                userfiles.append(filename)
        app.logger.info(f"Question selection page accessed by user: {username}")
        return render_template('editor_select.html', userfiles=userfiles)
    except Exception as e:
        app.logger.error(f"Error loading question selection page: {str(e)}")
        flash(f"Error loading question selection page: {str(e)}", "danger")
        return redirect('/menu')