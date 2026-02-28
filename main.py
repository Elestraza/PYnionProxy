import sys
import requests
import socket
import os
import subprocess
import threading
import signal

def bridges_handler(file_path):
    with open(file_path) as f:
        lines = [line.rstrip('\n') for line in f]
    return lines

PROXIES = {
    'ip':       '127.0.0.1',
    'port':     9051,
    'http':     'socks5h://127.0.0.1:9051',
    'https':    'socks5h://127.0.0.1:9051'
}
session = requests.session()
session.proxies = PROXIES 
print("Tor Proxies: ", session.proxies['http'], session.proxies['https'])

def tor_init():
    user_torrc = input(str("Enter location of your torrc file: "))
    INSTALL_PATH = 'C:\\Users\\Elestraza\\Desktop\\Tor Browser\\Browser\\TorBrowser\\Tor\\tor.exe -f' + user_torrc

    torDeamon = subprocess.Popen(INSTALL_PATH) #, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Tor deamon started on pid: ", torDeamon.pid)

def handle_client(client_socket):
    # Process client requests and send to internet
    pass

def start_proxy(proxies):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((session.proxies['ip'], session.proxies['port']))
    server.listen(100)
    print(f"[*] Listening on {"127.0.0.1"}:{9051}")
    
    while True:
        client_sock, addr = server.accept()
        print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")
        proxy_thread = threading.Thread(target=handle_client, args=(client_sock))
        proxy_thread.start()  

def exit_gracefully(signum, frame):
    signal.signal(signal.SIGINT, original_sigint)
    os.write(sys.stdout.fileno(), b"Terminating TOR deamon...")
    subprocess.Popen.terminate()
    sys.exit(1)

if __name__ == '__main__':
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)
    start_proxy(session.proxies)
    