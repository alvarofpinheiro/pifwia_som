#SOM
import math
import random
import matplotlib.pyplot as plt

#Parametros

NUMERO_NODES = 128

#Representaçao será 2d, logo o número de nodes será NUMERO_NODES^2

DIMENSAO = 3
RAIO_INICIAL = NUMERO_NODES/2
ITERACOES = 500
TAXA_APRENDIZADO = 0.2

#Treinamento

inputs = [[0,0,0],
          [0,0,1],
          [1,1,0],
          [1,1,1]]

#Classes

class node:
  def __init__(self, pesos):
    self.pesos = []
    for i in pesos:
      self.pesos.append(i)
  
  def distancia(self, pesos):
    distancia = 0
    for index, i in enumerate(pesos):
      distancia += (i - self.pesos[index])**2
    return math.sqrt(distancia)

def dist_nodes(node1, node2):
  aux = 0
  aux += (node1[0] - node2[0])**2
  aux += (node1[1] - node2[1])**2
  return math.sqrt(aux)

def melhor_posicao(weights, input):
  best = [0, 0]
  best_dist = 999999999999
  for index_i, i in enumerate(weights):
    for index_j, j in enumerate(i):
      node_dist = j.distancia(input)
      if node_dist < best_dist:
        best_dist = node_dist
        best = [index_i, index_j]
  return best + [best_dist]

def raio(iteracao_atual):
  return RAIO_INICIAL*math.exp(-(iteracao_atual/(ITERACOES/math.log(RAIO_INICIAL))))

def aprendizado(iteracao_atual):
  return TAXA_APRENDIZADO*math.exp(-(iteracao_atual/(ITERACOES/math.exp(TAXA_APRENDIZADO))))

#Execução

nodes = []
for i in range(NUMERO_NODES):
  node_line = []
  for j in range(NUMERO_NODES):
    node_weight = []
    for k in range(DIMENSAO):
      node_weight.append(random.random())
    node_line.append(node(node_weight))
  nodes.append(node_line)

for iteracao in range(ITERACOES):
  input = random.sample(inputs, 1)[0]

  best_atual = melhor_posicao(nodes, input)
  raio_atual = raio(iteracao)
  aprendizado_atual = aprendizado(iteracao)

  for i in range(NUMERO_NODES):
    for j in range(NUMERO_NODES):
      distancia = dist_nodes(best_atual[:2], [i,j])
      if distancia < raio_atual:
        taxa_de_proximidade = math.exp(-(distancia**2 / (2*(raio_atual**2))))
        for index, k in enumerate(input):
          aux = aprendizado_atual * taxa_de_proximidade * (k - nodes[i][j].pesos[index])
          nodes[i][j].pesos[index] += aux


#Visualização

lista = []
for i in range(NUMERO_NODES):
  node_line = []
  for j in range(NUMERO_NODES):
    node_line.append(sum(nodes[i][j].pesos))
  lista.append(node_line)

plt.pcolormesh(lista)

#Avaliação

novo_input = [0.8, 0.8, 0.8]
best_novo_input = melhor_posicao(nodes, novo_input)
plt.plot(best_novo_input[0], best_novo_input[1], 'ro')

plt.show()