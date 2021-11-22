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
import json
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
    global res
    res = request.json
    res = json.loads(res)
    return res["SOLICITUD_AUTORIZACION"]


@app.route('/devolver', methods = ['GET'])
def pasar_xml():
    read_json()
    return res["SOLICITUD_AUTORIZACION"]["DTE"][0]

def read_json():
    print(len(res["SOLICITUD_AUTORIZACION"]["DTE"]))
    
if __name__ == '__main__':
    app.run(debug=True, port=4000)
