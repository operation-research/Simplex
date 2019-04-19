#!/usr/bin/python3
import logging
import utils


__author__ = "Daniel Kogan, Janek Putz"


class Simplex:
    """
    Simplex algorithm

    Attributes:
        logger(Logger): logger
        tableau([]): simplex tableau
        initial_A([[]]): initial constraint matrix
        initial_b_vector([]): initial b vector
    """

    def __init__(self):
        """
        setup object
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.tableau = None
        self.initial_A = None
        self.initial_b_vector = None
        self.initial_c = None

        # config logging
        logging.basicConfig(level=logging.INFO)

        # initialize and prepare data
        utils.init_simplex(self)
        self.add_slack_vars()
        self.init_tableau()
        self.logger.info("Initialized")
    
    def init_tableau(self):
        """
        create tableau
        :param c: objective function constraints
        :param A: constraint matrix with coefficients and b values
        :return:
        """
        tableau = [row[:] + [x] for row, x in zip(self.initial_A, self.initial_b_vector)]
        tableau.append([i for i in self.initial_c] + [0])
        self.tableau = tableau

    def add_slack_vars(self):
        """
        add slack variables to the constraint matrix
        :return:
        """
        for idx, constraint in enumerate(self.initial_A):

            slack_var = [0] * len(self.initial_A)
            slack_var[idx] = 1
            self.initial_A[idx] += slack_var

        self.initial_c += [0] * len(self.initial_A)


if __name__ == "__main__":

    simplex = Simplex()

    # schlupfvariablen hinzufügen
    # A[0] += [1, 0]
    # A[1] += [0, 1]
    # c += [0, 0]

    simplex.logger.info("Initial tableau:")
    for row in simplex.tableau:
        simplex.logger.info(row)
