#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import thread
import os


HOST = '192.168.0.13'      # Endereco IP do Servidor
#HOST = '172.17.58.193'
PORT = 12111       # Porta que o Servidor esta

#cria o socket
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#tupla do destino
dest = (HOST, PORT)
#cria a conexão
tcp.connect(dest)

def receber (a,c):
    while receber:
        #recebe a resposta do Servidor
        recebido = tcp.recv(1024)
        print recebido
while 1:

    thread.start_new_thread(receber, ('',''))

    #pega a mensagem do usuário
    msg = raw_input()

    mensagem = msg.split(' ', 1)
    #se o usuário quiser sair sai
    if mensagem[0] == '/quit':
       tcp.close()
       break
    #se quiser limpar limpa
    elif mensagem[0] == '/clear':
        os.system('cls' if os.name == 'nt' else 'clear')

    #se quiser mandar arquivo
    elif mensagem[0] == '/file':
        tcp.send (msg)

        arq = open(mensagem[1], 'rb')

        for i in arq.read():
            tcp.send(i)

        arq.close()
        tcp.send('Mc Livinho')

    #se quiser receber
    elif mensagem[0] == '/get_file':
        tcp.send (msg)

        caminho = '../file/'+mensagem[1]

        arqo = open(caminho, 'wb')

        while 1:
            dados = tcp.recv(1024)
            print dados

            if ('Mc Livinho' in dados):
                print 'brecou'
                break

            arqo.write(dados)


        arqo.close()

    #envia a mensagem
    else:
        tcp.send (msg)
