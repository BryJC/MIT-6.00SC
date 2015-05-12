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
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
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
        if drug in self.resist:
            return self.resist[drug]
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
        for drug in activeDrugs:
            if not self.isResistantTo(drug):
                raise NoChildException()
                
        eventBirth = rand.random()
        if eventBirth < self.maxBirthProb * (1 - popDensity):
        
            new_resist = {}
            for drug in self.resist.keys():
                mutChance = rand.random()
                
                if mutChance < self.mutProb:
                    new_resist[drug] = not self.resist[drug] 
                else:
                    new_resist[drug] = self.resist[drug]
                        
            newVirus = ResistantVirus(self.maxBirthProb, self.clearProb, new_resist, self.mutProb)
            return newVirus
            
        else:
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
        SimplePatient.__init__(self, viruses, maxPop)
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
                
          
        popDensity = float(len(savedViruses))/ self.maxPop
        
        newViruses = []              
        for virus in savedViruses: 
            newViruses.append(virus)             
            try:
                newViruses.append(virus.reproduce(popDensity, self.prescrip))
            except NoChildException:
                continue

        self.viruses = newViruses
        return self.getTotalPop()
        # TODO


################################################################################
#
# PROBLEM 2
#
def runDrugSimulation(num_viruses, maxPop, maxBirthProb, clearProb, mutProb, \
                    resistances, prescriptions, time_steps_init, time_steps_plus):
        
        viruses = []
        for i in xrange(num_viruses):
            newVirus = ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)
            viruses.append(newVirus)
            
        newPatient = Patient(viruses, maxPop)
            
        total_virus_pop = []
        total_virus_pop_resist = []
        for step in xrange(time_steps_init + time_steps_plus):
            if step == time_steps_init:
                newPatient.addPrescription(prescriptions[0])                      
            total_virus_pop.append(newPatient.update())
            total_virus_pop_resist.append(newPatient.getResistPop([prescriptions[0]]))     
            
        #print total_virus_pop
        return (total_virus_pop, total_virus_pop_resist)
            
            
def simulationWithDrug(maxBirthProb=0.1, clearProb=0.05, mutProb=0.005, \
                       patient_type='Patient', num_viruses=100, maxPop=1000, resistances={'guttagonol': False}, \
                       prescriptions=['guttagonol'], time_steps_init=150, time_steps_plus=150, num_trials=20, plot='Y'):

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
        print "processing time steps {} trial...{}".format((time_steps_init + time_steps_plus), trial)
                
        (total_vpop, total_resist_vpop) = runDrugSimulation(num_viruses, maxPop, maxBirthProb, clearProb, \
                                                        mutProb, resistances, prescriptions, \
                                                        time_steps_init, time_steps_plus)
            
        for step in xrange(time_steps_init + time_steps_plus):
            if trial_results == []:
                trial_results = total_vpop
                trial_results_resist = total_resist_vpop
                break            
            else:
                trial_results[step] += total_vpop[step]
                trial_results_resist[step] += total_resist_vpop[step]                
                
        #print "Len trial_results: {}".format(len(trial_results))
        #print "Len trial_results_resist: {}".format(len(trial_results_resist))
    
    for i in xrange(len(trial_results)):
        trial_results[i] /= float(num_trials)
    for i in xrange(len(trial_results_resist)):
        trial_results_resist[i] /= float(num_trials)
        
    if plot=='Y':
        pass
    elif plot=='N':
        return (trial_results, trial_results_resist)
        
    #return "Total length of total_virus_pop= {}".format(total_virus_pop)
    plt.plot(xrange(time_steps_init + time_steps_plus + 1), trial_results, 'ro')
    plt.plot(xrange(time_steps_init + time_steps_plus + 1), trial_results_resist, 'go')
    plt.title("Virus population within a patient over {} time-steps".format(time_steps_init + time_steps_plus))
    plt.xlabel('Time-steps')
    plt.ylabel('Total virus population')
    plt.annotate('{} administration\n@ {} time steps'.format(prescriptions[0], time_steps_init), \
            xy=(time_steps_init, trial_results[time_steps_init]), \
            xytext=(time_steps_init + 50, trial_results[time_steps_init]-200), \
            arrowprops=dict(facecolor='black', shrink=0.05))
    plt.legend(["average total virus\npopulation over {} trials".format(num_trials), \
                "average total resistant-virus\npopulation over {} trials".format(num_trials)], loc=1)
    plt.show()
    
    return (trial_results, trial_results_resist) 
    # TODO



