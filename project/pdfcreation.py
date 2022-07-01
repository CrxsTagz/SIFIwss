from random import random
from fpdf import FPDF

#PDF function

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