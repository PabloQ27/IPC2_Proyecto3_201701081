from django.http import HttpResponse
from django.template import Template, Context
from django.template import loader
from django.template import RequestContext
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
import xml.etree.ElementTree as ET
import re

def format(cadena):
    mydoc = ET.tostring(archivo, 'utf-8').decode('utf8')
    reescribe = minidom.parseString(mydoc)
    return reescribe.toprettyxml(indent="  ")

def home(request):
    if request.method == 'POST':
        archivo = request.FILES['documento'].read()
        
        n = str(archivo).replace('\\n', '\n')
        r = n.replace('\\r', '\r')
        x = r.replace('\\x', '')
        x= x.replace("'",'')
        cadena = x.replace('\\t', '    ')
        print(cadena)

        c = ({"archivo_xml": cadena})      
        return render(request, "index.html", c)
        #return HttpResponse(archivo)
    doc_index = loader.get_template('index.html')
    docin = doc_index.render()
    return render(request, "index.html")
   


def carga_documento(request):
    c = {}
    print("..............")
    archivo = request.FILES['documento']
    print(archivo)
    return HttpResponse(archivo)
        


