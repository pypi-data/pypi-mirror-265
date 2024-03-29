from sympy import exp, sqrt, diff, lambdify, log
from sympy.abc import mu
from scipy.optimize import basinhopping
import numpy as np

def average(data, sigma):
    try:
        loglike = np.sum([log((1 - exp(-((d - mu) / s)**2 / 2))/(d - mu)**2) for d, s in zip(data, sigma)])
        ddloglike = diff(loglike, mu,2)
        negloglike = lambdify(mu, -loglike,)
        av = basinhopping(negloglike, np.average(data, weights = 1 / np.array(sigma)**2)).x[0]
        sig = 1 / sqrt(- ddloglike.subs(mu, av))
        return av, sig
    except Exception as e:
        print('An error accured. Please check your input.')