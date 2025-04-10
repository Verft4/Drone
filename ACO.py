import random
import math
from typing import List, Tuple, Dict, Optional
from multiprocessing import Pool

class ColoniaDeFormigas:
    def __init__(self, dados: Dict[int, Tuple[float, float]], num_formigas: int, num_iteracoes: int, alfa: float = 1, beta: float = 2, rho: float = 0.01, q: float = 10):
        self.dados = dados
        self.num_formigas = num_formigas
        self.num_iteracoes = num_iteracoes
        self.alfa = alfa  
        self.beta = beta  
        self.rho = rho    
        self.q = q        
        self.feromonio = self.inicializar_feromonio()
        self.distancias = self.calcular_distancias()
        self.heuristicas = self.calcular_heuristicas()
        self.melhor_caminho: Optional[List[int]] = None
        self.melhor_distancia: float = float('inf')

    def inicializar_feromonio(self) -> List[List[float]]:
        n = len(self.dados)
        return [[1 / (n * n) for _ in range(n)] for _ in range(n)]

    def calcular_distancias(self) -> Dict[Tuple[int, int], float]:
        distancias = {}
        pontos = list(self.dados.keys())
        for i, ponto_a in enumerate(pontos):
            for j, ponto_b in enumerate(pontos):
                if i != j:
                    x1, y1 = self.dados[ponto_a]
                    x2, y2 = self.dados[ponto_b]
                    dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
                    distancias[(i, j)] = dist
        return distancias

    def calcular_heuristicas(self) -> Dict[Tuple[int, int], float]:
        heuristicas = {}
        for (i, j), dist in self.distancias.items():
            heuristicas[(i, j)] = 1 / dist if dist > 0 else 0.0
        return heuristicas

    def encontrar_caminho(self, formiga: 'Formiga') -> List[int]:
        pontos = list(self.dados.keys())
        caminho = []
        visitados = set()

        ponto_atual = random.choice(pontos)
        visitados.add(ponto_atual)
        caminho.append(ponto_atual)

        while len(visitados) < len(pontos):
            proximo_ponto = formiga.escolher_proximo_no(ponto_atual, visitados)
            visitados.add(proximo_ponto)
            caminho.append(proximo_ponto)
            ponto_atual = proximo_ponto
        
        caminho.append(caminho[0])  # Retorna ao ponto de partida
        return caminho

    def atualizar_feromona(self) -> None:
        n = len(self.dados)
        for i in range(n):
            for j in range(n):
                self.feromonio[i][j] *= (1 - self.rho)
                
        if self.melhor_caminho:
            pontos = list(self.dados.keys())
            for i in range(len(self.melhor_caminho) - 1):
                ponto_atual = pontos.index(self.melhor_caminho[i])
                ponto_proximo = pontos.index(self.melhor_caminho[i + 1])
                self.feromonio[ponto_atual][ponto_proximo] += (self.q / self.melhor_distancia)
                
            # Intensificação: Aumenta o peso do feromônio no melhor caminho ao final de cada iteração
            if random.random() < 0.1:  # Probabilidade de intensificação
                for i in range(len(self.melhor_caminho) - 1):
                    ponto_atual = pontos.index(self.melhor_caminho[i])
                    ponto_proximo = pontos.index(self.melhor_caminho[i + 1])
                    self.feromonio[ponto_atual][ponto_proximo] += (self.q / self.melhor_distancia) * 0.5

    def ajustar_parametros(self, iteracao: int) -> None:
        fator = iteracao / self.num_iteracoes
        self.alfa = max(1, self.alfa * fator)
        self.beta = max(2, self.beta * fator)
        self.rho = min(0.5, self.rho * (1 + fator * 0.5))  # Rho adaptativo

    def executar(self) -> Tuple[Optional[List[int]], float]:
        with Pool() as pool:
            for iteracao in range(self.num_iteracoes):
                self.ajustar_parametros(iteracao)
                caminhos = pool.map(self.encontrar_caminho, [Formiga(self) for _ in range(self.num_formigas)])
                for caminho in caminhos:
                    if caminho:
                        distancia = self.calcular_distancia_do_caminho(caminho)
                        if distancia < self.melhor_distancia:
                            self.melhor_distancia = distancia
                            self.melhor_caminho = caminho
                self.atualizar_feromona()
        return self.melhor_caminho, self.melhor_distancia

    def calcular_distancia_do_caminho(self, caminho: List[int]) -> float:
        pontos = list(self.dados.keys())
        index_pontos = {ponto: i for i, ponto in enumerate(pontos)}  
        distancia = 0
        for i in range(len(caminho) - 1):
            ponto_atual = index_pontos[caminho[i]]
            ponto_proximo = index_pontos[caminho[i + 1]]
            distancia += self.distancias[(ponto_atual, ponto_proximo)]
        return distancia


class Formiga:
    def __init__(self, colonia: ColoniaDeFormigas):
        self.colonia = colonia

    def escolher_proximo_no(self, ponto_atual: int, visitados: set) -> int:
        pontos = list(self.colonia.dados.keys())
        possiveis_pontos = [p for p in pontos if p not in visitados]
        
        probabilidades = []
        for ponto in possiveis_pontos:
            idx_atual = pontos.index(ponto_atual)
            idx_proximo = pontos.index(ponto)
            feromonio = self.colonia.feromonio[idx_atual][idx_proximo] ** self.colonia.alfa
            heuristica = self.colonia.heuristicas[(idx_atual, idx_proximo)] ** self.colonia.beta
            probabilidades.append(feromonio * heuristica)
        
        soma_probabilidades = sum(probabilidades)
        if soma_probabilidades == 0:
            return random.choice(possiveis_pontos)
        probabilidades = [p / soma_probabilidades for p in probabilidades]

        # Utiliza soma acumulada para seleção mais precisa
        acumulada = 0
        r = random.random()
        for i, prob in enumerate(probabilidades):
            acumulada += prob
            if r <= acumulada:
                return possiveis_pontos[i]

        return possiveis_pontos[-1]  # Caso de segurança


def ler_dados(nome_arquivo: str) -> Dict[int, Tuple[float, float]]:
    dados = {}
    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            partes = linha.strip().split()
            cidade = int(partes[0])
            x = float(partes[1])
            y = float(partes[2])
            dados[cidade] = (x, y)
    return dados


if __name__ == "__main__":
    dados = ler_dados("Berlim52.txt")
    colonia = ColoniaDeFormigas(dados, num_formigas=500, num_iteracoes=500)
    melhor_caminho, melhor_distancia = colonia.executar()
    print("Melhor caminho:", melhor_caminho)
    print("Comprimento do melhor caminho:", melhor_distancia)
   
     
