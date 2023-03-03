__description__ = \
"""
Utility functions for these reaction simulators.
"""
__author__ = "Michael J. Harms"
__date__ = "2019-11-19"


import os
import re

def parse_reaction(some_string):
    """
    Load a reaction in from a string.  There are two types of lines.  
    
    Concentration lines indicate the initial concentration of a species:

    species_name = concentration_as_float

    These must have a string species_name, an "=" sign, and a concentration
    as a float.

    Reaction lines indicate a reaction:

    species_1 + species_2 ... -> species_3 + species_4 + ... ; rate_as_float  

    These must have reactants (separated by "+"), the string "->", the
    products (separated by "+"), a semicolon ";", and the rate as a float.  

    An example reaction is below:

    A = 10
    B = 0
    C = 0
    A -> B; 5
    B -> A + C; 100

    The first three lines are initial concentrations of A, B and C. The
    next two lines are the reaction of A to B with rate 5 and the reaction
    from B to A and C with rate 100.  To make a step reversible, add
    something like "B -> A; 1" to give a back reaction with rate 1.  You
    can specify as many reactions as you want, with as many species as you
    want.  You must specify an initial concentration for any species
    that is involved in any reaction.

    Lines starting with "#" are ignored as comments.

    Returns: 
    max_order: the maximum reaction order seen
    reactions: dictionary keying (reactant_tuple,product_tuple) to rate
    concentrations: dictionary keying species to concentration 
    """
    
    # Use these patterns to look for reaction and conc lines
    rxn_pattern = re.compile("->")
    conc_pattern = re.compile("=")

    # Split on newlines
    lines = some_string.split(os.linesep)

    # Data structures to populate
    reactions = {}
    concentrations = {}
    
    species_seen = []

    # Go through every line
    for raw_line in lines:

        # Strip trailing/leading blank spaces; remove anything after first "#" character
        line = raw_line.strip().split("#")[0].strip()
        
        # skip blank lines (will catch comments from above split call)
        if line == "":
            continue

        # reaction line
        if rxn_pattern.search(line):

            # Split on ->; should yield exactly two fields
            rxn = line.split("->")
            if len(rxn) != 2:
                err = "mangled reaction line\n ({})\n".format(line)
                raise ValueError(err)

            # Grab reactants
            reactants = [c.strip() for c in rxn[0].split("+")]
            reactants.sort()
            reactants = tuple(reactants)

            # Split second field on ";": should have exactly two outputs
            products_and_rate = rxn[1].split(";")
            if len(products_and_rate) != 2:
                err = "mangled reaction line\n ({})\n".format(line)
                raise ValueError(err)

            # Product is first output
            products = [c.strip() for c in products_and_rate[0].split("+")]
            products.sort()
            products = tuple(products)

            # Rate is second output
            try:
                rate = float(products_and_rate[1])
            except ValueError:
                err = "mangled reaction line (rate not a float)\n ({})\n".format(line)
                raise ValueError(err)

            # Reaction key defines what reaction is specified
            reaction_key = (reactants,products)
            try:

                # Make sure this reaction has not been seen before
                reactions[reaction_key]
                err = "reaction defined more than once ({})\n".format(reaction_key)
                raise ValueError(err)

            # Record reaction, rate, and what species have been seen
            except KeyError:
                reactions[reaction_key] = rate

            # Record species seen
            species_seen.extend(reactants)
            species_seen.extend(products)

        # Conc line
        elif conc_pattern.search(line):

            # split on "=".  Must have two fields
            conc_line = line.split("=")
            if len(conc_line) != 2:
                err = "mangled concentration line\n ({})\n".format(line)
                raise ValueError(err)

            # First field is species name.  Check to see if it has been seen before.
            species = conc_line[0].strip()
          
            # See if we have seen a concentration for this species.  If so, throw
            # an error. 
            try: 
                concentrations[species]
                err = "duplicate species concentration ({})\n".format(species)
                raise ValueError(err)
            except KeyError:
                pass
                
            # Second field is concentration. Must be float.
            try:
                conc = float(conc_line[1])
            except ValueError:
                err = "mangled concentration line\n ({})\n".format(line)
                raise ValueError(err)

            # Record the concentration of the species
            concentrations[species] = conc
    
        else:
            err = "line not recognizable.\n ({})\n".format(line)
            raise ValueError(err)
  
    # Unique set of species observed in reactions
    species_seen = set(species_seen)

    # Make sure that there is a concentration specified for every species in
    # a reaction.
    if not species_seen.issubset(set(concentrations.keys())):
        err = "not all species have initial concentrations\n"
        raise ValueError(err)

    max_order = 0
    for r in reactions.keys():
        if len(r[0]) > max_order:
            max_order = len(r[0])
        if len(r[1]) > max_order:
            max_order = len(r[1])

    return max_order, reactions, concentrations



def test():
    
    rxn = \
    """
    A -> B; 10
    B + C -> A; 1
    A = 5
    B = 0
    C = 0
    """

    print(rxn)
    print("gives\n")
    print(parse_reaction(rxn))    

