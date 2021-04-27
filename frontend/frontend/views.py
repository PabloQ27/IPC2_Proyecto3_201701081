from django.http import HttpResponse
from django.template import Template, Context
from django.template import loader

def prueba(request):
    doc_index = loader.get_template('index.html')
    #ctx= Context(doc_index)
    docin = doc_index.render()

    return HttpResponse(docin)