#!/usr/bin/python3

__author__ = "Daniel Kogan, Janek Putz"

import logging


class Simplex:

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(level=logging.INFO)
        self.logger.info("Initialized")
    
    def initial_tableau(self, c, A, b):
        tableau = [row[:] + [x] for row, x in zip(A, b)]
        tableau.append([i for i in c] + [0])
        return tableau


if __name__ == "__main__":

    simplex = Simplex()

    c = [3, 2]
    A = [[1, 2], [1, -1]]
    b = [4, 1]

    # schlupfvariablen hinzufügen
    A[0] += [1, 0]
    A[1] += [0, 1]
    c += [0, 0]

    simplex.logger.info("A matrix: " + str(A))
    simplex.logger.info("zielfunktion: " + str(c))
    simplex.logger.info("b vektor: " + str(b))

    # erstes tableau bestimmen
    tableau = simplex.initial_tableau(c, A, b)
    simplex.logger.info("Initial tableau:")
    for row in tableau:
        print(row)
