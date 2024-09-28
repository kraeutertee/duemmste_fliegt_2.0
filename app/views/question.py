import csv
import datetime
import os
from flask import Blueprint, current_app, flash, render_template, request, redirect, session, url_for
from app import data_access
from app.views import nav

question_bp = Blueprint('question', __name__)

@question_bp.route('/create_editor_set', methods=['POST'])
def create_editor_set():
    try:
        editor_set = request.form['editor_set']   
        file_path = create_csv( editor_set)
        
        return nav.show_editor(file_path)
    except Exception as e:
        current_app.logger.error(f"Error creating editor set: {str(e)}")
        flash(f"Error creating editor set: {str(e)}", "danger")
        return redirect('/questionselect')


def create_csv(file_name):
    try:
        file_path = os.path.join(data_access.get_questions_folder(), f"{file_name}.csv")

        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['question', 'answer', 'image_path', 'HasImage'])

        current_app.logger.info(f"CSV file created at {file_path}.")

        return file_path
    except Exception as e:
        current_app.logger.error(f"Error creating CSV file: {str(e)}")
        flash(f"Error creating CSV file: {str(e)}", "danger")
        return None
    
@question_bp.route('/save_question', methods=['POST'])
def save_question():
    try:
        selected_question_set = session.get('editor_set')
        question = request.form['question']
        answer = request.form['answer']
        image = request.files['image']
        HasImage = True
        username = session.get('username', 'default_user')
        image_dir = os.path.join('static', 'images')
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        if image and image.filename != '':
            try:
                filename, extension = os.path.splitext(image.filename)
                image_path = os.path.join(image_dir, f"{filename}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{username}{extension}")
                image.save(image_path)
                current_app.logger.info(f"Image saved at {image_path}")
            except Exception as e:
                current_app.logger.error(f"Error saving image: {str(e)}")
                flash(f"Error saving image: {str(e)}", "warning")
                image_path = ''
                HasImage = False
        else:
            image_path = ''
            HasImage = False

        try:
            with open(selected_question_set, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([question, answer, image_path, HasImage])
            current_app.logger.info(f"Question '{question}' saved to {selected_question_set}.")
        except Exception as e:
            current_app.logger.error(f"Error writing to CSV: {str(e)}")
            flash(f"Error writing to CSV: {str(e)}", "danger")
            return redirect('/questionselect')

        flash("Question saved successfully!", "success")
        return render_template('questioncreate.html')

    except Exception as e:
        current_app.logger.error(f"Error saving question: {str(e)}")
        flash(f"Error saving question: {str(e)}", "danger")
        return redirect('/questionselect')