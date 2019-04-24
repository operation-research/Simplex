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

    if data_set == 1:
        simplex.initial_A = [[-3, -1], [-2, -3], [2, 1]]
        simplex.initial_b = [-3, -6, 4]
        simplex.initial_c = [-5, -2]
    elif data_set == 2:
        simplex.initial_A = [[16, 6], [4, 12]]
        simplex.initial_b = [252, 168]
        simplex.initial_c = [150, 100]
    elif data_set == 3:
        simplex.initial_A = [[5, 2], [1, 5], [6, 6]]
        simplex.initial_b = [24, 24, 36]
        simplex.initial_c = [500, 800]
