import random







import itertools
import time



def encontrar_posicoes(matriz):
    pontos = {}
    posicao_inicial = None
    for r, linha in enumerate(matriz):
        for c, valor in enumerate(linha):
            if valor == 'R':
                posicao_inicial = (r, c)
            elif valor != '0':
                pontos[valor] = (r, c)
    return pontos, posicao_inicial

def distancia(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def distancia_total(rota, inicio, pontos):
    pos_atual = inicio
    dist = 0
    for ponto in rota:
        dist += distancia(pos_atual, pontos[ponto])
        pos_atual = pontos[ponto]
    dist += distancia(pos_atual, inicio)
    return dist

def gerar_populacao_inicial(pontos, tamanho=100):
    return [random.sample(pontos, len(pontos)) for _ in range(tamanho)]

def mutar(rota):
    idx1, idx2 = random.sample(range(len(rota)), 2)
    rota[idx1], rota[idx2] = rota[idx2], rota[idx1]
    return rota

def cruzar(pai1, pai2):
    idx1, idx2 = sorted(random.sample(range(len(pai1)), 2))
    filho = pai1[idx1:idx2] + [item for item in pai2 if item not in pai1[idx1:idx2]]
    return filho

def algoritmo_genetico(matriz, geracoes=100, tamanho_populacao=100, taxa_mutacao=0.1):
    pontos, inicio = encontrar_posicoes(matriz)

    populacao = gerar_populacao_inicial(list(pontos.keys()), tamanho_populacao)
    
    for _ in range(geracoes):
        populacao = sorted(populacao, key=lambda rota: distancia_total(rota, inicio, pontos))
        proxima_geracao = populacao[:2]  # Mantém as melhores soluções
        
        while len(proxima_geracao) < tamanho_populacao:
            pai1, pai2 = random.choices(populacao[:10], k=2)
            filho = cruzar(pai1, pai2)
            if random.random() < taxa_mutacao:
                filho = mutar(filho)
            proxima_geracao.append(filho)
        
        populacao = proxima_geracao
    
    melhor_rota = sorted(populacao, key=lambda rota: distancia_total(rota, inicio, pontos))[0]
    return melhor_rota, distancia_total(melhor_rota, inicio, pontos)

# Matriz de exemplo










# Matriz de exemplo
# Matriz de exemplo
arquivo=open("arquivo.txt","r")
linhas=arquivo.readlines()
arquivo.close()

matriz=[]
for linha in linhas:
    valores=linha.strip().split()
    matriz.append(valores)



mapa_matriz =matriz
tempo_inicio = time.time()
melhor_rota, melhor_distancia = algoritmo_genetico(mapa_matriz)
tempo_fim = time.time()
print("Melhor Rota:", melhor_rota)
print("Distância Total:", melhor_distancia)
print("Tempo de execução: {:.4f} segundos".format(tempo_fim-tempo_inicio))













class EntregaDrone:
    def __init__(self,matriz):
        self.matriz=matriz
        self.posiçãoinicial= self.encontrarPosição('R')
        
    def encontrarPosição(self,elements):#Econtra a posição dos locais 
        for a ,linha in enumerate(self.matriz):
            for b,coluna in enumerate(linha):
                if coluna==elements:
                    return (a,b)
        return None
            
    def calcularcusto(self,permutação):#calcula o custo das rotas
        custoTotal=0
        posiçãoAtual=self.posiçãoinicial
       
        
        
        for letra in permutação:
            proximaposiçao=self.encontrarPosição(letra)
          
            if proximaposiçao is None:
              continue
            distancia=abs(proximaposiçao[0]-posiçãoAtual[0]) + abs(proximaposiçao[1]-posiçãoAtual[1])
            custoTotal+=distancia
            posiçãoAtual=proximaposiçao
          
        
        
        if posiçãoAtual is not None:
         distanciaretorno=abs(self.posiçãoinicial[0]- proximaposiçao[0])+abs(self.posiçãoinicial[1]- proximaposiçao[1])
         custoTotal+=distanciaretorno
         
        return custoTotal
tempo_inicial = time.time()
drone=EntregaDrone(matriz)


letras=[]
for linha in matriz:
    for elemento in linha:
        if elemento.isalpha() and elemento!="R":
            letras.append(elemento)

Permutações=itertools.permutations(letras)

custofinal=float('inf')
permutação_final=None
for permutação in Permutações:
    custoAtual=drone.calcularcusto(permutação)
    if custoAtual<custofinal:
        custofinal=custoAtual
        permutação_final=permutação
if permutação_final:
        permutaçãoSaida=','.join(permutação_final)


print("O drone gasta",custofinal,"dronometros para pecorrer",permutação_final)
tempo_final = time.time()
duracao = tempo_final - tempo_inicial
print("Duração", duracao)
   
   


