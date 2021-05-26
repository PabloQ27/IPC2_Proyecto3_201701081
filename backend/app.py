from flask import Flask, Response, request
import xml.etree.ElementTree as ET
from xml.dom import minidom
import requests
import re
from evento import Evento
from fecha_frec import Fecha_Frec
from correo import Correo_Fecha
from error import Error
from n_error import N_Error
from user_afec import User_Afect
app = Flask(__name__)

@app.route('/')
def index():
    return 'hola mundo'

@app.route('/prueba')
def p():
    print('hi////////')
    return ("esta la prueba pal endpoint xd")

@app.route('/doc', methods = ['POST'])
def leer_xml():
    res = request.json
    text = res['archivo_xml']
    myfile = open('xmltemp.xml', 'w') 
    myfile.write(text)
    #print(text)
    #read_xml_back()
    print('-----')
    return res


@app.route('/devolver', methods = ['GET'])
def pasar_xml():
    read_xml_back()
    msj_fecha()
    para_listCorre()
    reporte()
    rep_user_afectado()
    errores()
    compara_error()
    comparar2()
    genera_XML()
    print('--------------------------')
    #print(xmlsalida)
    return xmlsalida
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

xmlsalida = ''
list_fecha = [] #--1-P/XML---almacena objetos fecha_frec fechas sin repetir y cada una con la cantidad de msj enviados esa fecha
list_correo = [] # todos los correos que reportaron, estan sin repetir correos 
list_CoFe = [] # ---2-P/XML----almacena objetos correo los correos con sus fechas y contadores
list_error = []#alamcena objetos error  con la fecha y el error
list_error2 = []
list_error3 = []#---4-P/XML  almacena los codigo de error con su frecuencia y fecha con objetos n_error
list_user_afec = []#---3-P/XML---almacena usuarios afectados con objetos user_afec

#---NT---ingresa las fechas y sus frecuencias(cantidad de msj enviados esa fecha) a list_fecha
def msj_fecha():
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
    #for x in list_fecha:
    #    print(x.fecha, x.frec)        


#-----NT-----inserta los correos que reportora a list_correo
def para_listCorre():
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
    #for x in list_correo:
    #    print(x)


#----NT----
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
    

#----NT-----metodo que recorra list_fecha y comparar esa fecha con fecha de list_event
def reporte():
    cont = 0
    for x in range(len(list_fecha)):
        for y in list_correo:
            compara(list_fecha[x].fecha, y)
    '''
    for x in list_CoFe:
        print(x.correo, end ='')
        print(x.fecha,end = '')
        print(x.num_rep)
    '''


#------NT--------
def delete_duplica(cadena, fecha):
    array = cadena.split(',')
    temp_c1 = []
    temp_c2 = []
    for x in array:
        #print(x.strip(" "))
        temp_c1.append(x.strip(" "))
    user_afec = User_Afect(temp_c1, fecha)
    list_user_afec.append(user_afec)

#----NT-----
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
        #print(cadena)
        delete_duplica(cadena,list_fecha[x].fecha)
        #print('----')


#----NT----------
def errores():
    for x in list_event:
        e = x.error.split(':')
        e = e[1].split('-')
        e = e[0].strip(' ')
        f = x.fecha.split(',')
        f = f[1].strip(' ')
        #print(e, f, end = '')
        er = Error(f, e)
        list_error.append(er)
    cont = 0

#---NT----
def compara_error():
    temp_e1 = []
    temp_e2 = []
    for x in list_error:
        temp_e1.append(x.error)
        temp_e2.append(x.error)

    for x in range(len(temp_e1)):
        if len(temp_e1) == 0:
            break
        temp = temp_e1[0]
        for z in range(len(temp_e2)):
            temp2 = temp_e2[z]
            if temp == temp2:
                temp_e1.remove(temp)
        list_error2.append(temp)
        #print(temp)    

def comparar2():
    for x in range(len(list_fecha)):
        for y in list_error2:
            cont = 0
            for z in list_event:
                f = z.fecha.split(',')
                f = f[1].strip(' ')
                e = z.error.split(':')
                e = e[1].split('-')
                e = e[0].strip(' ')
                if list_fecha[x].fecha == f and e == y:
                    cont +=1
                    
            if cont > 0:  
                '''
                print(list_fecha[x].fecha, end='')
                print('error -->'+y+' # en esa fecha-->',cont)
                print('----')
                '''
                errorf = N_Error(list_fecha[x].fecha, y, cont)
                list_error3.append(errorf)   
            cont = 0
            '''
    for x in list_error3:
        print(x.fecha, end='')
        print(x.error,'  ', x.cont)
'''

def format(cadena):
    #mydoc = ET.tostring(cadena, 'utf-8').decode('utf8')
    mydoc = ET.tostring(cadena, 'utf-8' )
    reescribe = minidom.parseString(mydoc)
    return reescribe.toprettyxml(indent="   ")

def genera_XML():
    global xmlsalida
    root = ET.Element('ESTADISTICAS')
    est = ET.SubElement(root, 'ESTADISTICA')
      
    for x in list_fecha:
        fech = ET.SubElement(est, 'FECHA')
        fech.text = x.fecha.strip('\n')
    
        cm = ET.SubElement(est, 'CANTIDAD_MENSAJES')
        cm.text = str(x.frec)

        rep_por = ET.SubElement(est, 'REPORTADO_POR')  
        
       
        for z in list_CoFe:
            if x.fecha == z.fecha:
                user = ET.SubElement(rep_por, 'USUARIO')
                email = ET.SubElement(user, 'EMAIL')
                email.text = z.correo.strip('\n')
                
                fech2 = ET.SubElement(user, 'CANTIDAD_MENSAJES')
                fech2.text = str(z.num_rep)
        
   
        #falta el listado de usuarios

        err = ET.SubElement(est,'ERRORES')
        for z in list_error3:
            
            if x.fecha == z.fecha:
                err2 = ET.SubElement(err, 'ERROR')
                err3 = ET.SubElement(err2, 'CODIGO')
                err3.text = z.error

                mjs = ET.SubElement(err2, 'CANTIDAD_MENSAJES')
                mjs.text = str(z.cont)
         
    texto = format(root)
    #texto = ET.tostring(root)
    myfile = open('Estadistica.xml', 'w')
    xmlsalida = texto
    myfile.write(texto)

'''  
read_xml_back()
msj_fecha()
para_listCorre()
reporte()
rep_user_afectado()
errores()
compara_error()
comparar2()
genera_XML()
print(xmlsalida)
''' 
        

if __name__ == '__main__':
    app.run(debug=True, port=4000)
