import http.client
import os
import sys
import requests
import socket
import urllib.request
import socketserver
import socks
import signal
import TorHandlerClass

PROXIES = {
    'ip':       '127.0.0.1',
    'port':     9150
}

# --- Configuration ---
PROXY_HOST = "localhost"
PROXY_PORT = 8888  # Port your custom proxy will listen on
TOR_SOCKS_PROXY = "127.0.0.1"
TOR_SOCKS_PORT = 9150

session = requests.Session()
session.proxies = PROXIES 
print("Tor Proxies: ", session.proxies)

def start_proxy(proxies):
    socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, TOR_SOCKS_PROXY, TOR_SOCKS_PORT, True)
    socket.socket = socks.socksocket
    print("Connected to TOR network...")

    conn = http.client.HTTPConnection(host="2ip.ru")
    conn.request('GET', "/")
    responce = conn.getresponse()
    print(responce.read())

def exit_gracefully(signum, frame):
    signal.signal(signal.SIGINT, original_sigint)
    os.write(sys.stdout.fileno(), b"Terminating TOR deamon...")
    sys.exit(1)

def main():
    start_proxy(session.proxies)

if __name__ == '__main__':
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, exit_gracefully)
    TorProxyHandler = TorHandlerClass()
    with socketserver.TCPServer((PROXY_HOST, PROXY_PORT), TorProxyHandler) as httpd:
        print(f"Tor proxy serving at {PROXY_HOST}:{PROXY_PORT}")
        httpd.serve_forever()
    main()