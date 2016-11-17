#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import thread

HOST = '172.31.219.91' # Endereco IP do Servidor - meu pc
#HOST = '172.17.58.193'  # Endereco IP do Servidor
PORT = 12018        # Porta que o Servidor esta

#tupla do destino
orig = (HOST, PORT)

#cria o socket
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#configura o servidor pra conectar com clientes
tcp.bind(orig)

#lista de grupos
grupos = []

#lista de conexões
conexoes = []

#lista de insdisponíveis
indisponiveis = []

def ausente(con,nick):
    if(jaEstaEmgrupo(nick)):
        msg = nick + ' está ausente'
        enviaMensagemAway(msg, con, nick)
        indisponiveis.append(con)

    else:
        con.send('você precisa estar em um grupo')
    return

#função que verifica se o user já está em algum grupo
def jaEstaEmgrupo(nick):
    #para caad grupo na lista global de grupos
    for i in grupos:
        #para cada registro de um grupo
        for j in i:
            #se há o registro do usuário no grupo retorna true
            if ((j[1] == 0 or j[1] == 1) and j[0] == nick ):
                return True
    return False

#função que kicka o usuário do grupo
def kickar(con, nick, nick_kick):
    for i in grupos:
        if((nick,1,con) in i):
            for j in i:

                if(j[0] == nick_kick):
                    i.remove(j)
                    msg = nick_kick + ' foi kickado'
                    enviaMensagem(msg, con, nick)
                    return

            con.send('o usuário não faz parte do grupo')
            return
        elif((nick,0,con) in i):
            con.send('você precisa ser administrador para executar esse comando')
            return

def banir(con, nick, nick_ban):
    for i in grupos:
        if((nick,1,con) in i):
            for j in i:

                if(j[0] == nick_ban):
                    jcopy = list(j)
                    jcopy[1] = 3
                    i.remove(j)
                    msg = nick_ban + ' foi banido'
                    enviaMensagem(msg, con, nick)
                    i.append(tuple(jcopy))
                    print i
                    return

            con.send('o usuário não faz parte do grupo')
            return
        elif((nick,0,con) in i):
            con.send('você precisa ser administrador para executar esse comando')
            return

#função para deixar o grupo
def deixarGrupo(con, nick):
    #verifica se usuário já tem grupo
    tchuco = jaEstaEmgrupo(nick)
    if(tchuco):
        #procura o grupo e entra nele
        for i in grupos:
            if ((nick,0,con) in i):
                msg = nick + ' saiu do grupo'
                enviaMensagem(msg, con, nick)

                i.remove((nick,0,con))


                return
            if ((nick,1,con) in i):
                msg = 'administrador '+ nick + ' saiu do grupo'
                enviaMensagem(msg, con, nick)

                i.remove((nick,1,con))


                return

    #se não tem grupo
    else:
        con.send('não tá em grupo')
        return

#função para juntarse ao grupo
def juntarSeAGrupo(con,nome_grupo, nick):
    #verifica se usuário já tem grupo
    tchuco = jaEstaEmgrupo(nick)
    if(tchuco):
        con.send('não pode estar em dois grupos diferentes')
        return
    #se não tem grupo
    else:
        #procura o grupo e entra nele
        for i in grupos:
            for j in i:
                if (len(j)==2 and j[1] == 2 and j[0] == nome_grupo):
                    print 'juntare ' + str(i)
                    if((nick,3,con) in i):
                        print 'TÁ NO IF'
                        con.send('você está banido deste grupo')
                        return

                    i.append((nick,0,con))

                    msg = nick + ' juntou-se ao grupo'
                    enviaMensagem(msg, con, nick)
                    return
    #se não avisa ao cliente que o grupo não existe
    con.send('grupo não encontrado')
    return

def enviaMensagemAway(msg, con, nick):
    print 'tá no envia away'
    for i in grupos:
        print 'tá em grupo'
        if(((nick,0,con) in i) or ((nick,1,con) in i)):
            for j in i:
                print 'tá em grupo'
                if(j[1] > 1 or (j[2] in indisponiveis)):
                    continue
                print 'tá em grupo'
                j[2].send(msg)
            return

