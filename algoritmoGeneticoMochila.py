import random
import pandas as pd


#CLASSE ITEM

class Item(object):
    def __init__(self, v, w):
        self.valor = v # Valor do Item
        self.peso = w # Peso do Item


# CONFIGURAÇÕES

ITEMS = []

ITEMS.clear()

mochila = pd.read_csv('Teste3.csv')
#ITEMS.clear()
for i in range(len(mochila)):
    #aux = Item(mochila['valor'][i], mochila['peso'][i])
    #print(aux.peso)
    #print(aux.valor)
    
    ITEMS.append(Item(mochila['valor'][i], mochila['peso'][i]))


# Itens de entrada
#ITEMS = [Item(1000,100), Item(2000,50), Item(500,100), Item(10000,450), Item(3000,150), Item(100,300), Item(10000,50), Item(15000,500), Item(9000,200)]

# Capacidade da mochila
CAPACIDADE = 6404180

# Tamanho da população incial de 0s e 1s
TAMANHO_POPULACAO = 30

# Numero maximo de gerações a serem executadas
GEN_MAX = 50000


##########################################################################################

peso_total = 0

def fitness(individuo):
    """
    fitness (individuo) retornará o valor de adequação do gene chamado "individuo".
    Pontuações mais altas são melhores e são iguais ao valor total dos itens do gene.
    Se peso_total for maior que a capacidade, retorne 0 porque o gene não pode ser usado.
    """
    valor_total = 0
    global peso_total
    peso_total = 0
    index = 0
    for i in individuo:        
        if index >= len(ITEMS):
            break
        if (i == 1):
            valor_total += ITEMS[index].valor
            peso_total += ITEMS[index].peso
        index += 1
        
    
    if peso_total > CAPACIDADE:
        # Se o peso for maior q a capacidade retorna 0
        return 0
    else:
        return valor_total

def gera_populacao(amount):
    return [individuo() for x in range (0,amount)]

def individuo():
        return [random.randint(0,1) for x in range (0,len(ITEMS))]

def mutacao(individuo):
    """
    Altera um elemento aleatório da matriz de permutação de 0 -> 1 ou de 1 -> 0.
    """ 
    r = random.randint(0,len(individuo)-1)
    if individuo[r] == 1:
        individuo[r] = 0
    else:
        individuo[r] = 1

def evolucao(pop):
    elegibilidade_pais = 0.2
    chance_mutacao = 0.08
    pais_lottery = 0.05

    pais_length = int(elegibilidade_pais*len(pop))
    pais = pop[:pais_length]
    nonpais = pop[pais_length:]

    # Sorteia pais!
    for np in nonpais:
        if pais_lottery > random.random():
            pais.append(np)

    # Sorteio de mutação
    for p in pais:
        if chance_mutacao > random.random():
            mutacao(p)

    filhos = []
    desired_length = len(pop) - len(pais)
    while len(filhos) < desired_length :
        pai = pop[random.randint(0,len(pais)-1)]
        mae = pop[random.randint(0,len(pais)-1)]        
        half = len(pai)/2
        filho = pai[:int(half)] + mae[int(half):] # do início à metade do pai, da metade ao fim da mãe
        if chance_mutacao > random.random():
            mutacao(filho)
        filhos.append(filho)

    pais.extend(filhos)
    return pais

def main():
    global peso_total
    geracao = 1
    populacao = gera_populacao(TAMANHO_POPULACAO)
    for g in range(0,GEN_MAX):
        print ("Geração %d with %d" % (geracao,len(populacao)))
        populacao = sorted(populacao, key=lambda x: fitness(x), reverse=True)
        for i in populacao:        
            print ("%s, fit: %s, peso: %s" % (str(i), fitness(i), peso_total))      
        populacao = evolucao(populacao)
        geracao += 1

if __name__ == "__main__":
    main()