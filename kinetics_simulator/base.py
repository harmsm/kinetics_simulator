__description__ = \
"""
A class for running abitrarily complex first-order chemical kinetics markov
models based on simple, human-readable string-basd input.
"""
__author__ = "Michael J. Harms (harmsm@gmail.com)"
__date__ = "2018-11-07"

from . import util

import numpy as np
import pandas as pd

import os

class ReactionSimulator:
    """
    Class for holding and manipulating a reaction scheme.
    """

    def setup_reaction(self,rxn_string):
        """
        """

        if os.path.isfile(rxn_string):
            rxn_string = open(rxn_string,"r").read()

        # Read from file or string
        max_order, reactions, concentrations = util.parse_reaction(rxn_string)

        # Convert dictionaries into forms useful for reaction simulations
        self._max_order = max_order
        self._reactions = reactions
        self._concentrations = concentrations
        
        # list of species in alphabetical order
        self._species = list(self._concentrations.keys())
        self._species.sort()

        # number of species and number of reactions
        self._num_species = len(self._species)
        self._num_reactions = len(self._reactions.keys()) 

        # reaction rates
        self._rates = []

        # slices for grabbing reactant and product concentrations
        self._reactant_slices = []
        self._product_slices = []

        species_to_index = dict([(s,i) for i, s in enumerate(self._species)])
        for k in self._reactions.keys():

            # rates
            self._rates.append(self._reactions[k])

            # slices for accessing reactants
            reactant_slice = []
            for reactant in k[0]:
                reactant_slice.append(species_to_index[reactant])
            self._reactant_slices.append(np.array(reactant_slice,dtype=np.int))

            # slices for accessing products
            product_slice = []
            for product in k[1]:
                product_slice.append(species_to_index[product])
            self._product_slices.append(np.array(product_slice,dtype=np.int))
  
        # current concentration, time, and conc_history
        self._current_conc = np.array([self._concentrations[s]
                                       for s in self._species]) 
        self._time_steps = [0.0]
        self._conc_history = [np.copy(self._current_conc)]


    @property
    def initial_conc(self):
        """
        Initial concentrations of all species.
        """

        return self._conc_history[0]

    @property
    def current_conc(self):
        """
        Current concentrations of all species.
        """
        
        return self._current_conc

    @property
    def t(self):
        """
        Times.
        """

        return np.array(self._time_steps)

    @property
    def conc_history(self):

        df_dict = {"time":np.array(self._time_steps)}
        c = np.array(self._conc_history)
        for i in range(len(self._species)):
            key = self._species[i]
            df_dict[key] = c[:,i]

        return pd.DataFrame(df_dict)
            
    @property
    def species(self):
        """
        List of species names.
        """

        return self._species

    @property
    def reactions(self):
        """
        Dictionary of reactions, with keys like (reactant,product) and values
        of rates.
        """

        return self._reactions

    @property
    def max_order(self):
        """
        Maximum reaction order in the scheme.
        """
    
        return self._max_order


