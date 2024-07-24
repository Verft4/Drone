import itertools
class Drone:
    def __init__(self,matriz):
        self.matriz=matriz
        self.posiçãoinicial= self.encontrarPosição('R')
    def encontrarPosição(self,elements):
        l=[]
        for i ,linha in enumerate(self.matriz):
            for j,coluna in enumerate(linha):
                if coluna==elements:
                    l.append(i)
                    l.append(j)

        return l[0],l[1]
            
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

   


