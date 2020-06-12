import statistics as stats
from statistics import NormalDist
import numpy as np
import math as mt
import random as rdm


def mu_lam(low,high,n,mu,lam,p,f,it,fit):

    dec = round(mt.pow(1.5,-0.25),15)
    det = round(mt.sqrt(2*mt.sqrt(n)),15)
    np.set_printoptions(precision=p)

    #initialization
    values = np.random.uniform(low,high,(mu,n))
    sigma = np.full((mu,n),0.2)
    print("Init population")
    print_po(values, sigma,mu)

    #first aptitude
    ap = calc(values,f,mu)
    print("Aptitude of the population")
    print_ap(values,sigma,ap,mu)

    ii = 1
    it += 1

    while(ii < it):

        values_n = np.zeros((lam,n))
        sigma_n = np.zeros((lam,n))
        f_n = np.zeros((lam,1))
        print("*****Iteration ",ii,"*****")
        for i in range(0,lam):
            #Select the parents
            print("Descendent N",i+1)
            print("Cross")
            mu_ = mu - 1
            indx1 = rdm.randint(0,mu_)
            indx2 = rdm.randint(0,mu_)
            if f(values[indx1]) < f(values[indx2]):
                p1 = indx1
            else:
                p1 = indx2
            print(indx1,'-',indx2,' => ',p1,' => ',values[p1],sigma[p1])
            indx1 = rdm.randint(0,mu_)
            indx2 = rdm.randint(0,mu_)
            if f(values[indx1]) < f(values[indx2]):
                p2 = indx1
            else:
                p2 = indx2
            print(indx1,'-',indx2,' => ',p2,' => ',values[p2],sigma[p2])

            child = np.zeros(n)
            sigma_ = np.zeros(n)
            for j in range(0,n):
                child[j] = np.mean([values[p1][j],values[p2][j]])
                sigma_[j] = mt.sqrt(sigma[p1][j]*sigma[p2][j])

            al_g = np.zeros(n)
            N1 = NormalDist(0,det)
            print("Mutation")
            for j in range(0,n):
                al = rdm.uniform(0,1)
                sigma_[j] *= mt.exp(N1.inv_cdf(al))
                N2 = NormalDist(0,sigma_[j])
                al = rdm.uniform(0,1)
                child[j] += N2.inv_cdf(al)
            print(child,sigma_,'\n')
            values_n[i] = child
            sigma_n[i] = sigma_
            f_n[i] = f(child)

        print("Aptitude of the all population")
        print_ap(values,sigma,ap,mu)

        L = np.hstack([values_n,sigma_n,f_n.reshape(1,lam).T])
        L = L[L[:,2*n].argsort(axis=0)]
        L = np.delete(L,slice(mu,lam),axis=0)
        values = np.copy(L[:,[0,n-1]])
        sigma = np.copy(L[:,[n,(2*n)-1]])
        ap = calc(values,f,mu)
        print("Aptitude of the new population")
        print_ap(values,sigma,ap,mu)
        #print(values,sigma,f(values),'\n')
        ii += 1


def print_np(L,lam,n):
    for i in range(0,lam):
        print(L[i][0:n],L[i][n:2*n],L[2*n])

def calc(m,f,n):
    ap = np.zeros(n)
    for i in range(0,n):
        ap[i] = f(m[i])
    return ap

def print_po(x,y,n):
    for i in range(0,n):
        print(x[i],'\t',y[i],'\n')

def print_ap(x,y,z,n):
    for i in range(0,n):
        print(x[i],'\t',y[i],'\t',z[i],'\n')

def print_al(n,x,y):
    print("Random number ",n,": ",x, "Gaussian random number:",y)

def f(v): return -mt.cos(v[0])*mt.cos(v[1])*mt.exp(-mt.pow(v[0]-mt.pi,2)-mt.pow(v[1]-mt.pi,2))

mu_lam(-10,10,2,8,10,5,f,300,min)
