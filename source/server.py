#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import thread

HOST = '192.168.1.107' # Endereco IP do Servidor
PORT = 12001        # Porta que o Servidor esta

#tupla do destino
orig = (HOST, PORT)

def parse():
    break

def conectado(con, cliente):
    print 'Conectado por', cliente
    for line in motd:
        con.send(line)

    while True:
        msg = con.recv(1024)
        if not msg: break
        con.send(msg.upper())
        print cliente, msg


    print 'Finalizando conexao do cliente', cliente
    con.close()
    thread.exit()

#cria o socket
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#configura o servidor pra conectar com clientes
tcp.bind(orig)

#carrega a Message of the day
motd = open('file/MOTD.txt','r')

#funçãao main
def main():
    #coloca o servidor para "escutar"
    tcp.listen(1)

    while True:
        #aceita a conexao do cliente
        con, cliente = tcp.accept()
        #cria uma nova thread para cada conexão
        thread.start_new_thread(conectado, tuple([con, cliente]))

    tcp.close()

if __name__ == "__main__":
    main()
