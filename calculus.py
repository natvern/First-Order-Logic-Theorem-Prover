## Project  : CCLITP
## Sequent Calculus Rules constructed as a class
## Created  : 7/4/2019 - 19:42
## andrewID : srahmoun

## NOTES FROM 7/10/2019
## Rules are independant of the engine, hence changing the logic
## would mean writing a new file for different inference rules

from propositions import FalseHood

# We will define the inference rules that would apply
# They are directly derived from sequent calculus
class Calculus:
    def __init__(self):
        self.axiom = [self.identity, self.found_falsehood]
        self.rules = [self.disjunction, self.conjunction, self.implication, self.negation]
        self.mainGoal = []
        self.Falsehood = FalseHood()

    # One axiom is when we have the same atomic clauses on both sides
    def identity(self, A, B):
        for i in A:
            if i in B:
                return True
        return False

    # Another axiom is when falsehood is found in the hypothesis
    def found_falsehood(self, hypothesis):
        for i in hypothesis:
            if len(i) == 1:
                if i[0].getState == False:
                    return True
        return False

    # When facing a disjunction, we separate the formula into two new formula
    # That we define as new goals
    def disjunction(self, goal, side, n):
        self.mainGoal = goal[side][n]
        if side == 0:
            newGoals = []
            for i in [self.mainGoal[0],self.mainGoal[1]]:
                newGoal = (self.mainGoal[0]+[i], self.mainGoal[1])
                newGoals.append(newGoal)
            return newGoals
        elif side == 1:
            # If there is an "or" on the right side, we delete it
            A = self.mainGoal[0]
            B = self.mainGoal[1]
            del goal[side][n]
            goal[side].append(A)
            goal[side].append(B)
            return goal
        raise "Error choosing the side (not 0 or 1)"

    # A conjunction would create two new goals
    def conjunction(self, A, B, goal):
        self.mainGoal = goal
        newGoals = []
        for i in [A,B]:
            newGoal = (self.mainGoal[0],self.mainGoal[1]+[i])
            newGoals.append(newGoal)
        return newGoals

    # If it is an implication (A -> B), we get two new goals
    # One for which A is part of the conclusion,
    # The other is when B is part of the hypothesis
    def implication(self, A, B, goal):
        self.mainGoal = goal
        newGoal_1 = (self.mainGoal[0], self.mainGoal[1] + [A])
        newGoal_2 = (self.mainGoal[0] + [B], self.mainGoal[1])
        return [newGoal_1, newGoal_2]

    # Negation is equivalent to A imply Falsehood
    def negation(self, goal, side, n):
        self.mainGoal = goal[side][n]
        A = self.mainGoal[0]
        goal[side][n] = [A, [self.Falsehood], "imply"]
        return goal
