"""
    
    Author - Dhruv Kakran
    June 2017
    
    """


import numpy
from pylab import *
import random


class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """    

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
        self.clearProb = clearProb
        self.maxBirthProb = maxBirthProb
        
    def doesClear(self):
        """
        Stochastically determines whether this virus is cleared from the
        patient's body at a time step. 

        returns: Using a random number generator (random.random()), this method
        returns True with probability self.clearProb and otherwise returns
        False.
        """
        x = random.random()
        if x <= self.clearProb:
            return True
        else:
            return False
    
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
        x = random.random()
        if x <= (self.maxBirthProb * ( 1 - popDensity)):
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            return 0



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
        
        maxPop: the maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.currentpop = len(self.viruses)
        self.maxPop = int(maxPop)

    def getTotalPop(self):
        """
        Gets the current total virus population. 

        returns: The total virus population (an integer)
        """
        return self.currentpop       

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

        returns: the total virus population at the end of the update (an
        integer)
        """
        for virus in self.viruses[:]:
            if virus.doesClear():
                self.viruses.remove(virus)
        self.currentpop = len(self.viruses)
        popdensity = float(self.currentpop / self.maxPop)
        for virus in self.viruses[:]:
            offspring = virus.reproduce(popdensity)
            if offspring != 0:
                self.viruses.append(offspring)
        self.currentpop = len(self.viruses)

#
# PROBLEM 2
#

