# logicPlan.py
# ------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In logicPlan.py, you will implement logic planning methods which are called by
Pacman agents (in logicAgents.py).
"""

import util
import sys
import logic
import game
import itertools


pacman_str = 'P'
ghost_pos_str = 'G'
ghost_east_str = 'GE'
pacman_alive_str = 'PA'

class PlanningProblem:
    """
    This class outlines the structure of a planning problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the planning problem.
        """
        util.raiseNotDefined()

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostPlanningProblem)
        """
        util.raiseNotDefined()
        
    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionPlanningProblem
        """
        util.raiseNotDefined()

def tinyMazePlan(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def sentence1():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    A or B
    (not A) if and only if ((not B) or C)
    (not A) or (not B) or C
    """
    "*** YOUR CODE HERE ***"
    A,B,C = logic.Expr('A'),logic.Expr('B'),logic.Expr('C')
    logic1 = A | B
    logic2 = (~A) % ((~B) | C)
    logic3 = logic.disjoin((~A),(~B),C)
    # logic3 = ~A | ~B | C
    return logic.conjoin(logic1,logic2,logic3)

def sentence2():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    C if and only if (B or D)
    A implies ((not B) and (not D))
    (not (B and (not C))) implies A
    (not D) implies C
    """
    "*** YOUR CODE HERE ***"
    A,B,C,D = logic.Expr('A'),logic.Expr('B'),logic.Expr('C'),logic.Expr('D')
    logic1 = C % ( B | D )
    logic2 = A >> ((~B) & (~D))
    logic3 = (~(B & (~C))) >> A
    logic4 = (~D) >> C
    return logic.conjoin(logic1,logic2,logic3,logic4)

def sentence3():
    """Using the symbols WumpusAlive[1], WumpusAlive[0], WumpusBorn[0], and WumpusKilled[0],
    created using the logic.PropSymbolExpr constructor, return a logic.PropSymbolExpr
    instance that encodes the following English sentences (in this order):

    The Wumpus is alive at time 1 if and only if the Wumpus was alive at time 0 and it was
    not killed at time 0 or it was not alive and time 0 and it was born at time 0.

    The Wumpus cannot both be alive at time 0 and be born at time 0.

    The Wumpus is born at time 0.
    """
    "*** YOUR CODE HERE ***"
    WA1 = logic.PropSymbolExpr('WumpusAlive[1]')
    WA0 = logic.PropSymbolExpr('WumpusAlive[0]')
    WB0 = logic.PropSymbolExpr('WumpusBorn[0]')
    WK0 = logic.PropSymbolExpr('WumpusKilled[0]')
    logic1 = WA1 % ((WA0 & (~WK0)) | (~WA0 & WB0))
    logic2 = ~(WA0 & WB0)
    logic3 = WB0
    return logic.conjoin(logic1,logic2,logic3)

def findModel(sentence):
    """Given a propositional logic sentence (i.e. a logic.Expr instance), returns a satisfying
    model if one exists. Otherwise, returns False.
    """
    "*** YOUR CODE HERE ***"
    CNF1=logic.to_cnf(sentence)
    return logic.pycoSAT(CNF1)

def atLeastOne(literals) :
    """
    Given a list of logic.Expr literals (i.e. in the form A or ~A), return a single 
    logic.Expr instance in CNF (conjunctive normal form) that represents the logic 
    that at least one of the literals in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    """
    "*** YOUR CODE HERE ***"
    return logic.disjoin(literals)


def atMostOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form) that represents the logic that at most one of 
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    literals = [~i for i in literals]
    literals = map(logic.disjoin, itertools.combinations(literals, 2))
    return logic.conjoin(literals)


def exactlyOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form)that represents the logic that exactly one of 
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    return logic.conjoin(atLeastOne(literals),atMostOne(literals))


def extractActionSequence(model, actions):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[3]":True, "P[3,4,1]":True, "P[3,3,1]":False, "West[1]":True, "GhostScary":True, "West[3]":False, "South[2]":True, "East[1]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print plan
    ['West', 'South', 'North']
    """
    "*** YOUR CODE HERE ***"
    willdo=[]
    for i,j in model.items():
        if j:
            willdo.append(logic.PropSymbolExpr.parseExpr(i))
    willdo=[i for i in willdo if i[0] in actions]
    # print(willdo)
    willdo=sorted(willdo,key=lambda x:int(x[1]))
    # print(willdo)
    willdo=[i[0] for i in willdo]
    return willdo


