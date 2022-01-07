# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        manhattan= lambda x1,x2:abs(x1[0]-x2[0])+abs(x1[1]-x2[1])
        food=newFood.asList()
        ghostposition=[i.getPosition() for i in newGhostStates]
        f_score=0
        if food:
            closefood=min([manhattan(newPos,i) for i in food])
            f_score=-closefood
        closeghost=min([manhattan(newPos,i) for i in ghostposition])
        if closeghost!=1:
            g_score=closeghost
        else:
            g_score=-5
        return childGameState.getScore()+0.8*f_score+0.2*g_score

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        legal=gameState.getLegalActions(0)
        nextstate=[gameState.getNextState(0,i) for i in legal]
        result=[self.min1(i,0,1) for i in nextstate]
        return legal[result.index(max(result))]

    def max1(self, gameState, depth, agent):
        if depth==self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        legal=gameState.getLegalActions(0)
        nextstate=[gameState.getNextState(0,i) for i in legal]
        return max([self.min1(i,depth,1) for i in nextstate])

    def min1(self, gameState, depth, agent):
        if depth==self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        legal=gameState.getLegalActions(agent)
        nextstate=[gameState.getNextState(agent,i) for i in legal]
        if agent==gameState.getNumAgents()-1:
            return min([self.max1(i,depth+1,0) for i in nextstate])
        else:
            return min([self.min1(i,depth,agent+1) for i in nextstate])
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha=-999999999
        beta=999999999
        legal=gameState.getLegalActions(0)
        score=-999999999
        action=[]
        for i in legal:
            nextstate=gameState.getNextState(0,i)
            this_act_score=self.min1(nextstate,0,1,alpha,beta)
            if this_act_score>score:
                score=this_act_score
                action=i
            alpha=max(alpha,this_act_score)
        return action

    def max1(self, gameState, depth, agent, alpha, beta):
        if depth==self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        legal=gameState.getLegalActions(0)
        v=-999999999
        for i in legal:
            nextstate=gameState.getNextState(0,i)
            this_act_score=self.min1(nextstate,depth,1,alpha,beta)
            v=max(v,this_act_score)
            if v>beta:
                return v
            alpha=max(alpha,this_act_score)
        return v
    
    def min1(self, gameState, depth, agent, alpha, beta):
        if depth==self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        legal=gameState.getLegalActions(agent)
        v=999999999
        for i in legal:
            nextstate=gameState.getNextState(agent,i)
            if agent==gameState.getNumAgents()-1:
                v=min(v,self.max1(nextstate,depth+1,0,alpha,beta))
            else:
                v=min(v,self.min1(nextstate,depth,agent+1,alpha,beta))
            if v<alpha:
                return v
            beta=min(beta,v)
        return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        legal=gameState.getLegalActions(0)
        nextstate=[gameState.getNextState(0,i) for i in legal]
        result=[self.E(i,0,1) for i in nextstate]
        return legal[result.index(max(result))]

    def E(self, gameState, depth, agent):
        if depth==self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        legal=gameState.getLegalActions(agent)
        nextstate=[gameState.getNextState(agent,i) for i in legal]
        num=gameState.getNumAgents()
        count=0
        if agent==num-1:
            count=1
        result=[self.E(i,depth+count,(agent+1)%num) for i in nextstate]
        if not agent:
            return max(result)
        return sum(result)/len(result)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    my function evaluate doesn't consider a lot about the state of the pacman and ghost, but the distance between pacman and food, and the number of food. Then use a linear way to combine them together to be my only for the evaluation.
    """
    "*** YOUR CODE HERE ***"
    manhattan=lambda x1,x2:abs(x1[0]-x2[0])+abs(x1[1]-x2[1])
    food=currentGameState.getFood().asList()
    dist=[manhattan(currentGameState.getPacmanPosition(),i) for i in food]
    mindist=0
    if len(dist):
        mindist=min(dist)
    return currentGameState.getScore()-mindist-currentGameState.getNumFood() 

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        alpha=-999999999
        beta=999999999
        legal=gameState.getLegalActions(0)
        score=-999999999
        action=[]
        for i in legal:
            nextstate=gameState.getNextState(0,i)
            this_act_score=self.min1(nextstate,0,1,alpha,beta)
            if this_act_score>score:
                score=this_act_score
                action=i
            alpha=max(alpha,this_act_score)
        return action

    def max1(self, gameState, depth, agent, alpha, beta):
        if depth==self.depth or gameState.isWin() or gameState.isLose():
            return betterEvaluationFunction(gameState)
        legal=gameState.getLegalActions(0)
        v=-999999999
        for i in legal:
            nextstate=gameState.getNextState(0,i)
            this_act_score=self.min1(nextstate,depth,1,alpha,beta)
            v=max(v,this_act_score)
            if v>beta:
                return v
            alpha=max(alpha,this_act_score)
        return v
    
    def min1(self, gameState, depth, agent, alpha, beta):
        if depth==self.depth or gameState.isWin() or gameState.isLose():
            return betterEvaluationFunction(gameState)
        legal=gameState.getLegalActions(agent)
        v=999999999
        for i in legal:
            nextstate=gameState.getNextState(agent,i)
            if agent==gameState.getNumAgents()-1:
                v=min(v,self.max1(nextstate,depth+1,0,alpha,beta))
            else:
                v=min(v,self.min1(nextstate,depth,agent+1,alpha,beta))
            if v<alpha:
                return v
            beta=min(beta,v)
        return v