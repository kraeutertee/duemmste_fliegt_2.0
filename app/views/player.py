from flask import Blueprint, current_app, flash, jsonify, render_template, request, redirect, session, url_for

player_bp = Blueprint('player', __name__)

@player_bp.route('/add_player', methods=['POST'])
def add_player():
    try:
        player_name = request.form['player_name']
        num_lives = int(request.form['num_lives'])
        players = session.get('players', [])
        index = len(players)
        player_data = {'index': index, 'name': player_name, 'lives': num_lives}
        players.append(player_data)
        session['players'] = players
        current_app.logger.info(f"Player '{player_name}' added with {num_lives} lives.")
        return redirect('/player')
    except ValueError:
        current_app.logger.error("Invalid number of lives entered.")
        flash("Invalid number of lives. Please enter a valid integer.", "danger")
        return redirect('/player')
    except Exception as e:
        current_app.logger.error(f"Error adding player: {str(e)}")
        flash(f"Error adding player: {str(e)}", "danger")
        return redirect('/player')

@player_bp.route('/delete_player/<int:index>')
def delete_player(index):
    try:
        players = session.get('players', [])
        if 0 <= index < len(players):
            deleted_player = players.pop(index)
            for i, player in enumerate(players):
                player['index'] = i
            session['players'] = players
            current_app.logger.info(f"Player '{deleted_player['name']}' deleted.")
        return redirect('/player')
    except Exception as e:
        current_app.logger.error(f"Error deleting player: {str(e)}")
        flash(f"Error deleting player: {str(e)}", "danger")
        return redirect('/player')
    
@player_bp.route('/remove_heart/<int:player_index>', methods=['POST'])
def remove_heart(player_index):
    try:
        players = session.get('players', [])
        if 0 <= player_index < len(players):
            players[player_index]['lives'] -= 1
            session['players'] = players
            current_app.logger.info(f"Heart removed from player {players[player_index]['name']}. Remaining lives: {players[player_index]['lives']}")
            return jsonify(success=True, player=players[player_index])
        return jsonify(success=False), 400
    except Exception as e:
        current_app.logger.error(f"Error removing heart: {str(e)}")
        return jsonify(error=f"Error removing heart: {str(e)}"), 500
    
def update_current_player_index():
    try:
        players = session.get('players', [])
        num_players = len(players)

        if num_players == 0:
            return

        current_index = session.get('current_player_index', 0)
        next_index = (current_index + 1) % num_players

        while players[next_index]['lives'] == 0:
            next_index = (next_index + 1) % num_players

        session['current_player_index'] = next_index
        current_app.logger.info(f"Player index updated to {next_index}.")
    except Exception as e:
        current_app.logger.error(f"Error updating current player index: {str(e)}")
        flash(f"Error updating current player index: {str(e)}", "danger")
