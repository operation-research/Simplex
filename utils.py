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


def init_simplex():
    """
    initialises simplex with user input
    :return: simplex object
    """
    # input of objective function coefficients
    of_input = input('Enter the objective function coefficients: ')
    c = [float(value) for value in of_input.split()]

    # init constraints
    A = []
    further_constraint = True

    while further_constraint:

        # does not ask at first loop
        if len(A) != 0:

            further_con_input = input('Further constraints? [Y/N] ')

            if further_con_input.lower() == 'y':
                pass
            elif further_con_input.lower() == 'n':
                further_constraint = False
                continue
            else:
                continue

        # input of coefficients
        coefficients_input = input('Enter the constraints coefficients: ')
        coefficients = [float(value) for value in coefficients_input.split()]
        if len(coefficients) != len(c):
            raise SimplexException('Invalid constraint length')
        constraint = coefficients

        # input b
        b_input = input('Enter the constraints b: ')
        constraint.append(float(b_input))

        A.append(constraint)

    simplex = Simplex()
    simplex.init_tableau(c, A)
    return simplex
