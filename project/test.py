# -*- coding: utf-8 -*-
from ctypes import alignment
from multiprocessing import Value
from re import X
import time as datetime 
from datetime import date
import os
from tkinter import CENTER
from click import command
from dash import Dash, Input, Output, callback, dash_table
from dash import Dash, dcc, html, callback_context, State
from dash.dependencies import Input, Output
import classes
import mysql.connector
from dash import Dash, dash_table
import pandas as pd
import numpy as np
from collections import OrderedDict
from pythonping import ping
import paramiko
import dash_daq as daq
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pdfcreation
from dash.exceptions import PreventUpdate

def Handshake(host: str, password: str, essid):
    host = host
    port = 22
    username = "kali"
    password = password
    essid = essid
    #command = "ls /home/kali/hs  | grep "+essid+" | > /home/kali/Reports/"+essid+".handshake"
    command = "ls /home/kali/hs  | grep "+essid
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    ssh.exec_command(command)
    stdin, stdout, stderr = ssh.exec_command(command)
    lines = stdout.readlines()
    error = stderr.readlines()
    if lines:
        a = lines[0][0:-1]
        return a
    

def PRINTHandshake(host: str, password: str, essid):
    host = host
    port = 22
    username = "kali"
    password = password
    essid = essid
    command = "cat /home/kali/Reports/"+essid+".handshake"
    #command = "ls /home/kali/hs  | grep "+bssid
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    ssh.exec_command(command)
    stdin, stdout, stderr = ssh.exec_command(command)
    lines = stdout.readlines()
    error = stderr.readlines()
    return lines

    


def Wifite(host: str, password: str, bssid, interface):
    host = host
    port = 22
    username = "kali"
    password = password
    DATE = date.today().strftime('%Y-%m-%d-%H_%M')
    data_wifi_csv = "wifi_net" + DATE
    #command = "sudo timeout 20s airodump-ng wlan1mon -w /home/kali/Reports/wifi_networks/"+data_wifi_csv+" --wps --output-format csv --write-interval 5 > /home/kali/Reports/wifi_networks/wifi_last.csv"
    #command = "ls"
    bssid = bssid
    interface = interface
    command = "screen -dmSL SIFI sudo wifite -i "+interface+" -b "+bssid+" --no-pmkid"
    #command = "sudo besside-ng wlan0mon -b "+ bssid +" -vv"
    #command = "sudo iwlist wlan0 scan | grep ESSID"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    ssh.exec_command(command)
    stdin, stdout, stderr = ssh.exec_command(command)
    lines = stdout.readlines()
    #lines = ""
    return lines

def toSCP(host: str, password: str):
    host = host
    port = 22
    username = "kali"
    password = password
    DATE = date.today().strftime('%Y-%m-%d-%H_%M')
    data_wifi_csv = "wifi_net" + DATE
    #command = "sudo timeout 20s airodump-ng wlan1mon -w /home/kali/Reports/wifi_networks/"+data_wifi_csv+" --wps --output-format csv --write-interval 5 > /home/kali/Reports/wifi_networks/wifi_last.csv"
    #command = "ls"
    command = "/home/kali/scripts/scp"
    #command = "sudo iwlist wlan0 scan | grep ESSID"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    ssh.exec_command(command)
    stdin, stdout, stderr = ssh.exec_command(command)
    lines = stdout.readlines()
    #lines = ""
    return lines



# DB Connection Parameters
dbPara = classes.dbCredentials()

def read_csv_sftp(hostname: str, username: str, remotepath: str, password: str, *args, **kwargs) -> pd.DataFrame:
    """
    Read a file from a remote host using SFTP over SSH.
    Args:
        hostname: the remote host to read the file from
        username: the username to login to the remote host with
        remotepath: the path of the remote file to read
        *args: positional arguments to pass to pd.read_csv
        **kwargs: keyword arguments to pass to pd.read_csv
    Returns:
        a pandas DataFrame with data loaded from the remote host
    """
    # open an SSH connection
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname, username=username, password=password)
    #command = "sudo timeout 10s wash -i wlan0mon -s -u -2 -5 -a -p > /home/kali/Reports/wifi_networks/basic.wifi.csv && cat /home/kali/Reports/wifi_networks/basic.wifi.csv"
    #client.exec_command(command)
    # read the file using SFTP
    sftp = client.open_sftp()
    remote_file = sftp.open(remotepath)
    dataframe = pd.read_csv(remote_file, *args, **kwargs)
    remote_file.close()
    # close the connections
    sftp.close()
    client.close()
    return dataframe




