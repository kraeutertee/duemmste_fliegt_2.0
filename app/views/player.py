from flask import Blueprint, current_app, flash, jsonify, render_template, request, redirect, session, url_for

from app.views import game

player_bp = Blueprint('player', __name__)

@player_bp.route('/add_player', methods=['POST'])
def add_player():
    try:
        # Get player details from the form
        player_name = request.form['player_name']
        num_lives = int(request.form['num_lives'])

        # Add the player to the session
        players = session.get('players', [])
        index = len(players)
        player_data = {'index': index, 'name': player_name, 'lives': num_lives}
        players.append(player_data)
        session['players'] = players

        # Log the addition of a new player
        current_app.logger.info(f"Player '{player_name}' added with {num_lives} lives.")
        return redirect('/player')
    
    except ValueError:
        # Handle invalid number of lives input
        current_app.logger.error("Invalid number of lives entered.")
        flash("Invalid number of lives. Please enter a valid integer.", "danger")
        return redirect('/player')

    except Exception as e:
        # General exception handling
        current_app.logger.error(f"Error adding player: {str(e)}")
        flash(f"Error adding player: {str(e)}", "danger")
        return redirect('/player')

@player_bp.route('/delete_player/<int:index>')
def delete_player(index):
    try:
        # Get the list of players
        players = session.get('players', [])
        
        # Check if the player index is valid
        if 0 <= index < len(players):
            deleted_player = players.pop(index)

            # Reindex the remaining players
            for i, player in enumerate(players):
                player['index'] = i

            # Save the updated players list back to the session
            session['players'] = players

            # Log successful deletion
            current_app.logger.info(f"Player '{deleted_player['name']}' deleted.")
        else:
            current_app.logger.error(f"Invalid player index: {index}")
            flash("Invalid player index.", "danger")
        
        return redirect('/player')
    
    except Exception as e:
        # General exception handling
        current_app.logger.error(f"Error deleting player: {str(e)}")
        flash(f"Error deleting player: {str(e)}", "danger")
        return redirect('/player')

@player_bp.route('/remove_heart/<int:player_index>', methods=['POST'])
def remove_heart(player_index):
    try:
        # Get the list of players
        players = session.get('players', [])
        
        # Ensure the player index is valid
        if 0 <= player_index < len(players):
            players[player_index]['lives'] -= 1  # Remove a heart from the player
            session['players'] = players  # Update the session with the modified players list
            
            # Log the heart removal
            current_app.logger.info(f"Heart removed from player {players[player_index]['name']}. Remaining lives: {players[player_index]['lives']}")
            return jsonify(success=True, player=players[player_index])
        else:
            current_app.logger.error(f"Invalid player index: {player_index}")
            return jsonify(success=False), 400

    except Exception as e:
        # General exception handling for removing a heart
        current_app.logger.error(f"Error removing heart: {str(e)}")
        return jsonify(error=f"Error removing heart: {str(e)}"), 500

def update_current_player_index():
    try:
        # Get the list of players
        players = session.get('players', [])
        
        # Count the number of players still alive
        num_players_alive = sum(1 for player in players if player['lives'] > 0)

        if num_players_alive == 0:
            # If no players are alive, return without updating
            current_app.logger.warning("No players alive to update index.")
            return

        # Get the current player index from the session
        current_index = session.get('current_player_index', 0)
        next_index = (current_index + 1) % len(players)  # Calculate the next player index

        # Loop to find the next player who is still alive
        while players[next_index]['lives'] == 0:
            next_index = (next_index + 1) % len(players)

        # Check if only two players are left and final mode should be started
        if num_players_alive == 2 and session.get('final_mode', True) and not session.get('final_mode_init', False):
            # Start the final mode if conditions are met
            game.start_final_mode()
            next_index = 0  # Reset index to 0 for the final mode
            session['final_mode_init'] = True

        # Update the session with the new current player index
        session['current_player_index'] = next_index

        # Log successful player index update
        current_app.logger.info(f"Player index updated to {next_index}.")

    except Exception as e:
        # General exception handling
        current_app.logger.error(f"Error updating current player index: {str(e)}")
        flash(f"Error updating current player index: {str(e)}", "danger")