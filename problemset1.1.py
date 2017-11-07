"""
    
Author - Dhruv Kakran
June 2017

"""


from math import *

primecount = 1
n = 2
while (primecount < 1000):
    check = None
    for i in range(2, int(sqrt(n))):
        if n % i == 0:
            check = False
            break
        elif n % i != 0:
            check = True
            continue
    if check == True:
        primenum = n 
        primecount += 1
    n += 1

    
print("1000th prime number is : ", primenum)
