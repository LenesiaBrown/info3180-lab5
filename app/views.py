"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app, db
from app.models import Movie
from app.forms import MovieForm
from flask import render_template, request, redirect, jsonify, send_file, send_from_directory, url_for, flash
from werkzeug.utils import secure_filename
from flask_wtf.csrf import generate_csrf
import os


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@app.route('/api/v1/movies', methods=['POST'])
def movies():
    myform = MovieForm()

    if request.method == 'POST'and myform.validate_on_submit():
        title = myform.title.data
        description = myform.description.data
        photofile = myform.poster.data

        filename = secure_filename(photofile.filename)
        photofile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        movie = Movie(title=title, description=description, poster=photofile)
        db.session.add(movie)
        db.session.commit()

        return jsonify({
            "message": "Movie added successfully",
            "title": title,
            "poster": photofile,
            "description": description
        }), 201
    else:
        errors = form_errors(myform)
        return jsonify({"errors": errors}), 400
    

@app.route('/api/v1/movies', methods=['GET'])
def display_movies():
    movie = Movie.query.all()
    list_movie = []
    for m in movie:
        movie_data = {
            'id': m.id,
            'title': m.title,
            'description': m.description,
            'poster': m.poster
        }
        list_movie.append(movie_data)
    return jsonify({'movies': list_movie})


@app.route('/api/v1/posters/<filename>', methods=['GET'])
def poster_image(file):
    return send_from_directory(app.config['UPLOAD_FOLDER'], file)

    
@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})

        


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