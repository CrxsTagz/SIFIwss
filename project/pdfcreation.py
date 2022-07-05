from fpdf import FPDF

#PDF function
class pdfcreator():

    def header(self):
        # Logo
        # self.image('sifi.png', 10, 8, 33)
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'SIFI WSS', 1, 0, 'C')
        # Line break
        self.ln(20)

    def getpdf(bssid, essid, devIP, ok):
        essid = essid
        bssid = bssid
        devIP = devIP


#save FPDF class into a variable pdf
        pdf = FPDF()

#Add page
        pdf.add_page()

        # pdf.set_font("Arial", size= 13)

#add format
        pdf.image("project/sifi-icon.jpg", 70, 0, 20)
        pdf.set_font('Arial', 'B', 15)
        pdf.cell(80)
        # Title
        pdf.cell(30, 10, 'SIFI WSS', 1, 0, 'C')
        # Line break
        pdf.ln(20)

#create cells 
        pdf.set_font("Arial", size= 13)
        pdf.cell(200, 10,  txt= f"Tu SSID seleccionado es: {essid}", ln= 2, align= 'L')
        pdf.cell(200, 10,  txt= f"La MAC BSSID del AP es: {bssid}", ln= 3, align= 'L')

#save the pdf with the .pdf extension

        pdf.output("PDFReports/PruebaWSS.pdf")