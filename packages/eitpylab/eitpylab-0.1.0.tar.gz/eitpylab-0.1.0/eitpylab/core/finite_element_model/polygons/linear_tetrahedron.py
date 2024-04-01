from eitpylab.core.finite_element_model.parameters.uniform_rho_simplex import UniformRhoSimplex

import numpy as np
from scipy import linalg as scipyLinalg

class LinearTetrahedron(UniformRhoSimplex):
    """
    4-node Linear tetrahedron element with uniform resistivity/conductivity.

    This class represents a 4-node linear tetrahedron element used in finite element modeling. It inherits from
    `UniformRhoSimplex` and includes additional methods specific to the linear tetrahedron element.

    Attributes:
        None

    Methods:
        __init__(elemNbr, connectivity, coords, rho, propertiesDict=None):
            Initializes the LinearTetrahedron instance.

    """

    def __init__(self, elemNbr,  # type: int
                 connectivity,  # type: Array[int]
                 coords,  # type: Array[float]
                 rho,  # type float
                 propertiesDict=None  # type: dict
                 ):
        """
        Initializes the LinearTetrahedron instance.

        Parameters:
            elemNbr (int): Number of the element.
            connectivity (numpy.ndarray): Nodes of the element in global terms. The local order of the nodes will be
                the same as the connectivity input.
            coords (numpy.ndarray): 2D array where each line is composed of 3 columns (X, Y, and Z) of the node.
                This matrix should contain all nodes of the FemModel, and the function will extract only the needed lines.
            rho (float): Resistivity of the element.
            propertiesDict (dict, optional): Dictionary containing the properties of the simplex.

        Returns:
            None
        """
        
        dimension = 3
        super().__init__(elemNbr, dimension, connectivity, coords, rho, False, propertiesDict)
        
        self.type = '4-node tetrahedron, linear'.lower()
        self.volume = self.calcSimplexVolume()
        self._calc_localKgeom()
        
    def _calc_localKgeom(self):
        """
        Compute the geometric component of the local stiffness matrix.
        """
        M = np.hstack((np.ones([4, 1]), self.coords))
        F = scipyLinalg.inv(M)[1:, :]

        # does not need to divide by (6xVolume)^2 bc I am inverting M directly
        self.Kgeom = self.volume * np.dot(F.T, F)
