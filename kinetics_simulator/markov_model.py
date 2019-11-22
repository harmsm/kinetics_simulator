__description__ = \
"""
A class for running abitrarily complex first-order chemical kinetics markov
models based on simple, human-readable string-basd input.
"""
__author__ = "Michael J. Harms (harmsm@gmail.com)"
__date__ = "2018-11-07"

import re, copy
import numpy as np

from .base import ReactionSimulator

class MarkovModel(ReactionSimulator):
    """
    Class for holding and manipulating a reaction scheme.
    """

    def __init__(self,rxn_input,min_self_prob=0.90):
        """
        Initialize reaction.  
            rxn_input: string holding reaction description or file with description
            min_self_prob: minimum self probability
        """

        self._rxn_input = rxn_input
        self._min_self_prob = min_self_prob
        if self._min_self_prob <= 0 or self._min_self_prob >= 1:
            err = "min_self_prob must be between 0 and 1 (not-inclusive)\n"
            raise ValueError(err)

        self.setup_reaction(self._rxn_input)
        if self.max_order > 1:
            err = "Markov matrices can only be used for first-order reactions\n"
            raise ValueError(err)

        self._construct_matrix()


    @property
    def dt(self):
        """
        Time step.
        """

        return self._dt

    @property
    def T(self):
        """
        Transition matrix.
        """

        return self._T

    def take_step(self,num_steps=1):

        if num_steps > 1:
            T = np.linalg.matrix_power(self.T,num_steps)
        else:
            T = self.T

        self._current_conc = np.dot(T,self._current_conc)
        self._time_steps.append(self._time_steps[-1] + num_steps*self.dt)
        self._conc_history.append(self._current_conc)


    def _construct_matrix(self):
        """
        Construct a transition matrix given the set of reactions.
        """

        # construct the rate matrix
        self._rate_matrix = np.zeros((self._num_species,self._num_species),dtype=float)

        # Go through every reactant/product pair
        for i, reactant in enumerate(self._species):
            for j, product in enumerate(self._species):

                # skip self reaction
                if reactant == product:
                    continue

                # Look for reaction between these species. If specified, add a rate.
                try:
                    rate = self._reactions[((reactant,),(product,))]
                    self._rate_matrix[j,i] = rate
                except KeyError:
                    pass

        # Figure out dt.  This is tuned so that the species with the highest
        # total out rate has a self probability of self._min_self_prob.
        highest_total_out_rate = np.max(np.sum(self._rate_matrix,0))
        self._dt = (1 - self._min_self_prob)/highest_total_out_rate

        # construct transition matrix, adding self-probabilities
        self._T = np.copy(self._rate_matrix)*self._dt
        p_self = (1 - np.sum(self._T,0))*np.eye(self._num_species)
        self._T = self._T + p_self

