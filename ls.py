import threading
import socket
import sys
import select


def ls():
    ts1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ts2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('LS server created')

    ts1hostname = socket.gethostbyname(sys.argv[2])
    ts1port = int(sys.argv[3])
    ts2hostname = socket.gethostbyname(sys.argv[4])
    ts2port = int(sys.argv[5])

    ts1bind = (ts1hostname, ts1port)
    ts1.connect(ts1bind)
    ts2bind = (ts2hostname, ts2port)
    ts2.connect(ts2bind)
    print('Connection successful')

    lsport = int(sys.argv[1])
    lsbind = ('', lsport)
    ss.bind(lsbind)
    ss.listen(1)
    lshostname = socket.gethostname()
    csockid, addr = ss.accept()
    servers = [ts1, ts2]

    while True:
        q = csockid.recv(256).decode('utf-8')
        if q == 'EOF':
            ts1.send('EOF'.encode('utf-8'))
            ts2.send('EOF'.encode('utf-8'))
            break
        ts1.send(q.encode('utf-8'))
        ts2.send(q.encode('utf-8'))
        inp, out, exc = select.select(servers, [], [], 5.0)
        if inp:
            s = inp[0]
            data = s.recv(256)
            response = data.decode('utf-8')
            csockid.send(response.encode('utf-8'))
        else:
            response = q + " - TIMED OUT\n"
            csockid.send(response.encode('utf-8'))

    ss.close()
    ts1.close()
    ts2.close()
    exit()

t1 = threading.Thread(name='ls', target=ls)
t1.start()