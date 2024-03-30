# SPDX-FileCopyrightText: 2021 G2Elab / MAGE
#
# SPDX-License-Identifier: Apache-2.0

import numpy as np, sys
from noloadj.optimization.Tools import *

'''Define optimization specifications including objectives and constraints'''
class Spec:
    """
    Attributes :

    - variables : dict for optimization inputs names and initial values.
    - bounds : dict for names and range of values of optimization variables
    - objectives : dict for names and 'estimated' range of values for objective functions
    - eq_cstr : dict for equality constraints names and references (fixed values)
    - ineq_cstr : dict for inequality constraints names and references ([min,max] where None is used for an infinite bound).
    - freeOutputs : list for outputs names that are not constrained
    - debug : bool (by default False) if you want to display optimization variables values in real-time.

    """
    # dict_bounds = {} # dictionnaire des bornes de recherche
    # dict_eq_cstr = {} # dictionnaire des contraintes d'egalite
    # dict_ineq_cstr = {} # dictionnaire des contraintes d'inegalite
    # iNames      = []  #noms des variables d'optimisation
    # bounds      = []  #domaine de recherche
    # xinit       = []  #valeurs initiales du vecteur d'optimisation
    # xinit_sh    = [] # shape des valeurs d'optimization
    # objectives  = []  #noms des objectifs
    # objectives_val = [] # bornes des objectifs
    # eq_cstr     = []  #noms des contraintes d'équalité
    # eq_cstr_val : StructList = None  #valeurs des contraintes d'égalité
    # ineq_cstr   = []  #noms des contraintes d'inégalité
    # ineq_cstr_bnd : StructList = None  # domaine des contraintes d'inégalité
    # freeOutputs = []  # list of outputs to monitor
    # nb          = 0 # nombre de noms variables de sorties (fonctions objectives
    # # + contraintes)
    # oNames       = [] # nom des variables de sorties
    # oShape      = [] # dimension de chaque sortie (objectives + contraintes)
    # nb_entrees  = 0  # nombre de variables d'entrées
    # nb_sorties  = 0  # nombre de variables de sorties (fonctions objectives +
    # # contraintes)
    # debug = False


    def __init__(self, variables:dict, bounds:dict, objectives:dict,
            eq_cstr:dict={}, ineq_cstr:dict={},freeOutputs:list=[],debug=False):
        self.dict_bounds=bounds
        self.dict_eq_cstr=eq_cstr
        self.dict_ineq_cstr=ineq_cstr
        if isinstance(variables,dict):
            self.iNames=list(variables.keys())
            xinit=list(variables.values())
        else:
            self.iNames=list(variables)
            xinit=[]
        x0 = StructList(xinit)
        if isinstance(variables,dict):
            self.xinit_sh = x0.shape
        else:
            self.xinit_sh=[0]*len(self.iNames)
        bounds=list(bounds.values())
        if self.xinit_sh != [0] * len(x0.List) or bounds!=[]:
            bnds = bounds
            bounds = []
            for i in range(len(bnds)):
                if isinstance(bnds[i][0], list):
                    for j in range(len(bnds[i])):
                        bounds.append(bnds[i][j])
                else:
                    bounds.append(bnds[i])
            x0 = StructList(xinit)
            xinit = x0.flatten()
        if not isinstance(bounds, np.ndarray):
            bounds = np.array(bounds)
        self.bounds = bounds
        for i in range(len(self.bounds)): # pour eviter bornes
            self.bounds[i][0]+=1e-16 # mathematiquement impossible
            self.bounds[i][1]-=1e-16
        if not isinstance(xinit, np.ndarray):
            xinit = np.array(xinit)
        self.xinit = xinit
        if isinstance(objectives,dict):
            self.objectives = list(objectives.keys())
            self.objectives_val=list(objectives.values())
            if len(self.objectives)==1:
                self.objectives_val=self.objectives_val[0]
        elif isinstance(objectives,list):
            print('Warning : Objectives must be described as this : '
                  '{',objectives[0],':[value_min,value_max]}.')
            sys.exit(0)
        self.eq_cstr = list(eq_cstr.keys())
        self.eq_cstr_val = StructList(list(eq_cstr.values()))
        self.ineq_cstr = list(ineq_cstr.keys())
        self.ineq_cstr_bnd = StructList(list(ineq_cstr.values()))
        self.freeOutputs = freeOutputs
        self.computeAttributes()
        for i in range(len(self.ineq_cstr_bnd.shape)): # si les contraintes
            # d'inégalité sont scalaires
            if self.ineq_cstr_bnd.shape[i]==2 and \
                    not isinstance(self.ineq_cstr_bnd.List[i][0],list):
                self.ineq_cstr_bnd.shape[i]=self.ineq_cstr_bnd.shape[i]-2
        self.oShape=[0]+self.eq_cstr_val.shape+self.ineq_cstr_bnd.shape
        self.nb_sorties=0
        for size in self.oShape:
            if size==0:
                self.nb_sorties+=1
            else:
                self.nb_sorties+=size
        self.nb_entrees=len(xinit)
        self.debug=debug

    def computeAttributes(self):
        """
        Concatenates the output names of the model in the list oNames.
        Computes the length of oNames in the integer nb.

        :return: /
        """
        self.oNames = self.objectives+self.eq_cstr+self.ineq_cstr
        self.nb = len(self.oNames)

    def removeObjective(self, fobj):
        """
        Removes a function from the objectives of the model.
        Calls the computeAttributes function.

        :param fobj: str: the objective function to remove
        :return: /
        """
        index=self.objectives.index(fobj)
        self.objectives.remove(fobj)
        self.objectives_val.pop(index)
        self.objectives_val=self.objectives_val[0]
        self.oShape = [0] + self.eq_cstr_val.shape + self.ineq_cstr_bnd.shape
        # on redimensionne
        self.computeAttributes()

    def insertObjective(self, position, fobj,fobj_val):
        """
        Adds a function to the objectives of the model.
        Calls the computeAttributes function.

        :param position: int : 0 for the 1st objective function, 1 for the 2nd one.
        :param fobj: str :the objective function to add
        :param fobj_val: list :the estimated bounds of objective function to add
        :return: /
        """
        self.objectives.insert(position, fobj)
        self.objectives_val=[self.objectives_val]
        self.objectives_val.insert(position,fobj_val)
        self.oShape = [0,0] + self.eq_cstr_val.shape + self.ineq_cstr_bnd.shape
        self.computeAttributes()

    def appendConstraint(self, cstr, value):
        """
        Adds an equality constraint.
        Calls the computeAttributes function.

        :param cstr: str : equality constraint to add
        :param value: float :the reference of the equality constraint
        :return: /
        """
        self.eq_cstr.append(cstr)
        self.eq_cstr_val.List.append(value)
        self.oShape.append(0)
        self.computeAttributes()

    def removeLastEqConstraint(self):
        """
        Removes the last equality constraint from the model.
        Calls the computeAttributes function.

        :return: /
        """
        self.eq_cstr.pop()
        self.eq_cstr_val.List.pop()
        self.oShape.pop(0)
        self.computeAttributes()


