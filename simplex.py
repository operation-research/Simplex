#!/usr/bin/python3
import logging
import utils

__author__ = "Daniel Kogan, Janek Putz"


class Simplex:
    """
    Simplex algorithm

    Attributes:
        dev(Boolean): development flag
        logger(Logger): logger
        tableau([]): simplex tableau
        initial_A([[]]): initial constraint matrix
        initial_b([]): initial b vector
        initial_c([]): initial c vector
    """

    def __init__(self, dev=False):
        """
        setup object
        :param dev: development flag
        """
        self.dev = dev
        self.logger = logging.getLogger(self.__class__.__name__)
        self.tableau = None
        self.initial_A = None
        self.initial_b = None
        self.initial_c = None

        # config logging
        logging.basicConfig(level=logging.INFO)
        self.logger.info("Initialize Simplex".center(40, '*'))

        # initialize and prepare data
        utils.init_simplex_data(self)
        self.add_slack_vars()
        self.init_tableau()

    def init_tableau(self):
        """
        build tableau using the initial values of the input
        :return:
        """
        tableau = [row[:] + [x] for row, x in zip(self.initial_A, self.initial_b)]
        tableau.append([i for i in self.initial_c] + [0])
        self.tableau = tableau

        self.logger.info("Initial tableau:")
        for row in self.tableau:
            self.logger.info(row)

    def add_slack_vars(self):
        """
        add slack variables to the constraint matrix
        :return:
        """
        for idx, constraint in enumerate(self.initial_A):
            slack_var = [0] * len(self.initial_A)
            slack_var[idx] = 1
            self.initial_A[idx] += slack_var

        # self.initial_c += [0] * len(self.initial_A)

    def run(self):
        """
        runs the simplex algorithm
        :return:
        """
        self.run_phase_1()
        self.run_phase_2()

    def run_phase_1(self):
        """
        run the first phase of the algorithm
        <description>
        :return:
        """
        self.logger.info('Start phase 1'.center(40, '*'))

    def run_phase_2(self):
        """
        run the second phase of the algorithm
        <description>
        :return:
        """
        self.logger.info('Start phase 2'.center(40, '*'))

        # if not at least one negative coefficient is found in the objective functions the algorithm terminates
        if self.check_negative_c():

            pivot_col = self.get_pivot_col()
            self.logger.info('Pivot column: %d' % pivot_col)
            pivot_row = self.get_pivot_row()
            self.logger.info('Pivot row: %d' % pivot_row)

        else:
            print('Algorithm terminates')

    def get_pivot_col(self):
        """
        provide the pivot columns index
        identify the lowest coefficient in the objective function
        :return: pivot column index
        """
        return self.tableau[-1].index(min(self.tableau[-1]))

    def get_pivot_row(self):
        """
        provide the pivot rows index
        calculate the quotient of pivot column coefficient and b, identify the minimum
        :return:
        """
        quotients = [con[self.get_pivot_col()] / con[-1] for con in self.tableau[:-1]]
        return quotients.index(min(quotients))

    def check_negative_c(self):
        """
        check for at least one negative coefficient in the objective function
        :return:
        """
        c = self.tableau[-1]
        for coefficient in c:
            if coefficient < 0:
                return True
        return False


if __name__ == "__main__":

    simplex = Simplex(dev=True)
    simplex.run()

