from flask import Flask, Response, request
import xml.etree.ElementTree as ET
from xml.dom import minidom
import requests
import re
from evento import Evento
from fecha_frec import Fecha_Frec
from correo import Correo_Fecha
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
        eve = Evento(fecha_a, report_a, usuarios_a, error_a)
        list_event.append(eve)            
        templectura.close()
'''
    for x in list_event:   
        print(x.fecha)
        print(x.report)
        print(x.usuarios)
        print(x.error)
'''

list_fecha = [] #almacena objetos fecha_frec fechas sin repetir y cada una con la cantidad de msj enviados esa fecha
list_correo = [] # todos los correos que reportaron, estan sin repetir correos 
list_CoFe = [] # almacena objetos correo los correos con sus fechas y contadores
def msj_fecha():#ingresa las fechas y sus frecuencias(cantidad de msj enviados esa fecha) a list_fecha
    temp_fech = []
    temp_fech2 = []
    for x in list_event:
        f = x.fecha.split(',')
        f[1].strip('\n')
        temp_fech.append(f[1].strip(' '))
        temp_fech2.append(f[1].strip(' '))
    #print('tamanio original-->',len(temp_fech))
    cont=0
    for x in range(len(temp_fech)):
        #print(x,'largo', len(temp_fech))
        if len(temp_fech) == 0:
            break
        temp = temp_fech[0]
        #print('tamanio despues de borrar', len(temp_fech))
        for z in range(len(temp_fech2)):
            temp2 = temp_fech2[z]
            if temp == temp2:          
                #print(x,' ',cont, 'fecha->', temp)
                cont += 1
                temp_fech.remove(temp)
                #temp_fech.pop(x)  
        #print('frec-->', cont, 'fecha-->', temp, end='')
        fech_frec_a = Fecha_Frec(temp, cont)   
        list_fecha.append(fech_frec_a)         
        cont = 0
    for x in list_fecha:
        print(x.fecha, x.frec)        

def para_listCorre():#inserta los correos que reportora a list_correo
    temp_c1 = []
    temp_c2=[]
    for x in list_event:
        c = x.report.split(':')
        temp_c1.append(c[1].strip(' '))
        temp_c2.append(c[1].strip(' '))

    for x in range(len(temp_c1)):
        if len(temp_c1)== 0:
            break
        temp = temp_c1[0]
        for z in range(len(temp_c2)):
            temp2 = temp_c2[z]
            if temp == temp2:
                temp_c1.remove(temp)
        list_correo.append(temp)
    for x in list_correo:
        print(x)
def compara(fecha, correo):
    cont = 0   
    #print(fecha)
    for x in list_event:
        c = x.report.split(':')
        c = c[1].strip(' ')
        #print(x.fecha)
        f = x.fecha.split(',')
        f = f[1].strip(' ')
        if fecha == f and correo == c:
            cont += 1
            
    if cont > 0:
        '''
        print('correo->'+correo, end='')
        print('# correos enviados ',cont)
        print('fecha->'+fecha,end='')
        print('----------')
        '''
        user = Correo_Fecha(correo, fecha, cont)     
        list_CoFe.append(user) 
    
#metodo que recorra list_fecha y comparar esa fecha con fecha de list_event
def reporte():
    cont = 0
    for x in range(len(list_fecha)):
        for y in list_correo:
            compara(list_fecha[x].fecha, y)

    for x in list_CoFe:
        print(x.correo, end ='')
        print(x.fecha,end = '')
        print(x.num_rep)

def rep_user_afectado():
    for x in range(len(list_fecha)):
        cadena = ''
        for z in list_event:
            f = z.fecha.split(',')
            f = f[1].strip(' ')
            if list_fecha[x].fecha == f:
                lista = z.usuarios.split(':')
                lista = lista[1].strip(' ')
                cadena += lista
                #print(lista)
        print(cadena)
        print('----')
read_xml_back()
msj_fecha()
para_listCorre()
reporte()
rep_user_afectado()

    
        

#if __name__ == '__main__':
 #   app.run(debug=True, port=4000)