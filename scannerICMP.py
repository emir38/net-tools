#!/usr/bin/env python3

import argparse
import subprocess
import signal
import sys
from concurrent.futures import ThreadPoolExecutor

def def_handler(sig,frame):
    print(f"\n Saliendo del programa... \n")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def get_arguments():
    parser = argparse.ArgumentParser(description="Herramienta para descubrir hosts activos en una red (ICMP)")
    parser.add_argument("-t", "--target", required=True, dest="target", help="Host o rango de red a escanear")

    args = parser.parse_args()

    return args.target

def parse_target(target_str):
    
    target_str_splitted = target_str.split('.')
    first_three_octets = '.'.join(target_str_splitted[:3])

    if len(target_str_splitted) == 4:
        if "-" in target_str_splitted[3]:
            start, end = target_str_splitted[3].split('-')
            return [f"{first_three_octets}.{i}" for i in range(int(start), int(end)+1)]
        else:
            return [target_str]
    else:
        print(f"\n El formato de IP o rango de IP no es valido\n")

def host_discovery(targets):
    try:
        ping = subprocess.run(["ping", "-c", "1", targets], timeout=1, stdout=subprocess.DEVNULL)

        if ping.returncode == 0:
            print(f"\t La IP {targets} esta activa")
    except subprocess.TimeoutExpired:
        pass
    except Exception as e:
        print(f"\n Error al ejecutar ping para {target}: {e}")

def main():

    target_str = get_arguments()
    targets = parse_target(target_str)

    print(f"\n Host activos en la red: \n")

    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(host_discovery, targets)

if __name__ == '__main__':
    main()
