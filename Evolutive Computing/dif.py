import random as rm
import numpy as np
import math as mt

#limits is a matrix dims*2
def init_dif(size, dims, limits):

  population = np.zeros((size,dims))

  i = 0
  while i < size:
    j = 0
    while j < dims:
      min_limit = limits[j][0]
      max_limit = limits[j][1]
      population[i][j] = rm.uniform(min_limit,max_limit)
      j += 1
    i += 1

  return population

def print_population(population):

  i = 1
  for indiv in population:
    code = f'{i})\t'
    for dim in indiv:
      code += f'{dim:.4f}\t'
    print(code)
    i += 1

def fitness(population,size_population,size_dim,fit):

  vec_fitness = np.zeros(size_population)

  i = 0
  for indv in population:
    vars_ = np.zeros(size_dim)
    j = 0
    for dim in indv:
      vars_[j] = dim
      j += 1
    vec_fitness[i] = fit(vars_)
    i += 1

  return vec_fitness

def print_fitness(population,vec_fitness,size_population):

  i = 0
  for indv in population:
    code = f'{i+1}) '
    for dim in indv:
      code += f'\t{dim:.4f}'
    code += f'\t\t{vec_fitness[i]}'
    print(code)
    i += 1

def differential(size_population, dims, limits, fit, epochs, c_cross, c_mut):

  population = init_dif(size_population,dims,limits)
  population = np.asarray(population, dtype=float)
  print("Init population")
  print_population(population)

  vec_fitness = fitness(population,size_population,dims,fit)
  print("Fitness of init population")
  print_fitness(population,vec_fitness,size_population)

  total_epochs = epochs + 1
  epoch = 1
  while epoch <= total_epochs:

    print(f'Iteration {epoch}\n')

    n_vec = 1
    total_vecs = size_population + 1
    indexes = list(range(0,size_population))

    while n_vec < total_vecs:

      print(f'Vector {n_vec}')
      print('Mutation')

      indexes = np.random.permutation(size_population)
      rand_1 = indexes[0]
      rand_2 = indexes[1]
      rand_3 = indexes[2]

      print(f'Random r1 = {rand_1}, random r2 = {rand_2}, random r3 = {rand_3}')

      vec_dif = population[rand_2] - population[rand_3]
      print(f'Diff vector (r2 - r3):\t\t\t\t\t',end = '')
      format_code(vec_dif, '\n')

      vec_wdif = c_mut * vec_dif
      print(f'Weighted vector (c_mut * (r2 - r3)):\t\t',end='')
      format_code(vec_wdif, '\n')

      vec_mut = population[rand_1] + vec_wdif
      print(f'Mutable vector (r1 + (c_mut * (r2 - r3))):\t',end='')
      format_code(vec_mut,'\n')

      print("Crossover")
      pos_vec = n_vec - 1
      vec_trial = np.copy(population[pos_vec])
      for pos in range(dims):
        p = rm.uniform(0,1)
        print(f'Probabilities({pos+1}): {p:.4f}')
        if p < c_cross:
          vec_trial[pos] = vec_mut[pos]

      print('Vector trial: ', end = '')
      format_code(vec_trial, '')
      fit_vec_trial = fit(vec_trial)
      print(f' fitness: {(fit_vec_trial)}')
      print(fit_vec_trial)
      if fit_vec_trial < vec_fitness[pos_vec]:
        population[pos_vec] = vec_trial
        print('Push vector trial on new population')
      else:
        print('Keep vector target on population')
      print()
      n_vec += 1

    print('New population')
    vec_fitness = fitness(population,size_population,dims,fit)
    print_fitness(population,vec_fitness,size_population)
    print()
    epoch += 1

def format_code(vec,final):
  print('[',end = '')
  for var in vec:
    print(f' {var:.4f}',end = '')
  print(' ]', end = final)

def f(v):
  x = v[0]
  y = v[1]
  a = v[2]
  b = v[3]
  return  pow((x + (2*y) - 7),2) + \
          pow(((2*x) + y - 5),2) + \
          pow((a + (2*b) - 7),2) + \
          pow(((2*a) + b - 5),2)

differential(8,4,[[-10,10],[-10,10],[-10,10],[-10,10]],f,75,0.5,1.2)
