"""
    Author - Dhruv Kakran
    June 2017
    
    """




def nestEggFixed(salary, save, growthrate, years):
    initial = salary * save * 0.01
    listoffunds = []
    listoffunds.append(initial)
    current = initial
    i = 2
    while ( i <= years):
        funds = current * ( 1 + (0.01 * growthrate) ) + initial
        listoffunds.append(funds)
        current = funds
        i += 1
    return listoffunds

def nestEggVariable(salary, save, growthrates):
    initial = salary * save * 0.01
    listoffunds = []
    listoffunds.append(initial)
    current = initial
    i = 2
    while ( i <= len(growthrates)):
        funds = current * ( 1 + (0.01 * growthrates[i - 1]) ) + initial
        listoffunds.append(funds)
        current = funds
        i += 1
    return listoffunds

def postretirement(savings, growthrates, expenses):
    retirementfunds = []
    i = 1
    while ( i <= len(growthrates)):
        funds = savings * ( 1 + (0.01 * growthrates[i - 1])) - expenses
        retirementfunds.append(funds)
        savings = funds
        i += 1
    return retirementfunds

def findMaxExpenses(salary, save, preRetiregrowthrates, postRetiregrowthrates, epsilon):
    preRetirefunds = nestEggVariable(salary, save, preRetiregrowthrates)
    savings = preRetirefunds[len(preRetirefunds) - 1]
    postRetirefunds = postretirement(savings, postRetiregrowthrates, 0)
    i = 1
    while (postRetirefunds[len(postRetirefunds) - 1] >= epsilon) and float(i) < savings:
        postRetirefunds = postretirement(savings, postRetiregrowthrates, i)
        i += epsilon 
    return i 
        
        
    
if __name__ == "__main__":
    """salary = int(input("Enter your salary : "))
    save = int(input("Enter savings : "))
    growthrate = int(input("Enter growthrate : "))
    years = int(input("Enter years : "))
    print(nestEggFixed(salary, save, growthrate, years))
    salary1 = int(input("Enter your salary : "))
    save1 = int(input("Enter savings : "))
    rates = [int(x) for x in input("Enter growth rates : ").split()]
    print(nestEggVariable(salary1, save1, rates))
    save2 = int(input("Enter savings : "))
    rates1 = rates = [int(i) for i in input("Enter growth rates : ").split()]
    expenses = int(input("Enter expenses : "))
    print(postretirement(save2, rates1, expenses))"""
    salary2 = int(input("Enter your salary : "))
    save3 = int(input("Enter savings : "))
    prerates = [int(x) for x in input("Enter pre-retirement growth rates : ").split(",")]
    postrates = [int(x) for x in input("Enter post-retirement growth rates : ").split(",")]
    epsilon = float(input("Epsilon : "))
    print(findMaxExpenses(salary2, save3, prerates, postrates, epsilon))
    
          
    
    

        
