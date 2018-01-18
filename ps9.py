

"""

Author - Dhruv Kakran
June 2017


"""



from string import *
from abc import ABCMeta,abstractmethod

class Shape(object):
    def area(self):
        raise AttributeException("Subclasses should override this method.")
    @abstractmethod
    def __str__(self):
        pass
    @abstractmethod
    def __eq__(self):
        pass

class Square(Shape):
    def __init__(self, s):
        self._side = float(s)
    def area(self):
        return self._side**2
    def __str__(self):
        return "Square with side " + str(self._side)
    def __eq__(self, other):
        return type(other) == Square and self._side == other._side

class Circle(Shape):
    def __init__(self, radius):
        self._radius = float(radius)
    def area(self):
        return 3.14159*(self._radius**2)
    def __str__(self):
        return 'Circle with radius ' + str(self._radius)
    def __eq__(self, other):
        return type(other) == Circle and self._radius == other._radius

class Triangle(Shape):
    def __init__(self, base, height):
        self._base = float(base)
        self._height = float(height)
    def area(self):
        return 0.5 * self._base * self._height
    def __str__(self):
        return 'Triangle with base ' + str(self._base) + ' and height ' + str(self._height)
    def __eq__(self, other):
        return type(other) == Triangle and self._base == other._base and self._height == other._height

class Shapeset:
    def __init__(self):
        self._set = []
    def addShape(self, sh):
        validShape = True
        if self._set != []:
            for s in self._set:
                if s == sh:
                    validShape = False
                    break
        if validShape:
            self._set.append(sh)
    def __iter__(self):
        for s in self._set:
            yield s
    def __str__(self):   #MAY NOT BE IDEAL SOLUTION
        for s in self._set:
            yield s


def findLargest(shapes):
    areas = []
    result = []
    for s in shapes:
        areas.append(s.area())
    maximum = max(areas)
    for s in shapes:
        if maximum == s.area():
            result.append(s)
    return result


def readShapesFromFile(filename):
    inputfile = open(filename)
    shapes = Shapeset()
    info = []
    for line in inputfile:
        info = line.rstrip('\n').split(',')
        if info[0] == 'triangle':
            shape = Triangle(info[1], info[2])
            shapes.addShape(shape)
        elif info[0] == 'square':
            shape = Square(info[1])
            shapes.addShape(shape)
        elif info[0] == "circle":
            shape = Circle(info[1])
            shapes.addShape(shape)
    return shapes


if __name__ == "__main__":
    ss = readShapesFromFile("shapes.txt")
    for shape in ss:
        print(shape)
    largest = findLargest(ss)
    for s in largest:
        print("LARGEST: ", s)
    for shape in ss:
        print("AREA : ", shape.area())
            
        
    
    
        
        
            
