import socket
import sys


def ts1():
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Server 1 created")
    dnsip, dnstype = {}, {}

    f = open('PROJ2-DNSTS1.txt', 'r')
    for l in f:
        line = l.strip().split()
        dnsip[line[0]] = line[1]
        dnstype[line[0]] = line[2]

    port = int(sys.argv[1])
    sbind = ('',  port)
    ss.bind(sbind)
    ss.listen(1)
    csockid, addr = ss.accept()
    print('Connection successful')

    while True:
        q = csockid.recv(256).decode('utf-8')
        if q == 'EOF':
            break
        if q:
            for key in dnsip:
                if key.lower() == q.lower():
                    result_string = key + " " + \
                        dnsip[key] + " " + dnstype[key] + " IN"
                    csockid.send(result_string.encode('utf-8'))
                    break
    ss.close()
    exit()

ts1()