import statistics as stats
from statistics import NormalDist
import numpy as np
import math as mt
import random as rdm


def one_one(low,high,n,p,f,it,fit):

    dec = round(mt.pow(1.5,-0.25),15)
    np.set_printoptions(precision=p)

    #initialization
    values = np.random.uniform(low,high,n)
    sigma = 0.2
    print("Init population")
    print(values, sigma,'\n')

    #first aptitude
    ap = f(values)
    print("Aptitude of the population")
    print(values,sigma,ap,'\n')

    ii = 1
    it += 1

    while(ii < it):

        print("*****Iteration ",ii,"*****")
        print(values,sigma,ap)
        al_g = np.zeros((n,))
        N = NormalDist(0,sigma)
        for i in range(0,n):
            al = rdm.uniform(0,1)
            al_g[i] = N.inv_cdf(al)
            print_al(i+1,al,al_g[i])

        new_values = np.copy(values)
        for i in range(0,n):
            new_values[i] += al_g[i]

        if f(new_values) <= f(values):
            values = np.copy(new_values)
            sigma *= 1.5
        else:
            sigma *= dec
        sigma = round(sigma,30)

        print(values,sigma,f(values),'\n')
        ii += 1

def print_al(n,x,y):
    print("Random number ",n,": ",x, "Gaussian random number:",y)

def f(v): return round(-mt.cos(v[0])*mt.cos(v[1])*mt.exp(-mt.pow(v[0]-mt.pi,2)-mt.pow(v[1]-mt.pi,2)),30)

one_one(-10,10,2,5,f,1000,min)
