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
        self.logger.info("Initialize Simplex".center(60, '*'))

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
        tableau.append([i * (-1) for i in self.initial_c])
        self.tableau = tableau

        self.logger.info("Initial tableau:")
        self.log_tableau()

    def add_slack_vars(self):
        """
        add slack variables to the constraint matrix
        :return:
        """
        self.initial_c += [0] * (len(self.initial_A[0]) + 1)

        for idx, constraint in enumerate(self.initial_A):
            slack_var = [0] * len(self.initial_A)
            slack_var[idx] = 1
            self.initial_A[idx] += slack_var

    def run(self):
        """
        runs the simplex algorithm
        :return:
        """
        # self.run_phase_1()
        self.run_phase_2()

    def run_phase_1(self):
        """
        run the first phase of the algorithm
        <description>
        :return:
        """
        self.logger.info('Start phase 1'.center(60, '*'))

        negative_b_row_indices = []
        for idx, con in enumerate(self.tableau[:-1]):
            if con[-1] < 0:
                negative_b_row_indices.append(idx)

        print(negative_b_row_indices)

        if len(negative_b_row_indices) > 0:
            # oEdA die erste Zeile nehmen -> x1 geht in die basis
            new_constraint = self.tableau[0]
            new_constraint[1:-1] = [-a for a in new_constraint[1:-1]]
            new_constraint = [a / self.tableau[0][0] for a in self.tableau[0]]
            print(new_constraint)

        else:
            pass

    def run_phase_2(self):
        """
        run the second phase of the algorithm
        <description>
        :return:
        """
        self.logger.info('Start phase 2'.center(60, '*'))
        i = 1

        # if not at least one negative coefficient is found in the objective functions the algorithm terminates
        while len(list(filter(lambda x: x < 0, self.tableau[-1]))) > 0:

            self.logger.info(('%d. Iteration' % i).center(40, '-'))
            self.base_exchange()
            self.log_tableau()
            self.get_base_point()
            i += 1

        self.logger.info('Algorithm terminates'.center(40, '-'))

    def get_pivot_col_idx(self):
        """
        provide the pivot columns index
        identify the lowest coefficient in the objective function
        :return: pivot column index
        """
        return self.tableau[-1].index(min(self.tableau[-1]))

    def get_pivot_row_idx(self):
        """
        provide the pivot rows index
        calculate the quotient of pivot column coefficient and b, identify the minimum
        :return:
        """
        quotients = [con[-1] / con[self.get_pivot_col_idx()] for con in self.tableau[:-1]]
        # print(quotients)
        return quotients.index(min(quotients))

    def base_exchange(self):
        """
        perform a base exchange
        :return:
        """
        pc_idx = self.get_pivot_col_idx()
        self.logger.info('Pivot column: %d' % pc_idx)
        pr_idx = self.get_pivot_row_idx()
        self.logger.info('Pivot row: %d' % pr_idx)
        pe = self.tableau[pr_idx][pc_idx]
        self.logger.info('Pivot element: %d' % pe)

        self.tableau[pr_idx] = [a / pe for a in self.tableau[pr_idx]]

        for i, row in enumerate(self.tableau):
            if i != pr_idx:
                pc_a = self.tableau[i][pc_idx]
                for j, a in enumerate(self.tableau[i]):
                    self.tableau[i][j] = a - (pc_a * self.tableau[pr_idx][j])

    def log_tableau(self):
        for row in self.tableau:
            self.logger.info(row)

    def get_base_point(self):
        """
        compose the the base point
        :return: base point as list
        """
        pass


if __name__ == "__main__":

    simplex = Simplex(dev=True)
    simplex.run()

