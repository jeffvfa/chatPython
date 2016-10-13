#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket

#HOST = '192.168.1.107'      # Endereco IP do Servidor
HOST = '172.17.40.173'
PORT = 12005        # Porta que o Servidor esta

#cria o socket
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#tupla do destino
dest = (HOST, PORT)
#cria a conexão
tcp.connect(dest)

while 1:
    #recebe a resposta do Servidor
    recebido = tcp.recv(1024)
    print recebido

    #pega a mensagem do usuário
    msg = raw_input()

    #se o usuário quiser sair sai
    if msg == '/quit':
       tcp.close()
       break
    #envia a mensagem
    tcp.send (msg)
