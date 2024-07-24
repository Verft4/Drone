import itertools
arquivo=open("arquivo.txt","r")
linhas=arquivo.readlines()
arquivo.close()
class Drone:
    def __init__(self,matriz):
        self.matriz=matriz
        self.posiçãoinicial= self.encontrarPosição('R')
    def busca_binaria(self,arr, x):
     esquerda, direita = 0, len(arr) - 1
    
     while esquerda <= direita:
        meio = (esquerda + direita) // 2
        if arr[meio] == x:
            return meio
        elif arr[meio] < x:
            esquerda = meio + 1
        else:
            direita = meio - 1
    
     return -1  # Retorna -1 se o elemento não for encontrado
    def quicksort(self,arr, indices):
     if len(arr) <= 1:
        return arr, indices
    
     pivo = arr[len(arr) // 2]
     esquerda, meio, direita = [], [], []
     indices_esquerda, indices_meio, indices_direita = [], [], []
    
     for i in range(len(arr)):
        if arr[i] < pivo:
            esquerda.append(arr[i])
            indices_esquerda.append(indices[i])
        elif arr[i] > pivo:
            direita.append(arr[i])
            indices_direita.append(indices[i])
        else:
            meio.append(arr[i])
            indices_meio.append(indices[i])
    
    # Chamadas recursivas
     esquerda_ordenada, indices_esquerda_ordenados = self.quicksort(esquerda, indices_esquerda)
     direita_ordenada, indices_direita_ordenados = self.quicksort(direita, indices_direita)
    
    # Concatenação dos resultados
     return esquerda_ordenada + meio + direita_ordenada, indices_esquerda_ordenados + indices_meio + indices_direita_ordenados
    def ordenar_com_indices(self,arr):
     indices = [(i, j) for i in range(len(arr)) for j in range(len(arr[i]))]
     flat_arr = [item for sublist in arr for item in sublist]
     arr_ordenada, indices_ordenados = self.quicksort(flat_arr, indices)
    
    # Manter apenas os índices originais
     tuplas_indices = indices_ordenados
     
     return arr_ordenada, tuplas_indices

    def encontrarPosição(self,elements):
       matriz_ordenada,tupla_indice=self.ordenar_com_indices(self.matriz)
       item=self.busca_binaria(matriz_ordenada,elements)
       tupla_final=tupla_indice[item]

       return tupla_final[0],tupla_final[1]

      
            
    def calcularcusto(self,permutação):
        custoTotal=0
        posiçãoAtual=self.posiçãoinicial
        
        for letra in permutação:
            proximaposiçao=self.encontrarPosição(letra)
            distancia=abs(proximaposiçao[0]-posiçãoAtual[0]) + abs(proximaposiçao[1]-posiçãoAtual[1])
            custoTotal+=distancia
            posiçãoAtual=proximaposiçao
        distanciaretorno=abs(self.posiçãoinicial[0]-proximaposiçao[0])+(self.posiçãoinicial[1]-proximaposiçao[1])
        custoTotal+=distanciaretorno
        return custoTotal
arquivo=open("arquivo.txt","r")
linhas=arquivo.readlines()
arquivo.close()
matriz=[]
for linha in linhas:
    valores=linha.strip().split()
    matriz.append(valores)
drone=Drone(matriz)
letras=[]
for linha in matriz:
    for elemento in linha:
        if elemento.isalpha() and elemento!="R":
            letras.append(elemento)

PermutaçõesLetras=itertools.permutations(letras)
menorcusto=float('inf')
melhorpermut=None
for permutação in PermutaçõesLetras:
    custoAtual=drone.calcularcusto(permutação)
    if custoAtual<menorcusto:
        menorcusto=custoAtual
        melhorpermut=permutação
        permutaçãoSaida=','.join(melhorpermut)
print("O drone gastara",menorcusto,"dronometros para pecorrer",permutação)

   


