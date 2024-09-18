import os
import pandas as pd
from flask import Blueprint, current_app, flash, render_template, request, redirect, session, url_for

from app import data_access
from app.views import player

game_bp = Blueprint('game', __name__)

@game_bp.route('/load_next_question', methods=['POST'])
def load_next_question():
    try:
        # Log start of question loading process
        current_app.logger.info("Starting process to load next question.")

        # Get the file path dynamically based on session data
        username = session.get('username')
        game_set = session.get('game_set')
        index = session.get('current_question_index', 0)

        # Log session data
        current_app.logger.info(f"Session Data - Username: {username}, Game Set: {game_set}, Current Index: {index}")

        # Construct file path
        file_path = os.path.join('data', 'questions', f"{username}", f"{game_set}")

        current_app.logger.info(f"Constructed file path: {file_path}")

        try:
            # Log attempt to read specific row from CSV
            current_app.logger.info(f"Attempting to read row {index + 1} from CSV file: {file_path}")
            row = pd.read_csv(file_path, skiprows=index + 1, nrows=1, header=None)
        except pd.errors.EmptyDataError:
            current_app.logger.info(f"End of file reached for {file_path}. Resetting question index.")

            # Reset index and log the action
            session['current_question_index'] = 0
            index = 0
            current_app.logger.info(f"Reset question index to 0. Loading the first question.")

            # Read the first question after header
            row = pd.read_csv(file_path, skiprows=1, nrows=1, header=None)

            # Check if in final mode
            if session.get('final_mode_active', False):
                current_app.logger.info("Final mode active. Updating current player index.")
                player.update_current_player_index()

        # Check if the row is empty
        if row.empty:
            current_app.logger.info(f"Empty row found at index {index}. Skipping to next row.")
            session['current_question_index'] = 0
            return None

        # Log that row data was successfully read
        current_app.logger.info(f"Successfully read row: {row.to_dict(orient='records')[0]}")

        # Manually assign column names from header
        current_app.logger.info(f"Reading column names from the CSV file: {file_path}")
        columns = pd.read_csv(file_path, nrows=0).columns.tolist()
        row.columns = columns

        # Log successful column assignment
        current_app.logger.info(f"Assigned columns: {columns}")

        # Log the question details
        current_app.logger.info(f"Loaded question {index + 1}: {row.to_dict(orient='records')[0]} from question set.")

        # Update session to point to the next question
        session['current_question_index'] = index + 1
        current_app.logger.info(f"Updated session question index to {index + 1}")

        return row.iloc[0]

    except FileNotFoundError as e:
        # Log file not found error
        current_app.logger.error(f"File not found: {file_path} - Error: {str(e)}")
        flash(f"File not found: {file_path}", "danger")
        return None

    except pd.errors.EmptyDataError as e:
        # Log if the CSV is empty
        current_app.logger.error(f"Empty CSV file: {file_path} - Error: {str(e)}")
        flash(f"The question set is empty: {file_path}", "danger")
        return None

    except Exception as e:
        # Log any other kind of exception
        current_app.logger.error(f"Error loading next question from {file_path}: {str(e)}")
        flash(f"Error loading next question: {str(e)}", "danger")
        return None



@game_bp.route('/load_next_question_call', methods=['POST'])
def load_next_question_call():
    try:
        # Only update the player index if not in final mode
        if not session.get('final_mode_active', False):
            player.update_current_player_index()

        # Render the game template with the loaded question and players
        return render_template('game.html', question=load_next_question(), players=session.get('players', []), current_player_index=session.get('current_player_index', 0))

    except Exception as e:
        # Log any exceptions while calling the load next question function
        current_app.logger.error(f"Error during loading the next question call: {str(e)}")
        flash(f"Error loading the next question: {str(e)}", "danger")
        return redirect(url_for('some_error_page'))  # Replace 'some_error_page' with your error handling route

def start_final_mode():
    try:
        # Set up the session for the final mode
        session['game_set'] = 'final.csv'
        session['current_question_index'] = 0
        session['final_mode_active'] = True
        current_app.logger.info("Final mode has been activated.")

    except Exception as e:
        # Log any errors during the start of final mode
        current_app.logger.error(f"Error starting final mode: {str(e)}")
        flash(f"Error starting final mode: {str(e)}", "danger")
        return redirect(url_for('some_error_page'))  # Replace 'some_error_page' with your error handling route


# game set zu finale ändern
# final modus aktivieren --> next player index muss daran merken ob es nächsten Spieler aktivieren soll, kann dabei auf den current_question index zugreifen erst wenn der wieder auf null gesetzt wird (rausfinden wo das gemacht wird)