#função para enviar mensagem
def enviaMensagem(msg, con, nick, nick_dest = None):
    #se o usuário estava ausente sai da lista
    if(con in indisponiveis):
        indisponiveis.remove(con)

    #verifica se a mensagem é pessoal
    if (nick_dest == None):
          #se não for envia para todos
          for i in grupos:
              if(((nick,0,con) in i) or ((nick,1,con) in i)):
                  for j in i:
                      if(j[1] > 1 or (j[2] in indisponiveis)):
                          continue
                      j[2].send(msg)
                  return
    #se for
    else:
          for i in grupos:
              if(((nick,0,con) in i) or ((nick,1,con) in i)):
                  for j in i:
                      if(j[1] > 1):
                          continue

                      elif(j[0] == nick_dest):
                          if(j[2] in indisponiveis):
                              con.send('usuário está ausente')
                              return
                          else:
                              msg = "*MENSAGEM PRIVADA* " + msg
                              con.send(msg)
                              #envia para usuário específico
                              j[2].send(msg)
                              return
                  # se o usuário não está no grupo avisa
                  msg = nick_dest + " não faz parte do seu grupo"
                  con.send(msg)
                  return

#envia a Message Of The Day
def enviaMotd(con):
    #carrega a Message of the day
    motd = open('../file/MOTD.txt','r')
    lines = ''
    for line in motd:
        lines += line

    lines += '\n'
    con.send(line)
    motd.close()
    return

#cria um grupo
def criarGrupo(con,nome_grupo, nick):
    #legenda dos códigos
    #4 é arquivo
    #3 é banido
    #2 é nome do grupo
    #1 é admin
    #0 é usuário normal

    #tupla de identificação do grupo
    nome_novo_grupo = (nome_grupo,2)

    #verifica se o grupo existe
    for i in grupos:

        if (nome_novo_grupo in i):
            con.send('grupo já existe')
            return

    #se não existir cria o grupo
    novo_grupo = []
    novo_grupo.append(nome_novo_grupo)
    novo_grupo.append((nick,1,con))

    grupos.append(novo_grupo)

    con.send('grupo criado')

    return

#lista os grupos se já está em um grupo lista os membrs do grupo
def listar(con, nick):
    lista = []

    if (jaEstaEmgrupo(nick)):
        for i in grupos:
              if(((nick,0,con) in i) or ((nick,1,con) in i)):
                  for j in i:
                      if((len(j)>2) and j[1]!=3):
                          lista.append(j[0])
        con.send(str(lista))
        return
    else:
        #coloca cada grupo existente em uma lista
        for i in grupos:

            for j in i:

                if (j[1] == 2 and len(j)==2):
                    lista.append(j[0])
                    break
                else:
                    continue

        #imprime a lista
        con.send(str(lista))
        return

def parser(mensagem, con, cliente, nick):
    msg = mensagem
    mensagem = mensagem.split(' ', 1)

    if mensagem[0] == '/quit':
        fecharConexao(con, cliente)
        return

    elif mensagem[0] == '/help':
        enviaMotd(con)
        return

    elif mensagem[0] == '/nick':
        novo_nick = str(mensagem[1]).strip()
        return

    elif mensagem[0] == '/leave':
        print 'comando /leave'
        deixarGrupo(con, nick)
        return

    elif mensagem[0] == '/list':
        listar(con, nick)
        print 'comando /list'
        return

    elif mensagem[0] == '/join':
        juntarSeAGrupo(con,mensagem[1], nick)
        print 'comando /join'
        return

    elif mensagem[0] == '/create':
        criarGrupo(con,mensagem[1],nick)
        print 'comando /create'
        return

    elif mensagem[0] == '/delete':
        print 'comando /delete'
        return

    elif mensagem[0] == '/away':
        print 'comando /away'
        print grupos
        print indisponiveis
        ausente(con,nick)
        return

    elif mensagem[0] == '/msg':
        mensagem = mensagem[1].split(' ', 1)
        msg = nick + ': ' + mensagem[1]
        enviaMensagem(msg, con, nick, mensagem[0])
        return

    elif mensagem[0] == '/ban':
        print 'comando /ban'
        banir(con, nick, mensagem[1])
        return

    elif mensagem[0] == '/kick':
        print 'comando /kick'
        kickar(con, nick, mensagem[1])
        return

    elif mensagem[0] == '/file':
        print 'comando /file'
        receberArquivo(con,mensagem[1],nick)
        return


    elif mensagem[0] == '/list_files':
        print 'comando /list_files'
        listarArquivos(con, nick)
        return

    elif mensagem[0] == '/get_file':
        print 'comando /get_file'
        mandarArquivo(con,mensagem[1],nick)
        return
    else:
        #se não for nenhum comando assume-se que é uma mensagem
        #verifica se o usuário está em algum grupo
        if(jaEstaEmgrupo(nick)):
            #se está envia mensagem ao grupo
            msg = nick + ': ' + msg
            enviaMensagem(msg, con, nick)
            return
        #se não avisa que precisa fazer parte de um grupo para enviar mensagem
        con.send('você precisa fazer parte de um grupo para mandar mensagem!')
        return

