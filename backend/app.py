from flask import Flask, Response, request
import xml.etree.ElementTree as ET
from xml.dom import minidom
import requests
import re
from evento import Evento
app = Flask(__name__)

@app.route('/')
def index():
    return 'hola mundo'

@app.route('/prueba')
def p():
    res = request.json
    print(res['somekey'])
    return ("esta la prueba pal endpoint xd")

def format(cadena):
        mydoc = ET.tostring(cadena).decode()
        reescribe = minidom.parseString(mydoc)
        return reescribe.toprettyxml(indent="")

@app.route('/doc', methods = ['POST'])
def leer_xml():
    res = request.json
    text = res['archivo_xml']
    myfile = open('xmltemp.xml', 'w') 
    myfile.write(text)
    #print(text)
    read_xml()
    return res

list_event = []
fecha_a = ''
report_a =''
usuarios_a = ''
error_a = ''

val = 0
def pasar_cadena(cadena):
    global fecha_a, report_a, usuarios_a, error_a
    #para fecha
    if re.findall('^guatemala', cadena.lower()):
        #print('fecha')
        fecha_a = cadena
    #reportado por (un correo)
    elif re.findall('^reportado por: ', cadena.lower()):
        #print('reportado por')
        report_a = cadena
    #para varios usarios(varios correos)
    elif re.findall('^usuarios afectados', cadena.lower()) or re.findall('@ing.usac.edu.gt$', cadena.lower()) :
        #print('usuarios afectados')
        usuarios_a += cadena
    #para error
    elif re.findall('^error', cadena.lower()) or re.findall('.$', cadena.lower()):
        #print('error')
        error_a += cadena
        
    #viene vacio
    else:
        print('posibles correos--->' + cadena)


def read_xml_back(): #extrae todo del xml y lo introduce a las listas 
    global usuarios_a, error_a    
    mydoc = minidom.parse('C:/Users/otrop/Desktop/IPC2_Proyecto3_201701081/backend/xmlTemp.xml')
    eventos = mydoc.getElementsByTagName('EVENTO')
    for xEve in range(len(eventos)):
        #print(eventos[xEve].firstChild.data)              
        temp = open('text.txt','w')
        temp.write(eventos[xEve].firstChild.data)
        temp.close()
        usuarios_a = '' #reinicia los valores ya que pueden ser los unicos que acumulen mas de 2 lineas
        error_a = ''
        #print(int(xEve)+1)
        templectura = open('text.txt', 'r')
        for linea in templectura.readlines():
            lin = linea.split()
            if len(lin) == 0:
                #print('en blanco',end="")
                continue
            else:
                #print(linea.strip(' '))
                pasar_cadena(linea.strip(' ')) 
        '''
        print(fecha_a)
        print(report_a)
        print(usuarios_a)
        print(error_a)   
        '''    
        eve = Evento(fecha_a, report_a, usuarios_a, error_a)
        list_event.append(eve)            
        templectura.close()
    for x in list_event:
        
        print(x.fecha)
        print(x.report)
        print(x.usuarios)
        print(x.error)


read_xml_back()

    
        

#if __name__ == '__main__':
 #   app.run(debug=True, port=4000)