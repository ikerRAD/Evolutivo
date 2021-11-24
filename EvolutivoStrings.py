# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 15:47:54 2021

@author: ikerb
"""
import random
MUTACION_R = 0.2
MUTACION_S = 0.1
GENES = " abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ1234567890,.-;:_¿?¡!áéíóú"



def biasedRoulette(oldgen):
    
    #we set the probabilities to appear
    suma = 0
    for i in range(len(oldgen)):
        suma += oldgen[i].invertedFitness()
        
    #we set a cummulative distribution
    probs = [0]*len(oldgen)
    
    val = oldgen[0].invertedFitness()
    probs[0] = val/suma
    
    for i in range(1, len(oldgen)):
        val = oldgen[i].invertedFitness()
        probs[i] = probs[i-1] + val/suma
        
    #now we set the indexes to return
    
    #first index
    parent1 = random.random()
    index1 = -1
    for i in range(len(probs)):
        if (parent1 - probs[i]) <= 0:
            index1 = i
            break
    
    #second index, we need to ensure that it will be different, so we recalculate the distribution
    
    suma = suma - oldgen[index1].invertedFitness()
    
    if index1 == 0:
        probs[0] = 0
    else:
        val = oldgen[0].invertedFitness()
        probs[0] = val/suma
    
    for i in range(1, len(oldgen)):
        val = oldgen[i].invertedFitness()
        if index1 == i:
            probs[i] = probs[i-1]
        else:
            probs[i] = probs[i-1] + val/suma
            
    #redistribution calculated, lets go for the second index
    parent2 = random.random()
    index2 = -1
    for i in range(len(probs)):
        if (parent2- probs[i]) <= 0:
            index2 = i
            break
        
    parent1 = oldgen[index1]  
    parent2 = oldgen[index2] 
    return (parent1, parent2)



def generateRandomPopulation(objective, size):
    
    ngenes = len(objective)
    population = []
    for _ in range(size):
        genoma = [random.choice(GENES) for i in range(ngenes)]
        population.append(Individuo(genoma, objective))
    
    return population



class Individuo:
    
    def __init__(self, genoma, objetivo):
        
        self.genoma = genoma
        self.objetivo = objetivo
        if len(genoma) != len(objetivo):
            self.fitness = float("inf")
        else:
            obj = 0
            
            for letra in range(len(objetivo)):
                if genoma[letra] != objetivo[letra]:
                    obj += 1
            
            self.fitness = obj
            
    def mix(self, pareja, corte):
        
        hijo = Individuo(self.genoma[:corte]+pareja.genoma[corte:], self.objetivo)   
        if random.random() <= MUTACION_R:
            
            loops = int(len(self.genoma)*MUTACION_S)
            loops = min(loops, len(self.genoma))
            tomute = list(range(len(self.genoma)))
            
            for _ in range(loops):
                indice = random.choice(tomute)
                hijo.genoma[indice] = random.choice(GENES)
                tomute.remove(indice)
            
        return hijo
        
    def invertedFitness(self):
        
        return len(self.objetivo)-self.fitness
    
    
def stringFinderEvo(objetivo, population_size = 200, iterations = 1000, elite_rate = 0.1, inmigration_rate = 0.1, reproduction_rate = 1):
    #inicializamos bariables de busqueda
    bestSol = ""
    bestIter = 0
    bestFit = len(objetivo)+1
    
    #creamos a la población 0
    poblacion = generateRandomPopulation(objetivo, population_size)
    poblacion = sorted(poblacion, key= lambda x:x.fitness)
    bestSol = poblacion[0].genoma
    bestFit = poblacion[0].fitness
    print("Mejor individuo en inicialización: \"",''.join(bestSol),"\"\ncon un fitness de: ", bestFit,"\n")
    
    #Corregimos los ratios
    elite_rate = min(elite_rate, 0.33)
    elite_rate = min(inmigration_rate, 0.33)
    
    #calculamos los valores para el salto generacional
    elite = int(population_size*elite_rate)
    inmigration = int(population_size*inmigration_rate)
    reproductions = population_size - elite - inmigration
    
    #variable que dice quienes se reproducen dependiendo de su fitness
    reproduction = max(0.25, min(1, reproduction_rate))
    mate = int(population_size*reproduction)
    
    #corregimos las reproducciones si salen impares
    if reproductions % 2 == 1:
        elite += 1
        reproductions -= 1
        
    #cantidade de parejas que uniremos
    actual_reproductions = int(reproductions/2)
    
    #empezamos la simulación
    iteration = 0
    while (iteration < iterations and bestFit > 0):
        
        #individuos que sobreviviran al salto generacional
        new_poblacion = poblacion[:elite]
        
        #individuos que inmigran a la población
        new_poblacion += generateRandomPopulation(objetivo, inmigration)
        
        #individuos que nacen de la generación anterior
        successful = poblacion[:mate]
        for _ in range(actual_reproductions):
            parent1, parent2 = biasedRoulette(successful)
            if len(objetivo) > 2:
                corte = random.randint(1, len(objetivo)-2)
            elif len(objetivo) == 1:
                corte = 0
            else:
                corte = 1
            new_poblacion.append(parent1.mix(parent2, corte))
            new_poblacion.append(parent2.mix(parent1, corte))
    
        #calculamos los datos para la siguiente generacion
        iteration += 1
        poblacion = sorted(new_poblacion, key= lambda x:x.fitness)
        tempBestFit = poblacion[0].fitness
        if tempBestFit < bestFit:
            bestFit = tempBestFit
            bestIter = iteration
            bestSol = poblacion[0].genoma
            print("Nuevo mejor individuo: \"",''.join(bestSol),"\"\ncon un fitness de: ", bestFit,"\nEncontrado en la iteracion: ",iteration,"\n")
            
    return ''.join(bestSol),bestFit,bestIter
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    