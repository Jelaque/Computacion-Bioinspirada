import initFuncTree as ift
import parser as fit
import math as mt
import numpy as np
import random as rm

def tree_func(n_individuals,size_genes,entry,outcome,epochs,p_r=.2,s_r=3,s_c=2,p_c=.4,p_m=.4,s_m=3):

  p_c += p_r
  p_m += p_c

  population = [] #np.zeros((n_individuals,size_genes))
  fits = np.zeros(n_individuals)
  n_evals = len(entry)
  n_vals = len(entry[0])
  i = 0
  while i < n_individuals:

    population.append(ift.init_func_tree(size_genes,n_vals,entry))
    i += 1

  print("Init population")
  print_population(population)

  i = 0
  while i < n_individuals:
    j = 0
    accs = np.zeros(n_evals)
    v = np.zeros(n_evals)
    while j < n_evals:

      accs[j] = fit.fit_func_tree(population[i],entry[j])
      v[j] = accs[j] - outcome[j]
      j += 1
    fits[i] = distance(v)
    print("Fitness #",i+1,' ',population[i])
    print_fitness(entry,outcome,accs,v,n_evals)
    i += 1

  i = 0
  while i < epochs:
    print("***Iteracion ",i+1,"***")
    new_population = population.copy()
    j = 0
    while j < n_individuals:

      p = rm.uniform(0,1)
      print("Aleatorio: ",p)
      if p < p_r:
        print("**Replicacion**")
        new_population[j] = replication(population,fits,outcome)
        j += 1

      elif p < p_c:
        print("**Cruzamiento**")
        a,b = cross(population,fits,outcome,size_genes)
        if j + 2 < n_individuals:
          new_population[j] = a
          new_population[j+1] = b
          j += 2
        else:
          pchild = rm.randint(0,1)
          if pchild == 0:
            new_population[j] = a
          else:
            new_population[j] = b
          j += 1
        print("Tamaño de la nueva poblacion: ",j)

      else:
        print("**Mutacion**")
        new_population[j] = mutation(population,fits,outcome,size_genes)
        j += 1
      print("Tamaño de la nueva poblacion: ",j,'\n')

    population = new_population
    k = 0
    while k < n_individuals:
      j = 0
      accs = np.zeros(n_evals)
      v = np.zeros(n_evals)
      while j < n_evals:

        accs[j] = fit.fit_func_tree(population[i],entry[j])
        v[j] = accs[j] - outcome[j]
        j += 1
      fits[i] = distance(v)
      print("Fitness #",i+1,' ',population[i])
      print_fitness(entry,outcome,accs,v,n_evals)
      k += 1
    i += 1
    print(population)

def distance(actual):
  a = 0
  for i in actual:
    a += pow(i,2)
  return a/len(actual)

def print_fitness(entry,outcome,acc,dif,n):

  i = 0
  while i < n:
    print(entry[i][0],'\t',outcome[i],'\t',acc[i],'\t',abs(dif))
    i += 1
  print()

def print_population(population):
  for i in population:
    print(i)
  print()

def mutation(population,fits,outcome,size_genes):

  individual = replication(population,fits,outcome)
  mut = rm.randint(0,size_genes-1)
  print("Individuo a mutar: ",individual)
  print("Gen a mutar: ",mut)
  n_vals = 1
  var = None
  if not (mut & 1):
    if rm.uniform(0,1) > .8:
      var = round(rm.uniform(-100,100),2)
    else:
      var = ift.list_vals[rm.randint(0,n_vals-1)]
  else:
    var = ift.list_ops[rm.randint(0,len(ift.list_ops)-1)]
  individual[mut] = var

  return individual

def cross(population,fits,outcome,size_genes):

  n = len(population)
  p1 = rm.randint(0,n-1)
  p2 = rm.randint(0,n-1)
  p3 = rm.randint(0,n-1)
  p4 = rm.randint(0,n-1)

  d1 = fits[p1]
  d2 = fits[p2]
  d3 = fits[p3]
  d4 = fits[p4]

  c1 = p1
  c2 = p3
  if d2 < d1:
    c1 = p2
  if d4 < d3:
    c2 = p4
  print("Seleccionados para el torneo (2): ", p1,'-',p2,'=>',c1,'=>',population[c1])
  print("Seleccionados para el torneo (2): ", p3,'-',p4,'=>',c2,'=>',population[c2])

  cut = rm.randint(0,size_genes-1)
  print("Punto para el cruzamiento: ",cut)
  cp1 = population[c1]
  cp2 = population[c2]
  while cut < size_genes:
    aux = cp2[cut]
    cp2[cut] = cp1[cut]
    cp1[cut] = aux
    cut += 1

  return cp1, cp2

def replication(population,fits,outcome):

  n = len(population)
  p1 = rm.randint(0,n-1)
  p2 = rm.randint(0,n-1)
  p3 = rm.randint(0,n-1)
  print("Seleccionados para el torneo (3): ", p1,'-',p2,'-',p3)
  d1 = fits[p1]
  d2 = fits[p2]
  d3 = fits[p3]

  pos = 0
  if d2 < d1:
    if d2 < d3:
      pos = 1
    else:
      pos = 2
  else:
    if d3 < d1:
      pos = 2
  print("Mejor del torneo: ",pos)
  return population[pos]

tree_func(8,7,[[0],[0.1],[0.2],[.3],[.4],[.5],[.6],[.7],[.8],[.9]],[0,0.005,0.002,0.045,0.08,1.125,0.18,0.245,0.32,0.405],50)


