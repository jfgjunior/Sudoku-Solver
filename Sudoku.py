# -*- coding: utf-8 -*-
#José Fernando Garcia Junior E-mail: jf.junior18@hotmail.com

import networkx as nx
import numpy as np
import os.path as ph
from sys import exit

def main():
    '''
    Função: Faz as chamadas para manipulação do jogo buscando a resolução automática
            do jogo sudoku
    Parametros: -
    Retorno: -
    '''
    #Verifica se o arquivo já existe e atribui o grafo da matriz de adjacencia à variável grafo
    if ph.exists('matriz_adjacencia.txt'):
        grafo = gera_grafo()
    else:
        grafo = matriz_adjacencia()  
    
    nome_arq_sudoku = raw_input('Digite o caminho e o nome do arquivo, se o arquivo já se encontra na pasta do projeto basta o nome do arquivo e a extenção \".txt\"\nNome: ')
    #Entrada da configuração inicial do jogo
    valores_iniciais(grafo,nome_arq_sudoku)
    #Modofica o nome para a resposta
    nome_arq_sudoku = nome_arq_sudoku[0:len(nome_arq_sudoku)-4]+'_Resposta.txt'
    print nome_arq_sudoku
    #coloração para resolução do sudoku
    Welsh_Powell(grafo,nome_arq_sudoku)

def Welsh_Powell(g,nome):
    '''
    Função: Resolver o sudoku, é gerado um arquivo com a resolução
            a resolução também é mostrada no programa
    Parametros: g, grafo de incompatibilidade do sudoku
    Retorno: -
    '''
    #Todos os vértices tem o mesmo grau
    #Atribui uma lista de possíveis "cores" para cada vértice
    ci = []
    for no_atual in range(81):
        #verifica se o no não tem valor
        if g.node[no_atual] == 0:
            g.node[no_atual] = []
            #Lista de vértices não resolvidos
            ci.append(no_atual)
            #recupera o valor que os vizinhos possuem
            valores_vertice = [g.node[v] for v in nx.neighbors(g,no_atual)]
            #Coloca como possível valor do no os valores que não estão presentes em seus 
            #vizinhos
            for possivel_valor in range(1,10):
                if possivel_valor not in valores_vertice:
                    g.node[no_atual].append(possivel_valor)
    
    #Enquanto houver mais de um elemento por nó
    while len(ci):
        #Escolhe um no que não tem seu valor definido
        for v in ci:
            #Escolhe um no que tem só uma possibilidade
            if len(g.node[v]) == 1:
                no_retirado = g.node[v][0]
                g.node[v] = g.node[v][0]                
                ci.remove(v)
                #Remove o valor do no que tinha só uma possibilidade dos vizinhos
                for i in nx.neighbors(g,v):
                    if i in ci and no_retirado in g.node[i]:
                        g.node[i].remove(no_retirado)
    resposta = []        
    for i in range(81):
        resposta.append(g.node[i])
    gravar = int(raw_input('Para guardar a resposta em arquivo digite:\n1 - Sim\n2 - Não\n'))
    #Grafa a resposta em arquivo
    if gravar:
        arq_resposta = open(nome,"w")
        for i in range(81):
            if (i+1) % 9 == 0:
                arq_resposta.write(str(resposta[i])+'\n')
            else:
                arq_resposta.write(str(resposta[i])+" ")
        arq_resposta.close()
    print '\nResposta: '
    #Mostra a resposta no console
    for i in range(81):
        print g.node[i],
        if (i+1) % 9 == 0:
            print 
    
def valores_iniciais(g,nome):
    '''
    Função: Atribuir os valores iniciais do jogo aos vértices partindo de um arquivo.txt
    Atributos: g, grafo do jogo
    Retorno: grafo g com os valores iniciais dos vértices
    '''
    #verifica se o arquivo esta presente
    if not ph.exists(nome):
        print '\n\n\nA matriz inicial do jogo não existe, criar uma no diretório do\
               projeto, a matriz deve ser uma 9x9, elementos separados por espaço\
               e casas vazias são representadas por 0, o nome do arquivo deve ser\
               \"matriz_sudoku.txt\"\n\n\n'
        exit()
    #le a matriz
    matriz_adj = np.loadtxt(nome)
    for i in range(9):
        for j in range(9):
            #Atribuição do valor do vértice ao vértice
                g.node[j+(i*9)] = int(matriz_adj[i][j])
    
