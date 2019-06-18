#!/usr/bin/python3
import logging
import utils

__author__ = "Daniel Kogan, Janek Putz, Tuananh Vu"


class Simplex:
    """
    Simplex algorithm

    Attributes:
        bland(Boolean): bland rule flag
        data_set(int): number of dev data set
        logger(Logger): logger
        tableau([]): simplex tableau
        initial_A([[]]): initial constraint matrix
        initial_b([]): initial b vector
        initial_c([]): initial c vector
    """

    def __init__(self, bland=False, data_set=None):
        """
        setup object
        :param data_set: number of dev data set
        """
        self.bland = bland
        self.data_set = data_set
        self.logger = logging.getLogger(self.__class__.__name__)
        self.tableau = None
        self.vars = []
        self.initial_A = None
        self.initial_b = None
        self.initial_c = None

        # config logging
        logging.basicConfig(level=logging.INFO)

        # initialize and prepare data
        utils.init_simplex_data(self, data_set)
        self.add_slack_vars()
        self.logger.info("Initialize Simplex".center(60, '*'))
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
        utils.log_tableau(self)

    def add_slack_vars(self):
        """
        add slack variables to the constraint matrix
        :return:
        """
        self.initial_c += [0] * (len(self.initial_A) + 1)

        for idx, n in enumerate(self.initial_A[0]):
            self.vars.append("x" + str(idx + 1))

        for idx, constraint in enumerate(self.initial_A):
            slack_var = [0] * len(self.initial_A)
            slack_var[idx] = 1
            self.initial_A[idx] += slack_var
            self.vars.append("u" + str(idx + 1))

        self.vars.append("b")

    def run(self):
        """
        runs the simplex algorithm
        :return:
        """
        self.check_empty_solution()

        # if base point is not allowed
        if utils.get_neg_value_number(self.initial_b) > 0:
            self.phase_1()

        self.phase_2()

    def check_empty_solution(self):
        """
        checks if no solution exists because of bad constraints
        :return:
        """
        for idx, con in enumerate(self.tableau[:-1]):
            # mit nur positiven Koeffizienten und der Nichtnegativitätsbedingung kann eine Nebenbedingung mit negativem
            # b Wert nie erfüllt werden
            if utils.get_neg_value_number(con[:-1]) is 0 and con[-1] < 0:
                self.logger.info("Leere Lösungsmenge aufgrund von %d. Nebenbedingung" % (idx + 1))
                exit()

    def check_limited_minimum(self, pc_idx):
        """
        Check whether a minimum can be assumed for a permitted quantity
        :param pc_idx: pivot column index
        :return:
        """
        pc_values = [con[pc_idx] for con in self.tableau[:-1]]
        if utils.get_neg_value_number(pc_values) is len(pc_values):
            self.logger.info('Algorithm terminates'.center(40, '-'))
            self.logger.info('Minimum is not limited')
            exit()

    def phase_1(self):
        """
        run the first phase of the algorithm
        <description>
        :return:
        """
        self.logger.info('Start phase 1'.center(60, '*'))
        i = 1

        while utils.get_neg_value_number([row[-1] for row in self.tableau[:-1]]) > 0:

            # GZSZ
            gute_zeilen = [row for row in self.tableau[:-1] if row[-1] >= 0]
            schlechte_zeilen = [row for row in self.tableau[:-1] if row[-1] < 0]

            # Fall 1: Wenn zul. Menge leer --> Algorithmus terminiert
            for row in schlechte_zeilen:
                if utils.get_neg_value_number(row[:-len(self.tableau)]) <= 0:
                    self.logger.info("Algorithmus terminiert...")
                    exit()

            # Fall 2:

            # Pivotzeile bestimmen
            s_zeile = schlechte_zeilen[0]
            for row in schlechte_zeilen:
                if row[-1] < s_zeile[-1]:
                    s_zeile = row
            g_zeile = gute_zeilen[-1]

            # Wähle Koeff. mit neg. Vorzeichen aus schlechten Zeile --> Pivotspalte (Dafür wird jeweils Quotient gezogen
            # von Koeff. der NBV und Koeff. der Var aus Zielfunktion gezogen)
            # Dadurch erhalten wir auch Pivotelement
            neg_var_idx = [s_zeile[:-1].index(n) for n in s_zeile[:-1] if n < 0]
            neg_var_quots = [self.tableau[-1][i] / s_zeile[:-1][i] for i in neg_var_idx]
            neg_var = neg_var_idx[neg_var_quots.index(max(neg_var_quots))]

            # Kleinster Quotient b/apk0, um zu bestimmen welche Schlupfvariable die Basis verlassen muss (Pivotzeile)
            row_quots = [s_zeile[-1] / s_zeile[neg_var], g_zeile[-1] / g_zeile[neg_var]]
            sm_quot = self.tableau[:-1].index(s_zeile)
            if ((row_quots[1] < row_quots[0]) & (row_quots[1] > 0)):
                self.tableau[:-1].index(g_zeile)

            # Basiswechsel durchführen, damit NBV in Basis eintritt und BV die Basis verlässt
            self.logger.info(('%d. Iteration' % i).center(40, '-'))
            self.base_exchange(neg_var, sm_quot)

            utils.log_tableau(self)
            # Basispunkt ermitteln
            base_point = self.get_base_point()
            self.logger.info(base_point)
            i += 1

    def phase_2(self):
        """
        run the second phase of the algorithm
        <description>
        :return:
        """
        self.logger.info('Start phase 2'.center(60, '*'))
        base_point = self.get_base_point()
        self.logger.info('Initial base point: %s' % base_point)
        of_value = self.tableau[-1][-1]
        self.logger.info('Initial objective function value: %f' % of_value)
        i = 1

        # Mindestens ein negativer Wert in der ZF Zeile gefunden, sonst kann nicht mehr weiter minimiert werden
        while utils.get_neg_value_number(self.tableau[-1][:-1]) > 0:

            pc_idx = self.get_pivot_col_idx()
            self.check_limited_minimum(pc_idx)
            pr_idx = self.get_pivot_row_idx(pc_idx)

            # Basiswechsel durchführen
            self.logger.info(('%d. Iteration' % i).center(40, '-'))
            # self.base_exchange(pc_idx, self.get_pivot_row_idx(pc_idx))
            self.base_exchange(pc_idx, pr_idx)
            utils.log_tableau(self)
            base_point = self.get_base_point()
            self.logger.info('New base point: %s' % base_point)
            of_value = self.tableau[-1][-1]
            self.logger.info('New objective function value: %f' % of_value)
            i += 1

        # Algorithmus kann ZF Wert nicht mehr weiter minimieren
        self.logger.info('Algorithm terminates'.center(40, '-'))
        self.logger.info('Optimal base point: ' + str(base_point))
        self.logger.info('Optimal objective function value: %f' % of_value)

    def base_exchange(self, pc_idx, pr_idx):
        """
        perform a base exchange
        :param pc_idx: pivot column index
        :param pr_idx: pivot row index
        :return:
        """
        self.logger.info('Pivot column: %d' % pc_idx)
        self.logger.info('Pivot row: %d' % pr_idx)
        # Pivot Element herausfinden
        pe = self.tableau[pr_idx][pc_idx]
        self.logger.info('Pivot element: %d' % pe)
        self.logger.info('Run base exchange')

        # Werte der Pivot Zeile durch Pivotelement teilen um Variable des Pivot Elements in die Basis aufzunehmen
        self.tableau[pr_idx] = [a / pe for a in self.tableau[pr_idx]]
        # Basiswechsel in allen anderen Reihen durchführen
        for i, row in enumerate(self.tableau):
            if i != pr_idx:
                # Wert der Zeile in Pivot Spalte ermitteln
                pc_a = self.tableau[i][pc_idx]
                # Alle Werte der Zeile mit dem Produkt aus Pivot Spalten Werten und
                # Pivot Zeilenwert an der jeweiligen Stelle verrechnen
                for j, a in enumerate(self.tableau[i]):
                    self.tableau[i][j] = a - (pc_a * self.tableau[pr_idx][j])

    def get_pivot_col_idx(self):
        """
        provide the pivot columns index
        identify the lowest coefficient in the objective function or uses blands rule
        :return: pivot column index
        """
        if self.bland:
            # Bland'sche Regel besagt eintretende und austretende Variable ist immer diejenige mit
            # kleinsten Index
            base_vars_idx = [idx for idx, value in enumerate(self.tableau[-1][:-1]) if value < 0]
            return min(base_vars_idx)
        else:
            return self.tableau[-1].index(min(self.tableau[-1]))

    def get_pivot_row_idx(self, pc_idx):
        """
        provide the pivot rows index
        calculate the quotient of pivot column coefficient and b, identify the minimum
        :param pc_idx: pivot column index
        :return:
        """
        if self.bland:
            not_base_vars = [row[pc_idx] for row in self.tableau[:-1]]
            not_base_vars_idx = [not_base_vars.index(num) for num in not_base_vars if num > 0]
            not_base_vars_quot = [self.tableau[:-1][idx][-1] / not_base_vars[idx] for idx in not_base_vars_idx]
            return not_base_vars_idx[not_base_vars_quot.index(min(not_base_vars_quot))]
        else:
            quotients = [con[-1] / con[pc_idx] if con[pc_idx] > 0 else None for con in self.tableau[:-1]]
            return quotients.index(min(list(filter(lambda x: x is not None, quotients))))

    def get_base_point(self):
        """
        compose the the base point
        :return: base point as list
        """
        base_point = []
        max_col_idx = len(self.tableau[0]) - 1
        b_vector = [row[max_col_idx] for row in self.tableau[:-1]]

        for col_idx in range(0, max_col_idx):
            # betrachtet Variable Teil der Basis ist, b Wert auslesen
            if self.tableau[-1][col_idx] == 0:
                col = [row[col_idx] for row in self.tableau[:-1]]
                base_point.append(b_vector[col.index(max(col))])
            # andernfalls 0
            else:
                base_point.append(0)

        return base_point


if __name__ == "__main__":
    simplex = Simplex(bland=True,
                      data_set=11)
    simplex.run()