def toSSH(host: str, password: str, interfaceValue: str):
    host = host
    port = 22
    username = "kali"
    password = password
    DATE = date.today().strftime('%Y-%m-%d-%H_%M')
    data_wifi_csv = "wifi_net" + DATE
    #command = "sudo timeout 20s airodump-ng wlan1mon -w /home/kali/Reports/wifi_networks/"+data_wifi_csv+" --wps --output-format csv --write-interval 5 > /home/kali/Reports/wifi_networks/wifi_last.csv"
    #command = "ls"

    interfaceValue = interfaceValue
    command = "sudo timeout 10s wash -i " + interfaceValue + " -s -u -2 -5 -a -p > /home/kali/Reports/wifi_networks/basic.wifi.csv || /home/kali/scripts/scp"
    #command = "sudo iwlist wlan0 scan | grep ESSID"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    #ssh.exec_command(command)
    stdin, stdout, stderr = ssh.exec_command(command)
    lines = stdout.readlines()
    #lines = ""
    return 
    
def toSSH2(host, password, interface):
    host = host
    port = 22
    username = "kali"
    password = password
    interface = interface
    DATE = date.today().strftime('%Y-%m-%d-%H_%M')
    data_wifi_csv = "wifi_net" + DATE
    #command = "sudo timeout 10s airodump-ng wlan0mon -w /home/kali/Reports/wifi_networks/wifi_last --wps --output-format csv | sudo python /home/kali/Reports/wifi_networks/pyexcel.py | cat /home/kali/Reports/wifi_networks/wifi_last-01.csv"
    command = "sudo rm -rf /home/kali/Reports/wifi_networks/wifi_last-01.csv && sudo timeout 10s airodump-ng "+interface+" -w /home/kali/Reports/wifi_networks/wifi_last --wps --output-format csv"
    #command = "ls"
    #command = "sudo timeout 10s wash -i wlan2mon -s -u -2 -5 -a -p > /home/kali/Reports/wifi_networks/basic.wifi.csv && cat /home/kali/Reports/wifi_networks/basic.wifi.csv"
    #command = "sudo iwlist wlan0 scan | grep ESSID"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    #ssh.exec_command(command)
    stdin, stdout, stderr = ssh.exec_command(command)
    lines = stdout.readlines()
    #lines = ""
    return 

#def UpdateSSIDTable():
            
          #  dash_table.DataTable(
                        #columns = [{'name': i, 'id': i} ],

                        #columns=[{"name": i, "id": i, 'type': "text", 'presentation':'markdown'} for i in  read_csv_sftp("100.64.0.2", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "kali").columns ],
                       # columns=[{"name": [["weburl"]], "id": "weburl", 'type': "", 'presentation':'markdown'}],
           #         data = read_csv_sftp("100.64.0.77", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "kali").to_dict('records'), style_cell={'textAlign': 'left'},
            #            style_header={
             #               'backgroundColor': 'rgb(30, 30, 30)',
              #              'color': 'white'
               #         },
                #        style_data={
                 #           'backgroundColor': 'rgb(50, 50, 50)',
                  #          'color': 'white'
                 #       },            
            #)


def check_ping(ip):
    response = os.system("ping -n 1 " + ip)
    # and then check the response...
    if response == 0:
        pingstatus = True
    else:
        pingstatus = False
    
    return pingstatus


def pingdef(ip):
    response_list = ping(ip,count=10)

    return response_list.rtt_avg_ms
    # Connect to DB
connectr = mysql.connector.connect(user = dbPara.dbUsername, password = dbPara.dbPassword, host = dbPara.dbServerIp , database = dbPara.dataTable)
    # Connection must be buffered when executing multiple querys on DB before closing connection.
pointer = connectr.cursor(buffered=True)
pointer.execute('SELECT * FROM agents;')
queryRaw = pointer.fetchall()
    # Transform the query payload into a dataframe
