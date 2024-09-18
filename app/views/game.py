import os
import pandas as pd
from flask import Blueprint, current_app, flash, render_template, request, redirect, session, url_for

from app import data_access
from app.views import player

game_bp = Blueprint('game', __name__)

@game_bp.route('/load_next_question', methods=['POST'])
def load_next_question():
    try:
        file_path = os.path.join('data', 'questions', f"{session.get('username')}", f"{session.get('game_set')}")
        index = session.get('current_question_index', 0)
        
        # Read only the specific row using skiprows and nrows
        row = pd.read_csv(file_path, skiprows=index + 1, nrows=1, header=None)
        
        # Check if the row is empty (i.e., end of file reached)
        if row.empty:
            # Reset index to 0 and read the first data row (skip header)
            session['current_question_index'] = 0
            row = pd.read_csv(file_path, skiprows=1, nrows=1, header=None)
        else:
            # Update the session index to the next one
            session['current_question_index'] = index + 1
        
        # Manually assign column names (assuming the first row in the CSV is the header)
        columns = pd.read_csv(file_path, nrows=0).columns.tolist()
        row.columns = columns
        
        current_app.logger.info(f"Loaded question {index + 1}: {row.to_dict(orient='records')[0]} from question set.")
        return row.iloc[0]
    except Exception as e:
        current_app.logger.error(f"Error loading next question: {str(e)}")
        flash(f"Error loading next question: {str(e)}", "danger")
        return None
    
@game_bp.route('/load_next_question_call', methods=['POST'])
def load_next_question_call():
    player.update_current_player_index()
    return render_template('game.html', question = load_next_question(), players = session.get('players', []), current_player_index = session.get('current_player_index', 0))

