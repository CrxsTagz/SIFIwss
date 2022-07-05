from fpdf import FPDF

#PDF function
class pdfcreator():
    def getpdf(bssid, essid, devIP, ok):
        essid = essid
        bssid = bssid
        devIP = devIP
        #save FPDF class into a variable pdf
        pdf = FPDF()

#Add page
        pdf.add_page()

        pdf.set_font("Arial", size= 13)

#create cells 

        pdf.cell(200, 10,  txt= f"Tu SSID seleccionado es: {essid}", ln= 1, align= 'L')
        pdf.cell(200, 10,  txt= f"La MAC BSSID del AP es: {bssid}", ln= 2, align= 'L')

#save the pdf with the .pdf extension

        pdf.output("PDFReports/PruebaWSS.pdf")