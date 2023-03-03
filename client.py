import socket
import sys


def client():
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Client created")

    argv = sys.argv[1:]
    hostname = socket.gethostbyname(argv[0])
    port = int(argv[1])

    server_binding = (hostname, port)
    cs.connect(server_binding)

    hn = open('PROJ2-HNS.txt', 'r')
    domains = hn.readlines()

    for domain in domains:
        domain = domain.strip()
        print("Domain: " + domain)
        cs.send(domain.encode('utf-8'))
        response = cs.recv(256).decode('utf-8').strip()
        resolved.append(response)
        print("Response: " + response)

    cs.send("EOF".encode('utf-8'))
    cs.close()

    file = open('RESOLVED.txt', 'w')
    for r in resolved:
        file.write(str(r)+'\n')

    exit()

resolved = []
client()
