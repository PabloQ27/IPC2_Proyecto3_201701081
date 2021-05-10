from django.http import HttpResponse
from django.template import Template, Context
from django.template import loader
from django.template import RequestContext
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
import xml.etree.ElementTree as ET
import re
import requests
from .forms import Archivo

endpoint = "http://127.0.0.1:4000/"

def home(request): 
    if request.method == 'POST':
        archivo = request.FILES['documento'].read()    
        print(archivo)     
        n = str(archivo).replace('\\n', '\n')
        r = n.replace('\\r', '\r')
        x = r.replace('\\x', '')
        x= x.replace("'",'')
        x = x.replace('b', '', 1)
        cadena = x.replace('\\t', '    ')

        #print(cadena)
        c = {"archivo_xml": cadena}  
        r = requests.post(endpoint+'doc', json=c)

        return render(request, "index.html", c)
        #return HttpResponse(archivo)
    doc_index = loader.get_template('index.html')
    docin = doc_index.render()
    return render(request, "index.html")
 
def cargar_el_xml(request):
    r = requests.get(endpoint+'devolver')
    doc = {'xml_salida': r.text}
    return render(request, "index.html", doc)

def carga_documento(request):
    
    x = requests.get(endpoint+'docsito')
    print(x.text)
    myobj = {'xml_salida': x.text}
    
    return render(request, "index.html", myobj)
        


