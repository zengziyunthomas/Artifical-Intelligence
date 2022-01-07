# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for i in range(self.iterations):
            values = {}
            for state in self.mdp.getStates():
                action = self.computeActionFromValues(state)
                if action and self.computeQValueFromValues(state,action):
                    values[state] = self.computeQValueFromValues(state,action)
            for j in values:  # copy
                self.values[j] = values[j]
        
    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        if action not in self.mdp.getPossibleActions(state):
            return None
        else:
            q=0
            for nextstate,prob in self.mdp.getTransitionStatesAndProbs(state,action):
                q+=prob*(self.mdp.getReward(state,action,nextstate)+self.discount*self.getValue(nextstate))
            return q 

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        value=[]
        for action in self.mdp.getPossibleActions(state):
            q = self.computeQValueFromValues(state,action)
            if q != None:
                value.append((q,action))
        if value == []:
            return None
        else:  # sort by q get action
            q,action = value[0]
            for i,j in value:
                if i > q:
                    q = i
                    action = j
            return action

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        for i in range(self.iterations):
            values = self.values.copy()
            state = states[i%len(states)]
            if not self.mdp.isTerminal(state):
                action = self.getAction(state)
                if action:
                    values[state] = self.getQValue(state, action)
            for i in states:  # copy
                self.values[i] = values[i]

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        predecessors = {} # predecessors
        for state in states:
            predecessors[state] = set()
        for state in states:
            for action in self.mdp.getPossibleActions(state):
                for i in self.mdp.getTransitionStatesAndProbs(state, action):
                    predecessors[i[0]].add(state)
        queue = util.PriorityQueue()  # queue
        for state in states:
            if self.mdp.isTerminal(state):
                continue
            queue.push(state,-abs(self.computeQValueFromValues(state,self.computeActionFromValues(state)) - self.values[state]))
        for i in range(self.iterations): # iter
            if queue.isEmpty():
                return
            state = queue.pop()
            if not self.mdp.isTerminal(state):  # get the maxvalue
                actions = self.mdp.getPossibleActions(state)
                maxv = -9999999
                for action in actions:
                    v = 0
                    for nextstate,prob in self.mdp.getTransitionStatesAndProbs(state,action):
                        v += prob*(self.mdp.getReward(state,action,nextstate)+self.discount*self.values[nextstate])
                    if v > maxv:
                        maxv=v
                if maxv!=-9999999:
                    self.values[state] = maxv
                else:
                    self.values[state] = 0
            for p in predecessors[state]:  # update by the diff
                if self.computeActionFromValues(p) == None:
                    continue
                diff = abs(self.computeQValueFromValues(p,self.computeActionFromValues(p))-self.values[p])
                if diff > self.theta:
                    queue.update(p,-diff)            
        