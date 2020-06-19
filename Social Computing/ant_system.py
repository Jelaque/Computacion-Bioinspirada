import numpy as np
import math as mt
import random as rnd
import formatting as format

class AntSystem:

  letters = 'ABCDEFGHIJKLMNOPQRST'
  flt = np.float32

  def __init__(self,n_ants,size,init_city,distances,epochs,init_traces=0.1,alpha=1,beta=1,evap_rate=0.99,pher_ratio=1.0):

    self.n_ants = n_ants
    self.distances = distances
    self.epochs = epochs

    self.alpha = alpha
    self.beta = beta
    self.evap_rate = evap_rate
    self.pher_ratio = pher_ratio
    self.init_city = init_city

    self.places = size
    self.formatting = format.Formatting()

    if type(init_traces) == float:
      init_traces = self.flt(init_traces)
      self.pheromones = np.full( int(self.places * (self.places - 1) / 2), init_traces)
    else:  
      self.pheromones = init_traces

  @staticmethod
  def hash(dim,offset,n_places):

    if offset < dim:

      aux = offset
      offset = dim
      dim = aux
    
    return (dim * (n_places - dim)) + (offset - 1)

  @staticmethod
  def diagonal2matrix(vector,size):
    matrix = np.zeros((size,size))
    i = 0
    row = 1
    j = row
    for val in vector:
      matrix[i][j] = val 
      matrix[j][i] = val
      j += 1
      if j == size:
        row += 1
        j = row
        i += 1
    return matrix

  def diversify(self,visibilities):

    header1 = ['t','n','t*n']
    header2 = ['prob']

    arcs     = list(reversed(range(self.places)))
    cur_city = self.init_city
    ranges   = list(range(self.places))

    arcs.remove(0)
    path_cities = np.zeros(self.places)
    path_cities[0] = cur_city
    next = 1

    print(f'Init city: {self.letters[cur_city]}')

    for arc in arcs:

      roulette = np.zeros(arc)
      ranges.remove(cur_city)
      matrix_vals = []
      rows = []

      sum = 0
      it = 0
      for i in ranges:

        t = self.pheromones [self.hash(cur_city, i, self.places)]
        n = visibilities    [self.hash(cur_city, i, self.places)]
        t_n = t*n
        matrix_vals.append([t,n,t_n])
        rows.append(f'{self.letters[cur_city]}-{self.letters[i]}')
        roulette[it] = t_n
        sum += t_n
        it += 1

      self.formatting.print_table(rows,header1,matrix_vals,3)
      print(f'Sum: {sum:.5f}')

      roulette = roulette / sum

      self.formatting.print_table(rows,header2,roulette,1)

      prob = rnd.uniform(0,1)

      print(f'Random number probability: {prob:.5f}')

      it = 1
      while it < arc:
        roulette[it] += roulette[it-1]
        it += 1

      city = 0
      for limit in roulette:
        if prob < limit:
          break
        city += 1

      cur_city = ranges[city]
      path_cities[next] = cur_city
      next += 1

      print(f'Next city {self.letters[cur_city]}\n\n')

    return path_cities
    

  def update_pheromones(self,ant_paths,fitness):

    self.pheromones *= self.evap_rate
    #rows = []
    #cols = f'p-1'+self.letters[:self.places-1]

    p = 0
    for path in ant_paths:

      arcs = range(self.places - 1)
      wcost = self.pher_ratio / fitness[p]

      for arc in arcs:

        id = self.hash(path[arc],path[arc+1],self.places)
        self.pheromones[id] += wcost

      p += 1
          
  def fit(self,ant_paths):

    fitness = np.zeros(self.n_ants)
    
    p = 0
    for path in ant_paths:
      arcs = range(self.places - 1)
      sum = 0

      for arc in arcs:

        sum += self.distances[self.hash(path[arc], path[arc+1], self.places)]

      fitness[p] = sum
      p += 1

    return fitness

  def print_path(self,path):

    spath = ''
    places = range(self.places-1)
    for p in places:
      spath += self.letters[path[p]] + ' - '
    spath += self.letters[path[self.places-1]]

    print(spath)

  def train(self):

    ant_paths = np.zeros((self.n_ants, self.places), dtype=int)

    visibilities = np.copy(1 / self.distances)

    """places = size points of the travel"""
    #init_city = rnd.randint(0, self.places - 1)

    print("Distances matrix")
    self.formatting.print_table(  self.letters[:self.places],
                                  self.letters[:self.places],
                                  self.diagonal2matrix(self.distances,self.places),
                                  self.places)

    epoch = 0

    best_ant = 0
    while epoch < self.epochs:

      print(f'########Epoch {epoch+1}#########\n')

      print("Visibility matrix")
      self.formatting.print_table(  self.letters[:self.places],
                                  self.letters[:self.places],
                                  self.diagonal2matrix(visibilities,self.places),
                                  self.places)

      print("Pheromona trace's")
      self.formatting.print_table(  self.letters[:self.places],
                                  self.letters[:self.places],
                                  self.diagonal2matrix(self.pheromones,self.places),
                                  self.places)
      print('---------------------------------\n')

      ants = range(self.n_ants)

      for ant in ants:
        
        print(f'Ant {ant+1}')
        ant_paths[ant] = self.diversify(visibilities)
        print(f'Ant {ant+1}: ',end='')
        self.print_path(ant_paths[ant])
        print('\n')
                
      fitness = self.fit(ant_paths)

      self.update_pheromones(ant_paths, fitness)
      
      best = fitness[0]
      best_ant = 0
      costs = range(1,self.n_ants)
      for c in costs:
        if fitness[c] < best:
          best_ant = c

      print(f'Epoch{epoch}/{self.epochs}: Best ant: {self.print_path(ant_paths[best_ant])}, distance: {fitness[best_ant]}')
      print('\n')
      epoch += 1

    print(f'Epoch{epoch}/{self.epochs}: Best ant: {self.print_path(ant_paths[best_ant])}, Best distance: {fitness[best_ant]}')

def main():
  distances = np.array([12,3,23,1,5,23,56,12,11,9,18,3,41,45,5,41,27,89,56,21,12,48,14,29,87,46,75,17,50,42,55,22,86,14,33,21,76,54,81,11,57,48,63,24,9], AntSystem.flt)
  #distances = np.array([12,3,23,1,9,18,3,89,56,87],AntSystem.flt)
  model = AntSystem(5,10,3,distances,100,0.1)
  model.train()

main()