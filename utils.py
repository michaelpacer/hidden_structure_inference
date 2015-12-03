import numpy as np
from itertools import chain, combinations
from scipy.misc import logsumexp

def powerset(iterable):
#    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
#
    len_powerset = 0
    powerset_vals = chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
    return powerset_vals

def scale_free_sampler(lower_bound = 1/10, upper_bound=10, size = 1):
    """
    This allows you to approximate the improper probability
    distribution P(λ) = 1/λ for the positive reals

    This is accomplished by identifying a range of values you are 
    interested in sampling from 

    For example, the default arguments for the sampler generate a
    single value λ from the range 10^{-1} to 10 with the pdf 1/λ.
    """
    if lower_bound >=upper_bound:
        error_statement = "Lower bound must be below upper bound."
        raise ValueError(error_statement)

    # if lower_bound <= 0:
    #     error_statement = "Lower bound must be greater than upper bound."
    #     raise ValueError(error_statement)


    bottom_val = np.log(lower_bound)
    top_val = np.log(upper_bound)
    
    return list(np.exp(np.random.uniform(bottom_val,top_val, size)))

def logmeanexp(arr, axis=0, b=None):
    """Computes np.log(np.mean(np.exp(arr))) in a way that is tolerant 
    to underflow, using scipy.misc.logsumexp.

    """
    a_max = np.amax(arr, axis=axis, keepdims=True)
    if a_max.ndim > 0:
        a_max[~np.isfinite(a_max)] = 0
    elif not np.isfinite(a_max):
        a_max = 0
    for idx,a in enumerate(arr):
        try:
            np.exp(a - a_max)
        except FloatingPointError:
            if arr[idx] < 0:
                arr[idx]= -np.inf

    return logsumexp(arr, axis=axis, b=b) - np.log(arr.shape[axis])

def mdp_logsumexp(arr, axis=0, b=None):
    """Computes np.log(np.sum(np.exp(arr))) in a way that is even more
    tolerant to underflow than the original logsumexp function in scipy

    """
    a_max = np.amax(arr, axis=axis, keepdims=True)
    if a_max.ndim > 0:
        a_max[~np.isfinite(a_max)] = 0
    elif not np.isfinite(a_max):
        a_max = 0
    for idx,a in enumerate(arr):
        try:
            np.exp(a - a_max)
        except FloatingPointError:
            if arr[idx] < 0:
                arr[idx]= -np.inf

    return logsumexp(arr, axis=axis, b=b)
