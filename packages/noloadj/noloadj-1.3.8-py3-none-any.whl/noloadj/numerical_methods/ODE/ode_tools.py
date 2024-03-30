import jax.numpy as np
from jax.lax import switch,cond
from jax import custom_jvp,jvp,Array
from functools import partial
from typing import Callable
from noloadj.numerical_methods.ODE.ode45_extract import final_time

def fonction(func):
    return lambda _: func()

def vect_temporel(debut,fin,pas):
    return np.linspace(debut,fin,int((fin-debut)/pas))

def indice_t(t,pas,debut=0.):
    return ((t-debut)/pas).astype(int)

def Switch(etat,funcs):
    return switch(etat,[fonction(func) for func in funcs],None)

def Condition(conditions,functions,state):
    for i in range(len(conditions)):
        state=cond(conditions[i],functions[i],lambda state:state,state)
    return state


###################################################### integrale
@partial(custom_jvp,nondiff_argnums=(0,1,2,3))
def integrale(t0,tf,pas,f,*inputs):
    '''
    Computes the integral of a function on a domain.

    :param t0: initial bound of the integral
    :param tf: final bounds of the integral
    :param pas: step size of the time vector
    :param f: the function on which the integral has to be computed
    :param inputs: input variables across a time vector
    :return: the integral value
    '''
    longueur=(tf-t0)/int(tf/pas)
    res=f(*inputs)
    S=2*np.sum(res)-res[0]-res[-1]
    S*=longueur*0.5
    return S

@integrale.defjvp
def integrale_jvp(t0,tf,pas,f,primals,tangents):
    longueur=(tf-t0)/int(tf/pas)
    primal_dot,tangent_dot=jvp(f,primals,tangents)
    S=2*np.sum(primal_dot)-primal_dot[0]-primal_dot[-1]
    S*=longueur*0.5
    dS = 2*np.sum(tangent_dot)-tangent_dot[0]-tangent_dot[-1]
    dS *= longueur * 0.5
    return S,dS
############################################################################

def vect_freq(t0,tf,Te):
    '''
    Computes the frequency vector for FFT computation.

    :param t0: initial time
    :param tf: final time
    :param Te: sampling period
    :return: the frequency vector
    '''
    M=int((tf-t0)/Te)
    freq=np.where(M//2==0,np.linspace(0.,(M/2-1)/(M*Te),M//2),
                          np.linspace(0.,(M-1)/(2*M*Te),M//2))
    return freq

def get_indice(names_vector,values_vector,desired_names):
    '''
    Returns the value(s) of an array corresponding to the variable name(s)
    given in desired_names.

    :param names_vector: a list with the names of state/output vector
    :param values_vector: the state/output vector
    :param desired_names: the name of the variable(s) to get
    :return: the value(s) of the desired names of variables in an array.
    '''
    if len(desired_names)==1:
        return values_vector[names_vector.index(desired_names[0])]
    else:
        return (values_vector[names_vector.index(i)] for i in desired_names)

from abc import abstractmethod

class ODESystem:
    '''
    Interface class to call when you create a dynamic system class.

    Attributes:
        - xnames : list for state variables names
        - ynames : list for output variables names
        - stop : Callable for stopping criteria
        - constraints : dict for features to extract from dynamic simulation
    '''
    def __init__(self):
        self.xnames:list=[]
        self.ynames:list=[]
        self.stop:Callable=final_time(1.0) # initialization with a stopping criteria
        self.constraints : dict={}

    @abstractmethod
    def timederivatives(self,X:Array,t:float,*P):
        '''
        Method to compute time derivatives of state vector.

        :param X: JaxArray : state vector at present iteration
        :param t: float :time at present iteration
        :param P: tuple : simulation parameters to optimize
        :return: JaxArray : time derivatives of state vector.
        '''
        pass

    @abstractmethod
    def output(self,X:Array,t:float,*P):
        '''
        Method to compute output vector.

        :param X: JaxArray : state vector at present iteration
        :param t: float :time at present iteration
        :param P: tuple : simulation parameters to optimize
        :return: JaxArray : output vector
        '''
        pass