def problem2():
    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).    

    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.    
    """
    viruses = []
    for i in range(0,100):
        viruses.append(SimpleVirus(0.1, 0.05))
    patient = SimplePatient(viruses, 1000)
    populationlist = []
    time = range(0,300)
    for i in range(0,300):
        patient.update()
        currentpopulation = patient.getTotalPop()
        populationlist.append(int(currentpopulation))
    title("Simulation (300 timesteps) ")
    xlabel("Time")
    ylabel("Virus Population")
    plot(time, populationlist)
    

    
    
#
# PROBLEM 3
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
        super().__init__(maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = float(mutProb)
        
    def getResistance(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.        

        drug: the drug (a string).

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        return self.resistances[str(drug)] 
        
        
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
        willreproduce = False #Checking if virus will reproduce
        if activeDrugs != []:
            for drug in activeDrugs:
                if self.resistances[drug] == True:
                    willreproduce = True
                else:
                    willreproduce = False
                    break
        else:
            willreproduce = True
        if willreproduce: # if it can reproduce
            x = random.random()
            if x <= (self.maxBirthProb * (1 - popDensity)): #the probability that it will have a child
                offspringresistances = {}
                for key in self.resistances.keys():
                    y = random.random()
                    if y <= self.mutProb: # if it mutates
                        offspringresistances[key] = not(self.resistances[key]) #inherit a different trait
                    else:
                        offspringresistances[key] = self.resistances[key] #inherit the same trait 
                return ResistantVirus(self.maxBirthProb, self.clearProb, offspringresistances, self.mutProb)
            else:
                return 0 
        else:
            return 0 
        



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
        super().__init__(viruses, maxPop)
        self.admindrugs = []
        
    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the 
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        if newDrug not in self.admindrugs:
            self.admindrugs.append(str(newDrug))

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.admindrugs 
        
    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in 
        drugResist.        

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        resistantpop = 0 
        for virus in self.viruses:
            isresistant = False
            for drug in drugResist:
                if virus.getResistance(drug) == True:
                    isresistant = True
                else:
                    isresistant = False
                    break
            if isresistant == True:
                resistantpop += 1

        return resistantpop
                    

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
        for virus in self.viruses[:]:
            if virus.doesClear():
                self.viruses.remove(virus)
        self.currentpop = len(self.viruses)
        popdensity = float(self.currentpop / self.maxPop)
        for virus in self.viruses[:]:
            offspring = virus.reproduce(popdensity, self.admindrugs)
            if offspring != 0:
                self.viruses.append(offspring)
        self.currentpop = len(self.viruses)
        

#
# PROBLEM 4
#

def problem4():
    """
    Runs simulations and plots graphs for problem 4.

    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.

    total virus population vs. time  and guttagonol-resistant virus population
    vs. time are plotted
    """
    viruses = []
    for i in range(0,100):
        viruses.append(ResistantVirus(0.1,0.05,{"guttagonol" : False}, 0.005))
    patient = Patient(viruses, 1000)
    viruspops = []
    resistantviruspops = []
    for j in range(0,150):
        patient.update()
        currentviruspop = patient.getTotalPop()
        resistantviruspop = patient.getResistPop(["guttagonol"])
        viruspops.append(int(currentviruspop))
        resistantviruspops.append(int(resistantviruspop))
    patient.addPrescription("guttagonol")
    for z in range(0,150):
        patient.update()
        currentviruspop = patient.getTotalPop()
        resistantviruspop = patient.getResistPop(["guttagonol"])
        viruspops.append(int(currentviruspop))
        resistantviruspops.append(int(resistantviruspop))
    time = range(0,300)
    title("Virus Population vs Time")
    xlabel("Time")
    ylabel("Virus Population")
    plot(time, viruspops)
    plot(time, resistantviruspops)
    
        
#
# PROBLEM 5
#

def problem5helper(delaytime):
    a = 1
    finalpops = []
    while a <= 30:
        viruses = []
        for i in range(0,100):
            viruses.append(ResistantVirus(0.1,0.05,{"guttagonol" : False}, 0.005))
        patient = Patient(viruses, 1000)
        for j in range(0, delaytime):
            patient.update()
        patient.addPrescription("guttagonol")
        for z in range(0,150):
            patient.update()
        finalpops.append(patient.getTotalPop())
        a += 1 
    return finalpops
    
    
    
def problem5():
    """
    Runs simulations and make histograms for problem 5.

    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """
    totalpopulations = []
    totalpopulations.append(problem5helper(0))
    totalpopulations.append(problem5helper(10))
    totalpopulations.append(problem5helper(75))
    totalpopulations.append(problem5helper(150))
    totalpopulations.append(problem5helper(300))
    totalpopulations.append(problem5helper(500))
    title("Total (Average) Virus population vs Delay times (for guttagonal)")
    xlabel("Delays")
    ylabel("Virus Populations")
    ##hist(totalpopulations, bins, histtype = "bar")
    
    
#
# PROBLEM 6
#

def problem6helper(delaytime):
    finalpops = []
    a = 1
    while a <= 30:
        viruses = []
        for i in range(0,100):
            viruses.append(ResistantVirus(0.1,0.05,{"guttagonol" : False, "grimpex" : False}, 0.005))
        patient = Patient(viruses, 1000)
        for j in range(0,150):
            patient.update()
        patient.addPrescription("guttagonol")
        for k in range(0, delaytime):
            patient.update()
        patient.addPrescription("grimpex")
        for l in range(0, 150):
            patient.update()
        finalpops.append(patient.getTotalPop())
        a += 1
    return finalpops
        

def problem6():
    """
    Runs simulations and make histograms for problem 6.

    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
    
    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """
    delays = []
    delays = [0,10,75,150,300,500]
    totalpopulations = []
    totalpopulations.append(problem5helper(0))
    totalpopulations.append(problem5helper(10))
    totalpopulations.append(problem5helper(75))
    totalpopulations.append(problem5helper(150))
    totalpopulations.append(problem5helper(300))
    totalpopulations.append(problem5helper(500))
    print("For guttagonol and grimpex : ", totalpopulations)
    title("Total (Average) Virus population vs Delay times (for guttagonol and grimpex)")
    xlabel("Virus Population")
    ylabel("Delays")
    ##hist(delays, totalpopulations)

#
# PROBLEM 7
#

def problem7a():
    """
    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.

    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.        
    """
    viruses = []
    time = range(0,600)
    for i in range(0,100):
        viruses.append(ResistantVirus(0.1,0.05,{"guttagonol" : False, "grimpex" : False}, 0.005))
    patient = Patient(viruses, 1000)
    guttagonolresistant = []
    grimpexresistant = []
    totalresistant = []
    for j in range(0,150):
        patient.update()
        guttagonolresistant.append(int(patient.getResistPop(["guttagonol"])))
        grimpexresistant.append(int(patient.getResistPop(["grimpex"])))
        totalresistant.append(int(patient.getResistPop(["guttagonol" , "grimpex"])))
    patient.addPrescription("guttagonol") #add guttagonol 
    for k in range(0,300):
        patient.update()
        guttagonolresistant.append(int(patient.getResistPop(["guttagonol"])))
        grimpexresistant.append(int(patient.getResistPop(["grimpex"])))
        totalresistant.append(int(patient.getResistPop(["guttagonol" , "grimpex"])))
    patient.addPrescription("grimpex") # add grimpex
    for l in range(0,150):
        patient.update()
        guttagonolresistant.append(int(patient.getResistPop(["guttagonol"])))
        grimpexresistant.append(int(patient.getResistPop(["grimpex"])))
        totalresistant.append(int(patient.getResistPop(["guttagonol" , "grimpex"])))
    xlabel("Time")
    ylabel("Population of resistant viruses")
    plot(time, guttagonolresistant, label = "Guttagonol resistant viruses")
    plot(time, grimpexresistant, label = "Grimpex resistant viruses")
    plot(time, totalresistant, label = "Viruses resistant to both")
        
        
def problem7b():
    viruses = []
    time = range(0,300)
    for i in range(0,100):
        viruses.append(ResistantVirus(0.1,0.05,{"guttagonol" : False, "grimpex" : False}, 0.005))
    patient = Patient(viruses, 1000)
    guttagonolresistant = []
    grimpexresistant = []
    totalresistant = []
    for j in range(0,150):
        patient.update()
        guttagonolresistant.append(int(patient.getResistPop(["guttagonol"])))
        grimpexresistant.append(int(patient.getResistPop(["grimpex"])))
        totalresistant.append(int(patient.getResistPop(["guttagonol" , "grimpex"])))
    patient.addPrescription("guttagonol") # add guttagonol and grimpex
    patient.addPrescription("grimpex")
    for k in range(0,150):
        patient.update()
        guttagonolresistant.append(int(patient.getResistPop(["guttagonol"])))
        grimpexresistant.append(int(patient.getResistPop(["grimpex"])))
        totalresistant.append(int(patient.getResistPop(["guttagonol" , "grimpex"])))
    xlabel("Time")
    ylabel("Population of resistant viruses")
    plot(time, guttagonolresistant, label = "Guttagonol resistant viruses")
    plot(time, grimpexresistant, label = "Grimpex resistant viruses")
    plot(time, totalresistant, label = "Viruses resistant to both")
    
    
if __name__ == "__main__":
    ##problem4()
    problem6()
    ##problem7a()
    ##problem7b()
    legend()
    show()
