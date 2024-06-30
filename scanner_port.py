#!/usr/bin/env python3

import socket
import argparse
import signal
import sys
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored

timeout = 0.1

open_sockets = []

def def_handler(sig, frame):
    print(colored(f"\n Saliendo del programa...", 'red'))

    for socket in open_sockets:
        socket.close()

    sys.exit(1)

signal.signal(signal.SIGINT, def_handler) # Ctrl+C

def get_arguments():
    parser = argparse.ArgumentParser(description = 'Fast TCP Port Scanner')
    parser.add_argument("-t", "--target", dest="target", required=True, help="Victim target to scan (Ex: -t 192.168.100.100)")
    parser.add_argument("-p", "--port", dest="port", required=True, help="Port target to scan (Ex: -p 1-100, -p 10,22,80,122 or -p 53)")
    options = parser.parse_args()

    return options.target, options.port

def create_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    open_sockets.append(s)

    return s

def port_scanner(port, host):

    s = create_socket()

    try:
        s.connect((host, port))
        print(colored(f"\n El puerto {port} esta abierto", 'green'))
        s.sendall(b"HEAD / HTTP/1.1\r\n\r\n")
        response = s.recv(1024)
        response = response.decode(errors='ignore').split('\n')[0]

        if response:
            print(colored(f"\n El puerto {port} esta abierto - {response}", 'green'))
        else:
            print(colored(f"\n El puerto {port} esta abierto", 'green'))

        s.close()
    except (socket.timeout, ConnectionRefusedError):
        s.close()

def scan_ports(ports,target):
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(lambda port: port_scanner(port, target), ports)

def parse_ports(port):

    if '-' in port:
        start, end = map(int, port.split('-'))
        return range(start, end+1)

    elif ',' in port:
        return map(int, port.split(','))

    else:
        return (int(port),)

def main():
    
    target, port = get_arguments()
    ports = parse_ports(port)
    scan_ports(ports,target)



if __name__ == '__main__':
    main()
