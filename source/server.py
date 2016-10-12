#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import thread

HOST = '192.168.1.107' # Endereco IP do Servidor
PORT = 12001        # Porta que o Servidor esta

#tupla do destino
orig = (HOST, PORT)

def parser(mensagem, con):
    msg = mensagem
    mensagem = mensagem.split(' ', 1)

    if mensagem[0] == '/quit':
        print 'comando /quit'
        return

    elif mensagem[0] == '/help':
        print 'comando /help'
        return

    elif mensagem[0] == '/nick':
        print 'comando /nick'
        return

    elif mensagem[0] == '/leave':
        print 'comando /leave'
        return

    elif mensagem[0] == '/list':
        print 'comando /list'
        return

    elif mensagem[0] == '/join':
        print 'comando /join'
        return

    elif mensagem[0] == '/create':
        print 'comando /create'
        return

    elif mensagem[0] == '/delete':
        print 'comando /delete'
        return

    elif mensagem[0] == '/away':
        print 'comando /away'
        return

    elif mensagem[0] == '/msg':
        print 'comando /msg'
        return

    elif mensagem[0] == '/ban':
        print 'comando /ban'
        return

    elif mensagem[0] == '/kick':
        print 'comando /kick'
        return

    elif mensagem[0] == '/clear':
        print 'comando /clear'
        return

    elif mensagem[0] == '/file':
        print 'comando /file'
        return


    elif mensagem[0] == '/list_files':
        print 'comando /list_files'
        return

    elif mensagem[0] == '/get_file':
        print 'comando /get_file'
        return
    else:
        print "nenhum comando"
        

def conectado(con, cliente):
    print 'Conectado por', cliente
    for line in motd:
        con.send(line)

    while True:
        msg = con.recv(1024)

        if msg <> '':
            print cliente, msg
            parser(msg,con)
            con.send(msg.upper())




    print 'Finalizando conexao do cliente', cliente
    con.close()
    thread.exit()

#cria o socket
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#configura o servidor pra conectar com clientes
tcp.bind(orig)

#carrega a Message of the day
motd = open('../file/MOTD.txt','r')

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
