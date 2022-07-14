from fpdf import FPDF
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# This function does not have a return, it only generates the PDF assesment.
#customerName = 'PUCMM'

def pdfGenerator(customerName):
    # save FPDF class into a variable pdf
    pdf = FPDF('P', 'mm', (300, 150))
    date = datetime. now(). strftime("%Y_%m_%d-%I-%M-%S_%p")

    # Add page
    pdf.add_page()

    # set new margins equation
    epw = pdf.w - pdf.l_margin - pdf.r_margin
    eph = pdf.h - pdf.t_margin - pdf.b_margin

    # Draw new margins.
    pdf.rect(pdf.l_margin, pdf.t_margin, w=epw, h=eph)   

    # add format
    # logo
    pdf.image("sifi-icon.jpg", 0, 0, 20)
    # font arial bold 15pts
    pdf.set_font('Arial', 'B', 15)
    # move to the right
    pdf.cell(125)
    # Title
    pdf.cell(30, 10, 'SIFI WSS', 1, 0, 'C')
    # Line break
    pdf.ln(20)

    Assesment_ID = 0

    try:
            connection = mysql.connector.connect(host='localhost',
                                             database='sifi',
                                             user='root',
                                             password='sifi')

            sql_select_Query = "select * from wss"
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
        # get all records
            records = cursor.fetchall()
            print("Total number of rows in table: ", cursor.rowcount)
            Assesment_ID = '{:0>5}'.format(int(records[0][0]))
            print("\nPrinting each row")
            for row in records:
                print("Id = ", row[0], )
                print("bssid = ", row[1])
                print("essid  = ", row[2])
                print("sifiagent  = ", row[3])
                print("handshake  = ", row[4])
                print("cracked_password  = ", row[5])
                print("test_type  = ", row[6], "\n")
                if row[4] is not None:
                    print("Se ha capturado el handshake")

    except Error as e:
            print("Error while connecting to MySQL", e)
    finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
            print("MySQL connection is closed")

    
    #create cells 
    pdf.set_font("Arial", size= 13)
    pdf.cell(200, 10,  txt= f"ID : {row[0]}", ln= 3, align= 'L')
    pdf.cell(200, 10,  txt= f"BSSID : {row[1]}", ln= 4, align= 'L')
    pdf.cell(200, 10,  txt= f"ESSID : {row[2]}", ln= 5, align= 'L')
    pdf.cell(200, 10,  txt= f"Agente SIFI : {row[3]}", ln= 6, align= 'L')
    pdf.cell(200, 10,  txt= f"El handshake capturado es : {row[4]}", ln= 7, align= 'L')
    pdf.cell(200, 10,  txt= f"Contraseña del AP : {row[5]}", ln= 8, align= 'L')
    pdf.cell(200, 10,  txt= f"Tipo de test realizado: {row[6]}", ln= 9, align= 'L')

    if row[4] is not None:
        pdf.add_page()
        epw = pdf.w - pdf.l_margin - pdf.r_margin
        eph = pdf.h - pdf.t_margin - pdf.b_margin

    # Draw new margins.
        pdf.rect(pdf.l_margin, pdf.t_margin, w=epw, h=eph)   

    #add format
    #logo
        pdf.image("cwsp_c.png", 0, 0, 20)
        pdf.set_font("Arial", size= 16)
        # pdf.ln(10)

    #ESTADO DE LA RED, SIFI WSS SCORE
    #Estable	Al menos 1 resultado negativo de cualquiera de las funciones principales
    if row[4] is not None:
        if row[5] is not None:
            pdf.set_font("Arial", size= 16)
            pdf.cell(125)
            pdf.cell(200, 10,  txt= "Sifi Score: ", ln= 24, align= 'L')
            pdf.set_font("Arial", size= 13)
            pdf.cell(-125)
            pdf.cell(200, 10,  txt= "Segun el assesment de la red, la puntuacion asignada es: ", ln= 25, align= 'L')
            pdf.cell(200, 10,  txt= "Sifi Score: Vulnerable. La red pudo ser vulnerada en al menos dos ambitos. ", ln= 26, align= 'L')

            pdf.set_font("Arial", size= 16)
            pdf.cell(110)
            pdf.cell(200, 10,  txt= "RECOMENDACIONES", ln= 24, align= 'L')
            pdf.set_font("Arial", size= 13)
            pdf.cell(-110)
            pdf.cell(200, 10, txt= "A parte de haber capturado el 4-full way handshake, se pudo hacer un crack de la contraseña", ln= 13, align= 'L')
            pdf.cell(200, 10,  txt= "Segun el libro CWSP en su capitulo 9.1.8 se recomienda actualizar a una solución de autenticación 802.1X/EAP usando autenticación ", ln= 14, align= 'L')
            pdf.cell(200, 1,  txt= "tunelada.", ln= 15, align= 'L')

            pdf.set_font("Arial", size= 16)
            pdf.cell(110)
            pdf.cell(200, 10,  txt= "Mejores practicas a tomar", ln= 24, align= 'L')
            pdf.set_font("Arial", size= 13)
            pdf.cell(-110)
            pdf.cell(200, 10,  txt= "- Política corporativa: Un apéndice adicional a las recomendaciones de seguridad podrían ser las recomendaciones de políticas WLAN ", ln= 19, align= 'L')
            pdf.cell(200, 1,  txt= "corporativas. El auditor puede ayudar al cliente a redactar una política de seguridad de la red inalámbrica si aún no tiene una.", ln= 20, align= 'L')
            pdf.ln(2)
            pdf.cell(200, 10,  txt= "- Seguridad física: La instalación de unidades de cerramiento para proteger contra el robo y el acceso físico no autorizado a los puntos", ln= 21, align= 'L')
            pdf.cell(200, 1,  txt= "de acceso puede ser una recomendación. Estas también se utilizan a menudo con fines estéticos. ", ln= 22, align= 'L')


        #Vulnerable	2 pentesting con resultados negativos de cualquier función de la plataforma.

        else:
            pdf.set_font("Arial", size= 16)
            pdf.cell(125)
            pdf.cell(200, 10,  txt= "Sifi Score: ", ln= 24, align= 'L')
            pdf.set_font("Arial", size= 13)
            pdf.cell(-125)
            pdf.cell(200, 10,  txt= "Segun el assesment de la red, la puntuacion asignada es: ", ln= 25, align= 'L')
            pdf.cell(200, 10,  txt= "Sifi Score: Estable. La red pudo ser vulnerada en al menos un ambito.", ln= 26, align= 'L')

            pdf.set_font("Arial", size= 16)
            pdf.cell(110)
            pdf.cell(200, 10,  txt= "RECOMENDACIONES", ln= 24, align= 'L')
            pdf.set_font("Arial", size= 13)
            pdf.cell(-110)
            pdf.cell(200, 10, txt= "Se ha capturado el 4 way handshake. Lo que significa que se ha podido hacer una deautenticacion del cliente conectado al Access Point", ln= 13, align= 'L')
            pdf.cell(200, 10,  txt= "Segun el libro CWSP en su capitulo 9.1.8 se recomienda actualizar a una solución de autenticación 802.1X/EAP usando autenticación ", ln= 14, align= 'L')
            pdf.cell(200, 1,  txt= "tunelada.", ln= 15, align= 'L')

            pdf.set_font("Arial", size= 16)
            pdf.cell(110)
            pdf.cell(200, 10,  txt= "Mejores practicas a tomar", ln= 24, align= 'L')
            pdf.set_font("Arial", size= 13)
            pdf.cell(-110)
            pdf.cell(200, 10,  txt= "- Política corporativa: Un apéndice adicional a las recomendaciones de seguridad podrían ser las recomendaciones de políticas WLAN ", ln= 19, align= 'L')
            pdf.cell(200, 1,  txt= "corporativas. El auditor puede ayudar al cliente a redactar una política de seguridad de la red inalámbrica si aún no tiene una.", ln= 20, align= 'L')
            pdf.ln(2)
            pdf.cell(200, 10,  txt= "- Seguridad física: La instalación de unidades de cerramiento para proteger contra el robo y el acceso físico no autorizado a los puntos", ln= 21, align= 'L')
            pdf.cell(200, 1,  txt= "de acceso puede ser una recomendación. Estas también se utilizan a menudo con fines estéticos. ", ln= 22, align= 'L')

    else:
        pdf.set_font("Arial", size= 16)
        pdf.cell(125)
        pdf.cell(200, 10,  txt= "Sifi Score: ", ln= 24, align= 'L')
        pdf.set_font("Arial", size= 13)
        pdf.cell(-125)
        pdf.cell(200, 10,  txt= "Segun el assesment de la red, la puntuacion asignada es: ", ln= 25, align= 'L')
        pdf.cell(200, 10,  txt= "Sifi Score: Seguro. Todos los pentest poseen resultados positivos y con ninguna vulnerabilidad detectada.", ln= 26, align= 'L')

        # pdf.cell(200, 10, txt= "No se ha capturado el handshake", ln= 11, align= 'L')

    #save the pdf with the .pdf extension
    pdf.output("PDFReports/SiFi_{}_{}_{}.pdf".format(Assesment_ID, customerName, date))