#
# PROBLEM 3
#        

def simulationDelayedTreatment(num_viruses=100, maxPop=1000, maxBirthProb=0.1, clearProb=0.05, mutProb=0.005, \
                                resistances={'guttagonol':False}, prescriptions=['guttagonol'], \
                                time_delays=[0, 75, 150, 300], time_plus=150, num_patients=50):
    """
    Runs simulations and make histograms for problem 5.
    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.
    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """    
    sim_collection = {}   
    
    for delay in time_delays:
        print "Starting simulation for delayed treatment of {} days\n".format(delay)
        sim_results = [] 
        for i in xrange(num_patients):
            (all_viruses, resist_viruses) = runDrugSimulation(num_viruses, maxPop, maxBirthProb, clearProb, \
                                                        mutProb, resistances, prescriptions, \
                                                        delay, time_plus)
            sim_results.append(all_viruses[-1])
        sim_collection[delay] = sim_results

    subplot_num = 1
    for n in time_delays:
        plt.subplot(2, 2, subplot_num)
        plt.title('delay = {} time-steps'.format(n))
        plt.hist(sim_collection[n], bins=15, range=(0,600))
        plt.ylabel('# of Patients\n({}) total'.format(num_patients))
        plt.xlabel('Virus population remaining after {} time-steps'.format(int(n) + time_plus))
        subplot_num += 1
    plt.show()
    
    return sim_collection
   
            
        
    # TODO

#
# PROBLEM 4
#
def runTwoDrugSimulation(num_viruses, maxPop, maxBirthProb, clearProb, mutProb, \
                    resistances, prescriptions, time_steps_init, time_steps_plus):
        
        viruses = []
        for i in xrange(num_viruses):
            newVirus = ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)
            viruses.append(newVirus)
            
        newPatient = Patient(viruses, maxPop)
            
        total_virus_pop = []
        total_virus_pop_resist = []
        for step in xrange(2*time_steps_init + time_steps_plus):
            if step == time_steps_init:
                newPatient.addPrescription(prescriptions[0])
            if step == time_steps_plus:
                newPatient.addPrescription(prescriptions[1])                                  
            total_virus_pop.append(newPatient.update())
            total_virus_pop_resist.append(newPatient.getResistPop([prescriptions]))     
            
        #print total_virus_pop
        return (total_virus_pop, total_virus_pop_resist)
        
        
def simulationTwoDrugsDelayedTreatment(num_viruses=100, maxPop=1000, maxBirthProb=0.1, clearProb=0.05, mutProb=0.005, \
                                resistances={'guttagonol':False, 'grimpex':False}, prescriptions=['guttagonol', 'grimpex'], \
                                time_init=150, time_plus=[0, 75, 150, 300], num_patients=50):
    """
    Runs simulations and make histograms for problem 6.
    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
   
    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """
    sim_collection = {}   
    
    for delay in time_plus:
        print "Starting simulation for delayed treatment of {} days\n".format(delay)
        sim_results = [] 
        for i in xrange(num_patients):
            (all_viruses, resist_viruses) = runDrugSimulation(num_viruses, maxPop, maxBirthProb, clearProb, \
                                                        mutProb, resistances, prescriptions, \
                                                        time_init, delay)
            sim_results.append(all_viruses[-1])
        sim_collection[delay] = sim_results

    subplot_num = 1
    for n in time_plus:
        plt.subplot(2, 2, subplot_num)
        plt.title('between drugs - delay = {} time-steps'.format(n))
        plt.hist(sim_collection[n], bins=15, range=(0,600))
        plt.ylabel('# of Patients\n({}) total'.format(num_patients))
        plt.xlabel('Virus population remaining after {} time-steps'.format(int(n) + 2*time_init))
        subplot_num += 1
    plt.show()
    
    return sim_collection
    # TODO



