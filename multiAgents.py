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
            if ghostDis < 3:
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
        return self.max(gameState, 0)

    def max(self, gameState, depth):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        moves = gameState.getLegalActions(0) # pacman is always 0
        bestScore = float('-inf')
        bestMove = moves[0]
        # print(moves)
        for move in moves: # move pacman
            score = self.min(gameState.generateSuccessor(0, move), depth, 1) # agent always 1, as this is the first enemy
            if score > bestScore:
                bestScore = score
                bestMove = move
        if depth is 0:
            return bestMove
        else:
            return bestScore
    
    def min(self, gameState, depth, agent):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        moves = gameState.getLegalActions(agent)
        # print(moves)
        bestScore = float('inf')
        bestMove = moves[0]
        for move in moves:
            if agent == gameState.getNumAgents()-1: # gone through all enemy agents, time to move pacman
                if depth == self.depth-1: # we are at max depth
                    score = self.evaluationFunction(gameState.generateSuccessor(agent, move))
                else: # done with enemies, move down depth to next pacman move
                    score = self.max(gameState.generateSuccessor(agent, move), depth+1)
            else: # still have enemies to move
                score = self.min(gameState.generateSuccessor(agent, move), depth, agent+1)
            if score < bestScore:
                bestScore = score
        return bestScore

                


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.max(gameState, 0, float('-inf'), float('inf'))
            
    # alter to include alpha beta 
    def max(self, gameState, depth, alpha, beta):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        moves = gameState.getLegalActions(0) # pacman is always 0
        bestScore = float('-inf')
        bestMove = moves[0]
        # print(moves)
        for move in moves: # move pacman
            score = self.min(gameState.generateSuccessor(0, move), depth, 1, alpha, beta) # agent always 1, as this is the first enemy
            if score > bestScore:
                bestScore = score
                bestMove = move
            alpha = max(alpha, bestScore)
            if bestScore > beta:
                return bestScore
        if depth is 0:
            return bestMove
        else:
            return bestScore
    
    # alter min function to include alpha, beta agents
    def min(self, gameState, depth, agent, alpha, beta):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        moves = gameState.getLegalActions(agent)
        # print(moves)
        bestScore = float('inf')
        bestMove = moves[0]
        for move in moves:
            if agent == gameState.getNumAgents()-1: # gone through all enemy agents, time to move pacman
                if depth == self.depth-1: # we are at max depth
                    score = self.evaluationFunction(gameState.generateSuccessor(agent, move))
                else: # done with enemies, move down depth to next pacman move
                    score = self.max(gameState.generateSuccessor(agent, move), depth+1, alpha, beta)
            else: # still have enemies to move
                score = self.min(gameState.generateSuccessor(agent, move), depth, agent+1, alpha, beta)
            if score < bestScore:
                bestScore = score
            beta = min(beta, bestScore)
            if bestScore < alpha:
                return bestScore
        return bestScore
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
        return self.max(gameState, 0)

    # max function is the same, since we are the one making the decision for pacman's move
    def max(self, gameState, depth):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        moves = gameState.getLegalActions(0) # pacman is always 0
        bestScore = float('-inf')
        bestMove = moves[0]
        # print(moves)
        for move in moves: # move pacman
            score = self.min(gameState.generateSuccessor(0, move), depth, 1) # agent always 1, as this is the first enemy
            if score > bestScore:
                bestScore = score
                bestMove = move
        if depth is 0:
            return bestMove
        else:
            return bestScore
    
    # expectimax now takes an average of all known moves
    def min(self, gameState, depth, agent):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        moves = gameState.getLegalActions(agent)
        # print(moves)
        bestScore = 0
        bestMove = moves[0]
        for move in moves:
            if agent == gameState.getNumAgents()-1: # gone through all enemy agents, time to move pacman
                if depth == self.depth-1: # we are at max depth
                    score = self.evaluationFunction(gameState.generateSuccessor(agent, move))
                else: # done with enemies, move down depth to next pacman move
                    score = self.max(gameState.generateSuccessor(agent, move), depth+1)
            else: # still have enemies to move
                score = self.min(gameState.generateSuccessor(agent, move), depth, agent+1)
            bestScore+=score
        return bestScore/len(moves)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>

    Current Evaluation function interacts with:
    pellets

    Does not interact with:
    ghosts (scared/unscared)
    power pellets (named capsules)

    current evaluation function also sometimes just gets stuck, since not moving is just about as good as nothing
    run the following command to see
    python pacman.py --frameTime 0 -p ReflexAgent -k 2
    """
    "*** YOUR CODE HERE ***"

    # since an action is no longer given as in the original evaluation function, things might be different for calculating
    # good reflex agent scores

    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    currentPos = currentGameState.getPacmanPosition()
    currentFood = currentGameState.getFood()
    score = 0
    
    # capsules, more valuable than pellets, in order to chase ghosts
    capsules = currentGameState.getCapsules()
    for capsule in capsules:
        capsuleDis = manhattanDistance(currentPos,capsule)
        if capsuleDis <= 1:
            score += 200
        if capsuleDis < 3:
            score += 20
    

    # need to add whether the ghost is scared or not
    for ghost in newGhostStates:
        ghostDis = manhattanDistance(currentPos, ghost.getPosition())
        if ghostDis <= 1:
            score -= 1000
        if ghostDis < 3:
            score -=500

    closestFoodDis = 1000000
    closestFood = currentFood.asList()[0]
    for food in currentFood.asList():
        foodDis = manhattanDistance(currentPos,food)
        if foodDis < closestFoodDis:
            closestFoodDis = foodDis
            closestFood = food
        if foodDis < 3:
            score += 10
        if foodDis <= 1:
            score += 100
        score -= closestFoodDis


    return score

# Abbreviation
better = betterEvaluationFunction
