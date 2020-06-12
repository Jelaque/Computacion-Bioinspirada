import random as rand
import numpy as np
import math

def scale(X, x_min, x_max):
    nom = (X-X.min(axis=0))*(x_max-x_min)
    denom = int(X.max(axis=0) - X.min(axis=0))
    denom[denom==0] = 1
    return x_min + nom/denom


def r_genetic(limit,dec,n_genes,N,p_cross,p_mut,func,it,mode):

    population = rget_population(dec,n_genes,N,limit)

    print('Poblacion inicial')
    print_pop_initial(population)

    fitness = rdecode(population,func)

    print_fitness(population,fitness,N)

    i = 1
    it = it + 1

    while i < it:
        print('****Iteracion ',i,'****')

        parents = rmating_pool(population, fitness, mode)

        population = rselect_parents(population, parents, fitness, p_cross, p_mut)

        fitness = rdecode(population,func)

        print('Nueva Poblacion')
        print_pop_initial(population)

        print_fitness(population,fitness,N)

        i += 1

def print_pop_initial(population):
    i = 1
    for row in population:
        print(i,')\t\t',row)
        i += 1
    print()

def print_fitness(population,fitness,n):
    i = 1
    print('Calcular la Aptitud para cada Individudo')
    j = 0
    for row in population:
        print(i,')\t\t',row,'\t\t',fitness[j])
        i += 1
        j += 1
    print()

def rget_population(dec,n_genes,N,limit):

    population = np.random.rand(N,n_genes)

    for i in range(0,2):
        population[:,i] = np.interp(population[:,i], (min(population[:,i]), max(population[:,i])), (-10,10))

    population = np.around(population, decimals = dec)

    return population

def rdecode(population, func):

    fitness = np.zeros(population.shape[0])

    for i in range(0,population.shape[0]):
        fitness[i] = func(population[i])

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
        print(a+1,'\t\t',b+1,'\t\t=>\t\t',int(parents[i])+1,'\t\t=>\t\t',population[int(parents[i])])
    print()

    return parents

def rselect_parents(population, parents, fitness, p_cross, p_mut):

    population = np.around(population,decimals=5)
    p_new = population
    n = population.shape[0]

    for i in range(0,n):
        a = rand.randint(0,n-1)
        b = rand.randint(0,n-1)
        r = population[int(parents[a])]
        s = population[int(parents[b])]
        pcss = 0
        print('Seleccion de Padres')
        print(a+1,'\t',b+1,' => ',int(parents[a])+1,' - ',int(parents[b])+1,' => ',r,' - ',s)
        if rand.uniform(0,1) >= p_cross:
            beta1 = rand.uniform(-0.5,1.5)
            beta2 = rand.uniform(-0.5,1.5)
            z = r
            x = r
            y = s
            x = [z[0],y[0]]
            y = [z[1],y[1]]
            H = abs(x[0]-x[1])
            lim = H*beta1
            v1 = round(rand.uniform(min(x)-lim,max(x)+lim),5)
            H = abs(y[0]-y[1])
            lim = H*beta2
            v2 = round(rand.uniform(min(y)-lim,max(y)+lim),5)
            if(v1 > 10 and v1 < -10) or (v2 > 10 and v2 < -10):
                if fitness[int(parents[a])] < fitness[int(parents[b])]:
                     p_new[i] = r
                else:
                     p_new[i] = s
            else:
                p_new[i] = [v1,v2]
            pcss = 1
            print('Cruzamiento')
        else:
            if fitness[int(parents[a])] < fitness[int(parents[b])]:
                p_new[i] = r
            else:
                p_new[i] = s
            print('Sin Cruzamiento')
        print(p_new[i])
        if rand.uniform(0,1) >= p_mut:
            d = mutation(p_new[i])
            if(d[0] <= 10 and d[0] >= -10) or (d[1] <= 10 and d[1] >= -10):
                p_new[i] = d
            print('Mutacion')
        else:
            print('Sin mutacion')
        print(p_new[i])
        print()
    print()

    return p_new

def mutation(vec):
    for i in range(0,len(vec)):
        vec[i] = round(rand.uniform(vec[i]-0.3,vec[i]+0.3),5)
    return vec

p_cross = 0.75
p_mut = 0.5
n = 5000
def f(x):
    return -math.cos(x[0])*math.cos(x[1])*math.exp(-math.pow(x[0]-math.pi,2)-math.pow(x[1]-math.pi,2))
print(f([8.29,-1.21]))
print('Parametros:')
print('- Cantidad de Individuos: ',16)
print('- Cantidad de Genes por Individuo: ',2)
print('- Selección por torneo (2)')
print('- Probabilidad de Cruzamiento: ',p_cross)
print('- Cruzamiento BLX-Alpha, Alpha = ',0.5)
print('- Probabilidad de Mutación: ',p_mut)
print('- Mutación Uniforme')
print('- Cantidad de Iteraciones: ',n)
r_genetic([[-100,100],[-100,100]],5,2,16,p_cross,p_mut,f,n,min)
