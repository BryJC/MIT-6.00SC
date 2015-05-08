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
        eventClear = rand.random()
        if eventClear < self.clearProb:
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
        eventBirth = rand.random()
        if eventBirth < self.maxBirthProb * (1 - popDensity):
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
        savedViruses = []
        for virus in self.viruses:
            if not virus.doesClear():
                savedViruses.append(virus)
                
        newViruses = []  
        popDensity = float(len(savedViruses))/ self.maxPop      
        for virus in savedViruses: 
            newViruses.append(virus)
            if len(newViruses) < self.maxPop:               
                try:
                    newViruses.append(virus.reproduce(popDensity))
                except NoChildException:
                    continue
            else:
                break
        self.viruses = newViruses
        return self.getTotalPop()
            
        # TODO



#
# PROBLEM 2
#
def simulationWithoutDrug(virus_type='SimpleVirus', maxBirthProb=0.1, \
                          clearProb=0.05, patient_type='SimplePatient', \
                          num_viruses=100, maxPop=1000, time_steps=300, \
                          num_trials = 20):

    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).    
    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.    
    """  
    trial_results = []
    for trial in xrange(1, num_trials+1):
        print "processing trial...{}".format(trial)
        total_virus_pop = [num_viruses]
        if virus_type == 'SimpleVirus':
            newVirus = SimpleVirus(maxBirthProb, clearProb)
            viruses = [newVirus] * num_viruses
            #print "Total length of virus list= {}".format(len(viruses))
        if patient_type == 'SimplePatient':
            newPatient = SimplePatient(viruses, maxPop)
        for step in xrange(time_steps):        
            total_virus_pop.append(newPatient.update())
        for step in xrange(len(total_virus_pop)):
            try:
                trial_results[step] += total_virus_pop[step]
            except IndexError:
                trial_results.append(total_virus_pop[step])
                
    avg_trial_results = []
    for cumulative in trial_results:
        avg_trial_results.append(float(cumulative)/num_trials)        
        
    #return "Total length of total_virus_pop= {}".format(total_virus_pop)
    plt.plot(xrange(time_steps + 1), avg_trial_results, 'ro')
    plt.title("Viral population within patient over {} time-steps".format(time_steps))
    plt.xlabel('Time-steps')
    plt.ylabel('Total viral population')
    plt.legend(["average virus population over {} trials".format(num_trials)], loc=4)
    plt.show()
    # TODO
