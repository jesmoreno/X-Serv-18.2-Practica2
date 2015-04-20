# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound
from models import urlsStored
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def sizeDB():
    size = 0
    
    dataBase = urlsStored.objects.all()
    for fila in dataBase:
        size = size+1    
    return size

@csrf_exempt
def server(request,recurso):
    verb = request.method    

    #Guardo las paginas reales y acortadas y calculo numero elementos
    pagReal = ""
    pagAcortada = ""    
    dataBase = urlsStored.objects.all()
    for fila in dataBase:
        
        pagReal += "<a href= "+fila.pagina+">"+ fila.pagina+"</a></p>"
        pagAcortada += "<a href=http://localhost:1234/"+str(fila.numPagina)+">"+"http://localhost:1234/"+str(fila.numPagina)+"</a></p>"

    if recurso == '':
        
        if verb == 'GET':
            response = ("<html>"
                        "<body bgcolor= #8181F7>"
                        "<h1>CORTADOR DE URL'S</h1>" +
                        "<form name= search  action= /  method= POST >" +
                        "Insertar URL: <input type= text  name= url >" +
                        "<input type= submit value= Buscar >" +
                        "<hr>"+
                        "<table align = center border=1>"+
                        "<td bgcolor = #BDBDBD>" +"URL'S REALES"+"</td>"+
                        "<td bgcolor = #BDBDBD>" +"URL'S ACORTADAS"+"</td>"+
                        "<tr><td bgcolor= #FBFBEF>"+
                        pagReal +
                        "<td bgcolor= #FBFBEF>"+ 
                        pagAcortada +
                        "</td></table>"+
                        "</body>"
                        "</html>")
            return HttpResponse(response)

        elif verb == 'POST':
            
            body = request.body
            url = body.split('=')[1]

            #Sustituyo la parte del string con caracteres especiales(: = %3A,// = %2F%2F)
            if(url == ("http%3A%2F%2F" + url[13:]) or url == ("https%3A%2F%2F" + url[14:])):

                url =url.replace("%3A",':')
                url =url.replace("%2F",'/')
                    
            else:
                #Completo la url si no empieza por http o https
                url = "http://" + url
            
            #Miro si contiene la pagina y sino la añado
            try:        
                urlsStored.objects.get(pagina = url)
            except urlsStored.DoesNotExist:
                num = sizeDB()
                newPage = urlsStored(pagina = url, numPagina = num)
                newPage.save()

            #Genero los Strings de la pagina real y acortada para imprimir
                  
            page = urlsStored.objects.get(pagina = url) 
            paginaAcortada = "http://localhost:1234/"+str(page.numPagina)
         
            response = ("<html>"
                        "<body bgcolor= #8181F7>"
                        "<h1>CORTADOR DE URL'S</h1>" +
                        "<table border=1>"+
                        "<td bgcolor = #BDBDBD>" +"Real"+"</td>"+
                        "<td bgcolor = #BDBDBD>" +"Acortada"+"</td>"+
                        "<tr><td bgcolor= #FBFBEF>"+
                        "<a href="+url+">"+page.pagina+"</a></p>"+
                        "<td bgcolor= #FBFBEF>"
                        "<a href="+paginaAcortada+">"+paginaAcortada+"</a></p>"
                        "</td></table>"+
                        "<hr>"+
                        "<form method= get action= http://localhost:1234>"
                        "<input type= submit  value= Volver a pagina inicial/>"+
                        "</form>"
                        "</body>"
                        "</html>")    

            return HttpResponse(response)

    else:

        try:        
            page = urlsStored.objects.get(numPagina = recurso)
            url = page.pagina
            return HttpResponse("<html>"
                                "<h1>"
                                "HTTP REDIRECT"
                                "</h1>"
                                "<head>"
                                "<meta http-equiv= Refresh  content= 2;url="+url+">"
                                "</head>"
                                "<body>"
                                "<p>URL ="+ url +"</p>"
                                "</body>"
                                "</html>")

        except urlsStored.DoesNotExist:
            return HttpResponseNotFound("<html>"
                                        "<h1>Error 404</h1>"
                                        "<p>Page not found</p>"
                                        "</html>")
        except:
            return HttpResponseNotFound("<html>"
                                        "<h1>Error 404</h1>"
                                        "<p>Page not found</p>"
                                        "</html>")
