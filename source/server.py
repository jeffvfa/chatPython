#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import thread

HOST = '192.168.1.107'
PORT = 12001
orig = (HOST, PORT)

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

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp.bind(orig)

motd = open('file/MOTD.txt','r')

def main():
    tcp.listen(1)

    while True:
        con, cliente = tcp.accept()
        thread.start_new_thread(conectado, tuple([con, cliente]))

    tcp.close()

if __name__ == "__main__":
    main()