queryPayload = np.array(queryRaw)
df = pd.DataFrame(queryPayload, columns=['idagents', 'ubicacion', 'ip', 'weburl', 'sshurl', 'agentname','connection'])
#Define Up or DOW in DataTaFrame
def LatencyRating():
    df['connection'] = df['ip'].apply(lambda x:
        'DOWN' if check_ping(x) == False else( 'UP' 
        
                            ))
    
    #Add Latency Column to DataFrame
    df['Latency(ms)'] = df['ip'].apply(lambda x:pingdef(x)
        if check_ping(x) == True else ('0'))
    

    #Rating de la conexions de los Sifi AGENTS desde el server.
    if check_ping("100.64.0.2") == True and check_ping("100.64.0.4") == True: 
        df['Rating'] = df['ip'].apply ( lambda x:
            '⭐⭐⭐' if pingdef(x) < 50 else (
            '⭐⭐' if pingdef(x) < 70 else (
            '⭐' if  pingdef(x) < 100  else '🔥not reliable'
              )))

def SSIDDataTable():
    return html.Div([ html.H3('Sifi Agent 64.2: SSID list'),
            html.H4(        
                dash_table.DataTable(
                        #columns = [{'name': i, 'id': i} ],

                        #columns=[{"name": i, "id": i, 'type': "text", 'presentation':'markdown'} for i in  read_csv_sftp("100.64.0.2", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "kali").columns ],
                       # columns=[{"name": [["weburl"]], "id": "weburl", 'type': "", 'presentation':'markdown'}],
                    data = read_csv_sftp("100.64.0.2", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "kali").to_dict('records'), style_cell={'textAlign': 'left'},           
                            )            
                ), html.H3('Sifi Agent 64.4: SSID list'),
            html.H4(   
                    dash_table.DataTable(
                        #columns = [{'name': i, 'id': i} ],

                        #columns=[{"name": i, "id": i, 'type': "text", 'presentation':'markdown'} for i in  read_csv_sftp("100.64.0.2", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "kali").columns ],
                       # columns=[{"name": [["weburl"]], "id": "weburl", 'type': "", 'presentation':'markdown'}],
                    data = read_csv_sftp("100.64.0.4", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "sifi2224").to_dict('records'), style_cell={'textAlign': 'left'},     
                        )
                        
)
        ])


app = Dash(__name__, title='SIFI Control Panel')

theme = {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}


tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '5px solid #d6d6d6',
    'padding': '10px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#00d1b2',
    'color': 'green',
    'padding': '8px'
}

app.layout = html.Div([ 
    dcc.Tabs(id="tabs-styled-with-inline", value='tab-1', className='dark-theme-control', children=[
        dcc.Tab(label='Sifi Agents', value='tab-2', style=tab_style, selected_style=tab_selected_style, className='dark-theme-control'),
        dcc.Tab(label='Pre-Run', value='tab-3', style=tab_style, selected_style=tab_selected_style, className='dark-theme-control'),
        dcc.Tab(label='Wireless Assessment', value='tab-4', style=tab_style, selected_style=tab_selected_style, className='dark-theme-control'),
        dcc.Tab(label='Wifi Dashboard', value='tab-5', style=tab_style, selected_style=tab_selected_style, className='dark-theme-control'),
    ], style=tabs_styles),
    html.Div(id='tabs-content-inline', className='dark-theme-control'),  html.Div(id='container-button-timestamp', className='dark-theme-control'),
    dcc.Dropdown(df.ip.unique(), value='100.64.0.2', id='pandas-dropdown-1', placeholder="Select SifiAgent"),
    dcc.Dropdown(id='dropdown-bssid', placeholder="BSSID"),
    dcc.Dropdown(id='dropdown-essid', placeholder="ESSID"),
    dcc.Dropdown(
    ['WPA/WPA2 Basic Crack', 'WPA/WPA2 Advanced', '4-full-way-Handshake'],
    placeholder="Select Actions To RUN",id='drop-multi',
    multi=True
    ),
    html.Button('LoadNetworks', id = 'submitButton2', n_clicks = 0),
    html.Button('RefreshData', id = 'submitButton', n_clicks = 0),
    html.Div(id='pandas-output-container-1', className='dark-theme-control'),
    html.Button('E.X.E.C.U.T.E WSS', id = 'submitButton3', n_clicks = 0),
    html.Div(id='pandas-output-container-2'),
    dcc.Interval(
        id='dataUpateInterval', 
        interval=5*1000, 
        n_intervals=0
    ), dbc.Alert(id='tbl_out', className='dark-theme-control'), dcc.ConfirmDialog(
        id='confirm-handshake')
   #html.Div([ html.Img(src=app.get_asset_url('sifi.png')), html.H3("A cup of Sifi running like a coffee!") ])
 
    


])
#@app.callback(
 #   Output('pandas-output-container-2', 'children'),
  #  Input('dropdown-bssid', 'options'),
   #Input('dropdown-essid', 'options'),
    #Input('pandas-dropdown-1', 'value')
