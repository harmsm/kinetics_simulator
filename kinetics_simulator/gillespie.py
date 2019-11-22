__description__ = \
"""
Python implementation of the Gillespie algorithm for simulation of small
chemical system with discrete chemical components.
            Gillespie DT (1977). J Phys Chem 81(25):2340-2361
"""

__author__ = "Michael J. Harms"
__date__ = "070508"

from .base import ReactionSimulator

import numpy as np

class Gillespie(ReactionSimulator):
    """
    """

    def __init__(self,rxn_input):

        self._rxn_input = rxn_input
        self.setup_reaction(self._rxn_input)
        self._terminated = False

    def take_step(self,num_steps=1):
        
        for i in range(num_steps):
            self._take_step()

    def _take_step(self):
        """
        Perform Monte Carlo move.
        """

        if self._terminated:
            return

        rxn_prob = np.zeros(self._num_reactions,dtype=np.float)
        for i in range(self._num_reactions):
            rxn_prob[i] = np.prod(self._current_conc[self._reactant_slices[i]])*self._rates[i]

        total_rxn_prob = np.sum(rxn_prob)
        if total_rxn_prob == 0:
            self._terminated = True
            print("no reactants left")
            return

        rxn_prob = rxn_prob/total_rxn_prob

        # time step
        tau = np.log(1/np.random.random())/total_rxn_prob
                
        # Figure out reaction that occurs on this time step
        rxn = np.random.choice(range(self._num_reactions),p=rxn_prob)

        # update concentrations
        self._current_conc[self._reactant_slices[rxn]] -= 1
        self._current_conc[self._product_slices[rxn]] += 1
        
        self._time_steps.append(self._time_steps[-1]+tau)
        self._conc_history.append(np.copy(self._current_conc))

    @property
    def terminated(self):
        return self._terminated
