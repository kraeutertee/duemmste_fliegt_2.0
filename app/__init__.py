# app/__init__.py
import os
import secrets
import logging
from flask import Flask

# Initialize Flask app
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['SESSION_TYPE'] = 'filesystem'

# Configure logging
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.log')
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,  # Set to DEBUG, INFO, WARNING, ERROR, or CRITICAL depending on your needs
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)

# Logging example on app start
app.logger.info('Flask application has started.')

# Import and register blueprints
from app.data_access import data_access_bp
from .views.user import user_bp
from .views.player import player_bp
from .views.question import question_bp
from .views.game import game_bp
from .views.nav import nav_bp

app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(player_bp, url_prefix='/player')
app.register_blueprint(question_bp, url_prefix='/question')
app.register_blueprint(game_bp, url_prefix='/game')
app.register_blueprint(nav_bp)
app.register_blueprint(data_access_bp)