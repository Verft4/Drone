arquivo=open("arquivo.txt","r")
linhas=arquivo.readlines()
arquivo.close()

matriz=[]
for linha in linhas:
    valores=linha.strip().split()
    matriz.append(valores)
import itertools
class EntregaDrone:
    def __init__(self,matriz):
        self.matriz=matriz
        self.posiçãoinicial= self.encontrarPosição('R')
        
    def encontrarPosição(self,elements):#Econtra a posição dos locais 
        l=[]
        for a ,linha in enumerate(self.matriz):
            for b,coluna in enumerate(linha):
                if coluna==elements:
                    l.append(a)
                    l.append(b)

        return l[0],l[1]
            
    def calcularcusto(self,permutação):#calcula o custo das rotas
        custoTotal=0
        posiçãoAtual=self.posiçãoinicial
        
        for letra in permutação:
            proximaposiçao=self.encontrarPosição(letra)
            distancia=abs(proximaposiçao[0]-posiçãoAtual[0]) + abs(proximaposiçao[1]-posiçãoAtual[1])
            custoTotal+=distancia
            posiçãoAtual=proximaposiçao
        distanciaretorno=abs(self.posiçãoinicial[0]-proximaposiçao[0])+abs(self.posiçãoinicial[1]-proximaposiçao[1])
        custoTotal+=distanciaretorno
        return custoTotal
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
        permutaçãoSaida=','.join(permutação_final)
print("O drone gasta",custofinal,"dronometros para pecorrer",permutação)