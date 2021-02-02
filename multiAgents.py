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
        currentPos = currentGameState.getPacmanPosition()
        currentFood = currentGameState.getFood()
        score = 0

        for ghost in newGhostStates:
            ghostDis = manhattanDistance(newPos, ghost.getPosition())
            if ghostDis is 0:
                score -= 1000
            if ghostDis < 2:
                score -=500

        closestFoodDis = 1000000
        closestFood = currentFood.asList()[0]
        for food in currentFood.asList():
            foodDis = manhattanDistance(newPos,food)
            if foodDis < closestFoodDis:
                closestFoodDis = foodDis
                closesFood = food
            if foodDis is 0:
                score += 100
            score -= closestFoodDis
        
        if manhattanDistance(newPos, closestFood) < manhattanDistance(currentPos,closestFood):
            score += 10

        return score

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
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        bestMove, bestScore = self.max(gameState, self.depth)
        # print(bestMove)
        # print()
        # print()
        # print()
        # print()
        return bestMove

        util.raiseNotDefined()
            
    def min(self, gameState, depth):
        if depth is 0 or gameState.isLose() or gameState.isWin():
            # we've searched as far as we need to or the game ended 
            return self.evaluationFunction(gameState)

        moves = gameState.getLegalActions()
        scores = [self.max(gameState.generateSuccessor(self.index, move), depth-1) for move in moves]
        # print("scores: ",scores, len(scores))
        for i in range(len(scores)):
            if type(scores[i]) is tuple:
                scores[i] = scores[i][1]
        # print("scores: ", scores, len(scores))
        # print("moves: ", moves)
        bestScore = min(scores)

        bestMove = moves[0]
        for i in range(len(scores)):
        #     print("current score: ", scores[i])
        #     print("best score: ", bestScore)
            if scores[i] == bestScore:
                bestMove = moves[i]
        # print(bestMove)
        # print(bestScore)
        # print()
        # print()
        return bestMove, bestScore

    def max(self, gameState, depth):
        if depth is 0 or gameState.isLose() or gameState.isWin():
            # we've searched as far as we need to or the game ended
            return self.evaluationFunction(gameState)

        moves = gameState.getLegalActions()
        scores = [self.min(gameState.generateSuccessor(self.index, move),depth-1) for move in moves]
        # print("scores: ", scores, len(scores))
        for i in range(len(scores)):
            if type(scores[i]) is tuple:
                scores[i] = scores[i][1]
        # print("scores: ", scores, len(scores))
        # print("moves: ", moves)

        bestScore = max(scores)

        bestMove = moves[0]
        for i in range(len(scores)):
        #     print("current score: ", scores[i])
        #     print("best score: ", bestScore)
            if scores[i] == bestScore:
                bestMove = moves[i]
        # print(bestMove)
        # print(bestScore)
        # print()
        # print()
        return bestMove, bestScore



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

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
