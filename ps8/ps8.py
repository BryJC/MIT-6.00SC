# 6.00 Problem Set 8
#
# Name:
# Collaborators:
# Time:



import numpy
import random
import pylab
from ps7 import *

#
# PROBLEM 1
#
class ResistantVirus(SimpleVirus):

    """
    Representation of a virus which can have drug resistance.
    """      

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):

        """

        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.        

        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        self.resist = resistances
        self.mutProb = mutProb

        # TODO



    def isResistantTo(self, drug):

        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.    

        drug: The drug (a string)
        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        if drug in self.resist == True:
            return True
        return False
        # TODO


    def reproduce(self, popDensity, activeDrugs):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:       
        
        self.maxBirthProb * (1 - popDensity).                       
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). 

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.        

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90% 
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population        

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings). 
        
        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.         
        """
        if activeDrugs != [] and any([self.isResistantTo(drug) for drug in activeDrugs]) == False:
            raise NoChildException()
        eventBirth = rand.random()
        if eventBirth <= self.maxBirthProb * (1 - popDensity):
            new_resist = {}
            for drug in self.resist:
                mutChance = rand.random()
                if self.resist[drug] == True:
                    if mutChance <= (1-self.mutProb):
                        new_resist[drug] = True 
                    else:
                        new_resist[drug] = False
                elif self.resist[drug] == False:
                    if mutChance <= (1-self.mutProb):
                        new_resist[drug] = False 
                    else:
                        new_resist[drug] = True
            newVirus = ResistantVirus(self.maxBirthProb, self.clearProb, new_resist, self.mutProb)
            return newVirus
        raise NoChildException()
        # TODO

            

class Patient(SimplePatient):

    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).               

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop
        self.prescrip = []
        # TODO
    

    def addPrescription(self, newDrug):

        """
        Administer a drug to this patient. After a prescription is added, the 
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        if newDrug not in self.prescrip:
            self.prescrip.append(newDrug)
        # TODO
        # should not allow one drug being added to the list multiple times


    def getPrescriptions(self):

        """
        Returns the drugs that are being administered to this patient.
        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.prescrip
        # TODO
        

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in 
        drugResist.        

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        totalResistantV = 0
        for virus in self.viruses:
            #if all self.resist == True for all drugs in drugResist:
            resistantV = True
            for drug in drugResist:
                if virus.resist[drug] == True:
                    continue
                else:
                    resistantV = False
                    break
            if resistantV == True:
                totalResistantV += 1
        return totalResistantV
            
        # TODO
                   


    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:
        
        - Determine whether each virus particle survives and update the list of 
          virus particles accordingly          
        - The current population density is calculated. This population density
          value is used until the next call to update().
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient. 
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces. 

        returns: the total virus population at the end of the update (an
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
                    newViruses.append(virus.reproduce(popDensity, self.prescrip))
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

def simulationWithDrug(virus_type='ResistantVirus', maxBirthProb=0.1, \
                          clearProb=0.05, mutProb = 0.005, 
                          patient_type='Patient', num_viruses=100, \
                          maxPop=1000, resistances = {'guttagonol': False}, \
                          prescriptions = ['guttagonol'], \
                          time_steps=300, num_trials = 20):

    """

    Runs simulations and plots graphs for problem 4.
    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.
    total virus population vs. time and guttagonol-resistant virus population
    vs. time are plotted
    """
    trial_results = []
    trial_results_resist = []
    for trial in xrange(1, num_trials+1):
        print "processing trial...{}".format(trial)
        total_virus_pop = []
        total_virus_pop_resist = []
        
        if virus_type == 'ResistantVirus':
            newVirus = ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)
            viruses = [newVirus] * num_viruses
            
        if patient_type == 'Patient':
            newPatient = Patient(viruses, maxPop)
            
        for step in xrange(time_steps+1):
            if step == (150):
                newPatient.addPrescription(prescriptions[0])                   
            total_virus_pop.append(newPatient.update())
            total_virus_pop_resist.append(newPatient.getResistPop([prescriptions[0]]))
            
        for step in xrange(time_steps+1):
            try:
                trial_results[step] += total_virus_pop[step]
                trial_results_resist[step] += total_virus_pop_resist[step]
            except IndexError:
                trial_results.append(total_virus_pop[step])
                trial_results_resist.append(total_virus_pop_resist[step])

    avg_trial_results = []
    avg_trial_results_resist = []
    for cumulative in trial_results:
        avg_trial_results.append(float(cumulative)/num_trials)
    for cumulative in trial_results_resist:
        avg_trial_results_resist.append(float(cumulative)/num_trials)        
        
    #return "Total length of total_virus_pop= {}".format(total_virus_pop)
    plt.plot(xrange(time_steps + 1), avg_trial_results, 'ro')
    plt.plot(xrange(time_steps + 1), avg_trial_results_resist, 'go')
    plt.title("Virus population within a patient over {} time-steps".format(time_steps))
    plt.xlabel('Time-steps')
    plt.ylabel('Total virus population')
    plt.annotate('{} administration\n@ 150 time steps'.format(prescriptions[0]), \
            xy=(149, avg_trial_results[149]), xytext=(185, 300), \
            arrowprops=dict(facecolor='black', shrink=0.05))
    plt.legend(["average total virus population\n over {} trials".format(num_trials), \
                "average total resistant-virus population\n over {} trials".format(num_trials)], loc=0)
    plt.show()
    # TODO



#
# PROBLEM 3
#        

def simulationDelayedTreatment():

    """
    Runs simulations and make histograms for problem 5.
    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.
    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """
    time_delays = [300, 150, 75, 0]
    for delay in time_delays:
        sim = simulationWithDrug(virus_type='ResistantVirus', maxBirthProb=0.1, \
                          clearProb=0.05, mutProb = 0.005, 
                          patient_type='Patient', num_viruses=100, \
                          maxPop=1000, resistances = {'guttagonol': False}, \
                          prescriptions = ['guttagonol'], \
                          time_steps=delay, num_trials = 20)
    # TODO

#
# PROBLEM 4
#

def simulationTwoDrugsDelayedTreatment():

    """
    Runs simulations and make histograms for problem 6.
    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
   
    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """

    # TODO



#
# PROBLEM 5
#    

def simulationTwoDrugsVirusPopulations():

    """

    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.
    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.        

    """
    #TODO