#comando delete
def deletarGrupo(con, cliente, nome_grupo):
    #verificar se o grupo existe
    for i in grupos:
        if (i[0] == (nome_grupo,2)):
            for j in i:
                if (j[1] < 1 or j[1] == 3):
                    con.send('o grupo deve estar vazio')
                    return
            grupos.remove(i)
            con.send('grupo deletado')
            return

    con.send('grupo não existe')
    return


def fecharConexao(con, cliente):
    print 'Finalizando conexao do cliente', cliente
    con.close()
    return


def conectado(con, cliente):
    print 'Conectado por', cliente

    conexoes.append((cliente,con))

    nick = buscaNick(cliente,con)

    enviaMotd(con)

    while 1:
        nick = buscaNick(cliente,con)
        msg = con.recv(1024)

        if msg != '':
            print nick, cliente, msg
            parser(msg, con , cliente, nick)




    fecharConexao(con, cliente)
    thread.exit()

#busca o nick do cliente na base de dados
def buscaNick(cliente,con):
    #enquanto o usuário não tem um nick
    while 1:
        #abre a base de dados
        base = open('../file/users.txt','r')
        database = ''
        #busca pelo nick
        for line in base:
            database = line.split('%')

        base.close()
        for par in database:
            verifica = par.split('=')

            if verifica[0] == str(cliente):
                return verifica[1]
        #se o nick não existe obriga o cliente a criar um nick
        criarNick(cliente,con)

#função onde o servidor pergunta ao cliente e recebe a resposta
def solicita(con,msg):
    con.send(msg)
    ret = con.recv(1024)
    return ret
#cria o nickname
def criarNick(cliente,con):
    #abre a abase de dados
    database = open('../file/users.txt','a')
    #pede o nick para o cliente
    nick = solicita(con,'informe o seu nick:')
    #coloca o nick no formato da base de dados
    registro = str(cliente)+'='+str(nick)+'%'

    #persiste os dados e fecha a base de dados
    database.write(registro)
    database.close()

    return
#atualiza o nick
def atualizaNick(cliente, nick, novo_nick):
    database = open('../file/users.txt','r')
    #coloca os dados do antigo registro no formato da base
    antigo = str(cliente)+'='+str(nick)+'%'
    #coloca os dados do novo registro no formato da base
    novo = registro = str(cliente)+'='+str(novo_nick)+'%'

    database_novo = ''

    for line in database:
        #faz o replace do registro
        database_novo = str(line).replace(antigo,novo)

    database.close()

    #abre a base para escrita e persiste
    database = open('../file/users.txt','w')
    database.write(database_novo)
    database.close()

    return

def receberArquivo(con,nome_arquivo,nick):
    if(jaEstaEmgrupo(nick)):
        nome_arquivo = nome_arquivo.split('/')
        nome_arq = nome_arquivo[(len(nome_arquivo)-1)]

        for i in grupos:
            if(((nick,0,con) in i) or ((nick,1,con) in i)):
                i.append((nome_arq,4))

        caminho = '../file/files/'+nome_arq

        arq = open(caminho, 'wb')

        dados = con.recv(1024)
        while dados:

            print dados

            arq.write(dados)

            print 'iterou'
            if ('Mc Livinho' in dados):
                break

            dados = con.recv(1024)


        arq.close()
        con.send('enviado com sucesso!')
        return

    else:
        con.send('você precisa fazer parte de um grupo!')
        return

def listarArquivos(con, nick):
    if(jaEstaEmgrupo(nick)):
        lista = []
        for i in grupos:
            if(((nick,0,con) in i) or ((nick,1,con) in i)):
                for j in i:
                    if j[1] == 4:
                        lista.append(j[0])
        con.send(str(lista))
        return
    else:
        con.send('você precisa fazer parte de um grupo!')
        return

def mandarArquivo(con,nome_arquivo,nick):
    if(jaEstaEmgrupo(nick)):

        for i in grupos:
            if(((nick,0,con) in i) or ((nick,1,con) in i)):
                for j in i:
                    if j == (nome_arquivo,4):
                        caminho = '../file/files/'+nome_arquivo
                        arq = open(caminho, 'rb')

                        for i in arq.read():
                            print i
                            con.send(i)

                        arq.close()
                        con.send('Mc Livinho')
                        return

            con.send('arquivo non ecxist')
            return

    else:
        con.send('você precisa fazer parte de um grupo!')
        return

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
