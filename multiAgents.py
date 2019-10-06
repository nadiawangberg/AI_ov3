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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
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

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

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
      
      #for every max layer you should have num ghosts min layers
      #game tree should be expanded to arbitrary depth
      # self.evaluationFunction (evaluates states) scores the leaf nodes
      # self.depth and self.evaluationFunction can be accessed cuz of super class
      # depth n search is n moves from all agents

      #grading : python autograder.py -q q2 --no-graphics
    """

    """
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]
    """

    def minimax(self, game_state, player_index, curr_depth):
      #player_index : 0,1,2,3 (0 is packman)
      #game_state : current state
      #curr_depth : depth of the tree, the depth is incremented when all agents have had their turn

      #this function is based on two pseudocodes for minimax
      # https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction/
      # https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-3-tic-tac-toe-ai-finding-optimal-move/

      #chooses between minimizing player and maximizing player
      if (player_index == 0):
        isPackman = True
      else:
        isPackman = False

      #if we are at self.depth or the agent has no actions to do, return the value of the heuristics
      if (curr_depth == self.depth) or (len(game_state.getLegalActions(player_index)) == 0):
        return self.evaluationFunction(game_state) # the heuristics of the game, will say something about how 'good' a state is

      if (isPackman):
        #MAXIMIZE
        packman_actions = game_state.getLegalActions(0)
        best_action = packman_actions[0]
        max_value = float('-inf')

        for action in packman_actions:
          future_state = game_state.generateSuccessor(0, action) # finds future state based on action, for agent 0 (aka packman)
          state_val = self.minimax(future_state, 1, curr_depth) # state_val will be given by the minimal action chosen by the ghost (index 1)

          #max(max_value, value)
          if (state_val > max_value):
            max_value = state_val
            best_action = action

        #return the max_value based on recursive minimax
        return max_value

      else:
        #MINIMIZE
        ghost_actions = game_state.getLegalActions(player_index)
        best_action = ghost_actions[0]
        min_value = float('inf')

        for action in ghost_actions:
          next_player = (player_index + 1) % game_state.getNumAgents() # will go through 1,2,0,1,2,0... if we have two ghosts

          #an action creates many potential future states (given by each action), must minimax all futures
          future_state = game_state.generateSuccessor(player_index, action)
          
          if (next_player == 0): #the last ghost
            state_val = self.minimax(future_state, next_player, curr_depth + 1)
          else:
            state_val = self.minimax(future_state, next_player, curr_depth)

          #min(min_value, value)
          if (state_val < min_value):
            min_value = state_val
            best_action = action

        #return the min_value based on recursive minimax
        return min_value



    def getAction(self, gameState):
        """
          HINTS

          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction(gameState).

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """

        #MAXIMIZE FOR PACKMAN
        packman_actions = gameState.getLegalActions(0)
        best_action = None
        max_value = float('-inf')

        for action in packman_actions:
          future_state = gameState.generateSuccessor(0, action) #agent index, action
          state_val = self.minimax(future_state, 1, 0) # ghost is index 1, curr depth is 0

          #max(max_value, value)
          if (state_val > max_value):
            max_value = state_val
            best_action = action

        #Packman has chose his fav action based on minimax
        return best_action

class AlphaBetaAgent(MultiAgentSearchAgent):
    #player_index : 0,1,2,3 (0 is packman)
    #game_state : current state
    #curr_depth : depth of the tree, the depth is incremented when all agents have had their turn

    #this function is based on two pseudocodes for minimax
    # https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction/
    # https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-3-tic-tac-toe-ai-finding-optimal-move/

    #chooses between minimizing player and maximizing player
    def minimax(self, game_state, player_index, curr_depth):
      if (player_index == 0):
        isPackman = True
      else:
        isPackman = False

      #if node is a leaf node / game ended
      if (curr_depth == self.depth) or (len(game_state.getLegalActions(player_index)) == 0):
        return self.evaluationFunction(game_state) # the heuristics of the game, will say something about how 'good' a state is

      #if isMaximizingPlayer
      if (isPackman):
        #MAXIMIZE
        packman_actions = game_state.getLegalActions(0)
        best_action = packman_actions[0]
        max_value = float('-inf')

        for action in packman_actions:
          future_state = game_state.generateSuccessor(0, action) # finds future state based on action, for agent 0 (aka packman)
          state_val = self.minimax(future_state, 1, curr_depth) # state_val will be given by the minimal action chosen by the ghost (index 1)

          #max(max_value, value)
          if (state_val > max_value):
            max_value = state_val
            best_action = action

        #return the max_value based on recursive minimax
        return max_value

      else:
        #MINIMIZE
        ghost_actions = game_state.getLegalActions(player_index)
        best_action = ghost_actions[0]
        min_value = float('inf')

        for action in ghost_actions:
          next_player = (player_index + 1) % game_state.getNumAgents() # will go through 1,2,0,1,2,0... if we have two ghosts

          #an action creates many potential future states (given by each action), must minimax all futures
          future_state = game_state.generateSuccessor(player_index, action)
          
          if (next_player == 0): #the last ghost
            state_val = self.minimax(future_state, next_player, curr_depth + 1)
          else:
            state_val = self.minimax(future_state, next_player, curr_depth)

          #min(min_value, value)
          if (state_val < min_value):
            min_value = state_val
            best_action = action

        #return the min_value based on recursive minimax
        return min_value

      def getAction(self, gameState):
          """
            Returns the minimax action using self.depth and self.evaluationFunction
          """
          packman_actions = gameState.getLegalActions(0)
          best_action = None
          max_value = float('-inf')

          for action in packman_actions:
            future_state = gameState.generateSuccessor(0, action) #agent index, action
            state_val = self.minimax(future_state, 1, 0) # ghost is index 1, curr depth is 0

            #max(max_value, value)
            if (state_val > max_value):
              max_value = state_val
              best_action = action

          #Packman has chose his fav action based on minimax
          return best_action
          #util.raiseNotDefined()

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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

