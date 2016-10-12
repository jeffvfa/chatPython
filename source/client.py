import socket
HOST = '192.168.1.107'      # Endereco IP do Servidor
PORT = 12001        # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)
print 'Para sair digite /quit'

while 1:
    msg = raw_input()
    if msg == '/quit':
        tcp.close()
        break
    tcp.send (msg)
    recebido = tcp.recv(1024)
    print recebido
