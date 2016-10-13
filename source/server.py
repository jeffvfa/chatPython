#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import thread

#HOST = '192.168.1.107' # Endereco IP do Servidor - meu pc 
HOST = '172.17.40.173'  # Endereco IP do Servidor
PORT = 12005        # Porta que o Servidor esta

#tupla do destino
orig = (HOST, PORT)


def solicita(con, msg): 
    con.send(msg) 
    return con.recv(1024)

def parser(mensagem, con, cliente, nick):
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
        novo_nick = mensagem[1]
        atualizaNick(cliente, nick, novo_nick)
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
    
    nick = buscaNick(cliente,con)
    
    for line in motd:
        con.send(line)

    while True:
        nick = buscaNick(cliente,con)
        msg = con.recv(1024)

        if msg <> '':
            print nick, cliente, msg
            parser(msg, con , cliente, nick)
            con.send(msg.upper())
        
        



    print 'Finalizando conexao do cliente', cliente
    con.close()
    thread.exit()

def buscaNick(cliente,con): 
    while 1:
        base = open('../file/users.txt','r') 
        database = ''
        for line in base:
            database = line.split('%') 
    
        base.close()
        for par in database: 
            verifica = par.split('=') 
            
            if verifica[0] == str(cliente): 
                return verifica[1] 
        criarNick(cliente,con)
            

def criarNick(cliente,con): 
    database = open('../file/users.txt','a') 
    nick = solicita(con,'informe o seu nick:') 
    registro = str(cliente)+'='+str(nick)+'%'  

    database.write(registro)  
    database.close() 
    
    return

def atualizaNick(cliente, nick, novo_nick): 
    database = open('../file/users.txt','r') 
    antigo = str(cliente)+'='+str(nick)+'%'
    novo = registro = str(cliente)+'='+str(novo_nick)+'%'
    
    database_novo = ''
    
    for line in database:
        database_novo = str(line).replace(antigo,novo)
    
    database.close() 
    
    database = open('../file/users.txt','w') 
    database.write(database_novo)
    database.close() 

    return

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