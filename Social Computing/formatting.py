import numpy as np

class Formatting:

  h_first   = f'    │'
  ch_first  = f'    ┌'
  hl_first  = f'┌───┬'
  fl_first  = f'┌───┼'
  ul_first  = f'├───┼'
  ll_first  = f'└───┴'

  ch_last   = f'──────┐'
  l_last    = f'──────┤'
  ll_last   = f'──────┘'

  ch_step   = f'──────┬'
  l_step    = f'──────┼'
  ll_step   = f'──────┴'
  
  @staticmethod
  def get_separator(first,step,last,length):
    separator = first
    separator += step * (length - 1)
    separator += last
    return separator
  
  @classmethod
  def print_header_ceil(cls,length):
    print(cls.get_separator(cls.ch_first,cls.ch_step,cls.ch_last,length))

  @classmethod
  def print_header_separator(cls,length):
    print(cls.get_separator(cls.h_first,cls.l_step,cls.ch_last,length))

  @classmethod
  def print_header_floor(cls,length):
    print(cls.get_separator(cls.fl_first,cls.l_step,cls.l_last,length))

  @classmethod
  def print_table_ceil(cls,length):
    print(cls.get_separator(cls.hl_first,cls.ch_step,cls.ch_last,length))

  @classmethod
  def print_table_separator(cls,length):
    print(cls.get_separator(cls.ul_first,cls.l_step,cls.l_last,length))

  @classmethod
  def print_table_floor(cls,length):
    print(cls.get_separator(cls.ll_first,cls.ll_step,cls.ll_last,length))

  @classmethod
  def print_header_cols(cls,vector):
    line = f'    │'
    for i in vector:
      line += f'{i:^6}│'
    print(line)
  
  @classmethod
  def print_lines_matrix(cls,id,vector):
    line = f'│{id:^3}│'
    if (type(vector) == np.ndarray) or (type(vector) == list):
      for i in vector:
        line += f'{i:^6.3f}│'
    else:
      line += f'{vector:^6.3f}│'
    print(line)

  @classmethod
  def print_lines_table(cls,id,vector,result):
    line = f'│{id:^3}│'
    if (type(vector) == np.ndarray) or (type(vector) == list):
      for i in vector:
        line += f'{i:^6.3f}│'
    else:
      line += f'{vector:^6.3f}│'
    line += result
    print(line)

  @classmethod
  def print_table(cls,rows,cols,matrix,length):
    cls.print_header_ceil(length)
    cls.print_header_cols(cols)
    cls.print_header_floor(length)
    size_rows = len(rows)
    i = 0
    for vector in matrix:
      cls.print_lines_matrix(rows[i],vector)
      i += 1
      if i < size_rows:
        cls.print_table_separator(length)
      else:
        cls.print_table_floor(length)

  @classmethod
  def print_table_ids(cls,ids,matrix,results,length):
    cls.print_table_ceil(length)
    i = 0
    size_rows = len(ids)
    for vector in matrix:
      cls.print_lines_table(ids[i],vector,results[i])
      i += 1
      if i < size_rows:
        cls.print_table_separator(length)
      else:
        cls.print_table_floor(length)
