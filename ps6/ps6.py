# Problem Set 6: Simulating robots
# Name:
# Collaborators:
# Time:

import math
import random
import numpy as np
import ps6_visualize
import matplotlib.pyplot as plt

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
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

        angle: float representing angle in degrees, 0 <= angle < 360
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

# === Problems 1

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
        tiles = np.full([width, height], 'dirty', dtype='a5')
        self.room = tiles[:]
        #raise NotImplementedError
    
    def roomDisplay(self):
        """
        Returns a display of room (array format)
        """
        return self.room
        
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        x = math.floor(pos.getX())
        y = math.floor(pos.getY()) 
        self.room[x, y] = 'clean'
        #raise NotImplementedError

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        if self.room[m, n] == 'clean':
            return True
        return False
        #raise NotImplementedError
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height
        #raise NotImplementedError

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        cleanedTiles = 0
        for row in self.room:
            for tile in row:
                if tile == 'clean':
                    cleanedTiles += 1
        return cleanedTiles
        #raise NotImplementedError
        
    def cleanRatio(self):
        """
        provides a ration of cleaned tiles to total tiles present in the room
        """
        return float(self.getNumCleanedTiles()) / float(self.getNumTiles())

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        randPos = Position(random.uniform(0, self.width), random.uniform(0, self.height))
        return randPos
        #raise NotImplementedError

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        x = pos.getX()
        y = pos.getY()
        if 0 <= x <= self.width:
            if 0 <= y <= self.height:
                return True
            return False
        return False
        #raise NotImplementedError


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.speed = speed
        self.room = room
        self.pos = room.getRandomPosition()
        self.direct = random.randrange(0, 360)
        self.room.cleanTileAtPosition(self.pos)
        
        #raise NotImplementedError

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.pos
        #raise NotImplementedError
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direct
        #raise NotImplementedError

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """ 
        self.pos = position
        #raise NotImplementedError

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direct = direction
        #raise NotImplementedError

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        
        raise NotImplementedError


# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        for unit in xrange(int(self.speed)):
            newPosition = self.pos.getNewPosition(self.direct, 1.0)
            if self.room.isPositionInRoom(newPosition):
                self.setRobotPosition(newPosition)
                self.room.cleanTileAtPosition(self.pos)
            else:
                self.direct = random.randrange(360)
        #raise NotImplementedError

# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials, robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """
    visualize = False
    time_steps_trials = []
    for trial in xrange(num_trials):
        if visualize:
            anim = ps6_visualize.RobotVisualization(num_robots, width, height)
                
        trial_room = RectangularRoom(width, height)
        
        bots = [robot_type(trial_room, speed) for i in xrange(num_robots)]
        if visualize:
            anim.update(trial_room, bots)
                
        time_steps = 0.0
        while trial_room.cleanRatio() < min_coverage:
            for bot in bots:
                bot.updatePositionAndClean()
            time_steps += 1
            if visualize:
                anim.update(trial_room, bots)
        if visualize:
            anim.done()
        time_steps_trials.append(time_steps)

    mean_time_steps_trials = sum(time_steps_trials)/len(time_steps_trials)    
    if visualize:
        print "mean clock time of " + str(mean_time_steps_trials) +" steps"
    return mean_time_steps_trials
    #raise NotImplementedError


# === Problem 4
#
# 1) How long does it take to clean 0.8 of a 20x20 room with each of 1-10 robots?
#
# 2) How long does it take two robots to clean 80% of rooms with dimensions 
#	 20x20, 25x16, 40x10, 50x8, 80x5, and 100x4?

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """ 
    num_bot_range = xrange(1,11)
    times1 = []
    times2 = []
    for bots in num_bot_range:
        times1.append(runSimulation(bots, 1.0, 20, 20, 0.8, 20, StandardRobot))
        times2.append(runSimulation(bots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))  
    plt.plot(num_bot_range, times1, 'ro-')
    plt.plot(num_bot_range, times2, 'go-')
    plt.title("Time to clean 80% of a given Room using a given number of Robots")
    plt.legend(('StandardRobot', 'RandomWalkRobot'))
    plt.xlabel('Number of Robots Used')
    plt.ylabel('Time-steps')
    plt.show()
    #raise NotImplementedError

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    #20x20, 25x16, 40x10, 50x8, 80x5, and 100x4
    #ratio of width to height
    w_by_h = [(20, 20), (25, 16), (40, 10), (50, 8), (80, 5), (100, 4)]
    w_to_h = []
    times1 = []
    times2 = []
    for width, height in w_by_h:
        w_to_h.append(float(width) / float(height))
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 20, StandardRobot))
        times2.append(runSimulation(2, 1.0, width, height, 0.8, 20, RandomWalkRobot))        
    plt.plot(w_to_h, times1, 'ro-')
    plt.plot(w_to_h, times2, 'go-')
    plt.title("Time to clean 80% of a given Room with Width x Height Dimensions")
    plt.legend(('StandardRobot', 'RandomWalkRobot'))
    plt.xlabel('# Width to Height Ratio of Room Dimensions')
    plt.ylabel('Time-steps')
    plt.show()
    #raise NotImplementedError

# === Problem 5

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """
    def updatePositionAndClean(self):
        for unit in xrange(int(self.speed)):
            newPosition = self.pos.getNewPosition(self.direct, 1.0)
            if self.room.isPositionInRoom(newPosition):
                self.setRobotPosition(newPosition)
                self.room.cleanTileAtPosition(self.pos)
            else:
                self.direct = random.randrange(360)
            self.direct = random.randrange(360)
        #raise NotImplementedError

# === Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.
def showPlot3():
    """
    Produces a plot comparing the speed of the robots.
    """
    #Speed == 1.0 --> 10.0
    #ratio of width to height
    speed_range = xrange(1,11)
    times1 = []
    times2 = []
    for speed in speed_range:
        times1.append(runSimulation(2, float(speed), 20, 20, 0.8, 20, StandardRobot))
        times2.append(runSimulation(2, float(speed), 20, 20, 0.8, 20, RandomWalkRobot))        
    plt.plot(speed_range, times1, 'ro-')
    plt.plot(speed_range, times2, 'go-')
    plt.title("Time to clean 80% of a given Room for a Robot with a given Speed")
    plt.legend(('StandardRobot', 'RandomWalkRobot'))
    plt.xlabel('Speed of Robot')
    plt.ylabel('Time-steps')
    plt.show()
    #raise NotImplementedError        
