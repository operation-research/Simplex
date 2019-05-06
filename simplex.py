#!/usr/bin/python3
import logging
import utils
import numpy as np

__author__ = "Daniel Kogan, Janek Putz, Tuananh Vu"


class Simplex:
    """
    Simplex algorithm

    Attributes:
        data_set(int): number of dev data set
        logger(Logger): logger
        tableau([]): simplex tableau
        initial_A([[]]): initial constraint matrix
        initial_b([]): initial b vector
        initial_c([]): initial c vector
    """

    def __init__(self, data_set=None):
        """
        setup object
        :param data_set: number of dev data set
        """
        self.data_set = data_set
        self.logger = logging.getLogger(self.__class__.__name__)
        self.tableau = None
        self.initial_A = None
        self.initial_b = None
        self.initial_c = None

        # config logging
        logging.basicConfig(level=logging.INFO)
        self.logger.info("Initialize Simplex".center(60, '*'))

        # initialize and prepare data
        utils.init_simplex_data(self, data_set)
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
        self.initial_c += [0] * (len(self.initial_A) + 1)

        for idx, constraint in enumerate(self.initial_A):
            slack_var = [0] * len(self.initial_A)
            slack_var[idx] = 1
            self.initial_A[idx] += slack_var

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
        base_swap_counter = 0
        opt_reached = False
        
        while(opt_reached == False): 
            self.logger.info('Start phase 1'.center(60, '*'))

            #Basispunkt (-b Spalte) zulässig oder nicht? GZSZ
            gute_zeilen = []
            schlechte_zeilen = []
            for row in self.tableau[:-1]:
                if row[-1] > 0:
                    gute_zeilen.append(row)
                else:
                    schlechte_zeilen.append(row)

            #Fall 1: Wenn zul. Menge leer --> Algorithmus terminiert
            m_leer = False
            for row in schlechte_zeilen:
                for n in row[:-len(self.tableau)]:
                    if n >= 0:
                        m_leer = True
                    else:
                        m_leer = False
                if m_leer == True:
                    print("Algorithmus terminiert...")
                    exit();

            #Fall 2:
            s_zeile = schlechte_zeilen[-1] #Warum die Zeile?
            g_zeile = gute_zeilen[-1]

            #Kleinster Quotient b/apk0
            sm_quot = pow;
            if (s_zeile[-1]/s_zeile[0]) < (g_zeile[-1]/g_zeile[0]):
                sm_quot = self.tableau[:-1].index(s_zeile)
            else:
                sm_quot = self.tableau[:-1].index(g_zeile)
            

            #Wähle Koeff. mit neg. Vorzeichen aus schlechten Zeile
            neg_var = pow; 
            for i,n in enumerate(s_zeile[:-1]):
                if n < 0:
                    neg_var = i;
                    break;

            #Nach x aufgelöst  boah ist des richtig?
            self.tableau[sm_quot] = [n/self.tableau[sm_quot][neg_var] for n in self.tableau[sm_quot]]

            zw_zeile = [0] * len(self.tableau[sm_quot])
            zw_zeile[-1] = self.tableau[sm_quot][-1]
            for i,n in enumerate(self.tableau[sm_quot][:-1]):
                if i != neg_var:
                    zw_zeile[i] = zw_zeile[i] - self.tableau[sm_quot][i]


            #Für X einsetzen in restliche Zeilen
            for row in self.tableau:
                if row != self.tableau[sm_quot]:
                    zw_zeile1 = [num*row[neg_var] for num in zw_zeile]
                    row[-1] = row[-1] - zw_zeile1[-1]
                    row[neg_var] = 0
                    for i,n in enumerate(row[:-1]):
                        row[i] = row[i] + zw_zeile1[i]

            #neg_var tritt in Basis ein
            for n in range(len(self.initial_A)-1, len(self.tableau[0])-1):
                if self.tableau[sm_quot][n] != 0:
                    for row in self.tableau:
                        swap = row[neg_var]
                        row[neg_var] = row[n]
                        row[n] = swap
                    break;

            base_swap_counter += 1

            for row in self.tableau:
                print(row)


            print("\n")
            base_point = self.get_base_point()
            print(base_point)

            for n in self.tableau[-1][:len(self.initial_A)-1]:
                if (n < 0) & (base_swap_counter == len(self.initial_A)-1):
                    opt_reached = True;
                else:
                    opt_reached = False;
                    


    def run_phase_2(self):
        """
        run the second phase of the algorithm
        <description>
        :return:
        """
        # base_point = self.get_base_point()
        # self.logger.info('Initial base point: %s' % base_point)
        # self.logger.info('Start phase 2'.center(60, '*'))
        # i = 1

        # # if not at least one negative coefficient is found in the objective functions the algorithm terminates
        # while len(list(filter(lambda x: x < 0, self.tableau[-1]))) > 0:

        #     self.logger.info(('%d. Iteration' % i).center(40, '-'))
        #     self.base_exchange()
        #     self.log_tableau()
        #     base_point = self.get_base_point()
        #     self.logger.info('Base point: %s' % base_point)
        #     i += 1

        # self.logger.info('Algorithm terminates'.center(40, '-'))
        # self.logger.info('Optimal base point: ' + str(base_point))

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

    def get_base_point(self):
        """
        compose the the base point
        :return: base point as list
        """
        base_point = []
        col_count = len(self.tableau[0])
        b_vector = self.get_col(col_count - 1)

        for col_idx in range(0, col_count - 1):
            # if column contains coefficients of a slack var
            if self.tableau[-1][col_idx] == 0:
                col = self.get_col(col_idx)
                base_point.append(b_vector[col.index(max(col))])
            else:
                base_point.append(0)

        return base_point

    def get_col(self, index):
        col = []
        for row in self.tableau:
            for idx, x in enumerate(row):
                if idx == index:
                    col.append(x)

        return col

    def log_tableau(self):
        for row in self.tableau:
            self.logger.info(row)


if __name__ == "__main__":

    simplex = Simplex(data_set=1)
    simplex.run()

