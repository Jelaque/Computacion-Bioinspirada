import random as rand
import numpy as np
import math

path = 'ABCDEFGHIJ'

def r_genetic(n_genes,N,p_cross,p_mut,tsp,it,mode):

    population = rget_population(n_genes,N)

    print('Poblacion inicial')
    print_pop_initial(population)

    fitness = rdecode(population,tsp)

    print_fitness(population,fitness,N)

    i = 1
    it = it + 1

    while i < it:
        print('****Iteracion ',i,'****')

        parents = rmating_pool(population, fitness, mode)

        population = rselect_parents(population, n_genes, parents, fitness, p_cross, p_mut)

        fitness = rdecode(population,tsp)

        print('Nueva Poblacion')
        print_pop_initial(population)

        print_fitness(population,fitness,N)

        i += 1

def print_pop_initial(population):
    i = 1
    for row in population:
        s = ''
        for j in row:
            s += str(path[int(j)])
        print(i,')\t\t',s)
        i += 1
    print()

def print_fitness(population,fitness,n):
    k = 1
    print('Calcular la Aptitud para cada Individudo')
    j = 0
    for row in population:
        s = ''
        for i in row:
            s += str(path[int(i)])
        print(k,')\t\t',s,'\t\t',fitness[j])
        k += 1
        j += 1
    print()

def rget_population(n_genes,N):

    population = np.zeros((N,n_genes))
    vec = np.zeros(n_genes)
    for i in range(0,n_genes):
        vec[i] = i
    for i in range(0,N):
        population[i] = np.random.permutation(vec)

    return population

def rdecode(population, tsp):

    fitness = np.zeros(population.shape[0])
    i = 0
    for row in population:
        for j in range(0,4):
            fitness[i] += tsp[int(row[j])][int(row[j+1])]
        i += 1

    return fitness

def rmating_pool(population, fitness, mode):

    n = population.shape[0]
    parents = np.zeros(n)

    for i in range(0,n):
        a = rand.randint(0,n-1)
        b = rand.randint(0,n-1)
        val = mode(fitness[a], fitness[b])
        if val == fitness[a]:
            parents[i] = a
        else:
            parents[i] = b
        s1 = ''
        for j in population[int(parents[i])]:
            s1 += str(path[int(j)])
        print(a+1,'\t\t',b+1,'\t\t=>\t\t',int(parents[int(i)])+1,'\t\t=>\t\t',s1)
    print()

    return parents

def rselect_parents(population, n_genes, parents, fitness, p_cross, p_mut):

    p_new = population
    n = population.shape[0]

    for i in range(0,int(n/2)):
        a = rand.randint(0,n-1)
        b = rand.randint(0,n-1)
        x = population[int(parents[a])]
        y = population[int(parents[b])]
        print('Seleccion de Padres')
        s1 = ''
        for k in x:
            s1 += str(path[int(k)])
        s2 = ''
        for k in y:
            s2 += str(path[int(k)])
        print(a,'\t',b,' => ',int(parents[a]),' - ',int(parents[b]),' => ',s1,' - ',s2)
        if rand.uniform(0,1) <= p_cross:
            v = []
            for f in range(0,n_genes):
                beta = rand.uniform(0,1)
                if beta > 0.5:
                    v.append(f)
            vec = np.zeros(n_genes)
            j = 0
            l = 0
            aux1 = v
            aux2 = v
            x = list(x)
            y = list(y)
            for w in range(0,len(v)):
                aux1.append(x.index(v[w]))
                aux2.append(y.index(v[w]))
            aux1.sort()
            aux2.sort()
            while j < len(v) and l < n_genes:
                if l == v[j]:
                    x[l] = y[aux1[j]]
                    y[l] = x[aux2[j]]
                    j += 1
                l += 1
            print('Cruzamiento')
            s1 = ''
            for f in x:
                s1 += str(path[int(f)])
            s2 = ''
            for f in y:
                s2 += str(path[int(f)])
        else:
            print('Sin Cruzamiento')
        print(s1,' - ',s2)
        if rand.uniform(0,1) <= p_mut:
            m = population.shape[1]
            p1 = rand.randint(0,m-1)
            p2 = rand.randint(0,m-1)
            aux = x[p1]
            x[p1] = x[p2]
            x[p2] = aux
            print('Mutacion 1')
            s11 = ''
            for f in x:
                s11 += str(path[int(f)])
            print('Posicion: ',p1,' - ',p2,' => ',s1,' - ',s11)
        else:
            print('Sin mutacion 1')
        if rand.uniform(0,1) <= p_mut:
            m = population.shape[1]
            p1 = rand.randint(0,m-1)
            p2 = rand.randint(0,m-1)
            aux = y[p1]
            y[p1] = y[p2]
            y[p2] = aux
            print('Mutacion 2')
            s22 = ''
            for f in x:
                s22 += str(path[int(f)])
            print('Posicion: ',p1,' - ',p2,' => ',s2,' - ',s22)
        else:
            print('Sin mutacion 2')
        print()
    print()

    return p_new

p_cross = 0.85
p_mut = 0.2
n = 2000
tsp = [ [0,12,3,23,1,5,23,56,12,11],
        [12,0,9,18,3,41,45,5,41,27],
        [3,9,0,89,56,21,12,48,14,29],
        [23,18,89,0,87,46,75,17,50,42],
        [1,3,56,87,0,55,22,86,14,33],
        [5,41,21,46,55,0,21,76,54,81],
        [23,45,12,75,22,21,0,11,57,48],
        [56,5,48,17,86,76,11,0,63,0,9],
        [12,41,14,50,14,54,57,63,0,9],
        [11,27,29,42,33,81,48,24,9,0]]

print('Parametros:')
print('- Cantidad de Individuos: ',8)
print('- Cantidad de Genes por Individuo: ',5)
print('- Selección por torneo (2)')
print('- Probabilidad de Cruzamiento: ',p_cross)
print('- Cruzamiento BLX-Alpha, Alpha = ',0.5)
print('- Probabilidad de Mutación: ',p_mut)
print('- Mutación Uniforme')
print('- Cantidad de Iteraciones: ',n)
r_genetic(8,16,p_cross,p_mut,tsp,n,min)