def matriz_adjacencia():
    '''
    Função: Ler a matriz de adjacencia do grafo de incompatibilidade do sudoku ou
            criar tal matriz, a matriz criada é salva em um arquivo para que os
            calculos não sejam sempre feitos, já que essa matriz nunca muda.
    Parametros: -
    Retorno: Matriz de adjacencia.
    '''
    arestas = []
    alavanca_retorno = 0
    contador = 1
    linha_matriz = 0
    #Cria a matriz de adjacencias
    for i in range(81):
        contador = 1
        if alavanca_retorno % 9 == 0 and alavanca_retorno != 0:
            alavanca_retorno = 0
            linha_matriz+=1
        for h in range(i+1): arestas.append(0)
        for j in range(i+1,81):
            #Verifica se o elemento esta na mesma linha, na mesma coluna ou mesmo quadro                      
            if (no_quadro(i,j,linha_matriz) or (j < i+9 - alavanca_retorno) or (contador % 9 == 0)):
                arestas.append(1)
            else:
                arestas.append(0)
            contador+=1
        alavanca_retorno+=1
    
    m_adj = open("matriz_adjacencia.txt","w")
    for i in range(6561):
        if (i+1) % 81 == 0:
            m_adj.write(str(arestas[i])+'\n')
        else:
            m_adj.write(str(arestas[i])+" ")
    m_adj.close()
    return gera_grafo()

def no_quadro(i, j,linha_matriz):
    '''
    Função: Verificar se posição esta no mesmo quadro do elemento i
    Parametros: i, elemento atual. posicao, elemento sendo comparado
    Retorno: True ou False
    '''            
    if j - i > 20:
        return False
    #primeira linha do quadrado
    if linha_matriz == 0 or linha_matriz == 3 or linha_matriz == 6:
        #primeira coluna do quadrado
        if i % 3 == 0 and (j == i+10 or j == i+11 or j == i+19 or j == i+20):         
            return True
        #segunda coluna do quadrado
        if (i-1) %3 == 0 and (j == i+8 or j == i+10 or j == i+17 or j == i+19):
            return True
        #terceira coluna do quadrado        
        if (i-2) %3 == 0 and (j == i+7 or j == i+8 or j == i+16 or j == i+17):
            return True
    #segunda linha do quadro
    if linha_matriz == 1 or linha_matriz == 4 or linha_matriz == 7:
        #primeira coluna do quadro
        if i % 3 == 0 and (j == i-8 or j == i-7 or j == i+10 or j == i+11):
            return True
        #segunda coluna do quadro
        if (i-1) % 3 == 0 and (j == i-10 or j == i-8 or j == i+8 or j == i+10):
            return True
        #terceira coluna do quadro
        if (i-2) % 3 == 0 and (j == i-11 or j == i-10 or j == i+7 or j == i+8):
            return True
    #terceira linha do quadro
    if linha_matriz == 2 or linha_matriz == 5 or linha_matriz == 8:
        #primeira coluna do quadro
        if i % 3 == 0 and (j == i-17 or j == i-16 or j == i-8 or j == i-7):
            return True
        #segunda coluna do quadro
        if (i-1) % 3 == 0 and (j == i-19 or j == i-17 or j == i-10 or j == i-8):
            return True
        #terceira coluna do quadro
        if (i-2) % 3 == 0 and (j == i-20 or j == i-19 or j == i-11 or j == i-10):
            return True
    return False

def gera_grafo():
    '''
    Parametro: nome_arquivo, tem nome do arquivo que possui a matriz de adjacencia
    Retorno: retorna o grafo correspondente à matriz de adjacencia
    Função: obter um grafo apartir da matriz de adjacencia
    '''
    #ler matriz de adjacencia
    matriz_adj = np.loadtxt('matriz_adjacencia.txt')
    #Obter coordenadas em que o peso é diferente de zero
    linha, coluna = np.where(matriz_adj > 0)
    #Combina a linha com a coluna, formando as arestas.
    aresta = zip(linha,coluna)
    #cria um grafo vazio
    g = nx.Graph() 
    #Preenche o grafo com as arestas e vertices    
    g.add_edges_from(aresta)
    #retorna o grafo
    return g

if __name__=="__main__":
    main()
