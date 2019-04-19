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
    """

    def __init__(self):
        """
        setup object
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(level=logging.INFO)
        self.logger.info("Initialized")
        self.tableau = None
    
    def init_tableau(self, c, A):
        """
        creates tableau
        :param c: objective function constraints
        :param A: constraint matrix with coefficients and b values
        :return:
        """
        tableau = [row[:] for row in A]
        tableau.append([i for i in c] + [0])
        self.tableau = tableau


if __name__ == "__main__":

    simplex = utils.init_simplex()

    # schlupfvariablen hinzufügen
    # A[0] += [1, 0]
    # A[1] += [0, 1]
    # c += [0, 0]

    simplex.logger.info("Initial tableau:")
    for row in simplex.tableau:
        simplex.logger.info(row)
