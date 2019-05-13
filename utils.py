from simplex import Simplex


__author__ = "Janek Putz, Daniel Kogan"


class SimplexException(Exception):
    """
    Own exception
    """

    def __init__(self, message):
        """
        creates SimplexException
        :param message: message
        """
        super().__init__(message)


def init_simplex_data(simplex, data_set):
    """
    initialises the simplex' data depending on the development flag
    :param simplex: simplex object to store data
    :param data_set: test data_set key
    :return:
    """
    if simplex.data_set is None:
        simplex_input(simplex)
    else:
        simplex_dev_data(simplex, data_set)


def simplex_input(simplex):
    """
    initialises simplex with user input
    :param simplex: simplex object to store data
    """
    # input of objective function coefficients
    of_input = input('Enter the objective function coefficients: ')
    simplex.initial_c = [float(value) for value in of_input.split()]

    # init constraints
    A = []
    b = []
    i = 1
    further_constraint = True

    while further_constraint:

        # does not ask at first loop
        if len(A) != 0:

            further_con_input = input('Further constraints? [Y/N] ')

            if further_con_input.lower() == 'y':
                i += 1
            elif further_con_input.lower() == 'n':
                further_constraint = False
                continue
            else:
                continue

        print('%d. constraint' % i)

        # input of coefficients
        coefficients_input = input('Coefficients: ')
        coefficients = [float(value) for value in coefficients_input.split()]

        if len(coefficients) != len(simplex.initial_c):
            print('Invalid constraint length')
            continue

        A.append(coefficients)

        # input b
        b_input = input('b: ')
        b.append(float(b_input))

    simplex.initial_A = A
    simplex.initial_b_vector = b


def simplex_dev_data(simplex, data_set):
    """
    initialises simplex with static development data
    :param simplex: simplex object to store data
    :param data_set: key of data_set
    :return:
    """
    # Phase 1

    if data_set == 1:  # Todorov Skript
        simplex.initial_A = [[-3, -1], [-2, -3], [2, 1]]
        simplex.initial_b = [-3, -6, 4]
        simplex.initial_c = [-5, -2]
        # Lösung: 1.5 1 2.5 0 0; -9.5

    # Phase 2

    elif data_set == 2:  # Mathebibel
        simplex.initial_A = [[16, 6], [4, 12]]
        simplex.initial_b = [252, 168]
        simplex.initial_c = [150, 100]
        # Lösung: 12 10 0 0; 2800 | funktioniert
    elif data_set == 3:  # Gruppe Nikola
        simplex.initial_A = [[5, 2], [1, 5], [6, 6]]
        simplex.initial_b = [24, 24, 36]
        simplex.initial_c = [500, 800]
        # Lösung: 1.5 4.5 7.5 0 0; 4350 | funktioniert
    elif data_set == 4:  # Marie (degeneriert)
        simplex.initial_A = [[4, 3], [4, 1], [4, 2]]
        simplex.initial_b = [12, 8, 8]
        simplex.initial_c = [2, 1]
        # Lösung: 2 0 4 0 0; -4 | funktioniert nicht ganz -> #TODO anschauen
    elif data_set == 5:  # Aller erstes Beispiel
        simplex.initial_A = [[-1, 1], [2, -3], [2, 3]]
        simplex.initial_b = [2, 3, 12]
        simplex.initial_c = [3, 5]
        # Lösung: 1.2 3.2 0 10.2 0; -19.6 | funktioniert nicht ganz -> #TODO anschauen
    elif data_set == 6:  # Fadi & Marius
        simplex.initial_A = [[2, 1], [4, 5], [6, 15]]
        simplex.initial_b = [80, 200, 450]
        simplex.initial_c = [16, 32]
        # Lösung: 25 20 10 0 0; 1040 | funktioniert
    elif data_set == 7:  # studyflix.de
        simplex.initial_A = [[2, 2], [4, 2], [4, 6]]
        simplex.initial_b = [16, 24, 36]
        simplex.initial_c = [80, 60]
        # Lösung: 4.5 3 1 0 0; 540 | funktioniert
    elif data_set == 8:  # studyflix.de
        simplex.initial_A = [[-1, 2], [-1, -2], [-1, -1]]
        simplex.initial_b = [-1, -4, 2]
        simplex.initial_c = [-1, -1]


def get_neg_value_number(l):
    """
    returns the number of positive values in a list
    :param l: list
    :return: number of positive values
    """
    return len(list(filter(lambda x: x < 0, l)))


def get_tableau_col(simplex, index):
    """
    returns values of a specific column
    :param simplex: simplex with tableau
    :param index: col index
    :return: list of values
    """
    col = []
    for row in simplex.tableau:
        for idx, x in enumerate(row):
            if idx == index:
                col.append(x)
    return col


def log_tableau(simplex):
    """
    logs the simplex' tableau
    :param simplex: simplex
    :return:
    """
    for row in simplex.tableau:
        simplex.logger.info(row)
