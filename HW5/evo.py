"""
evo.py: An evolutionary computing framework
"""

import random as rnd
import copy
from functools import reduce
import numpy as np
import time
from profiler import Profiler

class Evo:

    def __init__(self):
        self.pop = {}     # evaluation --> solution
        self.fitness = {} # name --> objective function
        self.agents = {} # name --> (operator function, num_solutions_input)

    def add_fitness_criteria(self, name, f):
        """ Register an objective with the environment """
        self.fitness[name] = f

    def add_agent(self, name, op, k=1):
        """ Register an agent with the environment
        The operator (op) defines how the agent tweaks a solution.
        k defines the number of solutions input to the agent. """
        self.agents[name] = (op, k)

    def add_solution(self, sol):
        """ Add a solution to the population   """
        eval = tuple([(name, f(sol)) for name, f in self.fitness.items()])
        self.pop[eval] = sol   # ((name1, objval1), (name2, objval2)....)  ===> solution




    def get_random_solutions(self, k=1):
        """ Pick k random solutions from the population """
        if len(self.pop) == 0: # no solutions in the population (This should never happen!)
            return []
        else:
            solutions = tuple(self.pop.values())
            # Doing a deep copy of a randomly chosen solution (k times)
            return [copy.deepcopy(rnd.choice(solutions)) for _ in range(k)]


    def run_agent(self, name):
        """ Invoke a named agent on the population """
        op, k = self.agents[name]
        picks = self.get_random_solutions(k)
        new_solution = op(picks)
        self.add_solution(new_solution)


    def dominates(self, p, q):
        """
        p = evaluation of one solution: ((obj1, score1), (obj2, score2), ... )
        q = evaluation of another solution: ((obj1, score1), (obj2, score2), ... )
        """
        pscores = np.array([score for name, score in p])
        qscores = np.array([score for name, score in q])
        score_diffs = qscores - pscores
        return min(score_diffs) >= 0 and max(score_diffs) > 0.0

    def reduce_nds(self, S, p):
        return S - {q for q in S if self.dominates(p, q)}

    def remove_dominated(self):
        nds = reduce(self.reduce_nds, self.pop.keys(), self.pop.keys())
        self.pop = {k: self.pop[k] for k in nds}

    @Profiler.profile
    def evolve(self, n=1, dom=100, status=1000, time_limit=None):
        """ Run random agents n times or until the time limit is reached.
        n: Number of agent invocations
        dom: Frequency for dominance checks
        status: Frequency for outputting the current population
        time_limit: Maximum time to run the evolution (in seconds)
        """
        agent_names = list(self.agents.keys())
        start_time = time.time()  # Record the start time

        for i in range(n):
            # Check if time limit has been reached
            if time_limit and (time.time() - start_time) >= time_limit:
                print(f"Time limit of {time_limit} seconds reached. Stopping evolution.")
                break

            # Randomly pick and run an agent
            pick = rnd.choice(agent_names)
            self.run_agent(pick)

            # Periodically remove dominated solutions
            if i % dom == 0:
                self.remove_dominated()

            # Periodically output the population status
            if i % status == 0:
                self.remove_dominated()
                print("Iteration: ", i)
                print("Size     : ", len(self.pop))
                print(self)

        # Final cleanup: remove dominated solutions
        self.remove_dominated()

    def __str__(self):
        """ Output the solutions in the population """
        rslt = ""
        for eval, sol in self.pop.items():
            rslt += str(eval) + ":\t" + str(sol) + "\n"
        return rslt


