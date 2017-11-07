"""
    
    Author - Dhruv Kakran
    June 2017
    
    """
    




import math
import random
#import ps11_visualize#
##from pylab import *

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).

        x: a real number indicating the x-coordinate
        y: a real nufzmber indicating the y-coordinate
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: integer representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)


# === Problems 1 and 2

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.
        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width 
        self.height = height
        self.tiledict = {}
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.
        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        x = pos.getX()
        y = pos.getY()
        self.tiledict[(math.floor(x), math.floor(y))] = "Cleaned"
        
    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        if (m,n) in self.tiledict.keys():
            if self.tiledict[(m,n)] == "Cleaned":
                return True
        else:
            return False 
        
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height 
    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        numtiles = 0
        for x in self.tiledict.values():
            if x == "Cleaned":
                numtiles += 1
        return numtiles 
        
    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        return Position(random.choice(range(self.width)),random.choice(range(self.height)))
    def isPositionInRoom(self, pos):
        
        """
        Return True if POS is inside the room.

        pos: a Position object.
        returns: True if POS is in the room, False otherwise.
        """
        if 0 <= pos.getX() < self.width and 0 <= pos.getY() < self.height:
            return True
        else:
            return False 
           

class BaseRobot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in
    the room.  The robot also has a fixed speed.

    Subclasses of BaseRobot should provide movement strategies by
    implementing updatePositionAndClean(), which simulates a single
    time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified
        room. The robot initially has a random direction d and a
        random position p in the room.

        The direction d is an integer satisfying 0 <= d < 360; it
        specifies an angle in degrees.

        p is a Position object giving the robot's position.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.speed = float(speed)
        self.room = room 
        self.robotpos = room.getRandomPosition()
        self.room.cleanTileAtPosition(self.robotpos)
        self.direction = random.randint(0, 360)

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.robotpos 
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction 
        
    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.robotpos = position 
    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction 


class Robot(BaseRobot):
    """
    A Robot is a BaseRobot with the standard movement strategy.

    At each time-step, a Robot attempts to move in its current
    direction; when it hits a wall, it chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        #move to newposition
        if self.room.isPositionInRoom(self.getRobotPosition().getNewPosition(self.getRobotDirection() , self.speed)):
            self.setRobotPosition(self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.speed))
            self.room.cleanTileAtPosition(self.getRobotPosition())
        else:
            self.setRobotDirection(random.randint(0,360))
            


# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type, visualize):
    """
    Runs NUM_TRIALS trials of the simulation and returns a list of
    lists, one per trial. The list for a trial has an element for each
    timestep of that trial, the value of which is the percentage of
    the room that is clean after that timestep. Each trial stops when
    MIN_COVERAGE of the room is clean.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE,
    each with speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    Visualization is turned on when boolean VISUALIZE is set to True.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    visualize: a boolean (True to turn on visualization)
    """
    #anim = ps11_visualize.RobotVisualization(num_robots, width, height, delay)
    triallist =[]
    total = 0
    trialcounter = num_trials 
    while trialcounter > 0:
        room = RectangularRoom(width, height)
        robots = []
        for i in range(0, num_robots):
            robots.append(robot_type(room, speed))
        coverage = 0
        trial = []
        while coverage < min_coverage:
            for x in robots:
                ##pos = x.getRobotPosition()
                ##xcord = pos.getX()
                ##ycord = pos.getY()
                ##a,b = xcord, ycord
                ##print(a,b)
                x.updatePositionAndClean()
            totaltiles = room.getNumTiles()
            cleantiles = room.getNumCleanedTiles()
            coverage = round(float(cleantiles / totaltiles), 2)
            trial.append(coverage)
            #anim.update(room,robots)
        total += len(trial)
        triallist.append(trial)
        trialcounter -= 1
    print("The average time is : ", total / num_trials, " clock ticks")
    return total / num_trials 
    #anim.done()
    
        
        

# === Provided function
def computeMeans(list_of_lists):
    """
    Returns a list as long as the longest list in LIST_OF_LISTS, where
    the value at index i is the average of the values at index i in
    all of LIST_OF_LISTS' lists.

    Lists shorter than the longest list are padded with their final
    value to be the same length.
    """
    # Find length of longest list
    longest = 0
    for lst in list_of_lists:
        if len(lst) > longest:
           longest = len(lst)
    # Get totals
    tots = [0]*(longest)
    for lst in list_of_lists:
        for i in range(longest):
            if i < len(lst):
                tots[i] += lst[i]
            else:
                tots[i] += lst[-1]
    # Convert tots to an array to make averaging across each index easier
    tots = pylab.array(tots)
    # Compute means
    means = tots/float(len(list_of_lists))
    return means


# === Problem 4
def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on room size.
    """
    title("Clean time vs Size")
    xlabel("Area of Room")
    ylabel("Average time")
    means = []
    for i in range(1,6):
        means.append(runSimulation(1, 1.0, i*5, i*5, 0.75, 30, Robot, False))
    plot([25, 100, 225, 400, 625] , means)
    

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    title("Clean time for 25x25 vs Number of Robots")
    xlabel("Number of Robots")
    ylabel("Average time")
    means = []
    for i in range(1, 11):
        means.append(runSimulation(i, 1.0, 25, 25, 0.75, 30, Robot, False))
    num_robots = []
    for i in range(1,11):
        num_robots.append(i)
    plot(num_robots, means)
        
    
