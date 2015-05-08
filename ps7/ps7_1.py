# Problem Set 7: Simulating the Spread of Disease and Virus Population Dynamics 
# Name:
# Collaborators:
# Time:

import numpy as np
import random as rand
import matplotlib.pyplot as plt

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 1
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):

        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        # TODO

    def doesClear(self):

        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.clearProb and otherwise returns
        False.
        """
        chanceLive = rand.random()
        if chanceLive < self.clearProb:
            return True
        return False
        # TODO

    
    def reproduce(self, popDensity):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        chanceBirth = rand.random()
        if chanceBirth > self.maxBirthProb * (1 - popDensity):
            new_virus = SimpleVirus(self.maxBirthProb, self.clearProb)
            return new_virus
        raise NoChildException()
        # TODO



class SimplePatient(object):

    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):

        """

        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the  maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop
        # TODO


    def getTotalPop(self):

        """
        Gets the current total virus population. 
        returns: The total virus population (an integer)
        """
        return len(self.viruses)
        # TODO        


    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        mark_to_clear = []
        popDensity = []
        newViruses = []
        for i, virus in enumerate(self.viruses):
            attempt_to_clear = virus.doesClear()
            if attempt_to_clear == True:
                mark_to_clear.append(i)
            elif attempt_to_clear == False:
                popDensity.append(float((self.getTotalPop() - len(mark_to_clear)) / self.maxPop))
        for i, virus in enumerate(self.viruses):
            if i not in mark_to_clear:
                newViruses.append(virus)
                #print "mark_to_clear list: {}".format(mark_to_clear)
                #print "length of viruses= {}".format(len(self.viruses))
                #print "current i number= {}".format(i)
                #break
                
        self.viruses = newViruses[:]
        number_density = 0
        for i, virus in enumerate(self.viruses): 
            if len(self.viruses) < self.maxPop:
                curr_popDensity = popDensity[number_density]
                number_density += 1
                try:
                    self.viruses.append(virus.reproduce(curr_popDensity))
                except NoChildException:
                    continue
        return self.getTotalPop()


#
# PROBLEM 2
#
def simulationWithoutDrug(virus_type='SimpleVirus', maxBirthProb=0.1, \
                          clearProb=0.05, patient_type='SimplePatient', \
                          num_viruses=10, maxPop=100, time_steps=15):

    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).    
    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.    
    """  
    if virus_type == 'SimpleVirus':
        newVirus = SimpleVirus(maxBirthProb, clearProb)
        viruses = [newVirus] * num_viruses
        print "Total length of virus list= {}".format(len(viruses))
    if patient_type == 'SimplePatient':
        newPatient = SimplePatient(viruses, maxPop)
    total_virus_pop = [num_viruses]
    for i in xrange(time_steps):        
        total_virus_pop.append(newPatient.update())
        print "processing...{}".format(i)
    #return "Total length of total_virus_pop= {}".format(total_virus_pop)
    plt.plot(xrange(time_steps + 1), total_virus_pop, 'ro')
    plt.title("Viral population in a patient over time-steps")
    plt.xlabel('Time-steps')
    plt.ylabel('Total viral population')
    plt.show()
    # TODO
