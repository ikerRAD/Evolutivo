# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 16:32:09 2021

@author: ikerb
"""

import random

'''Function that computes how many clauses are false with the assignation '''
def objectiveVal(num_variables, clauses, assignation):
    
    numfalses = 0
    
    for clause in clauses:
        trued = False
        
        for lit in clause:
            if lit < 0:
                if assignation[-lit] == 0:
                    trued = True
                    break
            else:
                if assignation[lit] == 1:
                    trued = True
                    break
                
        if not trued:
            numfalses += 1
            
    return numfalses

'''Function that returns 2 random elements of the old generation.
It is biased by the objective value the specimens have '''
def biasedRoulette(oldgen, n_clauses):
    
    #we set the probabilities to appear
    suma = 0
    for i in range(len(oldgen)):
        _, val = oldgen[i]
        suma += (n_clauses-val)
        
    #we set a cummulative distribution
    probs = [0]*len(oldgen)
    
    _, val = oldgen[0]
    val = n_clauses - val
    probs[0] = val/suma
    
    for i in range(1, len(oldgen)):
        _, val = oldgen[i]
        val = n_clauses - val
        probs[i] = probs[i-1] + val/suma
        
    #now we set the indexes to return
    
    #first index
    parent1 = random.random()
    index1 = -1
    for i in range(len(probs)):
        helper1 = parent1 - probs[i]
        if helper1<=0:
            index1 = i
            break
    
    #second index, we need to ensure that it will be different, so we recalculate the distribution
    
    _, val = oldgen[index1]
    val = n_clauses - val
    suma = suma - val
    
    if index1 == 0:
        probs[0] = 0
    else:
        _, val = oldgen[0]
        val = n_clauses - val
        probs[0] = val/suma
    
    for i in range(1, len(oldgen)):
        _, val = oldgen[i]
        val = n_clauses - val
        if index1 == i:
            probs[i] = probs[i-1]
        else:
            probs[i] = probs[i-1] + val/suma
            
    #redistribution calculated, lets go for the second index
    parent2 = random.random()
    index2 = -1
    for i in range(len(probs)):
        helper2 = parent2- probs[i]
        if helper2<=0:
            index2 = i
            break
        
    parent1,_ = oldgen[index1]  
    parent2,_ = oldgen[index2] 
    return (parent1, parent2)
    
'''Function that based on an old population creates a new generation which is more likely
to share good genes. It returns the population, and the values of the specimen number one of this generation
newgen, best objective val, best child '''  
def reproduce(oldgen, population, num_variables, n_clauses, clauses, mutation = 0.05):

    reproductions = int(population/2)
    bestchild = [None]*(num_variables+1)
    bestobj = n_clauses
    newgen = []
    
    for reproduction in range(reproductions):
        #we calculate the reproduction values
        cut = random.randint(1, num_variables-1)
        mutation1 = random.randint(1, num_variables)
        mutation2 = random.randint(1, num_variables)
        parent1, parent2 = biasedRoulette(oldgen, n_clauses)
        child1 = parent1[:cut]+parent2[cut:]
        child2 = parent2[:cut]+parent1[cut:]
        
        if(mutation >= random.random()):
            child1[mutation1] = (child1[mutation1] + 1)%2
            
        if(mutation >= random.random()):
            child2[mutation2] = (child2[mutation2] + 1)%2
            
        #once the two childs have been born, we just calculate how valid they are and store them
        obj1 = objectiveVal(num_variables, clauses, child1)
        
        if obj1 < bestobj:
            bestchild = child1
            bestobj = obj1
        
        obj2 = objectiveVal(num_variables, clauses, child2)
        
        if obj2 < bestobj:
            bestchild = child2
            bestobj = obj2
        
        newgen.append((child1, obj1))
        newgen.append((child2, obj2))
        
    #all the new generation is prepared, we return the new generation and its best specimen
    return (newgen, bestobj, bestchild)

#indicar número distinto de variables y las clausulas. Por ejemplo:
# num_variables = 6, clauses = [[1,2,-3],[4,2,6,5]]
#representa este problema SAT:
#(x1 or x2 or not x3) and ( x4 or x2 or x6 or x5)
def evoSAT(num_variables, clauses, iterations = 1000, population = 100):
    
    #We set the global values
    bestsol = [None]*(num_variables+1)
    bestobj = len(clauses)
    itsiter = 0
    n_clauses = len(clauses)
    
    #We generate the random population
    specimens = []
    for i in range(population):
        rndsp = []
        
        for j in range(num_variables+1):
            rndsp.append(random.randint(0, 1))
            
        objval = objectiveVal(num_variables, clauses, rndsp)
        
        if objval < bestobj:
            bestobj = objval
            bestsol = rndsp
            
        specimens.append((rndsp, objval))
        
    #Once the generation 0 is generated, we start the process
    iteration = 0
    while iteration < iterations and bestobj > 0:
        newgen, besto, bestc = reproduce(specimens, population, num_variables, n_clauses, clauses)
        
        if besto < bestobj:
            bestobj = besto
            bestsol = bestc
            itsiter = iteration
        
        iteration += 1
        
        specimens = newgen
        
    #once the process is finished, we return the best solution found
    return (bestsol, bestobj, itsiter)
        
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