def showPlot3():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    title("Clean time vs Shape")
    xlabel("Ratio of width to height")
    ylabel("Average time")
    means = []
    means.append(runSimulation(2, 1.0, 20, 20, 0.75, 30, Robot, False))
    means.append(runSimulation(2, 1.0, 25, 16, 0.75, 30, Robot, False))
    means.append(runSimulation(2, 1.0, 40, 10, 0.75, 30, Robot, False))
    means.append(runSimulation(2, 1.0, 50, 8, 0.75, 30, Robot, False))
    means.append(runSimulation(2, 1.0, 80, 5, 0.75, 30, Robot, False))
    means.append(runSimulation(2, 1.0, 100, 4, 0.75, 30, Robot, False))
    ratios = []
    ratios.append(20 / 20)
    ratios.append(25 / 16)
    ratios.append(40 / 10)
    ratios.append(50 / 8)
    ratios.append(80 / 5)
    ratios.append(100 / 4)
    plot(ratios, means)
    

def showPlot4():
    """
    Produces a plot showing cleaning time vs. percentage cleaned, for
    each of 1-5 robots.
    """
    title("Clean vs Percentage cleaned")
    xlabel("Percentage of floor cleaned")
    ylabel("Average time")
    percentages = [25, 50, 75, 100]
    for i in range(1,6):
        means = []
        for j in range(1,5):
            means.append(runSimulation(i, 1.0, 20, 20, 0.25*j, 30, Robot, False))
        plot(percentages, means)
                         
        
        


# === Problem 5

class RandomWalkRobot(BaseRobot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement
    strategy: it chooses a new direction at random after each
    time-step.
    """
    def updatePositionAndClean(self):
        if self.room.isPositionInRoom(self.getRobotPosition().getNewPosition(self.getRobotDirection() , self.speed)):
            self.setRobotPosition(self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.speed))
            self.room.cleanTileAtPosition(self.getRobotPosition())
            self.setRobotDirection(random.randint(0,360))
        else:
            self.setRobotDirection(random.randint(0,360))
            



# === Problem 6

def showPlot5():
    """
    Produces a plot comparing the two robot strategies.
    """
    title("Clean time vs Area for two Different Robots")
    xlabel("Area of Room")
    ylabel("Average time")
    areas = [25, 100, 225]
    means = []
    for i in range(1,4):
        means.append(runSimulation(1, 1.0, i*5, i*5, 1.00, 30, Robot, False))
    plot(areas, means)
    means2 = []
    for i in range(1,4):
        means2.append(runSimulation(1, 1.0, i*5, i*5, 1.00, 30, RandomWalkRobot, False))
    plot(areas, means2)

    
                    
    


if __name__ == "__main__":
    ##runSimulation(1, 1.0, 5, 5, 1.0, 1000, Robot, False)
    ##runSimulation(1, 1.0, 5, 5, 1.0, 1000, RandomWalkRobot, False)
    ##runSimulation(2, 1.0, 10, 10, 0.75, 1, Robot, False)
    runSimulation(1, 1.0, 20, 20, 1.0, 50, Robot, False)
    ##showPlot5()
    ##show()
    

