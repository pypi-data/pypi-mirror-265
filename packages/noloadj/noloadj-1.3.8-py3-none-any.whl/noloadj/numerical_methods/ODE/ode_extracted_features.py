import jax.numpy as np
from jax import jvp
from abc import abstractmethod

################################################################################
# TIME FEATURES
def T_pair(T):
    return lambda t:(t//T)%2==0

def T_impair(T):
    return lambda t:(t//T)%2!=0

def T_numero(T,n,i):
    return lambda t:(t//T)%n!=i

class TimeFeature:

    def __init__(self,name):
        self.name=name
        self.type='time'
    @abstractmethod
    def init(self,x0,t0,h0):
        pass
    @abstractmethod
    def expression(self,t_prev,x_prev,t_now,x_now,cstr,h_prev,T):
        pass
    @abstractmethod
    def fin(self,tf,cstr,T):
        pass
    @abstractmethod
    def dinit(self,x0,dx0,t0,h0):
        pass
    @abstractmethod
    def der_expression(self,t_prev,x_prev,dx_prev,t_now,x_now,dx_now,cstr,dcstr,
                    h_prev,T,dT):
        pass
    @abstractmethod
    def der_fin(self,tf,cstr,_,dcstr,dT,xf):
        pass


class Min(TimeFeature):
    '''
    Minimum of a variable over a dynamic simulation.
    '''
    def __init__(self,name):
        TimeFeature.__init__(self,name)
    def init(self,x0,t0,h0):
        return x0
    def expression(self,t_prev,x_prev,t_now,x_now,cstr,h_prev,_):
        return np.minimum(x_now,cstr)
    def fin(self,tf,cstr,_):
        return cstr
    def dinit(self,x0,dx0,t0,h0):
        return dx0
    def der_expression(self,t_prev,x_prev,dx_prev,t_now,x_now,dx_now,cstr,dcstr,
                    h_prev,_,__):
        return np.where(np.minimum(cstr,x_now)==x_now,dx_now,dcstr)
    def der_fin(self,tf,cstr,_,dcstr,dT,xf):
        return dcstr

class Max(TimeFeature):
    '''
    Maximum of a variable over a dynamic simulation.
    '''
    def __init__(self,name):
        TimeFeature.__init__(self,name)
    def init(self,x0,t0,h0):
        return x0
    def expression(self,t_prev,x_prev,t_now,x_now,cstr,h_prev,_):
        return np.maximum(x_now,cstr)
    def fin(self,tf, cstr, _):
        return cstr
    def dinit(self,x0, dx0, t0, h0):
        return dx0
    def der_expression(self,t_prev,x_prev,dx_prev,t_now,x_now,dx_now,cstr,dcstr,
                    h_prev,_,__):
        return np.where(np.maximum(cstr,x_now)==x_now,dx_now,dcstr)
    def der_fin(self,tf, cstr, _, dcstr, dT, xf):
        return dcstr

class moy(TimeFeature):
    '''
    Average value of a variable over a dynamic simulation.
    '''
    def __init__(self,name):
        TimeFeature.__init__(self,name)
    def init(self,x0,t0,h0):
        return 0.
    def expression(self,t_prev,x_prev,t_now,x_now,cstr,h_prev,_):
        return cstr+0.5*h_prev*(x_prev+x_now)
    def fin(self,tf,cstr,_):
        return cstr/tf
    def dinit(self,x0,dx0,t0,h0):
        return 0.
    def der_expression(self,t_prev,x_prev,dx_prev,t_now,x_now,dx_now,cstr,dcstr,
                    h_prev,_,__):
        return dcstr+0.5*h_prev*(dx_prev+ dx_now)
    def der_fin(self,tf,cstr,_,dcstr,dT,xf):
        return dcstr/tf

class eff(TimeFeature):
    '''
    RMS value of a variable over a dynamic simulation.
    '''
    def __init__(self,name):
        TimeFeature.__init__(self,name)
    def init(self,x0,t0,h0):
        return 0.
    def expression(self,t_prev,x_prev,t_now,x_now,cstr,h_prev,_):
        return cstr+0.5*h_prev*(x_prev**2+x_now**2)
    def fin(self,tf,cstr,_):
        return np.sqrt(cstr/tf)
    def dinit(self,x0,dx0,t0,h0):
        return 0.
    def der_expression(self,t_prev,x_prev,dx_prev,t_now,x_now,dx_now,cstr,dcstr,
                    h_prev,_,__):
        return dcstr+0.5*h_prev*(2*x_prev*dx_prev+2*x_now* dx_now)
    def der_fin(self,tf,cstr,_,dcstr,dT,xf):
        return dcstr/(2*tf*cstr)

class min_T(TimeFeature):
    '''
    Minimum of a variable over a period of dynamic simulation.
    '''
    def __init__(self,name,nbT=1):
        TimeFeature.__init__(self,name)
        self.nbT=nbT
    def init(self,x0,t0,h0):
        return x0
    def expression(self,t_prev,x_prev,t_now,x_now,cstr,h_prev,T):
        return np.where((t_prev//(self.nbT*T))==(t_now//(self.nbT*T)),
                        np.minimum(x_now,cstr),x_now)
    def fin(self,tf,cstr,T):
        return cstr
    def dinit(self,x0,dx0,t0,h0):
        return dx0
    def der_expression(self,t_prev,x_prev,dx_prev,t_now,x_now,dx_now,cstr,dcstr,
                    h_prev,T,dT):
        return jvp(self.expression,(t_prev,x_prev,t_now,x_now,cstr,h_prev,T),
                   (0.,dx_prev,0.,dx_now,dcstr,0.,dT))[1]
    def der_fin(self,tf,cstr,T,dcstr,dT,xf):
        return dcstr

class max_T(TimeFeature):
    '''
    Maximum of a variable over a period of dynamic simulation.
    '''
    def __init__(self,name,nbT=1):
        TimeFeature.__init__(self,name)
        self.nbT=nbT
    def init(self,x0,t0,h0):
        return x0
    def expression(self,t_prev,x_prev,t_now,x_now,cstr,h_prev,T):
        return np.where((t_prev//(self.nbT*T))==(t_now//(self.nbT*T)),
                        np.maximum(x_now,cstr),x_now)
    def fin(self,tf,cstr,T):
        return cstr
    def dinit(self,x0,dx0,t0,h0):
        return dx0
    def der_expression(self,t_prev,x_prev,dx_prev,t_now,x_now,dx_now,cstr,dcstr,
                    h_prev,T,dT):
        return jvp(self.expression,(t_prev,x_prev,t_now,x_now,cstr,h_prev,T),
                   (0.,dx_prev,0.,dx_now,dcstr,0.,dT))[1]
    def der_fin(self,tf,cstr,T,dcstr,dT,xf):
        return dcstr

class moy_T(TimeFeature):
    '''
    Average value of a variable over a period of dynamic simulation.
    '''
    def __init__(self,name):
        TimeFeature.__init__(self, name)
    def init(self,x0,t0,h0):
        return 0.
    def expression(self,t_prev,x_prev,t_now,x_now,cstr,h_prev,T):
        return np.where((t_prev//T)==(t_now//T),cstr+0.5*h_prev*(x_prev+x_now),
                        0.)
    def fin(self,tf,cstr,T):
        return cstr/T
    def dinit(self,x0,dx0,t0,h0):
        return 0.
    def der_expression(self,t_prev,x_prev,dx_prev,t_now,x_now,dx_now,cstr,dcstr,
                    h_prev,T,dT):
        return np.where((t_prev//T)==(t_now//T),dcstr+0.5*h_prev*(dx_prev+
                                                                  dx_now),0.)
    def der_fin(self,tf,cstr,T,dcstr,dT,xf):
        return dcstr/T+((xf-cstr)/T)*dT

class eff_T(TimeFeature):
    '''
    RMS value of a variable over a period of dynamic simulation.
    '''
    def __init__(self,name):
        TimeFeature.__init__(self,name)
    def init(self,x0,t0,h0):
        return 0.
    def expression(self,t_prev,x_prev,t_now,x_now,cstr,h_prev,T):
        return np.where((t_prev//T)==(t_now//T),cstr+0.5*h_prev*(x_prev**2+
                                                                 x_now**2),0.)
    def fin(self,tf,cstr,T):
        return np.sqrt(cstr/T)
    def dinit(self,x0,dx0,t0,h0):
        return 0.
    def der_expression(self,t_prev,x_prev,dx_prev,t_now,x_now,dx_now,cstr,dcstr,
                    h_prev,T,dT):
        return np.where((t_prev//T)==(t_now//T),dcstr+0.5*h_prev*(2*x_prev*
                                    dx_prev+2*x_now*dx_now),0.)
    def der_fin(self,tf,cstr,T,dcstr,dT,xf):
        return dcstr/(2*T*cstr)+(xf**2-cstr**2)/(2*cstr*T)*dT

################################################################################
# FREQUENCY FEATURES

class FreqFeature:

    def __init__(self,name):
        self.name=name
        self.type='freq'
    @abstractmethod
    def expression(self,module,phase,vect_freq,f):
        pass
    @abstractmethod
    def der_expression(self,module,phase,dmodule,dphase,vect_freq,f):
        pass


class Module_0Hz(FreqFeature):
    '''
    Module of the FFT of a variable for frequency=0Hz
    '''
    def __init__(self,name):
        FreqFeature.__init__(self,name)
    def expression(self,module,phase,vect_freq,f):
        res=module[0]
        return res
    def der_expression(self,module,phase,dmodule,dphase,vect_freq,f):
        res=module[0]
        dres=dmodule[0]
        return res,dres

class Module_Fondamental(FreqFeature):
    '''
    Module of the FFT of a variable for fundamental frequency
    '''
    def __init__(self,name):
        FreqFeature.__init__(self,name)
    def expression(self,module,phase,vect_freq,f):
        indf=np.argmin(np.abs(vect_freq-f))
        res=module[indf]
        return res
    def der_expression(self,module,phase,dmodule,dphase,vect_freq,f):
        indf=np.argmin(np.abs(vect_freq-f))
        res=module[indf]
        dres=dmodule[indf]
        return res,dres

class Module_Harmoniques(FreqFeature):
    '''
    Module of the FFT of a variable for multiples of fundamental frequency
    '''
    def __init__(self,name,number):
        FreqFeature.__init__(self,name)
        self.number=number
    def expression(self,module,phase,vect_freq,f):
        if isinstance(self.number,int):
            res=np.zeros(self.number)
            for j in range(len(res)):
                indf=np.argmin(np.abs(vect_freq-(j+2)*f))
                res=res.at[j].set(module[indf])
        else:
            res=np.zeros(len(self.number))
            for j in range(len(res)):
                indf=np.argmin(np.abs(vect_freq-self.number[j]))
                res=res.at[j].set(module[indf])
        return res
    def der_expression(self,module,phase,dmodule,dphase,vect_freq,f):
        if isinstance(self.number,int):
            res = np.zeros(self.number)
            dres=np.zeros(self.number)
            for j in range(len(res)):
                indf=np.argmin(np.abs(vect_freq-(j+2)*f))
                res=res.at[j].set(module[indf])
                dres=dres.at[j].set(dmodule[indf])
        else:
            res = np.zeros(len(self.number))
            dres=np.zeros(len(self.number))
            for j in range(len(res)):
                indf=np.argmin(np.abs(vect_freq-self.number[j]))
                res=res.at[j].set(module[indf])
                dres=dres.at[j].set(dmodule[indf])
        return res,dres

class THD(FreqFeature):
    '''
    Total Harmonic Distorsion (THD) of a variable.
    '''
    def __init__(self,name):
        FreqFeature.__init__(self, name)
    def expression(self,module,phase,vect_freq,f):
        ref=np.maximum(module[0],module[1])
        harm=module[2::]
        THD=np.sqrt(np.sum(harm**2))/ref
        return THD
    def der_expression(self,module,phase,dmodule,dphase,vect_freq,f):
        ref=np.maximum(module[0],module[1])
        dref=np.where(ref==module[0],dmodule[0],dmodule[1])
        harm,dharm=module[2::],dmodule[2::]
        THD=np.sqrt(np.sum(harm**2))/ref
        dTHD=-dref*THD/ref+np.sum(np.dot(harm,dharm))/(ref*ref*THD)
        return THD,dTHD