#)
@app.callback(Output('confirm-handshake', 'displayed'),
    Output('confirm-handshake', 'message'),[
              Input('submitButton3', 'n_clicks'),
              Input('dropdown-essid', 'value'),
              Input('pandas-dropdown-1', 'value')
              ]
              )
def display_confirm(callbackContext,essid,DropDownDevvalue,):
    callbackContext = callback_context
    button_id = callbackContext.triggered[0]['prop_id'].split('.')[0]
    if DropDownDevvalue == "100.64.0.4":
            passwordDev = "sifi2224"
    else:
            passwordDev = "kali"
    if button_id == 'submitButton3':
        result = Handshake(DropDownDevvalue, passwordDev, essid)
        if result:
            return True, f'Handshake Already Exists!! - Starting.... Password Basic Crack, {result}'
        else:
            return True, f'WPA/WPA2 4-Full-Way Handshake capture in progress...'
    return False, "Information Security Wireless Assessment System"


    

@app.callback(
    Output('pandas-output-container-1', 'children'),
     Output('dropdown-bssid', 'options'),
    Output('dropdown-essid', 'options'),
    Input('pandas-dropdown-1', 'value')
)
def update_output(value):
    if value == "100.64.0.4":
        passwordDev = "sifi2224"
        directory = "/home/ittadmin/Reports/wifi_networks/100.64.0.4/wifi_last-01.csv"

          
    else:
        passwordDev = "kali"
        directory = "/home/ittadmin/Reports/wifi_networks/100.64.0.2/wifi_last-01.csv"
    
    dfra = read_csv_sftp("100.64.0.1", "ittadmin", directory, "L1br0Sh@rkR1ng")
    #dfra=[{"name": "BSSID", "id": i, } for i in dfra.columns ],
    dfra4 = dfra.iloc[:, 0]
    dfra5 = dfra.iloc[:, 13]
    ko = f'You have selected {value}'
    return ko, dfra4, dfra5 
    
    
