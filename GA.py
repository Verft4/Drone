import random
from typing import List, Tuple, Callable, Dict
import math
random.seed(42)
# Encontra a posição das letras na matriz
def encontrar_posicoes(dados: Dict[int, Tuple[float, float]]) -> Tuple[Dict[str, Tuple[float, float]], Tuple[float, float]]:
    pontos = {str(cidade): (x, y) for cidade, (x, y) in dados.items()}
    posicao_inicial = list(pontos.keys())
    letra = pontos[random.choice(posicao_inicial)]
    return pontos, letra

# Calcula a distância euclidiana entre dois pontos
def distancia(ponto1: Tuple[float, float], ponto2: Tuple[float, float]) -> float:
    return math.sqrt((ponto1[0] - ponto2[0]) ** 2 + (ponto1[1] - ponto2[1]) ** 2)

# Calcula a aptidão de um indivíduo com base na distância
def aptidao_individuo(caminho: List[str], pontos: Dict[str, Tuple[float, float]], inicio: Tuple[float, float]) -> float:
    pos_atual = inicio
    dist = 0
    for ponto in caminho:
        dist += distancia(pos_atual, pontos[ponto])
        pos_atual = pontos[ponto]
    dist += distancia(pos_atual, inicio)
    return dist

# Cria uma população inicial
def criar_populacao(tamanho: int, pontos: Dict[str, Tuple[float, float]]) -> List[List[str]]:
    return [random.sample(list(pontos.keys()), len(pontos)) for _ in range(tamanho)]

# Avalia a aptidão de toda a população
def aptidao_populacao(pop: List[List[str]], pontos: Dict[str, Tuple[float, float]], inicio: Tuple[float, float]) -> List[float]:
    return [aptidao_individuo(ind, pontos, inicio) for ind in pop]

# Cruzamento dos pais para gerar filhos
def cruzamento_pais(pai1: List[str], pai2: List[str], taxa_cruzamento: float) -> Tuple[List[str], List[str]]:
    if random.random() <= taxa_cruzamento:
        ponto_cruzamento = random.randint(1, len(pai1) - 1)
        filho1 = pai1[:ponto_cruzamento] + [gene for gene in pai2 if gene not in pai1[:ponto_cruzamento]]
        filho2 = pai2[:ponto_cruzamento] + [gene for gene in pai1 if gene not in pai2[:ponto_cruzamento]]
        return filho1, filho2
    return pai1, pai2

# Realiza o cruzamento de toda a população
def cruzamento(pais: List[List[str]], taxa_cruzamento: float) -> List[List[str]]:
    lista_filhos = []
    for i in range(0, len(pais), 2):
        filho1, filho2 = cruzamento_pais(pais[i], pais[i + 1], taxa_cruzamento)
        lista_filhos.extend([filho1, filho2])
    return lista_filhos

# Realiza a mutação de um indivíduo
def mutacao_individuo(filho: List[str], taxa_mutacao: float) -> List[str]:
    if random.random() <= taxa_mutacao:
        idx1, idx2 = random.sample(range(len(filho)), 2)
        filho[idx1], filho[idx2] = filho[idx2], filho[idx1]
    return filho

# Aplica a mutação em toda a população
def mutacao(filhos: List[List[str]], taxa_mutacao: float) -> List[List[str]]:
    return [mutacao_individuo(filho, taxa_mutacao) for filho in filhos]

# Seleção por roleta
def roleta(apt: List[float]) -> int:
    soma_roleta = sum(apt)
    n_sorteado = random.random() * soma_roleta
    soma_atual = 0
    for i, valor_apt in enumerate(apt):
        soma_atual += valor_apt
        if soma_atual >= n_sorteado:
            return i

# Seleção por torneio
def torneio(apt: List[float]) -> int:
    pai1 = random.randint(0, len(apt) - 1)
    pai2 = random.randint(0, len(apt) - 1)
    return pai1 if apt[pai1] < apt[pai2] else pai2

# Seleciona os pais usando a função de seleção fornecida
def selecao_pais(pop: List[List[str]], apt: List[float], sel_func: Callable) -> List[List[str]]:
    return [pop[sel_func(apt)] for _ in range(len(pop))]

# Seleciona os sobreviventes com elitismo
def selecao_sobreviventes(pop: List[List[str]], apt_pop: List[float], filhos: List[List[str]], apt_filhos: List[float]) -> Tuple[List[List[str]], List[float]]:
    # Encontrar o melhor indivíduo da população atual
    melhor_aptidao = min(apt_pop)
    melhor_indice = apt_pop.index(melhor_aptidao)
    melhor_individuo = pop[melhor_indice]

    # Combinar pais e filhos
    nova_populacao = pop + filhos
    novas_aptidoes = apt_pop + apt_filhos

    # Selecionar o melhor indivíduo para a próxima geração
    indices_ordenados = sorted(range(len(nova_populacao)), key=lambda i: novas_aptidoes[i])
    nova_populacao = [nova_populacao[i] for i in indices_ordenados[:len(pop) - 1]] + [melhor_individuo]
    novas_aptidoes = [novas_aptidoes[i] for i in indices_ordenados[:len(pop) - 1]] + [melhor_aptidao]

    return nova_populacao, novas_aptidoes

# Função principal para evoluir a população
def evolucao(n_pop: int, taxa_cruzamento: float, taxa_mutacao: float, n_geracoes: int, sel_func: Callable, dados: Dict[int, Tuple[float, float]]) -> Tuple[List[List[str]], List[float], Dict[str, Tuple[float, float]], Tuple[float, float]]:
    pontos, inicio = encontrar_posicoes(dados)
    pop = criar_populacao(n_pop, pontos)
    apt = aptidao_populacao(pop, pontos, inicio)
    
    for geracao in range(n_geracoes):
        pais = selecao_pais(pop, apt, sel_func)
        filhos = cruzamento(pais, taxa_cruzamento)
        filhos = mutacao(filhos, taxa_mutacao)
        apt_filhos = aptidao_populacao(filhos, pontos, inicio)
        pop, apt = selecao_sobreviventes(pop, apt, filhos, apt_filhos)
    
    return pop, apt, pontos, inicio

# Função principal que lê o arquivo e inicia a evolução
def principal():
    # Ler o arquivo e converter os dados
    dados = {}
    with open("Berlim52.txt", "r") as arquivo:
        for linha in arquivo:
            partes = linha.strip().split()
            cidade = int(partes[0])
            x = float(partes[1])
            y = float(partes[2])
            dados[cidade] = (x, y)

    taxa_cruzamento = 0.5
    taxa_mutacao = 0.05
    tamanho_populacao = 1000
    geracoes = 1000
    sel_func = roleta
    pop, apt, pontos, inicio = evolucao(tamanho_populacao, taxa_cruzamento, taxa_mutacao, geracoes, sel_func, dados)
    melhor_aptidao = min(apt)
    melhor_indice = apt.index(melhor_aptidao)
    melhor_caminho = pop[melhor_indice]
    
    print(f"\n\n>>> Melhor solução encontrada é {melhor_caminho} com comprimento de {melhor_aptidao}\n\n")

if __name__ == "__main__":
    principal()
