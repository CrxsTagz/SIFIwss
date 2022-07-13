# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from random import random
from fpdf import FPDF
import PDF_creation

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

@main.route('/json')
def json():
    return render_template('json.html')

@main.route('/getpdf')
def getpdf():
    wpascore = random()
    fwfhs = random()
    #save FPDF class into a variable pdf
    pdf = FPDF()

#Add page
    pdf.add_page()

    pdf.set_font("Arial", size= 13)

#create cells 

    pdf.cell(200, 10,  txt= f"Tu score en wpa es: {wpascore}", ln= 1, align= 'L')
    pdf.cell(200, 10,  txt= f"Tu score en wpa es: {fwfhs}", ln= 2, align= 'L')

#save the pdf with the .pdf extension

    pdf.output("Prueba.pdf")