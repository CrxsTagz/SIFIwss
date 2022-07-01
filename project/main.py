# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from pdfcreation import getpfd
from project.pdfcreation import getpdf

main = Blueprint('main', __name__)



@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/menu')
def menu():
    return render_template('menu.html')

@main.route('/')
def my_link():
 return getpdf
