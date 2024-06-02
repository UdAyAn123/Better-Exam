import imp
from flask import Flask, render_template
import os
import secrets
import shutil
from datetime import date
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask.helpers import send_file, send_from_directory
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

AUDIO_STORE_PATH = 'app/uploads/users'

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='hi',
        S2T_KEY='',
        UPLOAD_FOLDER="app/uploads"
    )
    app.config.from_pyfile("config.py")

    # This api is used for generating unique tokens for user to support multiple users at a time
    # Client must send this token in every request header named "token-id"
    @app.route('/gettoken', methods=['GET'])
    def get_token():
        token = secrets.token_urlsafe(10)
        session[str(token)] = date.today()
        return token

    # This api is used for deleting a user session. It deletes the in static/users and the token
    @app.route('/poptoken', methods=['GET'])
    def poptoken():
        shutil.rmtree("app/static/users/"+request.headers["token-id"])
        session.pop(request.headers["token-id"], None)
        print(session)
        return "Session Deleted"

    from . import exam
    app.register_blueprint(exam.bp)


    app.jinja_env.globals =  { elem.__name__: elem for elem in exam.jinja_globals }

    @app.route('/teacher', methods=['GET'])
    def teacher():
        return render_template('teacher.html')

    @app.route('/test', methods=['GET'])
    def test():
        return 'Server is Working'

    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    @app.route('/recorder', methods=['GET'])
    def recorder():
        return render_template('recorder.html')

    @app.route('/audio', methods=['GET'])
    def audio():
        return render_template('audio.html')

    @app.route('/arman', methods=['GET'])
    def arman():
        return render_template('arman.html')

    
    return app