@app.callback( 
    Output('tabs-content-inline', 'children'),
    [
        Input('tabs-styled-with-inline', 'value'), 
        Input('submitButton', 'n_clicks'),
         Input('pandas-dropdown-1', 'value'),
         Input('submitButton2', 'n_clicks'),
         Input('submitButton3', 'n_clicks'),
          Input('dropdown-bssid', 'value'),
        Input('dropdown-essid', 'value'),
        Input('drop-multi', 'value')]
)
def render_content(tab, callbackContext,DropDownDevvalue,callbackContext2,callbackContext3, bssid,essid,dropmultichoise):
    # Instantiate the callback context, to find the button ID that triggered the callback
    callbackContext = callback_context
    callbackContext2 = callback_context
    callbackContext3 = callback_context
    # Get button ID
    button_id = callbackContext.triggered[0]['prop_id'].split('.')[0]
    button_id2 = callbackContext2.triggered[0]['prop_id'].split('.')[0]
    button_id3 = callbackContext3.triggered[0]['prop_id'].split('.')[0]
    if button_id == 'submitButton'and tab == 'tab-3':
        if check_ping("100.64.0.2") == True and check_ping("100.64.0.4") == True:
            toSSH("100.64.0.2", "kali", "wlan0mon")
            toSSH("100.64.0.4", "sifi2224", "wlan0mon")
            
        #if check_ping("100.64.0.77") == True:
           # toSSH("100.64.0.77", "kali", "wlan1mon")
           
       # SSIDDataTable()
            return html.Div([ html.H3('Sifi Agent 64.2: SSID list'),
                html.H4(        
                dash_table.DataTable(
                        #columns = [{'name': i, 'id': i} ],

                        #columns=[{"name": i, "id": i, 'type': "text", 'presentation':'markdown'} for i in  read_csv_sftp("100.64.0.2", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "kali").columns ],
                       # columns=[{"name": [["weburl"]], "id": "weburl", 'type': "", 'presentation':'markdown'}],
                    data = read_csv_sftp("100.64.0.1", "ittadmin", "/home/ittadmin/Reports/wifi_networks/100.64.0.2/basic.wifi.csv", "L1br0Sh@rkR1ng").to_dict('records'), style_cell={'textAlign': 'left'},           
                            )            
                ), html.H3('Sifi Agent 64.4: SSID list'),
                html.H4(   
                    dash_table.DataTable(
                        #columns = [{'name': i, 'id': i} ],

                        #columns=[{"name": i, "id": i, 'type': "text", 'presentation':'markdown'} for i in  read_csv_sftp("100.64.0.2", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "kali").columns ],
                       # columns=[{"name": [["weburl"]], "id": "weburl", 'type': "", 'presentation':'markdown'}],
                    data = read_csv_sftp("100.64.0.1", "ittadmin", "/home/ittadmin/Reports/wifi_networks/100.64.0.4/basic.wifi.csv", "L1br0Sh@rkR1ng").to_dict('records'), style_cell={'textAlign': 'left'},     
                        ), 
                ),

#                        html.H3('Sifi Agent 64.77: SSID list'),
 #           html.H4(   
             
  #                 dash_table.DataTable(
                        #columns = [{'name': i, 'id': i} ],

                        #columns=[{"name": i, "id": i, 'type': "text", 'presentation':'markdown'} for i in  read_csv_sftp("100.64.0.2", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "kali").columns ],
                       # columns=[{"name": [["weburl"]], "id": "weburl", 'type': "", 'presentation':'markdown'}],
   #               data = read_csv_sftp("100.64.0.77", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "kali").to_dict('records'), style_cell={'textAlign': 'left'},     
                       
    #               )),
                   ])
    if button_id3 == 'submitButton3':
        #pdfcreation.pdfcreator().getpdf(bssid, essid, DropDownDevvalue)
        if DropDownDevvalue == "100.64.0.4":
            passwordDev = "sifi2224"
            interface = "wlan0mon"
            directory = "/home/ittadmin/Reports/wifi_networks/100.64.0.4/wifi_last-01.csv"
        else:
            passwordDev = "kali"
            interface = "wlan1mon"
            directory = "/home/ittadmin/Reports/wifi_networks/100.64.0.2/wifi_last-01.csv"
        Wifite(DropDownDevvalue, passwordDev, bssid, interface)
        dfrawifi = read_csv_sftp("100.64.0.1", "ittadmin", directory, "L1br0Sh@rkR1ng")
        dframod = dfrawifi.loc[dfrawifi['BSSID'].isin([bssid])]
        return html.Div([ html.H3(

             dash_table.DataTable(
                      
                    data = dframod.to_dict('records'), style_cell={'textAlign': 'left'},     
                        ), 
                ),
        
          html.H3("Selected Network MAC:"+ bssid, style={
                          'backgroundColor': 'rgb(30, 30, 30)',
                            'color': 'white'
                        }),
          html.H3("Selected Network Name:"+ essid, style={
                          'backgroundColor': 'rgb(30, 30, 30)',
                            'color': 'white'
                        }),
                        html.H3( Handshake(DropDownDevvalue, passwordDev, essid), style={
                          'backgroundColor': 'rgb(30, 30, 30)',
                            'color': 'white'
                        }),
                        
                        ])
                        
        
   # if button_id3 == 'submitButton3' and dropmultichoise == '4-full-way-Handshake' and tab == 'tab-4':
      

    if button_id2 == 'submitButton2':
        toSCP("100.64.0.2", "kali")     
        toSCP("100.64.0.4", "sifi2224")              
    if button_id == 'submitButton' and tab == 'tab-2':
         LatencyRating()
    if button_id == 'submitButton' and tab == 'tab-5':
         if check_ping("100.64.0.2") == True and check_ping("100.64.0.4") == True:
            toSSH2("100.64.0.2", "kali", "wlan1mon")
            toSSH2("100.64.0.4", "sifi2224", "wlan0mon")
            toSCP("100.64.0.2", "kali", "wlan1mon")     
            toSCP("100.64.0.4", "sifi2224", "wlan0mon") 


            if DropDownDevvalue == "100.64.0.4":
              #  passwordDev = "sifi2224"
                    directory = "/home/ittadmin/Reports/wifi_networks/100.64.0.4/wifi_last-01.csv"
      #      toSSH2(DropDownDevvalue,passwordDev, "wlan0mon")
            
            else:
         #   passwordDev = "kali"
                    directory = "/home/ittadmin/Reports/wifi_networks/100.64.0.2/wifi_last-01.csv"
       #     toSSH2(DropDownDevvalue,passwordDev, "wlan0mon")
            return html.Div([
          # html.H3(toSSH2)
                    html.H4(        
                    dash_table.DataTable(
                        #columns = [{'name': i, 'id': i} ],

                        #columns=[{"name": i, "id": i, 'type': "text", 'presentation':'markdown'} for i in  read_csv_sftp("100.64.0.2", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "kali").columns ],
                       # columns=[{"name": [["weburl"]], "id": "weburl", 'type': "", 'presentation':'markdown'}],
                    data = read_csv_sftp("100.64.0.1", "ittadmin", directory,"L1br0Sh@rkR1ng").to_dict('records'), style_cell={'textAlign': 'left'},
                        style_header={
                          'backgroundColor': 'rgb(30, 30, 30)',
                            'color': 'white'
                        },
                        style_data={
                            'backgroundColor': 'rgb(50, 50, 50)',
                            'color': 'white'
                        }          
                            )
                )
       
                ])
   # if button_id == 'submitButton' and tab == 'tab-5':
    #    if DropDownDevvalue == "10.64.0.4":
     #       toSSH2("100.64.0.4", "wlan0mon")
      #      return html.Div([
          # html.H3(toSSH2)
       #     html.H4(        
        #        dash_table.DataTable(
                        #columns = [{'name': i, 'id': i} ],

                        #columns=[{"name": i, "id": i, 'type': "text", 'presentation':'markdown'} for i in  read_csv_sftp("100.64.0.2", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "kali").columns ],
                       # columns=[{"name": [["weburl"]], "id": "weburl", 'type': "", 'presentation':'markdown'}],
                            
         #                       data = read_csv_sftp("100.64.0.4", "kali", "/home/kali/Reports/wifi_networks/wifi_last-01.csv", "sifi2224").to_dict('records'), style_cell={'textAlign': 'left'},
          #              style_header={
           #               'backgroundColor': 'rgb(30, 30, 30)',
            #                'color': 'green'
             #           },
              #          style_data={
               #             'backgroundColor': '#00d1b2',
                #            'color': 'green'
                 #       }          
                  #          )
                #)

                 #   ])
       # elif DropDownDevvalue =="100.64.0.2":
        #    toSSH2("100.64.0.2", "wlan1mon")
         #   return html.Div([
          # html.H3(toSSH2)
          #  html.H4(        
           #     dash_table.DataTable(
                        #columns = [{'name': i, 'id': i} ],

                        #columns=[{"name": i, "id": i, 'type': "text", 'presentation':'markdown'} for i in  read_csv_sftp("100.64.0.2", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "kali").columns ],
                       # columns=[{"name": [["weburl"]], "id": "weburl", 'type': "", 'presentation':'markdown'}],
                            
            #                    data = read_csv_sftp("100.64.0.2", "kali", "/home/kali/Reports/wifi_networks/wifi_last-01.csv", "kali").to_dict('records'), style_cell={'textAlign': 'left'},
             #           style_header={
              #            'backgroundColor': 'rgb(30, 30, 30)',
               #             'color': 'green'
                #        },
                 #      style_data={
                  #          'backgroundColor': 'rgb(50, 50, 50)',
                   #         'color': 'green'
                    #    }          
                     #       )
                #)

                 #   ])
        

    if tab == 'tab-1':
        return html.Div([
            html.H3('Welcome to Sifi WSS')
        ])
    elif tab == 'tab-2':
        return html.Div([
            

                      dash_table.DataTable(
                        #columns = [{'name': i, 'id': i} ],

                        columns=[{"name": i, "id": i, 'type': "text", 'presentation':'markdown'} for i in df.columns ],
                       # columns=[{"name": [["weburl"]], "id": "weburl", 'type': "", 'presentation':'markdown'}],
                        data = df.to_dict('records'),
                        
                        
                      style_header={
                          'backgroundColor': 'rgb(30, 30, 30)',
                            'color': 'white'
                        },
                        style_data={
                            'backgroundColor': 'rgb(50, 50, 50)',
                            'color': 'green'
                        }         ) 
                         
        ])
    elif tab == 'tab-3':
         return html.Div([ html.H3('Sifi Agent 64.2: SSID list'),
                html.H4(        
                dash_table.DataTable(
                        #columns = [{'name': i, 'id': i} ],

                        #columns=[{"name": i, "id": i, 'type': "text", 'presentation':'markdown'} for i in  read_csv_sftp("100.64.0.2", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "kali").columns ],
                       # columns=[{"name": [["weburl"]], "id": "weburl", 'type': "", 'presentation':'markdown'}],
                    data = read_csv_sftp("100.64.0.1", "ittadmin", "/home/ittadmin/Reports/wifi_networks/100.64.0.2/basic.wifi.csv", "L1br0Sh@rkR1ng").to_dict('records'), style_cell={'textAlign': 'left'},           
                            )            
                ), html.H3('Sifi Agent 64.4: SSID list'),
                html.H4(   
                    dash_table.DataTable(
                        #columns = [{'name': i, 'id': i} ],

                        #columns=[{"name": i, "id": i, 'type': "text", 'presentation':'markdown'} for i in  read_csv_sftp("100.64.0.2", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "kali").columns ],
                       # columns=[{"name": [["weburl"]], "id": "weburl", 'type': "", 'presentation':'markdown'}],
                    data = read_csv_sftp("100.64.0.1", "ittadmin", "/home/ittadmin/Reports/wifi_networks/100.64.0.4/basic.wifi.csv", "L1br0Sh@rkR1ng").to_dict('records'), style_cell={'textAlign': 'left'},     
                        ), 
                ), 
        ])
    elif tab == 'tab-4':
            return html.Div([ 
                html.H4( "Customize You WIRELESS ASSESSMENT with S.I.F.I")
                ])        
    elif tab == 'tab-5':
       if DropDownDevvalue == "100.64.0.4":
          #  passwordDev = "sifi2224"
            directory = "/home/ittadmin/Reports/wifi_networks/100.64.0.4/wifi_last-01.csv"
      #      toSSH2(DropDownDevvalue,passwordDev, "wlan0mon")
            
       else:
         #   passwordDev = "kali"
            directory = "/home/ittadmin/Reports/wifi_networks/100.64.0.2/wifi_last-01.csv"
       #     toSSH2(DropDownDevvalue,passwordDev, "wlan0mon")
       return html.Div([
          # html.H3(toSSH2)
            html.H4(        
                dash_table.DataTable(
                        #columns = [{'name': i, 'id': i} ],

                        #columns=[{"name": i, "id": i, 'type': "text", 'presentation':'markdown'} for i in  read_csv_sftp("100.64.0.2", "kali", "/home/kali/Reports/wifi_networks/basic.wifi.csv", "kali").columns ],
                       # columns=[{"name": [["weburl"]], "id": "weburl", 'type': "", 'presentation':'markdown'}],
                    data = read_csv_sftp("100.64.0.1", "ittadmin", directory,"L1br0Sh@rkR1ng").to_dict('records'), style_cell={'textAlign': 'left'},
                        style_header={
                          'backgroundColor': 'rgb(30, 30, 30)',
                            'color': 'white'
                        },
                        style_data={
                            'backgroundColor': 'rgb(50, 50, 50)',
                            'color': 'white'
                        }          
                            )
                )

        ])





#def gotapdf(tab, callbackContext,devIDip,callbackContext2,callbackContext3, bssid,essid):
 #   callbackContext3 = callback_context
    # Get button ID
  #  button_id3 = callbackContext3.triggered[0]['prop_id'].split('.')[0]
   # if button_id3 == 'submitButton3':
    #    pdfo = pdfcreation.pdfcreator()
     #   pdfo.getpdf(bssid, essid, devIDip)

if __name__ == '__main__':
    
    app.run_server(debug=True, host='0.0.0.0', port='5007', dev_tools_silence_routes_logging=False)