#
# PROBLEM 5
#    
def runTwoDrugSimulation(num_viruses, maxPop, maxBirthProb, clearProb, mutProb, \
                    resistances, prescriptions, time_init, time_plus):
        
    viruses = []
    for i in xrange(num_viruses):
        newVirus = ResistantVirus(maxBirthProb, clearProb, resistances, mutProb)
        viruses.append(newVirus)
        
    newPatient = Patient(viruses, maxPop)
        
    all_viruses = []
    resist_virus1 = []
    resist_virus2 = []
    resistALL = []        

    for step in xrange(4*time_init):
        if step == 150:
            newPatient.addPrescription(prescriptions[0])
        if step == 150 and time_plus == 0:
            newPatient.addPrescription(prescriptions[1])
        if step == 450 and time_plus == 300:
            newPatient.addPrescription(prescriptions[1])                                  
        all_viruses.append(newPatient.update())
        resist_virus1.append(newPatient.getResistPop([prescriptions[0]]))
        resist_virus2.append(newPatient.getResistPop([prescriptions[1]]))
        resistALL.append(newPatient.getResistPop(prescriptions))
        
    #print total_virus_pop
    return (all_viruses, resist_virus1, resist_virus2, resistALL)

def simulationTwoDrugsVirusPopulations(num_viruses=100, maxPop=1000, maxBirthProb=0.1, clearProb=0.05, mutProb=0.005, \
                                resistances={'guttagonol':False, 'grimpex':False}, prescriptions=['guttagonol', 'grimpex'], \
                                time_init=150, time_plus=[0, 300], num_trials=30, plot='Y'):
                                
    """

    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.
    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.        
    """
    
    
    sim_collection = {}   
        
    for delay in time_plus:
    
        trial_results = []
        trial_resist1 = []
        trial_resist2 = []
        trial_resistALL = []        
        print "Starting simulation for delayed treatment of {} days\n".format(delay)
                 
        for trial in xrange(num_trials):
            print "processing delay {} trial...{}".format(delay, trial+1)
            
            (all_viruses, resist_drug1, resist_drug2, resist_all) = \
            runTwoDrugSimulation(num_viruses, maxPop, maxBirthProb, clearProb, \
                              mutProb, resistances, prescriptions, time_init, delay)
        
            for step in xrange(4*time_init):
                if trial_results == []:
                    trial_results = all_viruses
                    trial_resist1 = resist_drug1
                    trial_resist2 = resist_drug2
                    trial_resistALL = resist_all
                    break            
                else:
                    #print all_viruses
                    trial_results[step] += all_viruses[step]
                    trial_resist1[step] += resist_drug1[step]
                    trial_resist2[step] += resist_drug2[step]
                    trial_resistALL[step] += resist_all[step]
                    
        for i in xrange(len(trial_results)):
            trial_results[i] /= float(num_trials)
            trial_resist1[i] /= float(num_trials)
            trial_resist2[i] /= float(num_trials)
            trial_resistALL[i] /= float(num_trials)
                    
        sim_collection[delay] = (trial_results, trial_resist1, trial_resist2, trial_resistALL)        
                
        #print "Len trial_results: {}".format(len(trial_results))
        #print "Len trial_results_resist: {}".format(len(trial_results_resist))
                
    if plot=='Y':
        pass
    elif plot=='N':
        return sim_collection

    s_num = 1
    for delay in time_plus:
        plt.subplot(2, 1, s_num)
        plt.plot(xrange(600), sim_collection[delay][0], 'r-')
        plt.plot(xrange(600), sim_collection[delay][1], 'b-')
        plt.plot(xrange(600), sim_collection[delay][2], 'y-')
        plt.plot(xrange(600), sim_collection[delay][3], 'g-')
        
        plt.title("Virus population within a patient over {} time-steps".format(time_init + delay))
        plt.xlabel('Time-steps')
        plt.ylabel('Total virus population')
        plt.annotate('{} administration\n@ {} time steps'.format(prescriptions[0], time_init), \
                xy=(time_init-1, sim_collection[delay][0][time_init-1]), \
                xytext=(time_init + 50, sim_collection[delay][0][time_init]-200), \
                arrowprops=dict(facecolor='black', shrink=0.05))
        plt.annotate('{} administration\n@ {} time steps'.format(prescriptions[1], time_init+delay), \
                xy=(time_init+delay-1, sim_collection[delay][0][time_init+delay-1]), \
                xytext=(time_init+delay-50, sim_collection[delay][0][time_init+delay]-300), \
                arrowprops=dict(facecolor='black', shrink=0.05))
        plt.legend(["average total virus\npopulation over {} trials".format(num_trials), \
                    "average total {}-resistant virus\npopulation over {} trials".format(prescriptions[0], num_trials), \
                    "average total {}-resistant virus\npopulation over {} trials".format(prescriptions[1], num_trials), \
                    "average total both drugs-resistant virus\npopulation over {} trials".format(num_trials)], loc=1, prop={'size':8})
        s_num += 1
    plt.show()
  
    return sim_collection
    #TODO
