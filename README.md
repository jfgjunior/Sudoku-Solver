Sudoku-Solver
=============

Programa que visa resolver o jogo sudoku
O programa se baseia no algoritmo de Welsh & Powell, usando coloração de grafos. Funciona obtendo a matriz de adjacencia do grafo de incompatibilidade da matriz do sudoku, depois adiciona a configuração incial e usa coloração para a resolução.
São utilizadas as bibliotecas: networkx, numpy, os.path e sys.
O programa possuí algumas limitações, resolvendo somente jogos "fáceis", em que sempre a coloração de um quadro leva a única possibilidade de coloração do seu vizinho.
A matriz inicial lida é representada pelos valores de 1 a 9 e 0 quando não há valor.
