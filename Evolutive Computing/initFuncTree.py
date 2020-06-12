import numpy as np
import random as rm

def res(x,y): return x - y
def mul(x,y): return x * y
def div(x,y): return x / y
def sum(x,y): return x + y

ops = {'+':sum, '-':res, '*':mul, '/':div}

list_vals = "xyzwvu"
list_ops = "+-*/"
vals = np.zeros(0)

def init_func_tree(size,n_vals,entry):

  sign = False
  i = 0
  while i < len(entry):
    if entry[i][0] == 0:
      sign = True
    i += 1
  func_tree = []
  i = 0
  while i < size:
    var = None
    if not (i & 1):
      if rm.uniform(0,1) > .8:
        var = round(rm.uniform(-100,100),2)
      else:
        var = list_vals[rm.randint(0,n_vals-1)]
        if sign and i - 1 > 0 and func_tree[i-1] == '/':
          func_tree[i-1] = list_ops[rm.randint(0,len(list_ops)-2)]
    else:
      var = list_ops[rm.randint(0,len(list_ops)-1)]
    func_tree.append(var)
    i += 1

  return func_tree
