import jax.numpy as np
from jax import config
config.update("jax_enable_x64", True)
from jax.lax import *
from jax import custom_jvp,jvp
from functools import partial
from noloadj.numerical_methods.ODE.ode45 import next_der_step_simulation,\
    next_step_simulation,compute_new_point,odeint45,odeint45_etendu

def odeint45_extract(f,x0,*P,M=None,T=0.,h0=1e-5,tol=1.48e-8):
    '''
    Solves an ODE system described by f with Runge-Kutta 5 (7M) algorithm, without
    storing values across time and with features extraction.

    :param f: a class inherited from ODESystem abstract class that describes the ODE system
    :param x0: JaxArray: initial state vector
    :param P: tuple of JaxArray: optimization inputs
    :param M: int: number of points to compute the FFT
    :param T: float: operating period of the system (optional)
    :param h0: float: initial step size
    :param tol: float: tolerance for optimal step size computation
    :return: Several outputs :
    - final time 'tf'
    - final state vector 'xf'
    - final output vector 'yf'
    - extracted features dictionary 'cstr'
    - final configuration 'state' if the system is periodic.
    '''
    return _odeint45_extract(f,h0,tol,M,x0,T,*P)


@partial(custom_jvp,nondiff_argnums=(0,1,2,3))
def _odeint45_extract(f,h0,tol,M,x0,T,*P):
    type_,cond_stop=f.stop

    def cond_fn(state):
        x_prev2,x_prev,t_prev,_,h_prev,cstr,_,_=state
        if type_=='threshold':
            val,seuil=cond_stop(x_prev,f.xnames)
            valp,_=cond_stop(x_prev2,f.xnames)
            return (h_prev>0) & (np.sign(val-seuil)==np.sign(valp-seuil))
        else:
            return (h_prev > 0) & cond_stop(t_prev,t_prev+h_prev,cstr)


    def body_fn(state):
        _,x_prev,t_prev,y_prev,h_prev,cstr,i_prev,c_prev=state

        x_now,t_now,y_now,h_now,i_now,c_now=next_step_simulation(x_prev,t_prev,
                                    y_prev,i_prev,c_prev,h_prev,f,tol,T,*P)

        if type_=='threshold':
            output,seuil=cond_stop(x_now,f.xnames)
            outputprev,_=cond_stop(x_prev,f.xnames)
            condition=np.sign(output-seuil)!=np.sign(outputprev-seuil)
            x_now,h_prev,t_now,y_now=cond(condition,lambda state:
                compute_new_point(x_now,x_prev,t_prev,t_now,y_prev,y_now,
                output-seuil,outputprev-seuil),lambda state:state,(x_now,h_prev,
                                                                   t_now,y_now))
            x_now,t_now,y_now,h_now,i_now,c_now=cond(condition,lambda state:
                next_step_simulation(x_prev,t_prev,y_prev,i_prev,c_prev,h_prev,
                f,tol,T,*P),lambda state:state,(x_now,t_now,y_now,h_now,i_now,
                                                c_now))

        elif isinstance(type_,float):
            h_tf=type_-t_now
            h_now=np.minimum(h_now,h_tf)

        for i in f.constraints.keys():
            if isinstance(f.constraints[i],tuple):
                test_exp,feature=f.constraints[i]
            else:
                feature=f.constraints[i]
                test_exp = lambda t: True
            if feature.type=='time':
                if feature.name in f.xnames:
                    ind=f.xnames.index(feature.name)
                    cstr[i]=np.where(test_exp(t_now),feature.expression(t_prev,
                        x_prev[ind],t_now,x_now[ind],cstr[i],h_prev,T),cstr[i])
                else:
                    ind=f.ynames.index(feature.name)
                    cstr[i]=np.where(test_exp(t_now),feature.expression(t_prev,
                        y_prev[ind],t_now,y_now[ind],cstr[i],h_prev,T),cstr[i])

        return x_prev,x_now,t_now,y_now,h_now,cstr,i_now,c_now

    cstr=dict(zip(list(f.constraints.keys()),[0.]*len(f.constraints)))# INITIALISATION
    if hasattr(f,'state'):
        i0=f.state
    else:
        i0=0
    if hasattr(f,'commande'):
        _,c0=f.commande(0.,T)
    else:
        c0=0
    tempP=None
    if hasattr(f,'initialize'):
        tempP=P
        P=f.initialize(*P)
    y0=f.output(x0,0.,*P)
    if hasattr(f,'initialize'):
        P=tempP

    for i in f.constraints.keys():
        if isinstance(f.constraints[i],tuple):
            test_exp,feature=f.constraints[i]
        else:
            feature=f.constraints[i]
            test_exp=lambda t:True
        if feature.type=='time':
            if feature.name in f.xnames:
                ind=f.xnames.index(feature.name)
                cstr[i]=np.where(test_exp(0.),feature.init(x0[ind],0.,h0),
                                 cstr[i])
            else:
                ind=f.ynames.index(feature.name)
                cstr[i]=np.where(test_exp(0.),feature.init(y0[ind],0.,h0),
                                 cstr[i])

    _,xf,tf,yf,hf,cstr,ifinal,_=while_loop(cond_fn,body_fn,
                                         (x0,x0,0.,y0,h0,cstr,i0,c0))
    if hasattr(f,'state'):
        f.state=ifinal
    for i in f.constraints.keys():
        if isinstance(f.constraints[i],tuple):
            _,feature=f.constraints[i]
        else:
            feature=f.constraints[i]
        if feature.type == 'time':
            cstr[i]=feature.fin(tf,cstr[i],T)

    if M!=None:
        _,modX,phX,_,modY,phY,_=odeint45(f,xf,np.linspace(tf,tf+T,M),*P,
                                        M=M,T=T,h0=h0)
        vect_freq=np.where(M//2==0,np.linspace(0.,(M/2-1)/T,M//2),
                              np.linspace(0.,(M-1)/(2*T),M//2))
        for i in f.constraints.keys():
            if isinstance(f.constraints[i], tuple):
                _, feature = f.constraints[i]
            else:
                feature = f.constraints[i]
            if feature.type == 'freq':
                if feature.name in f.xnames:
                    ind = f.xnames.index(feature.name)
                    cstr[i]=feature.expression(modX[ind],phX[ind],vect_freq,1/T)
                else:
                    ind=f.ynames.index(feature.name)
                    cstr[i]=feature.expression(modY[ind],phY[ind],vect_freq,1/T)


    if hasattr(f,'state'):
        return (tf,xf,yf,cstr,ifinal)
    else:
        return (tf,xf,yf,cstr)


@_odeint45_extract.defjvp
def _odeint45_extract_jvp(f,h0,tol,M, primals, tangents):
    '''
    Solves an ODE system described by df/dP with Runge-Kutta 5 (7M) algorithm, and
    computes derivatives of extracted features w.r.t optimization inputs.

    :param f: a class that describes the ODE system
    :param h0: initial step size
    :param tol: tolerance for optimal step size computation
    :param M: number of points to compute the FFT
    :param primals: tuple including initial state vector,operating period and
        optimization inputs.
    :param tangents: tuple including differentials of initial state vector,
        operating period and optimization inputs.
    :return: the final time tf, final state vector xf, final output vector yf,extracted features dictionary cstr, their derivatives w.r.t P, and the final
    configuration state if the system is periodic.
    '''
    x0,T, *P = primals
    dx0,dT, *dP = tangents
    nPdP = len(P)

    res=odeint45_extract_etendu(f,nPdP,h0, tol,M, x0,dx0,T,dT, *P, *dP)

    if hasattr(f,'state'):
        xf,yf,cstr,tf,dtf,dxf,dyf,dcstr,states=res
        return (tf,xf,yf,cstr,states),(dtf,dxf,dyf,dcstr,states)
    else:
        xf,yf,cstr,tf,dtf,dxf,dyf,dcstr=res
        return (tf,xf,yf,cstr),(dtf,dxf,dyf,dcstr)


def odeint45_extract_etendu(f,nPdP,h0,tol,M,x0,dx0,T,dT,*P_and_dP):
    P,dP = P_and_dP[:nPdP],P_and_dP[nPdP:]
    type_,cond_stop=f.stop

    def cond_fn(state):
        x_prev2,x_prev,_,_,_,t_prev, h_prev,cstr,_,_,_,_,_,_ = state
        if type_=='threshold':
            val,seuil=cond_stop(x_prev,f.xnames)
            valp,_ = cond_stop(x_prev2,f.xnames)
            return (h_prev>0) & (np.sign(val-seuil)==np.sign(valp-seuil))
        else:
            return (h_prev > 0) & cond_stop(t_prev,t_prev+h_prev,cstr)


    def body_fn(state):
        _,x_prev,dx_prev,y_prev,dy_prev,t_prev, h_prev,cstr,\
                dcstr,i_prev,c_prev,Mat,dMat,chgt_state= state

        x_now,t_now,y_now,h_now,i_now,c_now=next_step_simulation(x_prev,t_prev,
                                        y_prev,i_prev,c_prev,h_prev,f,tol,T,*P)
        dx_now,dy_now,Mat,dMat=next_der_step_simulation(x_prev,t_prev,dx_prev,
                    x_now,t_now,h_prev,f, nPdP,chgt_state,Mat,dMat,*P_and_dP)
        chgt_state = np.bitwise_not(np.array_equal(i_now, i_prev))

        if type_=='threshold':
            output,seuil=cond_stop(x_now,f.xnames)
            outputprev,_=cond_stop(x_prev,f.xnames)
            condition=np.sign(output-seuil)!=np.sign(outputprev-seuil)
            x_now,h_prev,t_now,y_now=cond(condition,lambda state:
                compute_new_point(x_now,x_prev,t_prev,t_now,y_prev,y_now,
                output-seuil,outputprev-seuil),lambda state:state,(x_now,h_prev,
                                                                t_now,y_now))
            x_now,t_now,y_now,h_now,i_now,c_now=cond(condition,lambda state:
                next_step_simulation(x_prev,t_prev,y_prev,i_prev,c_prev,h_prev,
                f,tol,T,*P),lambda state:state,(x_now,t_now,y_now,h_now,i_now,
                                                c_now))
            dx_now,dy_now,_,_=cond(condition,lambda state:next_der_step_simulation
                (x_prev,t_prev,dx_prev,x_now,t_now,h_prev,f, nPdP,i_now,Mat,
                 dMat,*P_and_dP),lambda state:state,(dx_now,dy_now,Mat,dMat))

        elif isinstance(type_,float):
            h_tf=type_-t_now
            h_now=np.minimum(h_now,h_tf)

        for i in f.constraints.keys():
            if isinstance(f.constraints[i], tuple):
                test_exp,feature= f.constraints[i]
            else:
                feature=f.constraints[i]
                test_exp = lambda t: True
            if feature.type=='time':
                if feature.name in f.xnames:
                    ind=f.xnames.index(feature.name)
                    cstr[i] =np.where(test_exp(t_now),feature.expression(t_prev,
                        x_prev[ind],t_now,x_now[ind], cstr[i],h_prev,T),cstr[i])
                    dcstr[i]= np.where(test_exp(t_now),feature.der_expression(
                        t_prev,x_prev[ind],dx_prev[ind],t_now,x_now[ind],dx_now
                        [ind],cstr[i],dcstr[i],h_prev,T,dT),dcstr[i])
                else:
                    ind=f.ynames.index(feature.name)
                    cstr[i] =np.where(test_exp(t_now),feature.expression(t_prev,
                        y_prev[ind],t_now,y_now[ind],cstr[i],h_prev,T),cstr[i])
                    dcstr[i]= np.where(test_exp(t_now),feature.der_expression(
                        t_prev,y_prev[ind],dy_prev[ind],t_now,y_now[ind],dy_now
                        [ind],cstr[i],dcstr[i],h_prev,T,dT),dcstr[i])

        return x_prev,x_now,dx_now,y_now,dy_now,t_now,h_now,cstr,dcstr,i_now,\
               c_now,Mat,dMat,chgt_state

    cstr=dict(zip(list(f.constraints.keys()),[0.]*len(f.constraints)))#INITIALISATION
    dcstr=dict(zip(list(f.constraints.keys()),[0.]*len(f.constraints)))

    for element in f.__dict__.keys(): # pour eviter erreurs de code
        if hasattr(f.__dict__[element],'primal'):
            f.__dict__[element]=f.__dict__[element].primal
    if hasattr(f,'state'):
        i0=f.state
    else:
        i0=0
    if hasattr(f,'commande'):
        _,c0=f.commande(0.,T)
    else:
        c0=0
    tempP,tempdP,Mat,dMat=None,None,0,0
    if hasattr(f,'initialize'):
        tempP,tempdP=P,dP
        P,dP=jvp(f.initialize,(*P,),(*dP,))
        Mat,dMat=P,dP
    y0=f.output(x0,0.,*P)
    dy0=jvp(f.output,(x0,0.,*P),(dx0,0.,*dP))[1]
    if hasattr(f,'initialize'):
        P,dP=tempP,tempdP

    for i in f.constraints.keys():
        if isinstance(f.constraints[i], tuple):
            test_exp,feature = f.constraints[i]
        else:
            feature = f.constraints[i]
            test_exp = lambda t: True
        if feature.type=='time':
            if feature.name in f.xnames:
                ind=f.xnames.index(feature.name)
                cstr[i]=np.where(test_exp(0.),feature.init(x0[ind],0.,h0),
                             cstr[i])
                dcstr[i]=np.where(test_exp(0.),feature.dinit(x0[ind],dx0[ind],
                                    0.,h0),dcstr[i])
            else:
                ind=f.ynames.index(feature.name)
                cstr[i]=np.where(test_exp(0.),feature.init(y0[ind],0.,h0),
                             cstr[i])
                dcstr[i]=np.where(test_exp(0.),feature.dinit(y0[ind],dy0[ind],
                                    0.,h0),dcstr[i])

    chgt_state=False
    xfm1,xf,dxf,yf,dyf,tf,hf,cstr,dcstr,ifinal,_,_,_,_=while_loop(cond_fn,
        body_fn,(x0,x0,dx0,y0,dy0,0.,h0,cstr,dcstr,i0,c0,Mat,dMat,chgt_state))
    if hasattr(f,'state'):
        f.state=ifinal
    if hasattr(f,'initialize'):
        P=f.initialize(*P)
    for i in f.constraints.keys():
        if isinstance(f.constraints[i],tuple):
            _,feature=f.constraints[i]
        else:
            feature=f.constraints[i]
        if feature.type == 'time':
            if feature.name in f.xnames:
                ind = f.xnames.index(feature.name)
                cstr[i]=feature.fin(tf,cstr[i],T)
                dcstr[i]=feature.der_fin(tf,cstr[i],T,dcstr[i],dT,xf[ind])
            else:
                ind = f.ynames.index(feature.name)
                cstr[i]=feature.fin(tf,cstr[i],T)
                dcstr[i]=feature.der_fin(tf,cstr[i],T,dcstr[i],dT,yf[ind])

    if type_=='threshold': # partial derivatives of ts
        dout,_=cond_stop(dxf,f.xnames)
        xseuil,_=cond_stop(f.timederivatives(xf,tf,*P),f.xnames)
        dtf=-(1/xseuil)*dout
    elif type_=='steady_state':
        ind_rp=0
        xseuil=f.timederivatives(xf,tf,*P)[ind_rp]
        dtf=-(1/xseuil)*dxf[ind_rp]
    else:
        dtf=0.

    if M!=None:
        _,_,modX,phX,dmodX,dphX,_,_,modY,phY,dmodY,dphY,_=odeint45_etendu(f,
            nPdP,h0,tol,M,xf,dxf,np.linspace(tf,tf+T,M),T,*P_and_dP)

        vect_freq=np.where(M//2==0,np.linspace(0.,(M/2-1)/T,M//2),
                              np.linspace(0.,(M-1)/(2*T),M//2))
        for i in f.constraints.keys():
            if isinstance(f.constraints[i], tuple):
                _, feature = f.constraints[i]
            else:
                feature = f.constraints[i]
            if feature.type == 'freq':
                if feature.name in f.xnames:
                    ind = f.xnames.index(feature.name)
                    cstr[i],dcstr[i]=feature.der_expression(modX[ind],
                        phX[ind],dmodX[ind], dphX[ind],vect_freq,1/T)
                else:
                    ind = f.ynames.index(feature.name)
                    cstr[i],dcstr[i]=feature.der_expression(modY[ind],
                        phY[ind],dmodY[ind], dphY[ind],vect_freq,1/T)

    if hasattr(f,'state'):
        return xf,yf,cstr,tf,dtf,dxf,dyf,dcstr,ifinal
    else:
        return xf,yf,cstr,tf,dtf,dxf,dyf,dcstr


from noloadj.numerical_methods.ODE.ode_extracted_features import T_pair,\
    T_impair,min_T,max_T

def steady_state(T,nbT,names_var,a=1e-5):
    constr = {}
    for i in range(len(names_var)):
        constr[names_var[i]+'_min']=(T_pair(nbT * T),
                                     min_T(names_var[i],nbT))
        constr[names_var[i]+'_minimp']=(T_impair(nbT * T),
                                     min_T(names_var[i],nbT))
        constr[names_var[i]+'_max']=(T_pair(nbT * T),
                                     max_T(names_var[i],nbT))
        constr[names_var[i]+'_maximp']=(T_impair(nbT * T),
                                     max_T(names_var[i],nbT))
    def regime_perm(t_prev,t,cstr):
        vectp,vectimp=np.zeros(2*len(names_var)),np.zeros(2*len(names_var))
        for i in range(len(names_var)):
            vectp=vectp.at[i].set(cstr[names_var[i]+'_min'])
            vectp=vectp.at[2*i+1].set(cstr[names_var[i]+'_max'])
            vectimp=vectimp.at[i].set(cstr[names_var[i]+'_minimp'])
            vectimp=vectimp.at[2*i+1].set(cstr[names_var[i]+'_maximp'])
        return np.bitwise_not(np.bitwise_and(np.allclose(vectp,vectimp,atol=a),
                    np.not_equal(t_prev//T,t//T)))
    return ('steady_state',regime_perm),constr

def threshold(ind,threshold_=0.):
    return ('threshold', lambda x,names: (x[names.index(ind)], threshold_))

def final_time(tf):
    return (tf,lambda t_prev,t,cstr:t_prev<tf)

