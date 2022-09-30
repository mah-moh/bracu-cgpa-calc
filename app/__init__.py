from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'
app.config['UPLOAD_FOLDER'] = 'static/files'


from app import views
from app.pdfToData import cgpa_calculator
from app.pdftodata1 import calculator