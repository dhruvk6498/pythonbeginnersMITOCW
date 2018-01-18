"""
    
Author - Dhruv Kakran
June 2017


"""

from math import *

primesum = 0
n = int(input("Enter number: "))

for i in range(2,n):
    check = None
    for x in range(2,i):
        if i % x == 0:
            check = False
            break
        elif i % x != 0:
            check = True
            continue
    if check == True:
        primesum += log(i)


print(n)
print("The sum of logs of all primes is: ", primesum)
print("The ratio is: ", primesum/n )

            
            