def pacmanSuccessorStateAxioms(x, y, t, walls_grid): 
    """
    Successor state axiom for state (x,y,t) (from t-1), given the board (as a 
    grid representing the wall locations).
    Current <==> (previous position at time t-1) & (took action to move to x, y)
    """
    "*** YOUR CODE HERE ***"
    cur_pacman = logic.PropSymbolExpr(pacman_str,x,y,t)
    direction = [((x-1,y),'East'),((x,y+1),'South'),((x+1,y),'West'),((x,y-1),'North')]
    neighbour = [(i,j) for i,j in direction if not walls_grid[i[0]][i[1]]]
    # print(neighbour)
    formal_position = []
    for i in neighbour:
        truth=logic.PropSymbolExpr(pacman_str,i[0][0],i[0][1],t-1) & logic.PropSymbolExpr(i[1],t-1)
        formal_position.append(truth)
    return logic.disjoin(formal_position) % cur_pacman

def positionLogicPlan(problem):
    """
    Given an instance of a PositionPlanningProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()
    
    "*** YOUR CODE HERE ***"

    no_wall_neighbour = lambda t: logic.conjoin([pacmanSuccessorStateAxioms(i,j,t,walls) for i,j in no_wall])
    good_direction = lambda t: exactlyOne([logic.PropSymbolExpr(i,t-1) for i in direction])
    good_position = lambda t: exactlyOne([logic.PropSymbolExpr(pacman_str,i,j,t-1) for i,j in no_wall])
    end_state = lambda t: logic.PropSymbolExpr(pacman_str,end[0],end[1],t)
    
    direction = ['North','South','East','West']
    start = problem.getStartState()
    # print(start)
    end = problem.getGoalState()
    # print(end)
    t = 1
    no_wall = []
    for i in range(1,width+1):
        for j in range(1,height+1):
            if not walls[i][j]:
                no_wall.append((i,j))
    
    start_state=logic.PropSymbolExpr(pacman_str,start[0],start[1],0)
    for i in range(1,width+1):
        for j in range(1,height+1):
            if (i,j) != start:
                start_state=logic.conjoin(start_state , ~logic.PropSymbolExpr(pacman_str,i,j,0))
    print(start_state)
    
    __direction = good_direction(1)
    __position = good_position(1)
    __neighbour = no_wall_neighbour(1)-

    while True:
        if t > 1:
            __neighbour = logic.conjoin(__neighbour,no_wall_neighbour(t))
            __direction = logic.conjoin(__direction,good_direction(t))
            __position = logic.conjoin(__position,good_position(t))
        model=findModel(logic.conjoin(start_state,__neighbour,__direction,__position,end_state(t)))
        if not model:
            t+=1
        else:
            return extractActionSequence(model,direction)

def foodLogicPlan(problem):
    """
    Given an instance of a FoodPlanningProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()

    "*** YOUR CODE HERE ***"

    no_wall_neighbour = lambda t: logic.conjoin([pacmanSuccessorStateAxioms(i,j,t,walls) for i,j in no_wall])
    good_direction = lambda t: exactlyOne([logic.PropSymbolExpr(i,t-1) for i in direction])
    good_position = lambda t: exactlyOne([logic.PropSymbolExpr(pacman_str,i,j,t-1) for i,j in no_wall])

    direction = ['North','South','East','West']
    start,food = problem.getStartState()
    food=food.asList()

    t = 1
    no_wall = []
    for i in range(1,width+1):
        for j in range(1,height+1):
            if not walls[i][j]:
                no_wall.append((i,j))
    
    start_state=logic.PropSymbolExpr(pacman_str,start[0],start[1],0)
    for i in range(1,width+1):
        for j in range(1,height+1):
            if (i,j) != start:
                start_state=logic.conjoin(start_state , ~logic.PropSymbolExpr(pacman_str,i,j,0))
    
    __direction = good_direction(1)
    __position = good_position(1)
    __neighbour = no_wall_neighbour(1)

    count=0
    while True:
        end = None
        for i,j in food:
            count+=1
            temp = logic.PropSymbolExpr(pacman_str,i,j,0)
            for k in range(1,t+1):
                temp = logic.disjoin(temp,logic.PropSymbolExpr(pacman_str,i,j,k))
            if count == 1:
                end = temp
            else:
                end = logic.conjoin(end,temp)
        count=0
        if t > 1:
            __neighbour = logic.conjoin(__neighbour,no_wall_neighbour(t))
            __direction = logic.conjoin(__direction,good_direction(t))
            __position = logic.conjoin(__position,good_position(t))
        model=findModel(logic.conjoin(start_state,__neighbour,__direction,__position,end))
        if not model:
            t+=1
        else:
            return extractActionSequence(model,direction)


# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)
    