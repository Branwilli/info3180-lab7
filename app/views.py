"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app
from flask import render_template, request, jsonify, send_file, current_app, send_from_directory
import os
from app.forms import MovieForms
from app.models import Movies
from dotenv import load_dotenv
from . import db 
from flask_wtf.csrf import generate_csrf 
from werkzeug.utils import secure_filename

load_dotenv()

UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route('/api/v1/movies', methods=['POST'])
def movies():
    form = MovieForms()

    if request.method == 'POST' and form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        poster_file = request.files.get('poster')

        if poster_file:
            filename = secure_filename(poster_file.filename)
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            poster_file.save(upload_path)

            movie = Movies(title=title, description=description, poster=filename)
            db.session.add(movie)
            db.session.commit()

            return jsonify({
                'message': 'Movie Successfully added',
                'title': title,
                'description': description,
                'poster': filename
            })
            
    return jsonify(form_errors(form))

@app.route('/api/v1/movies', methods=["GET"])
def get_movies():
    movies = Movies.query.all()
    movies_list = [{
            'id': movie.id,
            'title': movie.title,
            'description': movie.description,
            'poster': movie.poster
        } for movie in movies]
    
    return jsonify(movies_list)

@app.route('/api/v1/csrf-token', methods=['GET']) 
def get_csrf(): 
    return jsonify({'csrf_token': generate_csrf()}) 

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404