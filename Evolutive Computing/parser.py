import initFuncTree as ift
level_ops = {'+':1, '-':1, '*':2, '/':2}

def fit_func_tree(infix,vals):
  """Passing infix string to posfix notation"""

  stack = []
  stackSize = 0
  buff = []
  n_vals = len(vals)
  for ch in infix:
    if is_operand(ch):
      if (not stack) or (level_ops[ch] > level_ops[stack[stackSize-1]]):
        stack.append(ch)
        stackSize += 1
      else:
        while stack and level_ops[ch] <= level_ops[stack[stackSize-1]]:
          a = buff.pop()
          b = buff.pop()
          buff.append(ift.ops[stack.pop()](b,a))
          stackSize -= 1
        stack.append(ch)
    else:
      if type(ch) == float:
        buff.append(float(ch))
      else:
        buff.append(float(vals[ift.list_vals.find(ch)]))
  r = buff.pop()
  while stack:
    r_ = buff.pop()
    r = ift.ops[stack.pop()](r_,r)

  return r

def is_operand(c):
  if c == '+':
    return True
  elif c == '-':
    return True
  elif c == '*':
    return True
  elif c == '/':
    return True
  else:
    return False

def is_val(c):
  if ift.list_vals.find(c) != -1:
    return True
  else:
    return Falste
