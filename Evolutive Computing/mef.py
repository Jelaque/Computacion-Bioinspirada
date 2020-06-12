import random as rm
import numpy as np
import queue as qu

statery = "ABCDEFGHI"

def evolutionary(total_individuals,n_states,entry,epochs):

  population = np.zeros((total_individuals, (n_states*7)+1))
  init_states = np.zeros(total_individuals)
  pos_fit = n_states*7

  i = 0
  while i < total_individuals:

    population[i], init_states[i] = init_mef_individual(n_states)
    i += 1

  population = fit_population(population, entry, init_states, total_individuals, pos_fit)
  print_population(population)

  i = 0
  while i < epochs:

    new_population = np.copy(population)
    new_init_states = np.copy(init_states)

    i += 1
    j = 0
    while j < total_individuals:

      rand = rm.uniform(0,1)

      if rand <= 0.1:

        s = rm.randint(0,n_states-1)

        while s == new_init_states[j]:
          s = rm.randint(0,n_states-1)

        new_population[j][s*7] = 0

      elif rand <= 0.3:

        s = rm.randint(0,n_states-1)
        new_population[j][s*7] = 2
        new_population[j][int(new_init_states[j])] = 1
        new_init_states[j] = s

      elif rand <= 0.5:

        s = rm.randint(0,n_states-1)
        pos = s*7
        temp = new_population[j][pos+1]
        new_population[j][pos+1] = new_population[j][pos+2]
        new_population[j][pos+2] = temp

      elif rand <= 0.7:

        s = rm.randint(0,n_states-1)
        extra = rm.randint(1,2)
        pos = (s * 7) + 2 + extra
        val = new_population[j][pos]
        new_population[j][pos] = abs(val-1)

      elif rand <= 0.9:

        s = rm.randint(0,n_states-1)
        extra = rm.randint(1,2)

        ns = rm.randint(0,n_states-1)

        while new_population[j][7*ns] == 0:
          ns = rm.randint(0,n_states-1)

        new_population[j][(s*7) + 4 + extra] = ns

      else:

        s = rm.randint(0,n_states-1)
        if new_population[j][7*s] == 0:
          new_population[j][7*s] = 1
      print(j)
      j += 1

    new_population = fit_population(new_population, \
        entry, new_init_states, total_individuals, pos_fit)

    new_population = new_population[new_population[:,pos_fit].argsort(axis=0)]
    population = population[population[:,pos_fit].argsort(axis=0)]

    j = 0
    k = int(total_individuals/2)
    while j < k:

      population[j] = new_population[k+j]
      j += 1

  print(population)

def print_population(population):
  for individual in population:
    i = 0
    print(i+1,') ',end="")
    for s in individual:
      if i%5 == 0 or i%6 == 0:
        print(statery[int(s)],end="")
      else:
        print(s,end="")
      i += 1
    print()

def aptitude(val1,val2,n):

  i = 0
  c = 0
  while i < n:
    if val1[i] == val2[i]:
      c += 1
    i += 1

  return float(c/n)

def fit_population(population, entry, init_states, n, n_fit):

  i = 0
  while i < n:

    population[i][n_fit] = fit(population[i],entry,init_states[i])
    i += 1

  return population

def fit(individual,entry,init_state):

  outcome = ""
  n = len(entry)
  state = int(init_state)

  i = 0
  while i < n:

    symbol = entry[i]

    pos = state*7
    extra = 3

    if individual[pos+2] == int(symbol):
      extra = 4

    outcome += str(individual[pos+extra])

    if individual[int(individual[pos+extra+2])] != 0:
      state = int(individual[pos+extra+2])
    i += 1

  return aptitude(entry,outcome,n)

def init_mef_individual(n):

  population = np.zeros((7*n)+1)
  active_states = np.zeros(n)
  init_state = rm.randint(0,n-1)

  qStates = qu.Queue()

  """First case"""
  outState1,outState2 = fill_individual(init_state, population, n, 2)

  qStates.put(outState1)
  qStates.put(outState2)

  active_states[init_state] = 1

  while not qStates.empty():

    state = qStates.get()

    if active_states[state] == 0:

      outState1, outState2 = fill_individual(state, population, n, 1)

      qStates.put(outState1)
      qStates.put(outState2)

      active_states[state] = 1

  i = 0
  while i < n:
    if active_states[i] == 0:
      outState1, outState2 = fill_individual(state, population, n, 0)
    i += 1

  return population, init_state

def fill_individual(state, individual, n, type_state):

  it = 7*state
  individual[it] = type_state

  symbol_in = rm.randint(0,1)
  individual[it+1] = symbol_in
  individual[it+2] = abs(symbol_in-1)

  symbol_out1 = rm.randint(0,1)
  symbol_out2 = rm.randint(0,1)
  individual[it+3] = symbol_out1
  individual[it+4] = symbol_out2

  state_out1 = rm.randint(0,n-1)
  state_out2 = rm.randint(0,n-1)
  individual[it+5] = state_out1
  individual[it+6] = state_out2

  return state_out1, state_out2

evolutionary(8,5,"011011011011011",100)
