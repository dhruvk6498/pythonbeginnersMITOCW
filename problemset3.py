"""
    
    Author - Dhruv Kakran
    June 2017
    
    """



from string import *

def countSubStringMatch(target, key):
    count = 0
    while target.find(key) != -1:
        index = target.find(key)
        target = target[index + 1:]
        count += 1
    return count 


def countSubStringMatchRecursive(target, key):
    count = 0
    if target.find(key) != -1:
        index = target.find(key)
        count = 1 + countSubStringMatchRecursive(target[index+1:] , key)
        return count 
    else:
        return 0

def subStringMatchExact(target, key):
    indexes = []
    originalindex = -1
    while target.find(key) != -1:
        index = target.find(key)
        target = target[index + 1:]
        originalindex += index + 1
        indexes.append(originalindex)
    return indexes

def constrainedMatchPair(firstmatch,secondmatch,m):
    result = []
    for n in firstmatch:
        for k in secondmatch:
            if n + m + 1 == k:
                result.append(n)
    return result

def subStringMatchExactlyOneSub(target,key):
    result = []
    exactmatches = subStringMatchExact(target, key)
    key1 = ""
    key2 = ""
    for n in range(0,len(key) - 2):
        key1 += str(key[n])
    key2 = str(key[len(key) -1])
    firstmatch = subStringMatchExact(target, key1)
    secondmatch = subStringMatchExact(target, key2)
    submatches = constrainedMatchPair(firstmatch,secondmatch,len(key1))
    for x in submatches:
        if x not in exactmatches:
            result.append(x)
    return result 
    
                                    


if __name__ == "__main__":
    target = str(input("Enter string : "))
    key = str(input("Enter sub-string to be searched : "))
    print(countSubStringMatch(target, key))
    print(countSubStringMatchRecursive(target, key))
    print(subStringMatchExact(target, key))
    key1 = str(input("Enter first key : "))
    key2 = str(input("Enter second key : "))
    start1 = subStringMatchExact(target, key1)
    start2 = subStringMatchExact(target, key2)
    length = len(key1) 
    print(constrainedMatchPair(start1,start2,length))
    print(subStringMatchExactlyOneSub(target,key))
    
    
