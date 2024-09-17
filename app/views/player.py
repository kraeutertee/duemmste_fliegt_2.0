from flask import Blueprint, current_app, flash, render_template, request, redirect, session, url_for

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